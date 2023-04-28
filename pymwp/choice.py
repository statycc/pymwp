from __future__ import annotations

import logging
from collections import Counter
from functools import reduce
from typing import Tuple, List, Set, Union, Optional

logger = logging.getLogger(__name__)

SEQ = Tuple[Tuple[int, int], ...]
"""Type hint to represent a sequence of deltas."""

CHOICES = List[List[List[int]]]
"""Type hint for representing a list of choice vectors."""


class Choices:
    """
    Generates a compact representation of derivation rule choices that do
    not lead to infinity.
    """

    def __init__(self, vectors: CHOICES = None):
        """Initialize representation with precomputed vector.

        This initialization is primarily useful for restoring a result from
        file. When first creating the choice representation, call
        [`generate()`](choice.md#pymwp.choice.Choices.generate) method
        instead.

        Arguments:
            vectors: list of choice vectors
        """
        self.valid = vectors or []

    @property
    def infinite(self):
        return len(self.valid) == 0

    @property
    def first(self) -> Optional[tuple[int]]:
        """Gets the first valid derivation choice, if exists"""
        # take first vector, then first choice at each index
        return tuple([choices[0] for choices in self.valid[0]]) \
            if not self.infinite else None

    @property
    def n_bounds(self) -> int:
        """Number of bounds that can be generated from a choice vector"""
        return sum([
            reduce(lambda total, n: total * (n[0] ** n[1]), lens.items(), 1)
            for lens in [Counter([len(x) for x in v]) for v in self.valid]])

    @staticmethod
    def generate(choices: List[int], index: int, inf: Set[SEQ]) -> Choices:
        """Generate the choice representation.

        This works in two steps: 1. simplify delta sequences 2. build
        choice vectors.

        Arguments:
            choices: list of valid choices for one index, e.g. [0,1,2]
            index: the length of the vector, e.g. 10. This is the same as
                number of assignments in the analyzed function.
            inf: set of deltas that lead to infinity

        Returns:
            Generated choice object.
        """
        # simplify the set of infinities
        sequences = Choices.simplify(choices, inf)

        # now only min unique paths that lead to infinity remain
        # only sorted here for presentation purposes
        paths = [str(list(i)) for i in sorted(
            list(sequences), key=lambda x: (len(x), x))]
        logger.debug(f'infinity paths: {" # ".join(paths) or "None"}')

        # build vectors representing valid choices
        valid = Choices.build_choices(choices, index, sequences)
        return Choices(valid)

    def is_valid(self, *choices: int) -> bool:
        """Checks if sequence of choices can be made without infinity.

        Example:

            ```Python
            choice_obj.is_valid(0,1,2,1,1,0)
            ```

        Arguments:
            choices: sequences of delta values to check

        Returns:
            True if the given choices can be made without infinity.
        """
        for vector in self.valid:
            if len(choices) <= len(vector) and False not in \
                    [value in vector[idx] for idx, value in
                     enumerate(choices)]:
                return True
        return False

    @staticmethod
    def simplify(choices: List[int], sequences: Set[SEQ]) -> Set[SEQ]:
        """Generate the most simplified, equivalent representation of
        the set of choices that cause infinity.

        Reduce sequences of deltas, as explained in [`reduce`](#reduce).
        This operation will repeat until set of sequences cannot be reduced
        any further. Then remove all superset contained by some shorter
        sequence. This process repeats until no more simplification can be
        applied.

        Arguments:
            choices: list of valid per index choices, e.g. [0,1,2]
            sequences: set of delta sequences

        Returns:
            Simplified list of infinity paths.
        """
        while True:
            while Choices.reduce(choices, sequences):
                continue
            len_before = len(sequences)
            sequences = Choices.unique_sequences(sequences)
            len_after = len(sequences)
            if len_before == len_after or len_after == 0:
                return sequences

    @staticmethod
    def reduce(choices: List[int], sequences: Set[SEQ]) -> bool:
        """Look for first reducible sequence, if exists, then replace it.

        ??? example "Example"

            Consider the following sequences, where deltas differ only on
            first value and never on index, and all possible choice values are
            represented in the first delta:

             ```
             (0,0) (2,1) (1,4)
             (1,0) (2,1) (1,4)
             (2,0) (2,1) (1,4)
             ```

            Since all possible choices occur at 0th index, and are followed
            by same subsequent deltas, it does not matter which choice is
            made at index 0. The 3 paths can be collapsed into a single,
            shorter path: `(2,1)(1,4)`.

        Arguments:
            choices: list of valid per index choices, e.g. [0,1,2]
            sequences: set of delta sequences

        Returns:
            True if a reduction occurred and False otherwise. The meaning of
            False is to say the operation is done and should not be repeated
            any further.
        """
        for s1 in [s for s in sequences if len(s) > 1]:
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
    def unique_sequences(infinities: Set[SEQ]) -> Set[SEQ]:
        """Remove superset delta sequences.

        Arguments:
            infinities: set of delta sequences causing infinity

        Returns:
            A list where all longer sequences, whose pattern is covered
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
    def sub_equal(first: SEQ, second: SEQ) -> bool:
        """Compare two delta sequences for equality, except their 0th value.

        Arguments:
            first: first delta sequence
            second: second delta sequence

        Returns:
            True if two delta sequences are equal excluding the 0th value,
            and False otherwise.
        """
        return first[0][1] == second[0][1] and first[1:] == second[1:]

    @staticmethod
    def prod(values: list) -> int:
        """Compute the product of numeric list.

        Arguments:
            values: 1d list of numbers

        Returns:
            Product of values.
        """
        return reduce((lambda x, y: x * y), values, 1)

    @staticmethod
    def build_choices(
            choices: List[int], index: int, infinities: Set[SEQ]
    ) -> CHOICES:
        """Build a list of distinct choice vectors excluding infinite choices.

        This method works by taking a list of delta paths that lead to infinity
        and then negates those choices; the result is a list of choice
        vectors such that any remaining choice will give a valid derivation.

        ??? example "Example"

            assume the paths leading to infinity are:

            `[(0,0)], [(1,0)], [(1,1)(0,3)]`

            Then, the valid choices that do not lead to infinity are:

            `[[ [2], [0,2], [0,1,2]]`  or  `[[2], [0,1,2], [1,2]]]`

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
        # sort the infinity paths by length, the shortest first
        sorted_infty = sorted(list(infinities), key=len)

        # get length of each infinity path
        lens = [len(i) for i in sorted_infty]
        # helper for generating distinct combinations of indices
        iters = [Choices.prod(lens[idx + 1:]) for idx, _ in enumerate(lens)]

        # the product of path lengths gives the max number of distinct vectors
        max_ = Choices.prod(lens)
        logger.debug(f'maximum distinct vectors: {max_}')

        # number of times each delta occurs in remaining paths
        delta_freq = Counter([j for sub in sorted_infty for j in sub])

        vectors = set()

        # generate all possible vectors by iterating the max count of
        # distinct vectors
        for iter_i in range(max_):

            # from iteration count, generate selectors for deltas
            # this one line does a lot - only edit if you have a good reason
            indices = [(iter_i // i) % x for x, i in zip(lens, iters)]

            # now choose the specific delta values, 1 value for each infinite
            # path, so that it is not possible to choose any bad path fully
            # this is same as taking cross product of deltas
            deltas = [sorted_infty[i][v] for i, v in enumerate(indices)]
            idx_freq = [i for v, i in set(deltas)]
            vector_freq = Counter(list(deltas))
            minimal = all([delta_freq[k] == vector_freq[k]
                           for k in vector_freq.keys()])
            is_valid = all([idx_freq.count(n) < len(choices)
                            for n in set(idx_freq)])

            # This iteration will not produce a valid vector if all choices
            # are eliminated at some index. It will also not produce the
            # optimal vector, if some delta is duplicated in the
            # infinities-set but not in this vector. Discard these choices
            # in both cases.
            if not is_valid or not minimal:
                continue

            # initialize a vector with all allowed choices
            vector = [set(choices[:]) for _ in range(index)]

            # iterate the infinity deltas to remove them from the vector
            for choice, idx in set(deltas):
                if choice in vector[idx]:
                    vector[idx].remove(choice)

            # must be hashable type to add to set, shouldn't generate same
            # vector ever but not sure, so using a set
            vector = tuple([tuple(entry) for entry in vector])
            vectors.add(vector)

        # change the remaining choices at each index to lists (not sets)
        # so the vectors can be saved to file
        return [list([list(c) for c in v]) for v in vectors]
