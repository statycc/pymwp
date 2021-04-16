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

        When creating a relations list, specify either `variables` or `relation_list`.

        Specifying a `relation_list` argument, whose value is a list of `Relations`, will
        initialize a `RelationList` containing the provided relations.

        If no `relation_list` argument is provided, the constructor will create a
        relation list with 1 relation, using the provided `variables` to initialize
        that relation.

        See [`RelationList.identity()`](relation_list.md#pymwp
        .relation_list.RelationList.identity) if you want to create a relation list
        containing an identity relation.

        Example:

        Create relation list using specific variables

        ```python
        rel_list = RelationList(['X0', 'X1', 'X2'])

        # Generates a list with 1 relation:
        #
        # 1:      X0    |     +o  +o  +o
        #         X1    |     +o  +o  +o
        #         X2    |     +o  +o  +o
        ```

        Create relation list by providing relations

        ```python
        r1 = Relation(['X0', 'X2'])
        r2 = Relation(['X0'])
        rel_list = RelationList(relation_list = [r1,r2])

        # Generates a list with 2 relations:
        #
        # 1:      X0    |     +o  +o
        #         X2    |     +o  +o
        #
        # 2:      X0    |     +o
        ```

        Arguments:
            variables: list of variables used to initialize
                a relation on relation list.
            relation_list: list of relations for initializing
                relation list
        """
        self.list = relation_list or [Relation(variables)]

    @staticmethod
    def identity(variables: List[str]) -> RelationList:
        """Create relation list that contains 1
        [identity relation](relation.md#pymwp.relation.Relation.identity).

        This is an alternative way to construct a relation list.

        Example:

        Create relation list containing an identity relation

        ```python
        rel_list = RelationList.identity(['X0', 'X1', 'X2'])

        # Generates a list with 1 identity relation:
        #
        # 1:      X0    |     +m  +o  +o
        #         X1    |     +o  +m  +o
        #         X2    |     +o  +o  +m
        ```

        Arguments:
            variables: list of variables

        Returns:
            RelationList that contains identity relation generated
            using the provided variables.
        """
        return RelationList(relation_list=[Relation.identity(variables)])

    def __str__(self) -> str:
        relations = ['{0}:\n{1}'.format(i + 1, r)
                     for i, r in enumerate(self.list)]

        return "--- Affiche {0} ---\n{1}\n--- FIN ---" \
            .format(super().__str__(), '\n'.join(relations))

    def __add__(self, other):
        return RelationList(relation_list=[
            r1 + r2 for r1 in self.list
            for r2 in other.list])

    def replace_column(self, vector: list, variable: str) -> None:
        """For each relation in a relation list, replace column
        with a provided vector, in place.

        Arguments:
            vector: vector that will replace a column
            variable: variable value; replace will occur
                at the index of this variable.
        """

        self.list = [rel.replace_column(vector, variable)
                     for rel in self.list]

    def composition(self, other: RelationList) -> None:
        """Apply composition to all relations in a relation list.

        This method takes as argument another relation list,
        then composes the product of `self` and `other` by computing
        the product of each relation.

        This operation is performed in place. After composition
        `self` will contain all obtained unique relations.

        To compose relation list and a single relation, see
        [`one_composition`](relation_list.md#pymwp.relation_list.
        RelationList.one_composition).

        Arguments:
            other: RelationList to compose with `self`
        """
        new_list = []
        for r1 in self.list:
            for r2 in other.list:
                output = r1 * r2
                if not any(m.matrix == output.matrix
                           in m for m in new_list):
                    new_list.append(output)

        self.list = new_list

    def one_composition(self, relation: Relation) -> None:
        """Compose each relation in a relation list × relation.

        This iterates current relation list and applies composition to each
        relation in the list, using the `relation` argument as the other operand.

        Arguments:
            relation: relation to compose with relations in current list.
        """
        self.list = [rel * relation for rel in self.list]

    def fixpoint(self) -> None:
        """Apply [fixpoint](relation.md#pymwp.relation.Relation.fixpoint)
         to all relations in relation list."""
        self.list = [rel.fixpoint() for rel in self.list]

    def show(self) -> None:
        """Display relation list."""
        print(str(self))

    def while_correction(self) -> None:
        """Apply [`while_correction`](relation.md#pymwp.relation.Relation
        .while_correction) to all relations in a relation list."""
        for rel in self.list:
            rel.while_correction()
