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

from typing import Union, Callable, Optional, Tuple, List

from . import B_TRIPLE
from .relation import SimpleRelation
from .semiring import UNIT_MWP, WEAK_MWP, POLY_MWP


class HonestPoly:
    """Models an honest polynomial.

    Attributes:
        variables (set[str]): List of variables.
        var_fmt(Callable): Variable formatter.
        op (str): Operator.
    """

    def __init__(self, operator: str, *init_vars: str):
        """Creates a honest polynomial.

        Arguments:
            operator (str): Operator.
            *init_vars (str): Arbitrary variables.
        """
        self.variables = set(init_vars)
        self.var_fmt: Optional[Callable[[str], str]] = None
        self.op = operator

    def __eq__(self, other: HonestPoly):
        return self.variables == other.variables

    @property
    def empty(self) -> bool:
        """True if honest polynomial is empty."""
        return len(self.variables) == 0

    @property
    def vars(self) -> List[str]:
        """Sorted list of variables."""
        var_list = [self.var_fmt(v) for v in self.variables] \
            if self.var_fmt else self.variables
        return sorted(list(var_list))

    @property
    def value(self) -> Union[int, str]:
        """String representation of HP value."""
        return 0 if self.empty else self.op.join(self.vars)

    def add(self, *identifier: str):
        """Add variables to HP."""
        for i in identifier:
            self.variables.add(i)

    def __str__(self):
        return str(self.value)


class MaxVar(HonestPoly):
    """Representation for m-variables."""

    def __init__(self, *init_vars: str):
        super().__init__(',', *init_vars)


class MwpBound:
    """Represents a mwp-bound.

    Attributes:
        x (Tuple[str]): List of m-variables.
        y (Tuple[str]): List of w-variables.
        z (Tuple[str]): List of p-variables.
    """

    def __init__(self, triple: str = None):
        """Create mwp-bound.

        Arguments:
            triple (str): Bound expression as bound_str.
        """
        x, y, z = self.parse(triple)
        self.x = MaxVar(*x)
        self.y = HonestPoly('+', *y)
        self.z = HonestPoly('*', *z)

    def __str__(self):
        return self.bound_poly(self)

    def __eq__(self, other: MwpBound):
        return (self.x == other.x
                and self.y == other.y
                and self.z == other.z)

    @property
    def bound_triple(self) -> B_TRIPLE:
        """Alternative bounds representation, as three tuples.

        Returns:
            Current bound as $(m_1,...m_n), (w_1,...w_n), (p_1,...p_n)$
                where the first contains list of variables in m,
                second contains variables in w, and last in p (if any).
        """
        return tuple(self.x.vars), tuple(self.y.vars), tuple(self.z.vars)

    @property
    def bound_str(self) -> str:
        """Alternative bounds representation, as a `;`-separated string.

        Returns:
            Current bound as $m;w;p$ where the first section contains
                list of variables in m, second contains variables in w,
                and last in p (if any). Multiple elements in the lists
                are separated by commas.
        """
        return f'{";".join([",".join(v) for v in self.bound_triple])}'

    def poly(self, k: str, compact: bool = False):
        bound_exp = MwpBound.bound_poly(self, compact)
        return f'{k}′{"≤" if compact else " ≤ "}{bound_exp}'

    @staticmethod
    def parse(value: str = None) -> B_TRIPLE:
        """Restore a bound from string-triple format."""
        return tuple([tuple(v.split(',')) if v else []
                      for v in value.split(";")]) if value \
            else (tuple(), tuple(), tuple())

    @staticmethod
    def bound_poly(mwp: MwpBound, compact=False):
        x, y, z, term = mwp.x, mwp.y, mwp.z, None
        # Any of the three variable lists might be empty
        if not x.empty and not y.empty:
            term = f'max({x},{y})'
        elif not x.empty:
            term = (f'max({x})' if len(x.vars) > 1 else str(x)) \
                if compact else (
                f'max({x},0)' if (len(x.vars) > 1 or not z.empty) else str(x))
        elif not y.empty:
            term = (f'max({y})' if len(y.vars) > 1 else str(y)) \
                if compact else (
                f'max({y},0)' if (len(y.vars) > 1 or not z.empty) else str(y))
        if term:
            return str(term) if z.empty else f'{term}+{z}'
        return str(z)

    def append(self, scalar: str, var_name: str):
        """Append variable dependency in the right list by scalar."""
        if scalar == UNIT_MWP:
            self.x.add(var_name)
        if scalar == WEAK_MWP:
            self.y.add(var_name)
        if scalar == POLY_MWP:
            self.z.add(var_name)


class Bound:
    """Represents a mwp-bound for a relation. If derivation succeeds,
    there is one mwp-bound expression for each input variable.

    Attributes:
        bound_dict (Dict[str, MwpBound]): Variable bounds.
    """

    LAND = '∧'

    def __init__(self, bounds: dict[str, str] = None):
        """Create a bound.

        Arguments:
            bounds (dict[str, str]): Dictionary of mwp-bounds.
        """

        self.bound_dict = dict([
            (k, MwpBound(triple=v)) for k, v in bounds.items()]) \
            if bounds else {}

    def __eq__(self, other: Bound):
        return (self.variables == other.variables and
                all(self.bound_dict[k] == other.bound_dict[k]
                    for k in self.variables))

    @property
    def variables(self) -> List[str]:
        """List of variables."""
        return list(self.bound_dict.keys())

    def calculate(self, relation: SimpleRelation) -> Bound:
        """Calculate bound from a simple-valued matrix.

        Arguments:
            relation: A simple-valued relation.

        Returns:
            The bound for the relation.
        """
        vars_, matrix = relation.variables, relation.matrix
        for col_id, name in enumerate(vars_):
            var_bound = MwpBound()
            for row_id in range(len(matrix)):
                var_bound.append(matrix[row_id][col_id], vars_[row_id])
            self.bound_dict[name] = var_bound
        return self

    def to_dict(self) -> dict:
        """A dictionary representation of a bound."""
        return dict([(k, v.bound_str)
                     for k, v in self.bound_dict.items()])

    def show(
            self, compact: bool = False, significant: bool = False,
            variables: Tuple[str] = None
    ) -> str:
        """Formatted display-string of a bound.

        Arguments:
            compact: reduce whitespace in the output
            significant: omit bounds that depend only on self
            variables: list of variables to display

        Returns:
            A formatted string of the bound.
        """
        key_filter = variables or list(self.bound_dict.keys())
        return f' {Bound.LAND} '.join([
            f'{k}′{"≤" if compact else " ≤ "}'
            f'{MwpBound.bound_poly(v, compact=compact)}'
            for k, v in self.bound_dict.items()
            if (not significant or str(k) != str(v)) and k in key_filter])
