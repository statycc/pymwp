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

from typing import List, Optional

from . import DeltaGraph, Relation


class RelationList:
    """
    Relation list holds a list of [`Relations`](relation.md).
    It provides methods for performing operations collectively on all
    relations in the list.

    Attributes:
        relations (List[Relation]): List of relations.
    """

    def __init__(self, variables: Optional[List[str]] = None,
                 relation_list: Optional[List[Relation]] = None):
        """To create a relations list, specify either `variables` or
        `relation_list`.

        Arguments:
            variables: List of variables used to initialize a relation on
                relation list.
            relation_list: List of relations for initializing relation list.

        Specifying a `relation_list` argument of a list of `Relations`,
        initializes a `RelationList` containing the provided relations.
        If no `relation_list` argument is provided, the constructor will
        create a relation list with one relation, using the provided
        `variables` to initialize that relation.

        Example:
            Create relation list using specific variables

            ```python
            rel_list = RelationList(['X0', 'X1', 'X2'])
            ```

            Generates a list with 1 relation:

            ```
            X0 |  +o  +o  +o
            X1 |  +o  +o  +o
            X2 |  +o  +o  +o
            ```

            Create relation list by providing relations

            ```python
            relations = [Relation(['X0', 'X1']), Relation(['X0'])]
            rel_list = RelationList(relation_list=relations)
            ```

            Generates a list with 2 relations:

            ```
            1:      X0  |  +o  +o
                    X1  |  +o  +o

            2:      X0  |  +o
            ```

            If no arguments are provided, the result is a relation list with an
            empty relation.

            ```python
            rel_list = RelationList()
            ```

            Generates a list with 1 empty relation.
        """
        self.relations = relation_list or [Relation(variables)]

    @staticmethod
    def identity(variables: List[str]) -> RelationList:
        """Create relation list that contains 1
        [identity relation](relation.md#pymwp.relation.Relation.identity).

        This is an alternative way to construct a relation list.

        Example:
            Create relation list containing an identity relation

            ```python
            rel_list = RelationList.identity(['X0', 'X1', 'X2'])
            ```

            Generates a list with 1 identity relation:

            ```
            X0 |  +m  +o  +o
            X1 |  +o  +m  +o
            X2 |  +o  +o  +m
            ```

        Arguments:
            variables: A list of variables.

        Returns:
            RelationList that contains identity relation generated using the
                provided variables.
        """
        return RelationList(relation_list=[Relation.identity(variables)])

    def __str__(self) -> str:
        relations = '\n\n'.join([f'{r}' for r in self.relations])
        divider = '\n' + ('-' * 72)
        return divider + '\n' + relations + divider

    def __add__(self, other):
        return RelationList(relation_list=[
            r1 + r2 for r1 in self.relations
            for r2 in other.relations])

    @property
    def first(self) -> Relation:
        """Gets the first relation in relation list."""
        return self.relations[0]

    def replace_column(self, vector: list, variable: str) -> None:
        """For each relation in a relation list, replace column with a provided
         vector, in place.

        This method takes as input a variable, then finds the index of that
        variable based on its name, then applies the column replacement at the
        discovered index.

        Arguments:
            vector: vector that will replace a column
            variable: variable value; replace will occur at the index of this
                variable.

        Raises:
            ValueError: if variable does not exists some relation belonging
                to this relation list.
        """

        self.relations = [rel.replace_column(vector, variable)
                          for rel in self.relations]

    def composition(self, other: RelationList) -> None:
        """Apply composition to all relations in two relation lists.

        This method takes as argument `other` relation list, then composes the
        product of `self` and `other` by computing the product of each
        relation, for all combinations.

        Composition occurs in place. After composition `self` will contain all
        unique relations obtained during composition.

        To compose `RelationList` and a single `Relation`, see
        [`one_composition()`](relation_list.md#pymwp.relation_list.
        RelationList.one_composition).

        Arguments:
            other: RelationList to compose with `self`
        """
        new_list = []
        for r1 in self.relations:
            for r2 in other.relations:
                output = r1 * r2
                if not RelationList.contains_matrix(new_list, output.matrix):
                    new_list.append(output)

        self.relations = new_list

    @staticmethod
    def contains_matrix(search_in: List[Relation], matrix: List[List]) -> bool:
        """Check if a list of relations contains the provided matrix.

        Arguments:
            search_in: list of relations to search
            matrix: search value to look for

        Returns:
            `True` if matrix is found somewhere in the list of relations and
                `False` otherwise.
        """
        for relation in search_in:
            if relation.matrix == matrix:
                return True
        return False

    def one_composition(self, relation: Relation) -> None:
        """Compose each relation in a relation list × relation.

        This method iterates current relation list and applies
        [`composition()`](relation.md#pymwp.relation.Relation.composition) to
        each of its relations, using argument `relation` as the other operand.

        Arguments:
            relation: relation to compose with relations in current list.
        """
        self.relations = [rel * relation for rel in self.relations]

    def fixpoint(self) -> None:
        """Apply [fixpoint](relation.md#pymwp.relation.Relation.fixpoint)
         to all relations in relation list."""
        self.relations = [rel.fixpoint() for rel in self.relations]

    def show(self) -> None:
        """Display relation list."""
        print(str(self))

    def while_correction(self, dg: DeltaGraph) -> None:
        """Apply [`while_correction()`](relation.md#pymwp.relation.Relation
        .while_correction) to all relations in a relation list."""
        for rel in self.relations:
            rel.while_correction(dg)

    def loop_correction(self, x_var: str, dg: DeltaGraph) -> None:
        """Apply loop correction."""
        for rel in self.relations:
            rel.loop_correction(x_var, dg)
