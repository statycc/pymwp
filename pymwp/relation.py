# flake8: noqa: W605

from __future__ import annotations
from typing import Optional

import itertools

import matrix as matrix_utils


class Relation:
    """
    A relation is made of a list of program variables and a 2D-matrix.

    Variables of a relation represent the variables of the input
    program under analysis, for example: $X_0, X_1, X_2$.

    Matrix holds [`polynomial`](polynomial.md#pymwp.polynomial) objects,
    and represents the current state of the analysis.
    """

    def __init__(self, variables: list[str], matrix: Optional[list[list]] = None):
        """Create a relation.

        When constructing a relation, provide a list of variables
        and an initial matrix. If matrix is not provided, the
        relation will be initialized to a zero matrix of size
        matching the number of variables.

        Arguments:
            variables: program variables
            matrix: relation matrix
        """
        self.variables = variables or []
        self.matrix = matrix or matrix_utils \
            .init_matrix(len(self.variables))

    @staticmethod
    def identity(variables: list) -> Relation:
        """Create an identity relation.

        This method allows creating a relation whose
        matrix is an identity matrix. This is an alternative
        way to construct a Relation.

        Arguments
            variables: list of variables

        Returns:
             Generated relation with given variables and
                identity matrix.
        """
        matrix = matrix_utils.identity_matrix(len(variables))
        return Relation(variables, matrix)

    @property
    def is_empty(self):
        return not self.variables or not self.matrix

    def __str__(self):
        return '\n'.join(
            [var + '    |   ' + ''.join(poly) for var, poly in
             [(var, [str(self.matrix[i][j]) for j in range(len(self.matrix))])
              for i, var in enumerate(self.variables)]])

    def __add__(self, other):
        return self.sum(other)

    def __mul__(self, other):
        return self.composition(other)

    def replace_column(self, vector: list, variable: str) -> Relation:
        """Replace matrix column by a vector.

        Arguments:
            vector: vector to insert into the matrix
            variable: program variable; column replacement
                will occur at the index of this variable.

        Returns:
            new relation after applying the column update.
        """
        new_relation = Relation.identity(self.variables)
        j = self.variables.index(variable)

        for idx, value in enumerate(vector):
            new_relation.matrix[idx][j] = value

        return new_relation

    def while_correction(self) -> None:
        """Loop correction.

        See: [MWP paper](https://dl.acm.org/doi/10.1145/1555746.1555752)
        """
        for i, vector in enumerate(self.matrix):
            for j, poly in enumerate(vector):
                for mon in poly.list:
                    if mon.scalar == "p" or (mon.scalar == "w" and i == j):
                        mon.scalar = "i"

    def sum(self, other: Relation) -> Relation:
        """Sum two relations.

        Arguments:
            other: Relation to sum with current

        Returns:
           new relation that is a sum of current
            and the argument.
        """
        er1, er2 = Relation.homogenisation(self, other)
        new_matrix = matrix_utils.matrix_sum(er1.matrix, er2.matrix)
        return Relation(er1.variables, new_matrix)

    def composition(self, other: Relation) -> Relation:
        """Composition of current and another relation.

        This is equivalent to performing operation
        relation * relation.

        Composition will combine the variables of two
        relations and have a matrix that is the product
        of their matrices of the two input relations.

        Arguments:
            other: Relation to compose with current

        Returns:
           new relation that is a product of current
            and the argument.
        """
        er1, er2 = Relation.homogenisation(self, other)
        new_matrix = matrix_utils.matrix_prod(er1.matrix, er2.matrix)
        return Relation(er1.variables, new_matrix)

    def equal(self, other: Relation) -> bool:
        """Determine if two relations are equal.

        For two relations to be equal they must have:

        1. the same variables (independent of order), and
        2. matrix polynomials must be equal element-wise.

        See [`polynomial#equal`](polynomial.md#pymwp.polynomial.equal)
        for details on how to determine equality of two polynomials.

        Arguments:
            other: relation to compare

        Returns:
            true when two relations are equal
            and false otherwise.
        """
        if set(self.variables) != set(other.variables):
            return False

        er1, er2 = Relation.homogenisation(self, other)

        for row1, row2 in zip(er1.matrix, er2.matrix):
            for poly1, poly2 in zip(row1, row2):
                if not poly1.equal(poly2):
                    return False
        return True

    def fixpoint(self):
        """Fixpoint: sum of compositions until no changes occur."""
        fix_vars = self.variables
        matrix = matrix_utils.identity_matrix(len(fix_vars))
        fix = Relation(fix_vars, matrix)
        prev_fix = Relation(fix_vars, matrix)
        current = Relation(fix_vars, matrix)

        while True:
            prev_fix.matrix = fix.matrix
            current = current * self
            fix = fix + current
            if fix.equal(prev_fix):
                return fix

    def eval(self, args) -> Relation:
        """TODO:

        Arguments:
            args: TODO:

        Returns:
            TODO:
        """
        result = Relation([])
        mat = []
        result.variables = self.variables
        for i, row in enumerate(self.matrix):
            mat.append([])
            for poly in row:
                mat[i].append(poly.eval(args))
        result.matrix = mat
        return result

    def is_infinite(self, choices, index):
        """TODO:

        Arguments:
            choices:
            index:

        Returns:
            TODO:
        """
        # uses itertools.product to generate all possible assignments
        args_list = list(itertools.product(choices, repeat=index))
        combinations = []
        for args in args_list:
            list_args = list(args)
            mat = self.eval(list_args).matrix
            if not matrix_utils.contains_infinite(mat):
                combinations.append(list_args)
        return combinations

    def to_dict(self) -> dict:
        """Dictionary representation of Relation."""
        return {
            "variables": self.variables,
            "matrix": matrix_utils.encode(self.matrix)
        }

    def show(self):
        """Display relation."""
        print(str(self))

    @staticmethod
    def homogenisation(r1: Relation, r2: Relation) -> tuple:
        """Performs relation homogenisation.

        After this operation both relations will have same
        variables and their matrices will be same size.

        This operation will resize matrices if needed.

        Arguments:
            r1: first relation to homogenise
            r2: second relation to homogenise

        Returns:
            a tuple of 2 relations where the outputs are
                homogenised versions of the 2 inputs relations
        """

        # check equality
        if r1.variables == r2.variables:
            return r1, r2

        # check empty cases
        if r1.is_empty:
            return Relation.identity(r2.variables), r2

        if r2.is_empty:
            return r1, Relation.identity(r1.variables)

        # build a list of all distinct variables; maintain order
        extended_vars = r1.variables + [v for v in r2.variables
                                        if v not in r1.variables]

        # resize matrices to match new number of variables
        new_matrix_size = len(extended_vars)

        # first matrix: just resize -> this one is now done
        matrix1 = matrix_utils.extend(r1.matrix, new_matrix_size)

        # second matrix: create and initialize as identity matrix
        matrix2 = matrix_utils.identity_matrix(new_matrix_size)

        # index of each new variable iff variable exists in r2
        index_dict = {index: r2.variables.index(var)
                      for index, var in enumerate(extended_vars)
                      if var in r2.variables}

        # generate all valid <row, column> combinations
        index_map = [t1 + t2 for t1 in index_dict.items()
                     for t2 in index_dict.items()]

        # fill the resized matrix with values from original matrix
        for mj, rj, mi, ri in index_map:
            matrix2[mi][mj] = r2.matrix[ri][rj]

        return Relation(extended_vars, matrix1), Relation(extended_vars, matrix2)
