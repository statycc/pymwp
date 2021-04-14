# flake8: noqa: W605

from polynomial import Polynomial
from monomial import Monomial
from polynomial import Zero, Unit


def init_matrix(size: int, value: any) -> list:
    """Create empty {size} X {size} matrix.

    Arguments:
        size: matrix size
        value: initial value

    Returns:
        Initialized matrix.
    """
    return [[value for _ in range(size)]
            for _ in range(size)]


def identity_matrix(size: int) -> list:
    """Create identity matrix of specified size.

    Arguments:
        size: matrix size

    Returns:
        New identity matrix.
    """
    return [[Unit if i == j else Zero
             for j in range(size)]
            for i in range(size)]


def encode(matrix: list) -> list:
    """TODO:

    Arguments:
        matrix: matrix to encode
    """
    new_matrix = []
    for (i, row) in enumerate(matrix):
        new_matrix.append([])
        for polynomial in row:
            monomials = []
            for mon in polynomial.list:
                monomials.append(mon.__dict__)
            new_matrix[i].append(monomials)
    return new_matrix


def decode(matrix: list) -> list:
    """TODO:

    Arguments:
        matrix: matrix to decode
    """
    result = []
    for (i, row) in enumerate(matrix):
        result.append([])
        for polynomial in row:
            poly = Polynomial()
            for monomial in polynomial:
                mon = Monomial(monomial["scalar"], monomial["deltas"])
                poly.list.append(mon)
            result[i].append(poly)
    return result


def matrix_sum(matrix1: list, matrix2: list) -> list:
    """Matrices sum matrix1 + matrix2."""
    res = []
    for i in range(len(matrix1)):
        res.append([])
        for j in range(len(matrix1)):
            res[i].append(matrix1[i][j] + matrix2[i][j])
    return res


def matrix_prod(matrix1: list, matrix2: list) -> list:
    """Matrices product matrix1 • matrix2."""
    res = []
    for i in range(len(matrix1)):
        res.append([])
        for j in range(len(matrix2)):
            new_value = Zero
            for k in range(len(matrix1)):
                new_value += (matrix1[i][k] * matrix2[k][j])
            res[i].append(new_value)
    return res


def extend_matrix(matrix: list, range_ext: int) -> list:
    """
    Add range_ext columns and lines to Mat
    (Initialized as identity : with unit on the diagonal and zero elsewhere)

    Arguments:
        matrix:
        range_ext:
        zero:
        unit:

    Returns
        TODO:
    """
    res = []
    for i in range(range_ext):
        res.append([])
        for j in range(range_ext):
            if i < len(matrix) and j < len(matrix):
                res[i].append(matrix[i][j])
            else:
                res[i].append(Unit if i == j else Zero)

    return res


def contains_infinite(matrix: list) -> bool:
    """Check if matrix contains $\infty$.

    Arguments:
        matrix: matrix to check

    Returns:
        True if matrix contains $\infty$,
        False otherwise.
    """

    # return any('i' in row for row in matrix)
    for row in matrix:
        if "i" in row:
            return True
    return False

# import itertools
# from semiring import ZERO_MWP, UNIT_MWP
# from monomial import Monomial
# from polynomial import Polynomial
# from relation import  Relation
# from relation_list import RelationList
# from constants import DEBUG as DEBUG
#
# import copy
#
# Zero = Polynomial([Monomial(ZERO_MWP, [])])
#
# Unit = Polynomial([Monomial(UNIT_MWP, [])])
#
#
# def Prod(a, b):
#     return a * b
#
#
# def Sum(a, b):
#     return a + b
#
#
# # Matrices product M1•M2
#
#
# def MatProd(M1, M2, prod=Prod, sum=Sum, zero=Zero):
#     res = []
#     print("M1=")
#     print(M1)
#     print("M2=")
#     print(M2)
#     for i in range(len(M1)):
#         res.append([])
#         for j in range(len(M2)):
#             new = zero
#             for k in range(len(M1)):
#                 new = sum(new, prod(M1[i][k], M2[k][j]))
#             res[i].append(new)
#     return res
#
#
# # Matrices sum M1•M2
#
#
# def MatSum(M1, M2, sum=Sum):
#     res = []
#     for i in range(len(M1)):
#         res.append([])
#         for j in range(len(M1)):
#             res[i].append(sum(M1[i][j], M2[i][j]))
#     return res
#
#
# # Empty matrix_utils
#
#
# def initMatrix(len, zero=Zero):
#     res = []
#     for i in range(len):
#         res.append([])
#         for j in range(len):
#             res[i].append(zero)
#     return res
#
#
# # Add range_ext columns and lines to Mat
# # (Initialized as identity : with unit on the diagonal and zero elsewhere)
#
#
# def extendMatrix(Mat, range_ext, zero=Zero, unit=Unit):
#     res = []
#     for i in range(range_ext):
#         res.append([])
#         for j in range(range_ext):
#             if i < len(Mat) and j < len(Mat):
#                 res[i].append(Mat[i][j])
#             else:
#                 if i == j:
#                     res[i].append(unit)
#                 else:
#                     res[i].append(zero)
#     return res
#
#
# # pretty printing of matrix Mat
#
#
# def printMatrix(Mat):
#     for i in range(len(Mat)):
#         line = ""
#         for j in range(len(Mat)):
#             line = line + "   " + str(Mat[i][j])
#         print(line)
#     return 0
#
#
# # Print a relation
#
#
# def printRel(Rel):
#     if DEBUG >= 2:
#         print("DEBUG Information, printRel.")
#         print(Rel[0])
#         print(Rel[1])
#     for i in range(len(Rel[1])):
#         line = str(Rel[0][i]) + "   |   "
#         for j in range(len(Rel[1])):
#             line = line + "   " + str(Rel[1][i][j])
#         print(line)
#     return 0
#
#
# # Return true if the relation is empty
#
#
# def is_empty(Rel):
#     if Rel[0] == []:
#         return True
#     if Rel[1] == []:
#         return True
#     return False
#
#
# # See Class Relation below
# # Performs homogeneisation (extend Matrices if needed in order to compose)
#
#
# def homogeneisation(R1, R2, zero=Zero, unit=Unit):
#     var_indices = []
#     var2 = []
#     # Empty cases
#     if is_empty(R1):
#         empty = Relation(R2[0])
#         empty.identity()
#         return ((empty.variables, empty.matrix), R2)
#     if is_empty(R2):
#         empty = Relation(R1[0])
#         empty.identity()
#         return (R1, (empty.variables, empty.matrix))
#     if DEBUG >= 2:
#         print("DEBUG info for Homogeneisation. Inputs.")
#         printRel(R1)
#         printRel(R2)
#     for v in R2[0]:
#         var2.append(v)
#     for v in R1[0]:
#         found = False
#         for j in range(len(R2[0])):
#             if R2[0][j] == v:
#                 var_indices.append(j)
#                 found = True
#                 var2.remove(v)
#         if not found:
#             var_indices.append(-1)
#     for v in var2:
#         var_indices.append(R2[0].index(v))
#     var_extended = R1[0] + var2
#     M1_extended = extendMatrix(R1[1], len(var_extended))
#     M2_extended = []
#     for i in range(len(var_extended)):
#         M2_extended.append([])
#         i_in = var_indices[i] != -1
#         for j in range(len(var_extended)):
#             if not i_in and i == j:
#                 M2_extended[i].append(unit)
#             elif i_in and var_indices[j] != -1:
#                 M2_extended[i].append(R2[1][var_indices[i]][var_indices[j]])
#             else:
#                 M2_extended[i].append(zero)
#     if DEBUG >= 2:
#         print("DEBUG info for Homogeneisation. Result.")
#         printRel(R1)
#         printRel(R2)
#         printRel((var_extended, M1_extended))
#         printRel((var_extended, M2_extended))
#     return ((var_extended, M1_extended), (var_extended, M2_extended))
#
#
# # Composition (homogeneisation in order to do the Relations product)
# def compositionRelations(R1, R2):
#     if DEBUG >= 2:
#         print("DEBUG info for compositionRelations. Inputs.")
#         printRel(R1)
#         printRel(R2)
#     (eR1, eR2) = homogeneisation(R1, R2)
#     if DEBUG >= 2:
#         print("DEBUG info for compositionRelations. homogeneises.")
#         printRel(eR1)
#         printRel(eR2)
#     Result = (eR1[0], MatProd(eR1[1], eR2[1]))
#     if DEBUG >= 2:
#         print("DEBUG info for compositionRelations. Outputs.")
#         printRel(Result)
#     return Result
#
#
# # Sum (homogeneisation in order to do the Relations sum)
#
#
# def sumRelations(R1, R2):
#     (eR1, eR2) = homogeneisation(R1, R2)
#     return (eR1[0], MatSum(eR1[1], eR2[1]))
#
#
# def isequalRel(R1, R2):
#     if set(R1[0]) != set(R2[0]):
#         return False
#     (eR1, eR2) = homogeneisation(R1, R2)
#     for i in range(len(eR1[1])):
#         for j in range(len(eR1[1])):
#             if not eR1[1][i][j].equal(eR2[1][i][j]):
#                 return False
#     return True
#
#
# # Identity relation
#
#
# def identityRel(var, unit=Unit, zero=Zero):
#     Id = []
#     for i in range(len(var)):
#         Id.append([])
#         for j in range(len(var)):
#             if i == j:
#                 Id[i].append(unit)
#             else:
#                 Id[i].append(zero)
#     return (var, Id)
#
#
# def algebraicRel(Rel, list, typeofdep, zero=Zero):
#     (Var, Mat) = Rel
#     out = Var.index(list[0][0])
#     Mat[out][out] = zero
#     for var in list[1]:
#         in_ind = Var.index(var)
#         Mat[in_ind][out] = typeofdep
#     return (Var, Mat)
#
#
# def unique(mat, lmat):
#     for out in lmat:
#         if mat == out.matrix:
#             return False
#     return True
#
#
# def contains_infinite(mat):
#     for row in mat:
#         if "i" in row:
#             return True
#     return False
#
#
# # An object for list of Relations (may simplify reading ^^')
#
#
# class RelationList:
#     def __init__(self, variables):
#         self.list = [Relation(variables)]
#
#     def identity(self):
#         Rel = Relation(self.list[0].variables)
#         self.list = [Rel.identity()]
#         return self
#
#     def replace_column(self, vect, i):
#         if DEBUG >= 2:
#             print("replace column: vect=", vect, "i=", i)
#             self.show()
#         new_list = []
#         for v in vect:
#             for Rel in self.list:
#                 new_list.append(Rel.replace_column(v, i))
#         self.list = list(new_list)
#         if DEBUG >= 2:
#             print("DEBUG: relation après replace_column")
#             self.show()
#
#     # Composition of the entire list of relations
#     def composition(self, RelList):
#         if DEBUG >= 2:
#             print("DEBUG: composition de relationList")
#             RelList.show()
#             self.show()
#         new_list = []
#         for Rel in self.list:
#             for Orel in RelList.list:
#                 output = Rel.composition(Orel)
#                 if unique(output.matrix, new_list):
#                     new_list.append(output)
#         self.list = list(new_list)
#         if DEBUG >= 2:
#             print("DEBUG: Result")
#             self.show()
#
#     # Composition of the entire list of relations
#     def one_composition(self, orel):
#         if DEBUG >= 2:
#             print("DEBUG: composition de relationList")
#             orel.show()
#             self.show()
#         new_list = []
#         for myrel in self.list:
#             new_list.append(myrel.composition(orel))
#         self.list = copy.deepcopy(new_list)
#         if DEBUG >= 2:
#             print("DEBUG: Result")
#             self.show()
#
#     # Sum of the entire list of relations
#     def sum_relation(self, RelList):
#         new_list = []
#         for rel in self.list:
#             for orel in RelList.list:
#                 new_list.append(rel.sumRel(orel))
#         self.list = list(new_list)
#         return self
#
#     # Fixpoint of the entire list of relations
#     def fixpoint(self):
#         new_list = []
#         for rel in self.list:
#             new_list.append(rel.fixpoint())
#         self.list = list(new_list)
#
#     def show(self):
#         i = 1
#         print("--- Affiche ", self, " ---")
#         for rel in self.list:
#             print(i, ":")
#             rel.show()
#             i += 1
#         print("--- FIN ---")
#
#     # Loop correction (see MWP - Lars&Niel paper)
#     def while_correction(self):
#         for rel in self.list:
#             rel.whileCorrection()
#
#     def isInfinit(self):
#         for rel in self.list:
#             if not rel.isInfinit():
#                 return False
#         return True
#
#
# # Object Relation
#
#
# class Relation:
#     # Cons : take list of variables, init matrix with zeros
#     def __init__(self, variables):
#         self.variables = variables
#         self.matrix = initMatrix(len(variables))
#
#     # Return dict representation of Relation
#     def as_dict(self):
#         return {"variables": self.variables, "matrix": self.encode_matrix()}
#
#     # Create matrix of dicts by converting each Polynomial to a list of dict
#     def encode_matrix(self):
#         new_matrix = []
#         for (i, row) in enumerate(self.matrix):
#             new_matrix.append([])
#             for polynomial in row:
#                 monomials = []
#                 for mon in polynomial.list:
#                     monomials.append(mon.__dict__)
#                 new_matrix[i].append(monomials)
#         return new_matrix
#
#     def decode_matrix(self, org_matrix):
#         """Create matrix of polynomials by converting each list of
#         dicts to instances of Polynomials
#         """
#         self.matrix = []
#         for (i, row) in enumerate(org_matrix):
#             self.matrix.append([])
#             for polynomial in row:
#                 poly = Polynomial([])
#                 for monomial in polynomial:
#                     mon = Monomial(monomial["scalar"], monomial["deltas"])
#                     poly.list.append(mon)
#                 self.matrix[i].append(poly)
#
#     # not used…
#     # list contains two list with left-hand and right-hand side
#     # variables respectively; they are supposed to be
#     def algebraic(self, list, typeofdep):
#         """ DEPRECATED """
#         # contained in self.variables already.
#         (Var, Mat) = algebraicRel((self.variables, self.matrix), list,
#                                   typeofdep)
#         self.matrix = Mat
#         return self
#
#     # True if infinit somewhere
#     def isInfinit(self):
#         size = len(self.variables)
#         for i in range(size):
#             for j in range(size):
#                 c = self.matrix[i][j]
#                 for mon in c.list:
#                     if mon.scalar == "i":
#                         return True
#         return False
#
#     def ReplaceColumnMatrix(self, vect, var):
#         # (Var,Mat)=Rel
#         new = Relation(self.variables)
#         new.identity()
#         j = self.variables.index(var)
#         for i in range(len(vect)):
#             new.matrix[i][j] = vect[i]
#         return new
#
#     def replace_column(self, vect, i):
#         return self.ReplaceColumnMatrix(vect, i)
#
#     def identity(self):
#         (Var, Mat) = identityRel(self.variables)
#         self.matrix = Mat
#         return self
#
#     # Loop correction (see MWP - Lars&Niel paper)
#     def whileCorrection(self):
#         size = len(self.variables)
#         for i in range(size):
#             for j in range(size):
#                 c = self.matrix[i][j]
#                 for mon in c.list:
#                     if mon.scalar == "p" or (mon.scalar == "w" and i == j):
#                         mon.scalar = "i"
#
#     def conditionLoop(self, list_var):
#         return
#
#     def conditionWhile(self, list_var):
#         return
#
#     #  Composition with a given relation Rel
#     def composition(self, Rel):
#         (var, Mat) = compositionRelations((self.variables, self.matrix),
#                                           (Rel.variables, Rel.matrix))
#         compo = Relation(var)
#         compo.matrix = Mat
#         return compo
#
#     #  Sum with a given relation Rel
#     def sumRel(self, Rel):
#         (var, Mat) = sumRelations((self.variables, self.matrix),
#                                   (Rel.variables, Rel.matrix))
#         result = Relation(var)
#         result.matrix = Mat
#         return result
#
#     def show(self):
#         printRel((self.variables, self.matrix))
#
#     def equal(self, Rel):
#         return isequalRel((self.variables, self.matrix),
#                           (Rel.variables, Rel.matrix))
#
#     #  Fixpoint (sum of compositions until no changes occur)
#     def fixpoint(self):
#         end = False
#         (v, M) = identityRel(self.variables)
#         Fix = Relation(v)
#         PreviousFix = Relation(v)
#         Current = Relation(v)
#         Fix.matrix = M
#         PreviousFix.matrix = M
#         Current.matrix = M
#         while not end:
#             PreviousFix.matrix = Fix.matrix
#             Current = Current.composition(self)
#             Fix = Fix.sumRel(Current)
#             if Fix.equal(PreviousFix):
#                 end = True
#             if DEBUG >= 2:
#                 print("DEBUG. Fixpoint.")
#                 print("DEBUG. Fixpoint.")
#                 self.show()
#                 Fix.show()
#         return Fix
#
#     def eval(self, args):
#         result = Relation([])
#         mat = []
#         result.variables = self.variables
#         for i, row in enumerate(self.matrix):
#             mat.append([])
#             for poly in row:
#                 mat[i].append(poly.eval(args))
#         result.matrix = mat
#         return result
#
#     def isInfinite(self, choices, index):
#         # uses itertools.product to generate all possible assignments
#         args_list = list(itertools.product(choices, repeat=index))
#         combinations = []
#         for args in args_list:
#             list_args = list(args)
#             mat = self.eval(list_args).matrix
#             if not contains_infinite(mat):
#                 combinations.append(list_args)
#         return combinations
