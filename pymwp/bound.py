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
from typing import List, Tuple, Union

from pymwp.relation import SimpleRelation


class HonestPoly:
    """Models an honest polynomial."""

    def __init__(self, operator: str, *init_vars: str):
        self.variables = set(init_vars)
        self.op = operator
        self.var_fmt = None

    def __eq__(self, other: HonestPoly):
        return self.variables == other.variables

    @property
    def empty(self) -> bool:
        return len(self.variables) == 0

    @property
    def vars(self) -> List[str]:
        var_list = [self.var_fmt(v) for v in self.variables] \
            if self.var_fmt else self.variables
        return sorted(list(var_list))

    @property
    def value(self) -> Union[int, str]:
        return 0 if self.empty else self.op.join(self.vars)

    def add(self, *identifier: str):
        for i in identifier:
            self.variables.add(i)

    def __str__(self):
        return str(self.value)


class MaxVar(HonestPoly):
    """m-variables"""

    def __init__(self, *init_vars):
        super().__init__(',', *init_vars)


class MwpBound:
    """Represents MWP bound."""

    def __init__(self, triple: str = None):
        x, y, z = self.parse_triple_str(triple)
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
    def bound_triple(self) -> Tuple[Tuple[str], Tuple[str], Tuple[str]]:
        """Alternative bounds representation.

        Example:
            ```
            (X1,) (,) (X4, X5)
            ```

        Returns:
            Current bound as $(m_1,...m_n), (w_1,...w_n), (p_1,...p_n)$
                where the first contains list of variables in m,
                second contains variables in w, and last in p (if any).
        """
        return tuple(self.x.vars), tuple(self.y.vars), tuple(self.z.vars)

    @property
    def bound_triple_str(self) -> str:
        """Alternative bounds representation.

        Example:
            ```
            X1;;X4,X5
            ```

        Returns:
            Current bound as `m;w;p` where the first section contains
                list of variables in m, second contains variables in w,
                and last in p (if any).
        """
        return f'{";".join([",".join(v) for v in self.bound_triple])}'

    @staticmethod
    def parse_triple_str(value: str = None):
        """Restore bound from triple format"""
        return [v.split(',') if v else [] for v in value.split(";")] \
            if value else ([], [], [])

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
        if scalar == 'm':
            self.x.add(var_name)
        if scalar == 'w':
            self.y.add(var_name)
        if scalar == 'p':
            self.z.add(var_name)


class Bound:
    """Represents an MWP bound for a relation.

    There is one mwp-bound expression for each input variable.
    """

    LAND = '∧'

    def __init__(self, bounds: dict = None):
        self.bound_dict = dict([
            (k, MwpBound(triple=v)) for k, v in bounds.items()]) \
            if bounds else {}

    @property
    def variables(self) -> list[str]:
        return list(self.bound_dict.keys())

    def __eq__(self, other: Bound):
        return (self.variables == other.variables and
                all(self.bound_dict[k] == other.bound_dict[k]
                    for k in self.variables))

    def calculate(self, relation: SimpleRelation) -> Bound:
        """Calculate bound from a simple-valued matrix.

        Arguments
            relation: a simple-valued relation.

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
        """Get serializable dictionary representation of a bound."""
        return dict([(k, v.bound_triple_str)
                     for k, v in self.bound_dict.items()])

    def show_poly(
            self, compact: bool = False, significant: bool = False,
            variables: List[str] = None
    ) -> str:
        """Format a nice display string of bounds.

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
