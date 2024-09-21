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

# flake8: noqa: W605

from __future__ import annotations

import logging
from functools import reduce
from typing import Optional, List, Tuple, Union

from . import DELTAS, Monomial
from .constants import Comparison, SetInclusion
from .semiring import ZERO_MWP, INFTY_MWP, sum_mwp

logger = logging.getLogger(__name__)


class Polynomial:
    """A polynomial is an ordered list of ordered Monomials.

    For polynomials, I introduce a total order on the monomials. This
    eases the computation of the sum: if we want to add a monomial to an
    ordered list of monomials, we compare the monomial to each of the
    elements of the list until we find either an element which is equal
    (and then we sum the scalars) or an element which is larger (and
    then we insert the new monomial there).

    Polynomials use the following ordering: $\\delta(i,j)$
    is smaller than $\\delta(m,n)$ iff either $j<n$ or $(j==n)$ and $(i<m)$.

    This is extended to products (which we consider ordered!) by
    letting $\\prod_k\\delta(i_k,j_k) < \\prod_l\\delta(m_l,n_l)$
    iff $\\delta(i_1,j_1) < \\delta(m_1,n_1)$.

    Attributes:
         list (List[Monomial]): List of monomials.
    """

    def __init__(
            self,
            *monomials: Optional[Union[str, Monomial, Tuple[str, DELTAS]]]
    ):
        """Create a polynomial.

        Example:
            Create polynomial with 0-monomial:

            ```python
            zero = Polynomial()
            ```

            Create polynomial with one monomial with specific scalar:

            ```python
            poly = Polynomial('w')               # shorthand
            poly = Polynomial(Monomial('w'))     # longer, equivalent
            ```

            Create polynomial with two monomials and lists of deltas:

            ```python
            poly = Polynomial(('m', (0, 1)), ('w', (0, 0), (1, 1)))
            ```

        Arguments:
            monomials: arbitrary monomials.
        """
        m_list = [Monomial.format(v) for v in monomials]
        self.list = m_list if len(m_list) > 0 else [Monomial(ZERO_MWP)]

    def __str__(self):
        values = ''.join(['+' + str(m) for m in self.list]) or ('+' + ZERO_MWP)
        return " " + values

    def __eq__(self, other):
        return self.equal(other)

    def __add__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.times(other)

    def eval(self, *scalars: str) -> List[DELTAS]:
        """List of monomial deltas with scalar in *scalars.
        Scalars always includes $\\infty$, but can include other flows."""
        match = scalars + (INFTY_MWP,)
        return [tuple(mono.deltas) for mono in
                [m for m in self.list if m.scalar in match]]

    @staticmethod
    def inclusion(list_monom: list, mono: Monomial, i: int = 0) \
            -> Tuple[bool, int]:
        """Filter list_monom regarding mono inclusion and return info.

        Remove all monomials of list_monom that are included in mono.

        Return CONTAINS if one of monomials of list_monom contains mono
        (regarding Monomial.inclusion def).

        Arguments:
            list_monom: A list of monomials.
            mono: A monomial we want to add.
            i: The position index where to add mono.

        Returns:
            False if mono already in list_monom and shifted index where to
                insert mono, return True if mono not in list_monom.
        """
        j = 0
        while j < len(list_monom):
            m = list_monom[j]
            incl = m.inclusion(mono)
            # if m ⊆ mono
            if incl == SetInclusion.CONTAINS:
                # We will then add mono so we can remove m
                list_monom.remove(m)
                # If removed monom is before i (where we want to insert mono)
                if j < i:
                    i = i - 1  # shift left position
                continue
            elif incl == SetInclusion.INCLUDED:
                # We don't want to add mono, inform with CONTAINS
                return False, i
            j = j + 1
        # No inclusion
        return True, i

    def add(self, polynomial: Polynomial) -> Polynomial:
        """Add two polynomials.

        - If both lists are empty the result is empty.
        - If one list is empty, the result will be the other list
        of polynomials.

        Otherwise, the operation will zip the two lists together and
        return a new polynomial of sorted monomials.

        Arguments:
            polynomial: Polynomial to add to self.

        Returns:
            New, sorted polynomial that is a sum of the two input polynomials.
        """
        # check for empty lists
        if not self.list and not polynomial.list:
            return Polynomial()
        if not self.list:
            return polynomial.copy()
        if not polynomial.list:
            return self.copy()

        i, j = 0, 0
        new_list = self.copy().list
        # self_len = len(new_list)
        poly_len = len(polynomial.list)

        # iterate lists of monomials until the end of shorter list
        while j < poly_len:
            mono2 = polynomial.list[j]

            tobe_inserted, i = Polynomial.inclusion(new_list, mono2, i)

            if not tobe_inserted:
                j = j + 1
                continue

            # handle case where first list is shorter
            # by just appending what remains of the
            # other list of monomials
            if i == len(new_list):
                for m in polynomial.list[j:]:
                    tobe_inserted, i = Polynomial.inclusion(new_list, m, i)
                    if tobe_inserted:
                        new_list = new_list + [m]
                break

            mono1 = new_list[i]

            check = Polynomial.compare(mono1.deltas, mono2.deltas)

            # move to next when self is smaller
            if check == Comparison.SMALLER:
                i = i + 1

            # insert when the second is smaller
            elif check == Comparison.LARGER:
                new_list.insert(i, mono2)
                i = i + 1
                j = j + 1

            # when both list heads are the same
            # recompute scalar and move to next element
            else:
                new_list[i].scalar = sum_mwp(mono1.scalar, mono2.scalar)
                j = j + 1

        sorted_monomials = Polynomial.sort_monomials(new_list)
        return Polynomial(*sorted_monomials).remove_zeros()

    def times(self, polynomial: Polynomial) -> Polynomial:
        """Multiply two polynomials.

        Here we assume at least self is a sorted polynomial,
        and the result of this operation will be sorted.

        This operation works as follows:

        1. We compute a table of all the separated products
            $P.m_1,...,P.m_n$. Each of the elements is itself
            a sorted list of monomials: $P.m_j=m^j_1,...,m^j_k$

        2. We then sort the list of the first (smallest) elements
            of each list. I.e. we sort the list $m^1_1,m^2_1,...,m^n_1$
            and produce the list corresponding list of indexes of
            length n, I.e. a permutation over ${0,...,n}$.

        3. Once all this preparatory operations are done, the main part
           of the algorithm goes as follows:

        4. We consider the first element — say j — of the list of indexes
           and append to the result the first element of the corresponding
           list $P.m_j$ of monomials.

        5. We remove both the first element of the list of index and
           the first element of $P.m_j$.

        6. If $P.m_j$ is not empty, we insert j in the list of index
           at the right position: for this we compare the (new) first
           element of $P.m_j$ to  $m^{i_2}_1$ (as we removed the
           first element, $i_2$ is now the head of the list of indexes),
           then $m^{i_3}_1$, until we reach the index h such that
           $m^{i_h}_1$ is larger than $m^{j}_1$.

        7. We start back at point 4. Unless only one element is left
           in the list of indexes. In this case, we simply append the
           tail of the corresponding list to the result.

        Arguments:
            polynomial: polynomial to multiply with self.

        Returns:
            A new polynomial that is the sorted product of the two input
                polynomials.
        """

        # 1: compute table of products
        # here we compute P1 x P2 for each polynomial, excluding from the
        # result all monomials that have scalar value 0
        products = [[mono for mono in (m1 * m2 for m1 in self.list)
                     if mono.scalar != ZERO_MWP] for m2 in polynomial.list]
        # filter out empty monomials
        table: List[List[Monomial]] = [p for p in products if p]

        # if table is empty, return zero polynomial
        if not table:
            return Polynomial()

        # 2: create an index lists that represents the ordered
        # monomials in table, ordered by deltas of first monomials
        index_list = [0]
        for i in range(1, len(table)):
            t1 = table[i][0].deltas
            for j in range(len(index_list)):
                t2 = table[index_list[j]][0].deltas
                if Polynomial.compare(t1, t2) == Comparison.SMALLER:
                    index_list.insert(j, i)
                    break
            if i not in index_list:
                index_list.append(i)

        # 3: start main part
        result = []
        while index_list:
            # 4. get first element and append to result
            # 5. remove from index and table
            smallest = index_list.pop(0)
            mono2 = table[smallest].pop(0)
            tobe_inserted, _ = Polynomial.inclusion(result, mono2)
            if tobe_inserted:
                result.append(mono2)

            # 6. when table is non-empty insert j at
            # the right index
            if table[smallest]:
                inserted = False
                t1 = table[smallest][0].deltas
                for j in range(len(index_list)):
                    t2 = table[index_list[j]][0].deltas
                    if Polynomial.compare(t1, t2) == Comparison.SMALLER:
                        index_list.insert(j, smallest)
                        inserted = True
                        break
                if not inserted:
                    index_list.append(smallest)
            # 7. repeat until done

        return Polynomial(*result).remove_zeros()

    def equal(self, polynomial: Polynomial) -> bool:
        """Determine if two polynomials are equal.

        This method will compare current polynomial (self) to
        another polynomial provided as argument. Result of
        true means both polynomials have an equal number of
        monomials, and element-wise each monomial has the same
        list of deltas. Otherwise, the result is false.

        This method is alias of `==` operator.

        Arguments:
            polynomial: polynomial to compare.

        Returns:
            True if polynomials are equal and false otherwise.
        """
        p1, p2 = self.list, polynomial.list

        # the only times deltas are equal is if they contain
        # same values and are equal in length; avoid calling
        # compare because it is more expensive method call; we
        # can do faster equality comparison on deltas this way
        same = [m1.scalar == m2.scalar and m1.deltas == m2.deltas
                for m1, m2 in zip(p1, p2)]

        # if False is in list it means some comparison of
        # deltas was determined not to be equal; do length
        # comparison last because it is almost never False
        return False not in same and len(p1) == len(p2)

    def copy(self) -> Polynomial:
        """Make a deep copy of polynomial."""
        return Polynomial(*[m.copy() for m in self.list])

    def show(self) -> None:
        """Display polynomial."""
        print(str(self))

    @property
    def some_infty(self) -> bool:
        """True if some monomial yields an infinity choice."""
        for mono in self.list:
            if mono.scalar == 'i':
                return True
        return False

    def choice_scalar(self, *choices: int, least_scalar: str = None) \
            -> Optional[str]:
        """For given sequence of choices, determine corresponding scalar.

        Arguments:
            choices: tuple of choices.
            least_scalar: typically zero, but can be m on the diagonal.

        Returns:
            Scalar value matching choices or None.
        """
        scalars = [mono.choice_scalar(*choices) for mono in self.list]
        scalars = [scalar for scalar in scalars if scalar]  # exclude None
        return reduce(sum_mwp, scalars) if scalars else least_scalar

    @staticmethod
    def compare(delta_list1: list, delta_list2: list) -> Comparison:
        """
        Compare 2 lists of deltas.

        We compare the initial segment up to the size of the shortest one.
        If the initial segments match, then the result is determined based
        on length. Three outputs are possible:

        - `SMALLER` if the first list is smaller than the second
        - `EQUAL` if both lists are equal in contents and length
        - `LARGER` if the first list is larger than the second

        The return value represents the relation of first
        list to the second one. `Smaller` means either

        - delta values of first list are smaller -or-
        - deltas are equal but first list is shorter.

        Larger is the opposite case.

        Arguments:
            delta_list1: first monomial list to compare.
            delta_list2: second monomial list to compare.

        Returns:
            Result of comparison.
        """
        # element wise comparison up to length of shorter list
        list_diff = [(a == b) for a, b in zip(delta_list1, delta_list2)]

        # if some difference exists
        if False in list_diff:

            # index of first difference
            idx = list_diff.index(False)

            (i, j), (m, n) = delta_list1[idx], delta_list2[idx]

            if (j < n) or (j == n and i < m):
                return Comparison.SMALLER
            else:
                return Comparison.LARGER

        # If the list coincide on their initial segment up to "max",
        # determine the lengths of the two lists
        first_len, second_len = len(delta_list1), len(delta_list2)

        # determine how first list relates to second list
        if first_len > second_len:
            return Comparison.LARGER
        if first_len < second_len:
            return Comparison.SMALLER
        else:
            return Comparison.EQUAL

    @staticmethod
    def sort_monomials(monomials: list) -> list:
        """Given a list of monomials this method will return them in order.

        The sort is performed by first dividing the list of monomials into
        halves recursively until each half contains at most one monomial.
        Then the sort will begin to combine (or zip) the halves into a sorted
        list.

        The sort performs comparison of deltas, and orders the monomials based
        on the delta values. If two monomials have the same deltas, we compute
        new scalar value, and if it is not 0, we keep the result monomial.
        Note that if we get 2 monomials with same deltas, and only at most 1
        is kept, with possibly updated scalar. This means sort can return a
        result that is shorter than the input argument.

        The original list argument is not mutated by this sort operation, i.e.
        this is not sort in place.

        Arguments:
            monomials: list of monomials to sort.

        Returns:
            list of sorted monomials.
        """
        list_len = len(monomials)

        # base case
        if list_len < 2:
            if monomials and monomials[0] == ZERO_MWP:
                return []
            return monomials

        # split list into two halves equally
        mid_point = list_len // 2
        left = Polynomial.sort_monomials(monomials[mid_point:])
        right = Polynomial.sort_monomials(monomials[:mid_point])

        # construct sorted list by iteratively combining
        # monomials from left and right halves
        new_list = []
        while left and right:
            lhead, *ltail = left
            rhead, *rtail = right
            comparison = Polynomial.compare(lhead.deltas, rhead.deltas)

            # head of left list is smaller -> add it to list
            if comparison == Comparison.SMALLER:
                new_list.append(lhead)
                left = ltail

            # head of right list is smaller -> add it to list
            if comparison == Comparison.LARGER:
                new_list.append(rhead)
                right = rtail

            # list heads are equal i.e. same deltas.
            if comparison == Comparison.EQUAL:
                monomial = lhead
                # append to list as long as scalar
                # product is not 0
                monomial.scalar = sum_mwp(
                    lhead.scalar, rhead.scalar)
                if monomial.scalar != ZERO_MWP:
                    new_list.append(monomial)
                left = ltail
                right = rtail

        # either left or right is empty so order
        # doesn't matter; just append whatever
        # remains of left or right tail
        return new_list + right + left

    def remove_zeros(self) -> Polynomial:
        """Removes all encountered 0s from a polynomial.

        Before returning, if the list is empty, the result produces a
            0-monomial.

        Returns:
            polynomial with list of monomials for which zeros are
            removed, unless 0 is the only monomial.
        """
        filtered_monomials = list(filter(
            lambda mono: mono.scalar != ZERO_MWP, self.list))

        if len(filtered_monomials) == 0:
            self.list = [Monomial(ZERO_MWP)]
        else:
            self.list = filtered_monomials

        return self

    @staticmethod
    def from_scalars(index: int, *scalars: str) -> Polynomial:
        """Build a polynomial of multiple monomials with deltas.

        Example:
            For arguments `index=5` and `scalars= m, w, p`,
            the method returns a Polynomial equal to:

            ```Python
            m1 = Monomial('m', (0, 5))
            m2 = Monomial('w', (1, 5))
            m3 = Monomial('p', (2, 5))

            Polynomial(m1, m2, m3)
            ```

        Arguments:
            index: Delta index.
            scalars: Scalar values.

        Returns:
             Generated polynomial.
         """

        monomials = [Monomial(scalar, (number, index))
                     for number, scalar in enumerate(scalars)]
        return Polynomial(*monomials)
