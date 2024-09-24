# -----------------------------------------------------------------------------
# Copyright (c) 2020-2024 C. Aubert, T. Rubiano, N. Rusch and T. Seiller.
#
# This file is part of pymwp.
#
# pymwp is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pymwp is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pymwp. If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from __future__ import annotations

import logging
from collections import Counter
from functools import reduce
from itertools import product
from typing import Tuple, List, Set, Union, Optional, Generator, Callable

from . import SEQ, VECT, CHOICES

logger = logging.getLogger(__name__)


class Choices:
    """
    A compact representation of derivation choices.

    Attributes:
        valid (CHOICES): list of choice vectors.
        index (int): degree of choice.
    """

    def __init__(self, valid: CHOICES = None, index: int = -1):
        """Initialize representation from a precomputed vector.

        This is primarily useful for restoring a result from file.
        To create a choice representation, call
        [`generate()`](choice.md#pymwp.choice.Choices.generate) instead.
        """
        self.valid = valid or []
        if index < 0 and valid and len(valid):
            self.index = len(valid[0])
        else:
            self.index = index

    def __bool__(self):
        return not self.infinite

    @property
    def infinite(self):
        """True if no valid choice exists."""
        return len(self.valid) == 0 and self.index > 0

    @property
    def first(self) -> Optional[tuple[int]]:
        """Gets the first valid derivation choice, if at least one exists."""
        # take first vector, then first choice at each index
        return tuple([choices[0] for choices in self.valid[0]]) \
            if not self.infinite else None

    @property
    def n_bounds(self) -> int:
        """Number of bounds that can be generated from a choice vector.
        This is calculated directly from the vector form. It is the product
        of number of choices at each index: $\\prod_{c \\in v} |c|$.

        Example:
            1. Vector `[[0, 1, 2], [0, 1, 2], [0]]` allows making `[3, 3, 1]`
               choices/index. It has $3 * 3 * 1 = 9$ total bounds.

            2. A vector with choices/index: `[3, 1, 2, 1, 3, 3]` has
                $3^3 * 2^1 * 1^2 = 54$ possible bounds.

        Returns:
            Number of possible choices (non-distinct).
        """
        return sum([
            reduce(lambda total, n: total * n, lens, 1)
            for lens in [[len(x) for x in v] for v in self.valid]])

    def is_valid(self, *choices: int) -> bool:
        """Checks if sequence of choices can be made without infinity.

        Example:
           ```Python
           choice_obj.is_valid(0, 1, 2, 1, 1, 0)
           ```

        Arguments:
            choices: sequences of delta values to check.

        Returns:
            True if the given choices can be made without infinity.
        """
        for vector in self.valid:
            if len(choices) <= len(vector) and False not in \
                    [value in vector[idx] for idx, value in
                     enumerate(choices)]:
                return True
        return False

    def all(self) -> Generator[Tuple[int, ...]]:
        """Generator for all valid derivation choices.

        Note:
            Calling this method is very inefficient. Generally, we do not
            want to generate all choices. The method _yields_ the next value
            in series, so it is possible to step through the choices one at a
            time. Use with caution/only call if necessary.

        Yields:
            The next valid choice.
        """
        for choices in self.valid:
            for p in product(*choices):
                yield p

    @staticmethod
    def generate(domain: List[int], index: int, inf: Set[SEQ]) -> Choices:
        """Generate the choice representation.

        This works in two steps: (1) simplify delta sequences, (2) build
        choice vectors.

        Arguments:
            domain: valid choices at index, e.g. `[0, 1, 2]`.
            index: the length of the vector, e.g. 10. This is the same as
                number of assignments in the analyzed function.
            inf: set of deltas that lead to infinity.

        Returns:
            Generated choice object.
        """
        # simplify the set of infinities
        sequences = Choices.simplify(domain, inf)

        # now only min unique paths that lead to infinity remain
        # only sorted here for presentation purposes
        paths = [str(list(i)) for i in sorted(
            list(sequences), key=lambda x: (len(x), x))]
        logger.debug(f'infinity paths: {" # ".join(paths)}')

        # build vectors representing valid choices
        valid = Choices.build_choices(domain, index, sequences)
        return Choices(valid, index)

    @staticmethod
    def simplify(domain: List[int], sequences: Set[SEQ]) -> Set[SEQ]:
        """Generate the most simplified, equivalent representation of
        the set of choices that cause unwanted derivation results.

        Reduce sequences of deltas, until set of sequences cannot be reduced
        any further. Then remove all superset contained by some shorter
        sequence. Lastly, remove deltas that would generate an invalid
        choice vector. This process repeats until no more simplification
        can be applied.

        Arguments:
            domain: list of valid per index choices, e.g. `[0, 1, 2]`.
            sequences: set of delta sequences.

        Returns:
            Simplified list of infinity paths.
        """
        while True:
            len_before = len(sequences)
            while Choices.reduce(domain, sequences):
                continue
            while Choices.reduce_end(domain, sequences):
                continue
            sequences = Choices.unique_sequences(sequences)
            sequences = Choices.except_one(domain, sequences)
            len_after = len(sequences)
            if len_before == len_after or len_after == 0:
                return sequences

    @staticmethod
    def _reduce(
            domain: List[int], sequences: Set[SEQ],
            sub_eq: Callable[[SEQ, SEQ], bool], get_: Callable[[SEQ], int],
            keep_: Callable[[SEQ], SEQ]
    ) -> bool:
        """Implement sequence reduction from select direction.

        Arguments:
            domain: list of valid per index choices, e.g. `[0, 1, 2]`.
            sequences: set of delta sequences.
            sub_eq: subsequence comparison function.
            get_: choice value getter, e.g., first or last value of sequence.
            keep_: getter for sub-sequence that should be preserved.

         Returns:
            True if a reduction occurred and False otherwise.
        """
        for s1 in [s for s in sequences if len(s) > 1]:
            subs = [get_(s2) for s2 in sequences if sub_eq(s1, s2)]
            # all paths must exist
            if set(subs) == set(domain):
                # keep rest of sequence
                keep = keep_(s1)
                # remove all sequences contained by the shorter path
                Choices.remove_subset(keep, sequences)
                # finally add the shorter sequence to the set
                sequences.add(keep)
                return True
        return False

    @staticmethod
    def reduce(domain: List[int], sequences: Set[SEQ]) -> bool:
        """Look for first reducible sequence, if exists, then replace it.

        Example:
           We can reduce a sequences where deltas differ only on first value,
           never on index, and all possible choice values are represented
           in the first delta. Below, it does not matter which choice is
           made at index 0. The 3 paths can be collapsed into a single,
           shorter path: `(2,1)(1,4)`.

           ```
           (0,0) (2,1) (1,4)
           (1,0) (2,1) (1,4)
           (2,0) (2,1) (1,4)
           ```

        Arguments:
            domain: list of valid per index choices, e.g. `[0, 1, 2]`.
            sequences: set of delta sequences.

        Returns:
            True if a reduction occurred and False otherwise. The meaning of
                False is to say the operation is done and should not be
                repeated any further.
        """
        return Choices._reduce(
            domain, sequences, Choices.sub_equal,
            get_=lambda s2: s2[0][0], keep_=lambda s1: s1[1:])

    @staticmethod
    def reduce_end(domain: List[int], sequences: Set[SEQ]) -> bool:
        """Like `reduce`, but from end of sequence.

        Example:
           When deltas only differ at last index, and all choices
           occur at last index, reduce choices to a shorter path.
           E.g., Below, choice at index 5 is irrelevant; keep `(2,1) (1,4)`.

           ```
           (2,1) (1,4) (0,5)
           (2,1) (1,4) (1,5)
           (2,1) (1,4) (2,5)
           ```

        Arguments:
            domain: list of valid per index choices, e.g. `[0, 1, 2]`.
            sequences: set of delta sequences.

        Returns:
            True if a reduction occurred and False otherwise.
        """
        return Choices._reduce(
            domain, sequences, Choices.sub_equal_end,
            get_=lambda s2: s2[-1][0], keep_=lambda s1: s1[:-1])

    @staticmethod
    def except_one(domain: List[int], sequences: Set[SEQ]) -> Set[SEQ]:
        """Look for deltas of length=1 where all-but-one choices are made
        at same index. The remaining one choice can be eliminated from paths
        that contain it, because it would yield an invalid choice vector.

        Example:
            Given sequence `((0,0),), ((1,0),), ((2,0),(2,1),(1,4),)` and
            the goal to build a choice vector. Deltas `(0,0)` and `(1,0)` must
            be chosen. For `((2,0),(2,1),(1,4),)` one of the deltas must be
            chosen. But choosing `(0,0), (1,0), (2,0)` eliminates all choices
            at index 0. It suffices to keep sequence
            `((0,0),), ((1,0),), ((2,1),(1,4),)`.

        Arguments:
            domain: list of valid per index choices, e.g. `[0, 1, 2]`.
            sequences: set of delta sequences.

        Returns:
            A set of sequences after applying simplification.
        """
        l1 = [s[0] for s in sequences if len(s) == 1]
        while l1:
            (v, index) = l1.pop(0)
            matches = [itm for itm in l1 if itm[1] == index]
            values = [m[0] for m in matches]
            find = [(c, index) for c in domain
                    if c != v and c not in values]
            if len(find) == 1:
                for p in [s for s in sequences
                          if find[0] in s and len(s) > 1]:
                    sequences.add(tuple([x for x in p if x != find[0]]))
                    sequences.remove(p)
            map(l1.remove, matches)
        return sequences

    @staticmethod
    def unique_sequences(infinities: Set[SEQ]) -> Set[SEQ]:
        """Remove superset delta sequences.

        Arguments:
            infinities: set of delta sequences causing infinity.

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
            match: single delta sequence.
            items: list of delta sequences to check against match.
        """
        for item in sorted(list(items)):
            if set(match).issubset(set(item)):
                items.remove(item)

    @staticmethod
    def sub_equal(first: SEQ, second: SEQ) -> bool:
        """Compare two delta sequences for equality, except their 0th value.

        Arguments:
            first: first delta sequence.
            second: second delta sequence.

        Returns:
            True if two delta sequences are equal excluding the 0th value,
                and False otherwise.
        """
        return first[0][1] == second[0][1] and first[1:] == second[1:]

    @staticmethod
    def sub_equal_end(first: SEQ, second: SEQ) -> bool:
        """Compare two delta sequences for equality, except their N-th
        value. This is like `sub_equal`, but comparison is done at the end of
        sequences.

        Arguments:
            first: first delta sequence.
            second: second delta sequence.

        Returns:
            True if two delta sequences are equal excluding the N-th
                value, and False otherwise.
        """
        return first[-1][1] == second[-1][1] and first[:-1] == second[:-1]

    @staticmethod
    def prod(values: list) -> int:
        """Compute the product of numeric list.

        Arguments:
            values: 1d list of numbers.

        Returns:
            Product of values.
        """
        return reduce((lambda x, y: x * y), values, 1)

    @staticmethod
    def build_choices(domain: List[int], index: int, infinities: Set[SEQ]) \
            -> CHOICES:
        """Build a list of distinct choice vectors excluding unwanted choices.

        This method works by taking a list of delta paths that give unwanted
        scalars (e.g., $\\infty$) and then negates those choices; the result
        is a list of choice vectors such that any remaining choice will give
        a valid derivation.

        Example:
           * Assume paths leading to $\\infty$ are:
             `[(0,0)], [(1,0)], [(1,1)(0,3)]`.
           * The choices that do not lead to $\\infty$ are:
             `[[[2], [0,2], [0,1,2]]` or `[[2], [0,1,2], [1,2]]]`.

        Arguments:
            domain: list of valid choices for one index, e.g. `[0, 1, 2]`.
            index: the length of the vector, e.g. 10.
            infinities: set of deltas that lead to unwanted choices.

        Returns:
            Choice vector that excludes all paths leading to unwanted choices.
        """
        if not infinities:
            return [[list(domain[:]) for _ in range(index)]]

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

        # noinspection PyTypeChecker
        # number of times each delta occurs in remaining paths
        delta_freq = Counter([j for sub in sorted_infty for j in sub])
        distinct = max(delta_freq.values()) == 1 if delta_freq else 0
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
            is_valid = all([idx_freq.count(n) < len(domain)
                            for n in set(idx_freq)])
            # This iteration will not produce a valid vector if all choices
            # are eliminated at some index.
            if not is_valid:
                continue

            # initialize a vector with all allowed choices
            vector = [set(domain[:]) for _ in range(index)]

            # iterate the infinity deltas to remove them from the vector
            for choice, idx in set(deltas):
                if choice in vector[idx]:
                    vector[idx].remove(choice)

            vector = tuple([tuple(entry) for entry in vector])
            # keep maximal and distinct choices
            if distinct or Choices.vect_new(vectors, vector):
                if not distinct:
                    Choices.vect_rm(vectors, vector)
                vectors.add(vector)

        # change the remaining choices at each index to lists (not sets)
        # so the vectors can be saved to file
        return Choices.to_choices(list(vectors))

    @staticmethod
    def to_choices(vectors: List[VECT]) -> CHOICES:
        """Convert a list of vectors to CHOICES type.
        This is a simple type conversion over the inner collection-types."""
        return [list([list(c) for c in v]) for v in vectors]

    @staticmethod
    def vect_new(vectors: Set[VECT], vector: VECT) -> bool:
        """Determines if a vector is distinct from all existing vectors.

        Arguments:
            vectors: a set of known vectors.
            vector: vector to check.

        Returns:
            True if vector does not occur in vectors.
        """
        return not next((Choices.vect_contains(v, vector)
                         for v in vectors), False)

    @staticmethod
    def vect_rm(vectors: Set[VECT], vector: VECT) -> None:
        """Remove from vectors those that are contained by vector.

        Arguments:
            vectors: a set of vectors.
            vector: vector compare against.
        """
        to_remove = [v for v in vectors if Choices.vect_contains(vector, v)]
        [vectors.remove(v) for v in to_remove]

    @staticmethod
    def vect_contains(a: VECT, b: VECT) -> bool:
        """Check if A allows making all choices of B.

        Arguments:
            a: first vector.
            b: second vector.

        Returns:
            True if A contains B, and False otherwise.
        """
        return all(all(ib in super_v for ib in sub)
                   for super_v, sub in zip(a, b))

    @staticmethod
    def vect_intersection(a: VECT, b: VECT) -> Optional[VECT]:
        """Intersection of two vectors.

        The intersection is the maximal choice at each index, permitted
        by both vectors A and B. The intersection is empty if, at some
        index, no choice exists.

        Example:
            Let a=`((0,1),(0,2))`, b=`((1,),(1,2))`, and c=`((1,),(1,))`.

            * The intersection of a&b is `((1,),(2,))`.
            * The intersection of a&c is None.
            * The intersection of b&c is `((1,),(1,))`.

        Arguments:
            a: first vector.
            b: second vector.

        Returns:
            A new vector that is the intersection of A and B; `None` when the
                intersection is empty.
        """
        tmp = tuple([tuple([ax for ax in av if ax in bv])
                     for av, bv in zip(a, b)])
        empty = next((True for x in tmp if len(x) == 0), False)
        return None if empty else tmp

    @staticmethod
    def intersection(c1: Choices, c2: Choices) -> Choices:
        """Intersection of two choice vectors.

        Intersection is a cross-product of non-empty vector intersections.
        If the none of the vectors intersect, the resulting Choice is empty.

        Arguments:
            c1: First Choice vector.
            c2: Second Choice vector.

        Returns:
              New Choices representing the intersection of the two arguments.
        """
        assert c1.index == c2.index
        choices = Choices.to_choices([j for sub in [
            [Choices.vect_intersection(v1, v2)
             for v2 in c2.valid] for v1 in c1.valid] for j in sub if j])
        return Choices(valid=choices, index=c1.index)

    @staticmethod
    def choice_reduce(*c: Choices) -> Choices:
        if len(c) == 0:
            return Choices()
        result = c[0]
        for n in range(1, len(c)):
            result = Choices.intersection(result, c[n])
        return result
