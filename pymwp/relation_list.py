# flake8: noqa: W605

from __future__ import annotations
from typing import List, Optional

from relation import Relation


class RelationList:
    """
    Relation list holds a list of [`relations`](relation.md#pymwp.relation)
    and provides methods for performing operations on those relations.
    """

    def __init__(self, variables: Optional[List[str]] = None,
                 relation_list: Optional[List[Relation]] = None):
        """Create relation list.

        When constructing a relation list, you can provide a list of relations
        by specifying a relation_list argument value is a list of relations.

        If no initial list is provided, the constructor will construct a list
        with 1 relation, using the provided variables.


        Arguments:
            variables: list of variables used to initialize
                a relation on relation list.
            relation_list: list of relations for initializing
                relation list

        Returns:
            RelationList with initialized relation(s)
        """
        self.list = relation_list or [Relation(variables)]

    @staticmethod
    def identity(variables: list) -> RelationList:
        """Create relation list that contains 1
        [`identity relation`](relation.md#pymwp.relation.identity).

        This is an alternative way to construct a relation list.

        Arguments:
            variables: list of variables

        Returns:
            RelationList that contains identity relation generated
            using the provided variables.
        """
        return RelationList(relation_list=[Relation.identity(variables)])

    def __str__(self) -> str:
        return "--- Affiche {0} ---\n{1}\n--- FIN ---" \
            .format(super().__str__(),
                    '\n'.join(['{0}:\n{1}'.format(i + 1, r)
                               for i, r in enumerate(self.list)]))

    def __add__(self, other):
        return RelationList(relation_list=[
            r1 + r2 for r1 in self.list
            for r2 in other.list])

    def replace_column(self, vector: list, variable: str) -> None:
        """Replace column with a provided vector.

        Arguments:
            vector: vector that will replace column
            variable: variable value; replace will occur
                at the index of this variable.
        """
        self.list = [rel.replace_column(value, variable)
                     for rel in self.list
                     for value in vector]

    def composition(self, other: RelationList) -> None:
        """Composition of the entire list of relations

        Arguments:
            other: RelationList to compose with self
        """
        new_list = []
        for r1 in self.list:
            for r2 in other.list:
                output = r1 * r2
                if RelationList.unique(output.matrix, new_list):
                    new_list.append(output)

        self.list = new_list

    def one_composition(self, other: Relation) -> None:
        """Composition of the entire list of relations.

        Arguments:
            other: Relation to compose with current list's relations.
        """
        self.list = [r * other for r in self.list]

    def fixpoint(self) -> None:
        """Compute fixpoint for all relations in this relation list."""
        self.list = [rel.fixpoint() for rel in self.list]

    def show(self) -> None:
        """Display relation list."""
        print(str(self))

    def while_correction(self) -> None:
        """Loop correction (see MWP - Lars&Niel paper)."""
        for rel in self.list:
            rel.while_correction()

    @staticmethod
    def unique(matrix: List[list], matrix_list: List[List[list]]) -> bool:
        """Determine if matrix list contains matrix.

        Arguments:
            matrix: matrix to find
            matrix_list: list of matrices

        Returns:
            True if matrix not found, i.e. all matrices are unique,
            and false otherwise.
        """
        return not any(m.matrix == matrix in m for m in matrix_list)
