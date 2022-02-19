from __future__ import annotations
import logging
from typing import Tuple, List, Set, Union

logger = logging.getLogger(__name__)

SEQ = List[Tuple[int, int]]


class Choices:

    def __init__(self, choices: List[int], index: int, infinities: Set[SEQ]):

        # first ensure no sequence is contained by another
        sequences = Choices.unique_sequences(infinities)

        # reduce when all paths exist and lead to same infinity choice
        Choices.reduce_subsequences(choices, sequences)

        # now only min unique paths that lead to infinity remain
        joined = '#'.join([str(list(i)) for i in sorted(list(sequences))])
        logger.debug(f'infinity paths: {joined}')

        # build vectors representing valid choices
        self.valid = Choices.build_vectors(choices, index, sequences)
        logger.debug(f"valid choices:\n{self.valid}")

    @staticmethod
    def unique_sequences(infinities: Set[SEQ]):
        """Remove longer delta sequences if already covered by a shorter
        sequence.
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
        """if any item in result contains match, remove the superset"""
        for item in sorted(list(result)):
            if set(match).issubset(set(item)):
                result.remove(item)

    @staticmethod
    def reduce_subsequences(choices: List[int], sequences: Set[SEQ]):
        """Find first sequence of deltas that only differ on first value
        and such that all choice paths are included.
        """
        while Choices.reduce(choices, sequences):
            pass

    @staticmethod
    def reduce(choices: List[int], sequences: Set[SEQ]):
        """Look for first reducible sequence if exist, then replace it."""
        for s1 in sequences:
            subs = [s2[0][0] for s2 in sequences if Choices.sub_equal(s1, s2)]
            # all paths must exist
            if set(subs) == set(choices):
                keep = s1[1:]  # keep rest of sequence
                Choices.remove_subset(keep, sequences)
                sequences.add(keep)
                return True
        return False

    @staticmethod
    def sub_equal(first: SEQ, second: SEQ):
        """true if two delta sequences are equal excluding the 0th value."""
        return first[0][1] == second[0][1] and first[1:] == second[1:]

    @staticmethod
    def path_exists(path, vector):
        return False not in [v in vector[i] for (v, i) in path]

    @staticmethod
    def build_vectors(choices: List[int], index: int, infinities: Set[SEQ]):
        """Build a list of choice vectors excluding infinite choices."""
        vector = [set(choices[:]) for _ in range(index)]
        for item in sorted(list(infinities), key=len):
            path, [(i, idx)] = item[:-1], item[-1:]
            # TODO: how to handle if this assert fails?
            # is it possible to make such choices ???
            # -> need another vector where this seq of choices can be made
            assert Choices.path_exists(path, vector)
            # remove invalid choices
            if i in vector[idx]:
                vector[idx].remove(i)
        vector = list([list(entry) for entry in vector])
        return vector
