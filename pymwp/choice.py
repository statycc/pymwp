from __future__ import annotations

import logging
from typing import Tuple, List, Set, Union
from itertools import islice, chain
from functools import reduce

logger = logging.getLogger(__name__)

SEQ = List[Tuple[int, int]]
"""Type hint to represent a sequence of deltas: `List[Tuple[int, int]]`"""
CHOICES = List[List[List[int]]]
"""Type hint for representing choices"""


class Choices:
    """Generates a compact representation of sequences of choices that do not
    lead to infinity.

    !!! Inputs
        - list of valid choices at one index (e.g. $[0,1,2]$)
        - index (int) - represents number of assignments in original program
        - set of delta-sequences that lead to $\\infty$, obtained from matrix

    Steps:

    Using delta-sequences set, reduce the set in two ways:

    1. remove all sequences that are contained by shorter sequences:

           ```Python
           a = [(0,0)]  b = [(0,0), (0,1), (2,2)]

           # a is subset of b: b cannot be selected without selecting a
           # thus b is redundant => remove b
           ```

    2. replace combinations of delta sequences that can be represented by a
       single, shorter sequence

           ```Python
           choices = [0,1,2]
           a = [(0,1)(2,2)(1,4)]
           b = [(1,1)(2,2)(1,4)]
           c = [(2,1)(2,2)(1,4)]

           # all possible choices are represented at index 1 therefore it
           # does not matter which one is selected: if any choice at index 1
           # is followed by sequence (2,2)(1,4) then the result is infinity.

           # => remove a, b, c and insert [(2,2)(1,4)] in their place.
           ```

    3. Repeat steps 1-2 until no more reduction can be applied.

    4. Build the choice vectors: initialize all choices as valid, then
       eliminate those that lead to infinity, for all possible combinations

           ```Python
           index = 3
           choices = [0,1,2]

           # each index is a set of choices and len(vector) == index
           vector = [{0,1,2}, {0,1,2}, {0,1,2}]

           infinity_choices = { [(0,0)], [(1,0)], [(1,1)(0,3)] }

           # eliminate infinity choice: [(0,0)]
           vector = [{1,2}, {0,1,2}, {0,1,2}]

           # eliminate infinity choice: [(1,0)]
           vector = [{2}, {0,1,2}, {0,1,2}]

           # infinity choice: [(1,1) (0,3)]
           # considering all possible combinations yields 2 distinct vectors:
           vectors = [[{2}, {0,1,2}, {1,2}], [{2}, {0,2}, {0,1,2}]]
           ```
    """

    def __init__(self, vectors: CHOICES = None):
        """Initialize representation with precomputed vector.


        This initialization is primarily useful for restoring a result from
        file. When first creating the choice representation, call
        [`generate()`](choice.md#pymwp.choice.Choices.generate) method
        instead.

        Arguments:
            vectors: choice vectors
        """
        self.valid = vectors or []

    @staticmethod
    def generate(choices: List[int], index: int, inf: Set[SEQ]) -> Choices:
        """Generate the choice representation.

        Arguments:
            choices: list of valid choices for one index, e.g. [0,1,2]
            index: the length of the vector, e.g. 10
            inf: set of deltas that lead to infinity

        Returns:
            Generated choice object.
        """
        # first ensure no sequence is contained by another
        sequences = Choices.unique_sequences(inf)

        # reduce when all paths exist and lead to same infinity choice
        Choices.reduce_subsequences(choices, sequences)

        # now only min unique paths that lead to infinity remain
        paths = [str(list(i)) for i in sorted(
            list(sequences), key=lambda x: (len(x), x))]
        logger.debug(f'infinity paths: {" # ".join(paths) or "None"}')

        # build vectors representing valid choices
        valid = Choices.build_choices(choices, index, sequences)
        return Choices(valid)

    def is_valid(self, *choices: List[int]) -> bool:
        """Check if some sequence of choices can be made without causing
        infinity to occur in the program matrix.

        Example:

        ```Python
        # returns True if this sequence gives non-infinite derivation:

        choice_obj.is_valid(0,1,2,1,1,0)
        ```

        Arguments:
            choices: sequences of delta values to check

        Returns:
            True if the given choices can be made without infinity.
        """
        for vector in self.valid:
            good = True
            if len(choices) > len(vector):
                good = False
            else:
                for idx, value in enumerate(choices):
                    if value not in vector[idx]:
                        good = False
            if good:
                return True
        return False

    @staticmethod
    def unique_sequences(infinities: Set[SEQ]) -> Set[SEQ]:
        """Remove longer delta sequences if already covered by some shorter
        sequence.

        Arguments:
            infinities: set with delta sequences causing infinity

        Returns:
            Reduced list where all longer patterns, whose pattern is covered
            by some shorter sequence, are removed.
        """
        sequences = set()
        infinity_deltas: List[SEQ] = sorted(list(infinities), key=len)
        while infinity_deltas:
            first: SEQ = infinity_deltas.pop(0)
            Choices.remove_subset(first, infinity_deltas)
            sequences.add(first)
        return sequences

    @staticmethod
    def remove_subset(match: SEQ, items: Union[Set, List]):
        """If `match` is a subset of any item in `items`, removes the superset
        from items, in place.

        Arguments:
            match: single delta sequence
            items: list of delta sequences to check against match
        """
        for item in sorted(list(items)):
            if set(match).issubset(set(item)):
                items.remove(item)

    @staticmethod
    def reduce_subsequences(choices: List[int], sequences: Set[SEQ]):
        """Reduce sequences of deltas to simplify sequences leading to
        infinity, as explained in [`reduce`](#reduce). This operation
        will repeat until set of sequences cannot be reduced any further.

        Arguments:
            choices: list of valid per index choices, e.g. [0,1,2]
            sequences: set of delta sequences
        """
        while Choices.reduce(choices, sequences):
            pass

    @staticmethod
    def reduce(choices: List[int], sequences: Set[SEQ]) -> bool:
        """Look for first reducible sequence, if exist, then replace it.

        Example:

            Consider the following sequences, where deltas differ only on
            first value and never on index, and all possible choice values are
            represented in the first delta:

             ```
             - (0,0) (2,1) (1,4)
             - (1,0) (2,1) (1,4)
             - (2,0) (2,1) (1,4)
             ```

        Since all possible choices occur at 0th index, and are followed
        by same subsequent deltas, it does not matter which choice is
        made at index 0. The 3 paths can be collapsed into a single, shorter
        path: `(2,1)(1,4)`.

        Arguments:
            choices: list of valid per index choices, e.g. [0,1,2]
            sequences: set of delta sequences

        Returns:
            True if a reduction occurred and False otherwise. The meaning of
            False is to say the operation is done and should not be repeated
            any further.
        """
        for s1 in sequences:
            subs = [s2[0][0] for s2 in sequences if Choices.sub_equal(s1, s2)]
            # all paths must exist
            if set(subs) == set(choices):
                # keep rest of sequence
                keep = s1[1:]
                # remove all sequences contained by the shorter path
                Choices.remove_subset(keep, sequences)
                # finally add the shorter sequence to the set
                sequences.add(keep)
                return True
        return False

    @staticmethod
    def sub_equal(first: SEQ, second: SEQ) -> bool:
        """Compare two delta sequences for equality, except their 0th value.

        Arguments:
            first: first delta sequence
            second: the other delta sequence

        Returns:
            True if two delta sequences are equal excluding the 0th value,
            and False otherwise.
        """
        return first[0][1] == second[0][1] and first[1:] == second[1:]

    @staticmethod
    def build_choices(
            choices: List[int], index: int, infinities: Set[SEQ]
    ) -> CHOICES:
        """Build a list of distinct choice vectors excluding infinite choices.

        This method works by taking a list of delta paths that lead to infinity
        and then negates those choices; the result is a list of choice
        vectors such that any remaining choice will give a valid derivation.

        Example:

            assume the paths leading to infinity are:
            { [(0,0)], [(1,0)], [(1,1)(0,3)] }

            Then, the valid choices that do not lead to infinity are:
            [[[2], [0,2], [0,1,2]]  or  [[2], [0,1,2], [1,2]]]

            Read as: choose either vector (left or right) then at each
            index choose one of the remaining choices.

        Arguments:
            choices: list of valid choices for one index, e.g. [0,1,2]
            index: the length of the vector, e.g. 10
            infinities: set of deltas that lead to infinity

        Returns:
            Choice vector that excludes all paths leading to infinity.
        """
        if not infinities:
            return [[list(choices[:]) for _ in range(index)]]

        # noinspection PyTypeChecker
        # sort the infinity paths by length, shortest first
        sorted_infty = sorted(list(infinities), key=len)

        # get length of each infinity path
        lens = [len(i) for i in sorted_infty]
        # get the number of bits needed to represent each path; this binary
        # magic is necessary because itertools does not seem to have a nice
        # way of producing combinations for choosing 1 from each set
        bin_lens = [len(bin(i - 1)[2:]) for i in lens]

        # in each vector, choose 1 delta from each infinity path; so that no
        # path can be selected fully => the product of all path lengths gives
        # the max number of distinct vectors:
        max_ = reduce((lambda x, y: x * y), lens)

        logger.debug(f'maximum distinct vectors: {max_}')
        logger.debug(f'path lengths/bits: {lens} / {bin_lens}')

        vectors = set()

        # generate all possible vectors by iterating the max count of
        # distinct vectors: use the iteration count as selector for deltas
        for iter_i in range(max_):

            # convert the iteration number to 0-filled binary
            bin_iter = iter(bin(iter_i)[2:].zfill(len(sorted_infty)))

            # convert the binary number to a list of indices
            # these indices decide which delta to pick from each path
            indices = [int(n) for n in chain.from_iterable(
                [list(islice(bin_iter, bl)) for bl in bin_lens])]

            # using the indices, now choose the specific delta values
            # 1 value for each infinite path, so that it is not possible
            # to choose any path fully
            deltas = [sorted_infty[i][v] for i, v in enumerate(indices)]

            # initialize a vector with all allowed choices
            vector = [set(choices[:]) for _ in range(index)]
            valid = True

            # iterate the infinity deltas to remove them from the vector
            for choice, idx in deltas:
                if choice in vector[idx]:
                    vector[idx].remove(choice)
                # if all choices are eliminated at some index, stop
                if len(vector[idx]) == 0:
                    valid = False
                    break
            # discard the vector if it is invalid
            if not valid:
                continue

            # must be hashable type to add to set
            # shouldn't generate same vector ever, but not sure, so using a set
            vector = tuple([tuple(entry) for entry in vector])
            vectors.add(vector)

        # change the remaining choices at each index to lists (not sets)
        # so the vectors can be saved to file
        return [list([list(c) for c in v]) for v in vectors]
