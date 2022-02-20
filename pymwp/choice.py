from __future__ import annotations
import logging
from typing import Tuple, List, Set, Union

logger = logging.getLogger(__name__)

SEQ = List[Tuple[int, int]]


class Choices:
    """Choice-object generates a compact representation of sequences of
    choices such that the result is not infinity.
    """

    def __init__(self, vector: List[List[int]] = None):
        """Initialize representation with precomputed vector.

        This initialization is primarily useful for restoring a result from
        file. When first creating the choice representation, call `generate()`
        method instead.

        Arguments
            vector: choice vector
        """
        self.valid = vector or []

    @staticmethod
    def generate(choices: List[int], index: int, infinities: Set[SEQ]) \
            -> Choices:
        """Generate the choice representation.

        Arguments:
            choices - list of valid choices for one index, e.g. [0,1,2]
            index - the length of the vector, e.g. 10
            infinities - set of deltas that lead to infinity

        Returns:
            Generated choice object.
        """

        # first ensure no sequence is contained by another
        sequences = Choices.unique_sequences(infinities)

        # reduce when all paths exist and lead to same infinity choice
        Choices.reduce_subsequences(choices, sequences)

        # now only min unique paths that lead to infinity remain
        joined = '#'.join([str(list(i)) for i in sorted(list(sequences))])
        logger.debug(f'infinity paths: {joined or "None"}')

        # build vectors representing valid choices
        valid = Choices.build_choices(choices, index, sequences)
        return Choices(valid)

    def is_valid(self, *choices) -> bool:
        """Check if some sequence of choices can be made without causing
        infinity to occur in the program matrix.

        Example:

        ```
        # returns True is this sequence gives non-infinite derivation:
        choice_obj.is_valid(0,1,2,1,1,0) # True/False
        ```

        Arguments:
            choices: sequences of deltas to check

        Returns:
            True if the choices can be made without infinity.
        """
        vector = self.valid
        if len(choices) > len(vector):
            return False
        for idx, value in enumerate(choices):
            if value not in vector[idx]:
                return False
        return True

    @staticmethod
    def unique_sequences(infinities: Set[SEQ]) -> Set[SEQ]:
        """Remove longer delta sequences if already covered by some shorter
        sequence.

        Arguments:
            infinities - set with delta sequences causing infinity

        Returns
            Reduced list where longer patterns whose pattern is covered
            by some shorter sequence are removed.
        """
        sequences = set()
        infinity_deltas: List[SEQ] = sorted(list(infinities), key=len)
        while infinity_deltas:
            first: SEQ = infinity_deltas.pop(0)
            Choices.remove_subset(first, infinity_deltas)
            sequences.add(first)
        return sequences

    @staticmethod
    def remove_subset(match: SEQ, result: Union[Set, List]):
        """If any item in match is a subset of any item in result,
        removes the superset from result (in place).

        Arguments:
            match: single delta sequence
            result: list of delta sequences to check against match
        """
        for item in sorted(list(result)):
            if set(match).issubset(set(item)):
                result.remove(item)

    @staticmethod
    def reduce_subsequences(choices: List[int], sequences: Set[SEQ]):
        """Reduce sequences of deltas to simplify sequences leading to
        infinity, as explained in [`reduce`](#reduce). This operation
        will repeat until set of sequences cannot be reduced any further.

        Arguments:
            choices  - list of valid per index choices, e.g. [0,1,2]
            sequences - set of delta sequences

        Returns:
            Simplified list on infinite sequences.
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

             - (0,0) (2,1) (1,4)
             - (1,0) (2,1) (1,4)
             - (2,0) (2,1) (1,4)

        Since all possible choices occur at 0th index, and are followed
        by same choices (2,1)(1,4) => any choice at 0th index followed by same
        subsequent pattern will cause infinity; does not matter which choice is
        made at index 0. In such case the 3 paths can be collapsed into a
        single, shorter path: (2,1)(1,4).

        Arguments:
            choices  - list of valid per index choices, e.g. [0,1,2]
            sequences - set of delta sequences

        Returns:
            True if a reduction occurred and False otherwise. The meaning of
            False is to say the operation is done and should not be repeated
            further.
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
            first - first delta sequence
            second - the other delta sequence

        Returns:
            True if two delta sequences are equal excluding the 0th value
            and False otherwise.
        """
        return first[0][1] == second[0][1] and first[1:] == second[1:]

    @staticmethod
    def path_exists(path: SEQ, vector: List[Set[int]]) -> bool:
        """Ensure a sequence of choices can be made wrt given vector."""
        return False not in [v in vector[i] for (v, i) in path]

    @staticmethod
    def build_choices(
            choices: List[int], index: int, infinities: Set[SEQ]
    ) -> List[List[int]]:
        """Build a list of choice vectors excluding infinite choices.

        Arguments:
            choices - list of valid choices for one index, e.g. [0,1,2]
            index - the length of the vector, e.g. 10
            infinities - set of deltas that lead to infinity

        Returns:
            Choice vector that excludes all paths leading to infinity.
        """

        # make a vector (len=index) that includes all choices
        # e.g. [{0,1,2}, {0,1,2}, {0,1,2}]
        vector = [set(choices[:]) for _ in range(index)]

        # iterate the infinity choices to remove them from the vector
        for item in sorted(list(infinities), key=len):

            # split the infinity delta path into two parts:
            # (1) all except last delta (2) value and index of last delta
            path, [(i, idx)] = item[:-1], item[-1:]

            # Ensure the sequences of choices (path) can be made
            # TODO: how to handle if this assert fails?
            # is it possible to make such choices ???
            # -> if yes: add another vector where choices can be made
            assert Choices.path_exists(path, vector)

            # remove invalid choice value at specified index
            # e.g. if 1 at 0 causes infinity we remove it to get:
            # [{0,2}, {0,1,2}, {0,1,2}]
            if i in vector[idx]:
                vector[idx].remove(i)

        # change the remaining choices at each index to lists (not sets)
        vector = list([list(entry) for entry in vector])

        return vector
