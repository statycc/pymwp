import itertools
from semiring import ZERO_MWP, UNIT_MWP
from monomial import Monomial
from polynomial import Polynomial
from constants import DEBUG as DEBUG_LEVEL

Zero = Polynomial([Monomial(ZERO_MWP, [])])

Unit = Polynomial([Monomial(UNIT_MWP, [])])


# Matrices product M1•M2


def MatProd(M1, M2, zero=Zero):
    res = []
    print("M1=")
    print(M1)
    print("M2=")
    print(M2)
    for i in range(len(M1)):
        res.append([])
        for j in range(len(M2)):
            new = zero
            for k in range(len(M1)):
                new = new + (M1[i][k] * M2[k][j])
            res[i].append(new)
    return res


# Matrices sum M1•M2


def MatSum(M1, M2):
    res = []
    for i in range(len(M1)):
        res.append([])
        for j in range(len(M1)):
            res[i].append(M1[i][j] + M2[i][j])
    return res


# Empty Matrix


def initMatrix(len, zero=Zero):
    res = []
    for i in range(len):
        res.append([])
        for j in range(len):
            res[i].append(zero)
    return res


# Add range_ext columns and lines to Mat
# (Initialized as identity : with unit on the diagonal and zero elsewhere)


def extendMatrix(Mat, range_ext, zero=Zero, unit=Unit):
    res = []
    for i in range(range_ext):
        res.append([])
        for j in range(range_ext):
            if i < len(Mat) and j < len(Mat):
                res[i].append(Mat[i][j])
            else:
                if i == j:
                    res[i].append(unit)
                else:
                    res[i].append(zero)
    return res


# Print a relation


def printRel(Rel):
    s = ""
    if DEBUG_LEVEL >= 2:
        s += "DEBUG_LEVEL Information, printRel."
        s += str(Rel[0])
        s += str(Rel[1])
    for i in range(len(Rel[1])):
        line = str(Rel[0][i]) + "   |   "
        for j in range(len(Rel[1])):
            line = line + "   " + str(Rel[1][i][j])
        s += line
    return s


# Return true if the relation is empty


def is_empty(Rel):
    if Rel[0] == []:
        return True
    if Rel[1] == []:
        return True
    return False


# Performs homogeneisation (extend Matrices if needed in order to compose)

def homogeneisation(R1, R2, zero=Zero, unit=Unit):
    var_indices = []
    var2 = []
    # Empty cases
    if is_empty(R1):
        empty = Relation(R2[0])
        empty.identity()
        return ((empty.variables, empty.matrix), R2)
    if is_empty(R2):
        empty = Relation(R1[0])
        empty.identity()
        return (R1, (empty.variables, empty.matrix))
    if DEBUG_LEVEL >= 2:
        print("DEBUG_LEVEL info for Homogeneisation. Inputs.")
        printRel(R1)
        printRel(R2)
    for v in R2[0]:
        var2.append(v)
    for v in R1[0]:
        found = False
        for j in range(len(R2[0])):
            if R2[0][j] == v:
                var_indices.append(j)
                found = True
                var2.remove(v)
        if not found:
            var_indices.append(-1)
    for v in var2:
        var_indices.append(R2[0].index(v))
    var_extended = R1[0] + var2
    M1_extended = extendMatrix(R1[1], len(var_extended))
    M2_extended = []
    for i in range(len(var_extended)):
        M2_extended.append([])
        i_in = var_indices[i] != -1
        for j in range(len(var_extended)):
            if not i_in and i == j:
                M2_extended[i].append(unit)
            elif i_in and var_indices[j] != -1:
                M2_extended[i].append(R2[1][var_indices[i]][var_indices[j]])
            else:
                M2_extended[i].append(zero)
    if DEBUG_LEVEL >= 2:
        print("DEBUG_LEVEL info for Homogeneisation. Result.")
        printRel(R1)
        printRel(R2)
        printRel((var_extended, M1_extended))
        printRel((var_extended, M2_extended))
    return ((var_extended, M1_extended), (var_extended, M2_extended))


# Composition (homogeneisation in order to do the Relations product)
def compositionRelations(R1, R2):
    if DEBUG_LEVEL >= 2:
        print("DEBUG_LEVEL info for compositionRelations. Inputs.")
        printRel(R1)
        printRel(R2)
    (eR1, eR2) = homogeneisation(R1, R2)
    if DEBUG_LEVEL >= 2:
        print("DEBUG_LEVEL info for compositionRelations. homogeneises.")
        printRel(eR1)
        printRel(eR2)
    Result = (eR1[0], MatProd(eR1[1], eR2[1]))
    if DEBUG_LEVEL >= 2:
        print("DEBUG_LEVEL info for compositionRelations. Outputs.")
        printRel(Result)
    return Result


# Sum (homogeneisation in order to do the Relations sum)


def sumRelations(R1, R2):
    (eR1, eR2) = homogeneisation(R1, R2)
    return (eR1[0], MatSum(eR1[1], eR2[1]))


def isequalRel(R1, R2):
    if set(R1[0]) != set(R2[0]):
        return False
    (eR1, eR2) = homogeneisation(R1, R2)
    for i in range(len(eR1[1])):
        for j in range(len(eR1[1])):
            if not eR1[1][i][j].equal(eR2[1][i][j]):
                return False
    return True


# Identity relation


def identityRel(var, unit=Unit, zero=Zero):
    Id = []
    for i in range(len(var)):
        Id.append([])
        for j in range(len(var)):
            if i == j:
                Id[i].append(unit)
            else:
                Id[i].append(zero)
    return (var, Id)


def algebraicRel(Rel, list, typeofdep, zero=Zero):
    (Var, Mat) = Rel
    out = Var.index(list[0][0])
    Mat[out][out] = zero
    for var in list[1]:
        in_ind = Var.index(var)
        Mat[in_ind][out] = typeofdep
    return (Var, Mat)


def contains_infinite(mat):
    for row in mat:
        if "i" in row:
            return True
    return False


class Relation:
    # Cons : take list of variables, init matrix with zeros
    def __init__(self, variables):
        self.variables = variables
        self.matrix = initMatrix(len(variables))

    def __str__(self):
        return printRel((self.variables, self.matrix))

    # Return dict representation of Relation
    def as_dict(self):
        return {"variables": self.variables, "matrix": self.encode_matrix()}

    # Create matrix of dicts by converting each Polynomial to a list of dict
    def encode_matrix(self):
        new_matrix = []
        for (i, row) in enumerate(self.matrix):
            new_matrix.append([])
            for polynomial in row:
                monomials = []
                for mon in polynomial.list:
                    monomials.append(mon.__dict__)
                new_matrix[i].append(monomials)
        return new_matrix

    def decode_matrix(self, org_matrix):
        """Create matrix of polynomials by converting each list of
        dicts to instances of Polynomials
        """
        self.matrix = []
        for (i, row) in enumerate(org_matrix):
            self.matrix.append([])
            for polynomial in row:
                poly = Polynomial([])
                for monomial in polynomial:
                    mon = Monomial(monomial["scalar"], monomial["deltas"])
                    poly.list.append(mon)
                self.matrix[i].append(poly)

    # not used…
    # list contains two list with left-hand and right-hand side
    # variables respectively; they are supposed to be
    def algebraic(self, list, typeofdep):
        """ DEPRECATED """
        # contained in self.variables already.
        (Var, Mat) = algebraicRel((self.variables, self.matrix), list,
                                  typeofdep)
        self.matrix = Mat
        return self

    # True if infinit somewhere
    def isInfinit(self):
        size = len(self.variables)
        for i in range(size):
            for j in range(size):
                c = self.matrix[i][j]
                for mon in c.list:
                    if mon.scalar == "i":
                        return True
        return False

    def ReplaceColumnMatrix(self, vect, var):
        # (Var,Mat)=Rel
        new = Relation(self.variables)
        new.identity()
        j = self.variables.index(var)
        for i in range(len(vect)):
            new.matrix[i][j] = vect[i]
        return new

    def replace_column(self, vect, i):
        return self.ReplaceColumnMatrix(vect, i)

    def identity(self):
        (Var, Mat) = identityRel(self.variables)
        self.matrix = Mat
        return self

    # Loop correction (see MWP - Lars&Niel paper)
    def whileCorrection(self):
        size = len(self.variables)
        for i in range(size):
            for j in range(size):
                c = self.matrix[i][j]
                for mon in c.list:
                    if mon.scalar == "p" or (mon.scalar == "w" and i == j):
                        mon.scalar = "i"

    def conditionLoop(self, list_var):
        return

    def conditionWhile(self, list_var):
        return

    #  Composition with a given relation Rel
    def composition(self, Rel):
        (var, Mat) = compositionRelations((self.variables, self.matrix),
                                          (Rel.variables, Rel.matrix))
        compo = Relation(var)
        compo.matrix = Mat
        return compo

    #  Sum with a given relation Rel
    def sum_relation(self, Rel):
        (var, Mat) = sumRelations((self.variables, self.matrix),
                                  (Rel.variables, Rel.matrix))
        result = Relation(var)
        result.matrix = Mat
        return result

    def show(self):
        print(str(self))

    def equal(self, Rel):
        return isequalRel((self.variables, self.matrix),
                          (Rel.variables, Rel.matrix))

    #  Fixpoint (sum of compositions until no changes occur)
    def fixpoint(self):
        end = False
        (v, M) = identityRel(self.variables)
        Fix = Relation(v)
        PreviousFix = Relation(v)
        Current = Relation(v)
        Fix.matrix = M
        PreviousFix.matrix = M
        Current.matrix = M
        while not end:
            PreviousFix.matrix = Fix.matrix
            Current = Current.composition(self)
            Fix = Fix.sum_relation(Current)
            if Fix.equal(PreviousFix):
                end = True
            if DEBUG_LEVEL >= 2:
                print("DEBUG. Fixpoint.")
                print("DEBUG. Fixpoint.")
                self.show()
                Fix.show()
        return Fix

    def eval(self, args):
        result = Relation([])
        mat = []
        result.variables = self.variables
        for i, row in enumerate(self.matrix):
            mat.append([])
            for poly in row:
                mat[i].append(poly.eval(args))
        result.matrix = mat
        return result

    def isInfinite(self, choices, index):
        # uses itertools.product to generate all possible assignments
        args_list = list(itertools.product(choices, repeat=index))
        combinations = []
        for args in args_list:
            list_args = list(args)
            mat = self.eval(list_args).matrix
            if not contains_infinite(mat):
                combinations.append(list_args)
        return combinations
