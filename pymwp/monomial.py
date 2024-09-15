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

from typing import List, Optional, Tuple, Union

from . import DELTA
from .constants import SetInclusion
from .semiring import ZERO_MWP, UNIT_MWP, prod_mwp, sum_mwp


class Monomial:
    """
    A monomial is a pair made of:

    1. `scalar` - a value in the semi-ring
    2. a sorted list of `deltas`, where an index occurs at most once.

    Deltas are coded as pairs $(i,j)$ with:

    - $i$ the value and
    - $j$ the index in the domain (infinite product)

    We will have that $(i,j)$ will be equal to the unit of the semi-ring
    iff the $j^{th}$ input is equal to $i$ (so, the $j^{th}$ choice is $i$).

    We will make the assumption that the deltas of delta is sorted
    and no two deltas can have the same index.

    Attributes:
        scalar (str): Monomial scalar.
        deltas (List[DELTA]): List of deltas.
    """

    def __init__(self, scalar: str = UNIT_MWP,
                 deltas: Optional[Union[List[DELTA], DELTA]] = None,
                 *args: Optional[DELTA]):
        """Create a monomial.

        Example:
            Create a monomial.

            ```python
            mono = Monomial()
            ```

            Create monomial with scalar $m$ explicitly.

            ```python
            mono = Monomial('m')
            ```

            Create monomial with scalar $w$ and two deltas.

            ```python
            mono = Monomial('w', (0, 0), (1, 1))
            ```

        Arguments:
            scalar: Monomial scalar.
            deltas: A delta or a list of deltas.
            *args: Arbitrary number of subsequent deltas.
        """
        self.deltas = []
        self.scalar = scalar

        if deltas is not None:
            if isinstance(deltas, list):
                Monomial.insert_deltas(self, deltas)
            if isinstance(deltas, tuple):
                delta_list = [deltas] + list(args if args else [])
                Monomial.insert_deltas(self, delta_list)

    def __str__(self) -> str:
        deltas = [".delta({0},{1})".format(*delta) for delta in self.deltas]
        return self.scalar + ''.join(deltas)

    def __mul__(self, other) -> Monomial:
        return self.prod(other)

    @staticmethod
    def format(value: Union[str, Monomial, Tuple]) -> Monomial:
        if isinstance(value, Monomial):
            return value
        if isinstance(value, str):
            return Monomial(value)
        if isinstance(value, Tuple):
            return Monomial(*value)

    def contains(self, m: Monomial) -> bool:
        """Check if all deltas of m are in deltas of self.

        Arguments:
            m: A monomial to search for intersection.

        Returns:
            False if one delta of m not in self, True otherwise.
        """
        for b in m.deltas:
            if b not in self.deltas:
                return False
        return True

    def inclusion(self, monomial: Monomial) -> SetInclusion:
        """Gives info about inclusion of self monomial with monomial.

        Arguments:
            monomial: A monomial to see inclusion.

        Returns:
            CONTAINS if self contains monomial, INCLUDED if self is included
                in monomial, and EMPTY none of them.
        """
        # self contains monomial ?
        contains: bool = self.contains(monomial)

        summ = sum_mwp(self.scalar, monomial.scalar)
        # if self contains monomial and self.scalar >= monomial.scalar
        if contains and (monomial.scalar == summ):
            return SetInclusion.CONTAINS
        else:
            # self included in monomial and self.scalar <= monomial.scalar
            included: bool = monomial.contains(self)
            if included and (self.scalar == summ):
                return SetInclusion.INCLUDED
            else:
                return SetInclusion.EMPTY

    def prod(self, monomial: Monomial) -> Monomial:
        """Prod combines two monomials where one is this monomial (self)
        and the second is an argument.

        The attributes of the resulting monomial are determined as follows:

        - output scalar is a product of the input scalars
        - two lists of deltas are merged according to rules of insert_delta

        Arguments:
            monomial: The second monomial.

        Returns:
            A new Monomial that is a product of two monomials.
        """
        # make a copy of self
        mono_product = self.copy()

        # determine the new scalar
        mono_product.scalar = prod_mwp(self.scalar, monomial.scalar)

        # if scalar is 0, monomial cannot have deltas
        if mono_product.scalar == ZERO_MWP:
            mono_product.deltas = []

        # otherwise merge the two lists of deltas
        # result already contains deltas from "self"
        # so we are adding to it the deltas from
        # the second monomial passed in as argument
        elif monomial.deltas:
            # TODO here insert only those not contained ?
            Monomial.insert_deltas(mono_product, monomial.deltas)

        return mono_product

    def choice_scalar(self, *choices: int) -> Optional[str]:
        """Determine if given sequence of choices matches monomial.

        Arguments:
            choices: Tuple of choices.

        Returns:
            Monomial's scalar if structure matches choices and None otherwise.
        """
        for (i, j) in self.deltas:
            if not i == choices[j]:
                return None
        return self.scalar

    def copy(self) -> Monomial:
        """Make a deep copy of a monomial."""
        return Monomial(self.scalar, self.deltas[:])

    def show(self) -> None:
        """Display scalar and the list of deltas."""
        print(str(self))

    def to_dict(self) -> dict:
        """Get dictionary representation of a monomial."""
        return {
            "scalar": self.scalar,
            "deltas": self.deltas
        }

    @staticmethod
    def insert_deltas(monomial: Monomial, deltas: List[DELTA]) -> None:
        """Insert new deltas into monomial list of deltas.

        Arguments:
            monomial: The monomial into whose list of deltas values will
                be inserted.
            deltas: List of deltas to insert into monomial.
        """

        # Deltas are inserted one after the other so that
        # the resulting list is ordered
        for delta in deltas:
            monomial.deltas = Monomial.insert_delta(monomial.deltas, delta)

            # change the scalar to 0 because we have a null
            # monomial after insert
            if not monomial.deltas:
                monomial.scalar = ZERO_MWP
                # we can stop inserting if this happens
                break

    @staticmethod
    def insert_delta(sorted_deltas: List[DELTA], delta: DELTA) -> List[DELTA]:
        """
        Takes as input a _sorted_ list of deltas and a delta.

        Check if two deltas have the same index:

        If they do, and if they:

        - disagree on the value expected, returns `[]` (empty list)
        - agree on the value expected, returns the original deltas

        If they don't:

        - add the new delta in the deltas "at the right position".

        Arguments:
            sorted_deltas: List of deltas where to perform insert.
            delta: The delta value to be inserted.

        Returns:
            updated list of deltas.
        """

        # insert position index
        i = 0

        # iterate existing deltas and look for
        # where to insert the new value
        while i < len(sorted_deltas):

            # if delta to insert has higher index
            # go to next one
            if sorted_deltas[i][1] < delta[1]:
                i = i + 1

            # if delta to insert matches existing index
            elif sorted_deltas[i][1] == delta[1]:

                # when delta to insert is already in the
                # list, return the original list without
                # performing insert
                if sorted_deltas[i][0] == delta[0]:
                    return sorted_deltas

                # If the delta disagrees with the choices
                # previously stored, we simply return the
                # empty list: we will never be able to
                # accommodate both the requirement of
                # the existing list and of the new delta.
                return []

            else:
                break

        # perform insert at appropriate index
        sorted_deltas.insert(i, delta)
        return sorted_deltas
