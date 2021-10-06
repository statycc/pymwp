# flake8: noqa: W605

from __future__ import annotations
from typing import Optional, List, Tuple
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
    """

    def __init__(self, scalar: str = UNIT_MWP, deltas: Optional[List[Tuple[int, int]]] = None):
        """Create a monomial.

        Example:


        Create a monomial

        ```python
        mono = Monomial()
        ```

        Create monomial with scalar $m$ explicitly.

        ```python
        mono = Monomial('m')
        ```

        Create monomial with scalar $w$ and two deltas

        ```python
        mono = Monomial('w', [(0, 0), (1, 1)]
        ```

        Arguments:
            scalar: monomial scalar
            deltas: list of deltas
        """

        self.deltas = []
        self.scalar = scalar

        if deltas:
            Monomial.insert_deltas(self, deltas)

    def __str__(self) -> str:
        deltas = [".delta({0},{1})".format(*delta)
                  for delta in self.deltas]
        return self.scalar + ''.join(deltas)

    def __mul__(self, other) -> Monomial:
        return self.prod(other)

    def contains(self, m: Monomial) -> bool:
        """check if all deltas of m are in deltas of self

        Arguments:
            self: this monomial
            m: a monomial to search for intersection

        Returns:
            False if one delta of m not in self
            True otherwise
        """
        for b in m.deltas:
            if not (b in self.deltas):
                return False
        return True

    def inclusion(self, monomial: Monomial) -> SetInclusion:
        """gives info about inclusion of self monomial with monomial

        Arguments:
            self: this monomial
            monomial: a monomial to see inclusion

        Returns:
            CONTAINS if self contains monomial
            INCLUDED if self is included in monomial
            EMPTY none of them
        """
        # self contains monomial ?
        contains:bool = self.contains(monomial)

        summ = sum_mwp(self.scalar,monomial.scalar)
        # if self contains monomial and self.scalar >= monomial.scalar
        if contains and (monomial.scalar == summ):
            return SetInclusion.CONTAINS
        else:
            # self included in monomial and self.scalar <= monomial.scalar
            included:bool = monomial.contains(self)
            if included and (self.scalar==summ):
                return SetInclusion.INCLUDED
            else:
                return SetInclusion.EMPTY

    def prod(self, monomial: Monomial) -> Monomial:
        """
        prod operation combines two monomials where
        one is this monomial (self) and the second is
        provided as an argument.

        The attributes of the resulting monomial are
        determined as follows:

        - output scalar is a product of the input scalars
        - two lists of deltas are merged according
          to rules of insert_delta

        Arguments:
            monomial: the second monomial

        Returns:
            a new Monomial that is a product of two monomials
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

    def eval(self, argument_list: List[int]) -> str:
        """Evaluate delta values against argument list.

        The result of eval is determined as follows:

        If the list of values given as an argument "match" all
        the deltas, then the value is returned. Otherwise 0 is
        returned.

        When matching we compare delta value $i$ at index $j$ to the
        $j^{th}$ value in the argument list.

        It can accommodate list of values that are of length
        greater than the max of the indices in the deltas, but
        not a list whose length is shorter than the max of the
        indices in the delta.

        Arguments:
            argument_list: list of deltas to evaluate

        Raises:
            IndexError: if argument list length is less than
                max index in the list of deltas.

        Returns:
            Scalar of the monomial if the evaluation matches and
            otherwise 0.
        """
        for (i, j) in self.deltas:
            if argument_list[j] != i:
                return ZERO_MWP
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
    def insert_deltas(monomial: Monomial, deltas: List[tuple]) -> None:
        """Insert new deltas into monomial list of deltas.

        Arguments:

            monomial: the monomial into whose list of
                deltas values will be inserted

            deltas: list of deltas to insert into monomial
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
    def insert_delta(sorted_deltas: List[tuple], delta: tuple) -> List[tuple]:
        """
        Takes as input a _sorted_ list of deltas and a delta.

        Check if two deltas have the same index:

        If they do, and if they:

        - disagree on the value expected, returns `[]` (empty list)
        - agree on the value expected, returns the original deltas

        If they don't:
         add the new delta in the deltas "at the right position".

        Arguments:
            sorted_deltas: list of deltas where to perform insert
            delta: the delta value to be inserted

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
