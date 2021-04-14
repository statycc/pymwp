# flake8: noqa: W605

from __future__ import annotations

import itertools

import matrix as Matrix
from polynomial import Zero, Unit
from constants import DEBUG


class Relation:
    """
    TODO: what is a relation & what is the purpose of this class?
    """

    def __init__(self, variables: list, matrix=None):
        """Create relation.

        Arguments:
            variables: list of variables -> TODO: what type is variable?
        """
        self.variables = variables
        if matrix is not None:
            self.matrix = Matrix.decode(matrix)
        else:
            self.matrix = Matrix.init_matrix(len(variables), Zero)

    def __str__(self):
        s, mtx_len = "", len(self.matrix)
        if DEBUG >= 2:
            s += "DEBUG Information, printRel.{0}{1}" \
                .format(self.variables, self.matrix)

        for i in range(mtx_len):
            line = str(self.variables[i]) + "   |   "
            for j in range(mtx_len):
                line = line + "   " + str(self.matrix[i][j])
                s += line
        return s

        # return printRel((self.variables, self.matrix))

    def __add__(self, other):
        variables, matrix = Relation.sum_relations(
            (self.variables, self.matrix),
            (other.variables, other.matrix))
        result = Relation(variables)
        result.matrix = matrix
        return result

    def to_dict(self):
        """Dictionary representation of Relation."""
        return {
            "variables": self.variables,
            "matrix": Matrix.encode(self.matrix)
        }

    def replace_column(self, vector, variable) -> Relation:
        """Replace a column in a matrix by a vector.

        Arguments:
            vector: vector to replace in matrix
            variable: TODO: add description

        Returns:
            new Relation object with
        """
        new_relation = Relation(self.variables)
        new_relation.identity()

        j = self.variables.index(variable)
        for idx in range(len(vector)):
            new_relation.matrix[idx][j] = vector[idx]
        return new_relation

    def identity(self) -> Relation:
        """
        TODO: add docstring
        """
        _, matrix = Relation.identity_relation(
            self.variables, Unit, Zero)
        self.matrix = matrix
        return self

    def while_correction(self) -> None:
        """Loop correction (see MWP - Lars&Niel paper)"""
        size = len(self.variables)
        for i in range(size):
            for j in range(size):
                c = self.matrix[i][j]
                for mon in c.list:
                    if mon.scalar == "p" or (mon.scalar == "w" and i == j):
                        mon.scalar = "i"

    def composition(self, other: Relation) -> Relation:
        """Composition with a given relation other"""
        variable, matrix = Relation.composition_relations(
            (self.variables, self.matrix),
            (other.variables, other.matrix))
        compo = Relation(variable)
        compo.matrix = matrix
        return compo

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
        return Relation.is_equal(
            (self.variables, self.matrix),
            (other.variables, other.matrix))

    def fixpoint(self):
        """Fixpoint (sum of compositions until no changes occur)."""
        end = False
        (v, M) = Relation.identity_relation(self.variables, Unit, Zero)
        Fix = Relation(v)
        PreviousFix = Relation(v)
        Current = Relation(v)
        Fix.matrix = M
        PreviousFix.matrix = M
        Current.matrix = M
        while not end:
            PreviousFix.matrix = Fix.matrix
            Current = Current.composition(self)
            Fix = Fix + Current
            if Fix.equal(PreviousFix):
                end = True
            if DEBUG >= 2:
                print("DEBUG. Fixpoint.")
                print("DEBUG. Fixpoint.")
                self.show()
                Fix.show()
        return Fix

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
            if not Matrix.contains_infinite(mat):
                combinations.append(list_args)
        return combinations

    @staticmethod
    def identity_relation(var, unit, zero):
        """Identity relation.

        Arguments:
            var:
            unit:
            zero:

        Returns:
            TODO:
        """
        Id = []
        for i in range(len(var)):
            Id.append([])
            for j in range(len(var)):
                if i == j:
                    Id[i].append(unit)
                else:
                    Id[i].append(zero)
        return var, Id

    @staticmethod
    def composition_relations(r1: tuple, r2: tuple) -> tuple:
        """Composition (homogenisation in order to do the Relations product).

        Arguments:
            r1: first Relation
            r2: second Relation

        Returns:
            TODO:
        """
        if DEBUG >= 2:
            print("DEBUG info for compositionRelations. Inputs.", r1, r2)

        eR1, eR2 = Relation.homogenisation(r1, r2, Zero, Unit)

        if DEBUG >= 2:
            print("DEBUG info for compositionRelations. homogenises.", eR1, eR2)

        result = (eR1[0], Matrix.matrix_prod(eR1[1], eR2[1], Zero))

        if DEBUG >= 2:
            print("DEBUG info for compositionRelations. Outputs.", result)

        return result

    @staticmethod
    def sum_relations(r1: tuple, r2: tuple) -> tuple:
        """Sum (homogenisation in order to do the Relations sum)

        Arguments:
            r1: first pair of (variables, matrix)
            r2: second pair of (variables, matrix)

        Returns:
            TODO:
        """
        er1, er2 = Relation.homogenisation(r1, r2, Zero, Unit)
        return er1[0], Matrix.matrix_sum(er1[1], er2[1])

    @staticmethod
    def is_equal(r1: tuple, r2: tuple) -> bool:
        """Determine if two relations are equal.

        Arguments:
            r1: first pair of (variables, matrix)
            r2: second pair of (variables, matrix)

        Returns:
            TODO:
        """
        if set(r1[0]) != set(r2[0]):
            return False
        (eR1, eR2) = Relation.homogenisation(r1, r2, Zero, Unit)
        for i in range(len(eR1[1])):
            for j in range(len(eR1[1])):
                if not eR1[1][i][j].equal(eR2[1][i][j]):
                    return False
        return True

    @staticmethod
    def is_empty(r: tuple) -> bool:
        """Return true if the relation is empty"""
        if r[0] == []:
            return True
        if r[1] == []:
            return True
        return False

    @staticmethod
    def homogenisation(r1, r2, zero, unit):
        """Performs homogeneisation (extend Matrices if needed in order to compose).

        :param r1:
        :param r2:
        :param zero:
        :param unit:
        :return:
        """
        var_indices = []
        var2 = []
        # Empty cases
        if Relation.is_empty(r1):
            empty = Relation(r2[0])
            empty.identity()
            return ((empty.variables, empty.matrix), r2)
        if Relation.is_empty(r2):
            empty = Relation(r1[0])
            empty.identity()
            return (r1, (empty.variables, empty.matrix))
        if DEBUG >= 2:
            print("DEBUG info for Homogeneisation. Inputs.", r1, r2)

        for v in r2[0]:
            var2.append(v)
        for v in r1[0]:
            found = False
            for j in range(len(r2[0])):
                if r2[0][j] == v:
                    var_indices.append(j)
                    found = True
                    var2.remove(v)
            if not found:
                var_indices.append(-1)
        for v in var2:
            var_indices.append(r2[0].index(v))
        var_extended = r1[0] + var2
        M1_extended = Matrix.extend_matrix(r1[1], len(var_extended), Zero, Unit)
        M2_extended = []
        for i in range(len(var_extended)):
            M2_extended.append([])
            i_in = var_indices[i] != -1
            for j in range(len(var_extended)):
                if not i_in and i == j:
                    M2_extended[i].append(unit)
                elif i_in and var_indices[j] != -1:
                    M2_extended[i].append(r2[1][var_indices[i]][var_indices[j]])
                else:
                    M2_extended[i].append(zero)
        if DEBUG >= 2:
            print("DEBUG info for Homogeneisation. Result.", r1, r2,
                  (var_extended, M1_extended), (var_extended, M2_extended))
        return ((var_extended, M1_extended), (var_extended, M2_extended))
