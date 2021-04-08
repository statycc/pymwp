# flake8: noqa: W605

from __future__ import annotations
from semiring import ZERO_MWP, UNIT_MWP, prod_mwp


class Monomial:
    """
    A monomial is a pair made of:

    1. scalar - a value in the semi-ring
    2. a sorted list of deltas, where an index occurs at most once.

    Deltas are coded as pairs $(i,j)$ with:

     - $i$ the value and
     - $j$ the index in the domain (infinite product)

    We will have that $(i,j)$ will be equal to the unit of the semi-ring
    iff the $j^{th}$ input is equal to $i$ (so, the $j^{th}$ choice is $i$).

    We will make the assumption that the deltas of delta is sorted
    and no two deltas can have the same index.
    """

    def __init__(self, scalar: str = UNIT_MWP, deltas: list = []):
        """Create a monomial.

        Arguments:
            scalar: monomial scalar
            deltas: list of deltas
        """

        self.deltas = []
        self.scalar = scalar

        Monomial.insert_deltas(self, deltas)

        # monomial.list is alias for monomial.deltas; earlier
        # versions of code used attribute name list but "list"
        # shadows a built-in name in Python. The next line can
        # be removed after all references to monomial.list are
        # removed
        self.list = getattr(self, 'deltas')

    def __str__(self) -> str:
        deltas = [".delta({0},{1})".format(*delta)
                  for delta in self.deltas]
        return self.scalar + ''.join(deltas)

    def __mul__(self, other) -> Monomial:
        return self.prod(other)

    def prod(self, monomial: Monomial) -> Monomial:
        """
        prod operation combines two monomials where
        one is this monomial (self) and the second is
        provided as an argument.

        The attributes of the resulting monomial are
        determined as follows:

        - output scalar is a product of the input scalars
        - two lists of deltas are merged according
          to rules of insert_delta <utility.insert_delta>

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
        elif monomial.list:
            Monomial.insert_deltas(mono_product, monomial.deltas)

        return mono_product

    def eval(self, argument_list: list) -> str:
        """Evaluate delta values against argument list.

        !!! danger "Important!"
            This is one of the most costly methods. If you change
            it, check impact on performance.

        The result of eval is determined as follows:

        If the list of values given as an argument "match" all
        the deltas, then the value is returned. Otherwise 0 is
        returned.

        When matching we compare delta _value at index j_ to the
        $j^{th}$ value in the argument list.

        It can accommodate list of values that are of length
        greater than the max of the indices in the deltas, but
        not a list whose length is shorter than the max of the
        indices in the delta.

        Arguments:
            argument_list: list of deltas to evaluate

        Returns:
            - scalar of the monomial if the evaluation matches
            - otherwise: 0 (represented as `'o'`)

        """
        for (i, j) in self.deltas:
            if argument_list[j] != i:
                return ZERO_MWP
        return self.scalar

    def copy(self) -> Monomial:
        """Make a deep copy."""
        return Monomial(self.scalar, self.deltas[:])

    def show(self) -> None:
        """Display scalar and the list of deltas."""
        print(str(self))

    @staticmethod
    def insert_deltas(monomial: Monomial, deltas_to_insert: list) -> None:
        """Given a monomial with a sorted list of deltas,
        insert new deltas into the list.

        Arguments:
            monomial: the monomial into whose list of
                deltas values will be inserted
            deltas_to_insert: list of deltas to insert
        """

        # Deltas are inserted one after the other so that
        # the resulting list is ordered
        for delta in deltas_to_insert:
            monomial.deltas = Monomial.insert_delta(monomial.deltas, delta)

            # change the scalar to 0 because we have a null
            # monomial after insert
            if not monomial.deltas:
                monomial.scalar = ZERO_MWP
                # we can stop inserting if this happens
                break

    @staticmethod
    def insert_delta(sorted_deltas: list, delta: tuple) -> list:
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
            updated list of deltas
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
