from monomial import Monomial
from polynomial import Polynomial
from relation import Relation
from semiring import ZERO_MWP
from matrix import init_matrix


def test_init_relation_creates_zero_matrix():
    rel_variables = ['X0', 'X1', 'X2']
    r = Relation(rel_variables)

    assert r.variables == rel_variables
    assert r.matrix[0][0].list[0].scalar == ZERO_MWP
    assert (r.matrix[0][0] == r.matrix[1][0] == r.matrix[2][0] ==
            r.matrix[0][1] == r.matrix[1][1] == r.matrix[2][1] ==
            r.matrix[0][2] == r.matrix[1][2] == r.matrix[2][2])


def test_init_relation_with_existing_matrix():
    rel_variables = ['X0', 'X1']
    matrix = init_matrix(2, Polynomial([Monomial('w')]))
    r = Relation(rel_variables, matrix)

    assert r.variables == rel_variables
    assert r.matrix == matrix


def test_create_identity_relation():
    rel_variables = ['X0', 'X1', 'X2']
    r = Relation.identity(rel_variables)

    assert r.variables == rel_variables
    assert r.matrix[0][0] == r.matrix[1][1] == r.matrix[2][2]
    assert r.matrix[0][0] != r.matrix[0][1] and r.matrix[0][1] == r.matrix[0][2]
    assert r.matrix[1][1] != r.matrix[1][0] and r.matrix[1][0] == r.matrix[1][2]
    assert r.matrix[2][2] != r.matrix[2][0] and r.matrix[2][0] == r.matrix[2][1]


def test_empty_relation_is_empty():
    empty = Relation(variables=[], matrix=[])
    assert empty.is_empty is True


def test_empty_relation_not_empty():
    empty = Relation(['X1', 'X2'])
    assert empty.is_empty is False


def test_replace_column():
    before = Relation(['X0', 'X1', 'X2'])
    poly = Polynomial([Monomial('w')])
    vector = [poly.copy(), poly.copy(), poly.copy()]
    r = before.replace_column(vector, 'X1')

    assert r.matrix[0][1] == r.matrix[1][1] == r.matrix[2][1] == poly
    assert r.matrix[0][0] == r.matrix[2][2] and r.matrix[2][2] != poly  # m
    assert (r.matrix[1][0] == r.matrix[2][0] == r.matrix[0][2] ==
            r.matrix[1][2] and r.matrix[1][2] != poly)  # 0
