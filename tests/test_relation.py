from pymwp import Polynomial, Relation
from pymwp.semiring import ZERO_MWP
from pymwp.matrix import init_matrix


def test_init_relation_creates_zero_matrix():
    """Init matrix creates a matrix of 0-monomials"""

    rel_variables = ['X0', 'X1', 'X2']
    r = Relation(rel_variables)

    assert r.variables == rel_variables
    assert r.matrix[0][0].list[0].scalar == ZERO_MWP
    assert (r.matrix[0][0] == r.matrix[1][0] == r.matrix[2][0] ==
            r.matrix[0][1] == r.matrix[1][1] == r.matrix[2][1] ==
            r.matrix[0][2] == r.matrix[1][2] == r.matrix[2][2])


def test_init_relation_with_existing_matrix():
    """Initializing relation with existing matrix instantiates a relation
    with that provided matrix."""
    rel_variables = ['X0', 'X1']
    matrix = init_matrix(2, Polynomial('w'))
    r = Relation(rel_variables, matrix)

    assert r.variables == rel_variables
    assert r.matrix is matrix  # same reference
    assert r.matrix == matrix  # equal values


def test_create_identity_relation():
    """Creating identity relation gives relation with provided variables
    and identity matrix."""
    rel_variables = ['X0', 'X1', 'X2']
    r = Relation.identity(rel_variables)

    assert r.variables == rel_variables
    assert r.matrix[0][0].list[0].scalar == 'm'  # diagonal all m's
    assert r.matrix[0][1].list[0].scalar == 'o'  # non-diagonals 0s
    assert r.matrix[0][0] == r.matrix[1][1] == r.matrix[2][2]
    assert (r.matrix[0][1] == r.matrix[0][2] == r.matrix[1][0] ==
            r.matrix[1][0] == r.matrix[1][2] == r.matrix[2][0] ==
            r.matrix[2][0] == r.matrix[2][1])


def test_empty_relation_is_empty():
    """Method is_empty returns true when relation is empty."""
    empty = Relation(variables=[], matrix=[])
    assert empty.is_empty is True


def test_empty_relation_not_empty():
    """Method is_empty return false when relation is not empty."""
    not_empty = Relation(['X1', 'X2'])
    assert not_empty.is_empty is False


def test_replace_column():
    """Replacing matrix column by vector gives expected result."""
    p = Polynomial('w')
    before = Relation(['X0', 'X1', 'X2'])
    vector = [p.copy(), p.copy(), p.copy()]
    after = before.replace_column(vector, 'X1')

    assert after.matrix[0][1] == after.matrix[1][1] == after.matrix[2][1] == p
    assert after.matrix[0][0] == after.matrix[2][2] and after.matrix[2][2] != p
    assert after.matrix[1][0] == after.matrix[2][0] == after.matrix[0][2]
    assert after.matrix[0][2] == after.matrix[1][2] and after.matrix[1][2] != p
