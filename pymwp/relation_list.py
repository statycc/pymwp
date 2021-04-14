# flake8: noqa: W605

from __future__ import annotations

from constants import DEBUG
from relation import Relation


class RelationList:
    """
    TODO: What is this class? Add description
    """

    # TODO: what type is variables?
    def __init__(self, variables):
        """Create relation list"""
        self.list = [Relation(variables)]

    def __str__(self) -> str:
        relations = ["{0}:\n{1}".format(i + 1, r)
                     for i, r in enumerate(self.list)]
        return "--- Affiche {0} ---\n{1}\n--- FIN ---" \
            .format(super().__str__(), '\n'.join(relations))

    # TODO: this happens in place -> change uses to in-place
    def identity(self) -> RelationList:
        """
        TODO: add description

        Returns:
            TODO: Updated object?
        """
        rel = Relation(self.list[0].variables)
        self.list = [rel.identity()]
        return self

    # TODO: add vector type
    # TODO: add i type
    def replace_column(self, vector, i) -> None:
        """Replace column with a provided vector.

        Arguments:
            vector: vector that will replace column
            i: TODO: add description
        """
        if DEBUG >= 2:
            print("replace column: vector=", vector, "i=", i, self)

        self.list = [rel.replace_column(value, i)
                     for value in vector
                     for rel in self.list]

        if DEBUG >= 2:
            print("DEBUG_LEVEL: relation après replace_column", self)

    def composition(self, other: RelationList) -> None:
        """Composition of the entire list of relations

        Arguments:
            other: RelationList to compose with self
        """
        if DEBUG >= 2:
            print("DEBUG_LEVEL: composition de relationList", other, self)

        new_list = []

        for r1 in self.list:
            for r2 in other.list:
                output = r1.composition(r2)
                if RelationList.unique(output.matrix, new_list):
                    new_list.append(output)

        self.list = new_list

        if DEBUG >= 2:
            print("DEBUG: Result", self)

    def one_composition(self, other: Relation) -> None:
        """Composition of the entire list of relations

        Arguments:
            other: Relation to compose with self
        """
        if DEBUG >= 2:
            print("DEBUG: composition de relationList", other, self)

        self.list = [r.composition(other) for r in self.list]

        if DEBUG >= 2:
            print("DEBUG: Result", self)

    # TODO: this happens in place -> change uses to in-place
    def sum_relation(self, other: RelationList) -> RelationList:
        """Sum of the entire list of relations

        Arguments:
            other: Relation list to sum with self

        Returns:
            new relation list
        """
        self.list = [r1.sum_relation(r2)
                     for r1 in self.list
                     for r2 in other.list]
        return self

    def fixpoint(self) -> None:
        """Fixpoint of the entire list of relations."""
        self.list = [rel.fixpoint() for rel in self.list]

    def show(self) -> None:
        """Display relation list."""
        print(str(self))

    def while_correction(self) -> None:
        """Loop correction (see MWP - Lars&Niel paper)."""
        for rel in self.list:
            rel.whileCorrection()

    @staticmethod
    def unique(matrix: list, matrix_list: list) -> bool:
        """Determine if matrix list contains matrix.

        Arguments:
            matrix: matrix to find
            matrix_list: list of matrices

        Returns:
            True if list does not contain matrix
        """
        return next((False for o in matrix_list if
                     o.matrix == matrix), True)
