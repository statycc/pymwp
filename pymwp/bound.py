from __future__ import annotations
from typing import List

from pymwp.relation import SimpleRelation


class HonestPoly:
    """Models an honest polynomial."""

    def __init__(self, operator: str):
        self.variables = set()
        self.op = operator

    @property
    def empty(self) -> bool:
        return len(self.variables) == 0

    @property
    def vars(self) -> List[str]:
        return sorted(list(self.variables))

    def add(self, identifier: str):
        self.variables.add(identifier)

    def __str__(self):
        return '0' if self.empty else \
            self.op.join(self.vars)


class MaxVar(HonestPoly):
    """m-variables"""

    def __init__(self):
        super().__init__(operator=',')


class MwpBound:
    """Represents MWP bound."""

    def __init__(self):
        self.x = MaxVar()
        self.y = HonestPoly('+')
        self.z = HonestPoly('*')

    def __str__(self):
        # Any of the three variable lists x, y, z might be empty
        term = (f'max({self.x},{self.y})'
                if not self.x.empty and not self.y.empty else
                self.x if not self.x.empty else
                self.y if not self.y.empty else None)
        return (str(term) if self.z.empty else f'{term}+{self.z}') \
            if term else str(self.z)

    def append(self, scalar: str, var_name: str):
        """Append variable dependency in the right list by scalar."""
        if scalar == 'm':
            self.x.add(var_name)
        if scalar == 'w':
            self.y.add(var_name)
        if scalar == 'p':
            self.z.add(var_name)


class Bound:
    """Calculates MWP bound for a relation."""

    # TODO: make this bound format easier to recover
    #   serialize: to_dict() -> deserialize: how???
    def __init__(self, relation: SimpleRelation = None):
        self.bound_dict = {}
        if relation:
            vars_, matrix = relation.variables, relation.matrix
            for col_id, name in enumerate(vars_):
                var_bound = MwpBound()
                for row_id in range(len(matrix)):
                    var_bound.append(matrix[row_id][col_id], vars_[row_id])
                self.bound_dict[name] = var_bound

    def show(self, compact=False, significant=False) -> str:
        """Format a nice display string of mwp-bounds.

        Arguments:
            compact - reduce whitespace in the output
            significant - omit bounds that depend only on self

        Returns:
            A formatted string of the bound.
        """
        return ' ∧ '.join([f'{k}′ ≤ {v}' if not compact else f'{k}≤{v}'
                           for k, v in self.bound_dict.items()
                           if (not significant or str(k) != str(v))])

    def to_dict(self) -> dict:
        """Get (serializable) dictionary representation of a bound."""
        return dict([(k, str(v)) for k, v in self.bound_dict.items()])
