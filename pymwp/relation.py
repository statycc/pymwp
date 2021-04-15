# flake8: noqa: W605

from __future__ import annotations

import itertools

import matrix as matrix_utils
from polynomial import Zero, Unit
from constants import DEBUG


class Relation:
    """
    TODO: what is a relation & what is the purpose of this class?
    """

    def __init__(self, variables: list[str], matrix: list[list] = None):
        """Create relation.

        Arguments:
            variables: list of string variables
            matrix: matrix
        """
        self.variables = variables or []
        self.matrix = matrix or matrix_utils \
            .init_matrix(len(self.variables), Zero)

    def __str__(self):
        s, mtx_len = "", len(self.matrix)
        for i in range(mtx_len):
            line = str(self.variables[i]) + "   |   "
            for j in range(mtx_len):
                line = line + "   " + str(self.matrix[i][j])
                s += line
        return s

    def __add__(self, other):
        er1, er2 = Relation.homogenisation(self, other)
        new_matrix = matrix_utils.matrix_sum(er1.matrix, er2.matrix)
        return Relation(er1.variables, new_matrix)

    def to_dict(self) -> dict:
        """Dictionary representation of Relation.

        Returns:
            dictionary representing current Relation.
        """
        return {
            "variables": self.variables,
            "matrix": matrix_utils.encode(self.matrix)
        }

    def replace_column(self, vector: list, variable: str) -> Relation:
        """Replace a column in a matrix by a vector.

        Arguments:
            vector: vector to replace in matrix
            variable: variable value; replace will occur
                at the index of this variable.

        Returns:
            new Relation object with
        """
        new_relation = Relation.identity(self.variables)
        j = self.variables.index(variable)

        for idx in range(len(vector)):
            new_relation.matrix[idx][j] = vector[idx]
        return new_relation

    def while_correction(self) -> None:
        """Loop correction (see MWP - Lars&Niel paper)"""
        for i in range(len(self.variables)):
            for j in range(len(self.variables)):
                for mon in self.matrix[i][j].list:
                    if mon.scalar == "p" or (mon.scalar == "w" and i == j):
                        mon.scalar = "i"

    def composition(self, other: Relation) -> Relation:
        """Composition with a given relation other

        Arguments:
            other: Relation to compose with self

        Returns:
           TODO:
        """
        er1, er2 = Relation.homogenisation(self, other)
        new_matrix = matrix_utils.matrix_prod(er1.matrix, er2.matrix)
        return Relation(er1.variables, new_matrix)

    def show(self):
        """Display relation."""
        print(str(self))

    def equal(self, other: Relation) -> bool:
        """Determine if two relations are equal.

        Arguments:
            other: relation to compare

        Returns:
            True is current and other are equal
            and False otherwise.
        """
        if set(self.variables) != set(other.variables):
            return False
        er1, er2 = Relation.homogenisation(self, other)
        for i in range(len(er1.matrix)):
            for j in range(len(er1.matrix)):
                if not er1.matrix[i][j].equal(er2.matrix[i][j]):
                    return False
        return True

    def fixpoint(self):
        """Fixpoint (sum of compositions until no changes occur)."""
        v = self.variables[:]
        matrix = matrix_utils.identity_matrix(len(v))
        fix = Relation(v, matrix)
        prev_fix = Relation(v, matrix)
        current = Relation(v, matrix)

        while True:
            prev_fix.matrix = fix.matrix
            current = current.composition(self)
            fix = fix + current
            if fix.equal(prev_fix):
                break
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

    @staticmethod
    def identity(variables: list) -> Relation:
        """
        Create new identity relation

        Arguments
            variables: list of variables

        Returns:
             Generated relation with given
             variables and identity matrix.
        """
        matrix = matrix_utils.identity_matrix(len(variables))
        return Relation(variables, matrix)

    @staticmethod
    def is_empty(r: Relation) -> bool:
        """Return true if the relation is empty"""
        return not r.variables or not r.matrix

    @staticmethod
    def homogenisation(r1: Relation, r2: Relation) -> tuple:
        """Performs homogenisation.

        After this operation both relations will have same
        variables and their matrices will be same size.

        This operation will extend matrices if needed.

        Arguments:
            r1: first relation to homogenise
            r2: second relation to homogenise

        Returns:
            a tuple of 2 Relations where these outputs are
                homogenised versions of the 2 inputs
        """

        # check equality
        if r1.variables == r2.variables:
            return r1, r2

        # check empty cases
        if Relation.is_empty(r1):
            return Relation.identity(r2.variables), r2

        if Relation.is_empty(r2):
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
