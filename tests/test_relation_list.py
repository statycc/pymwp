from pymwp import Polynomial, Relation, RelationList
from pymwp.matrix import init_matrix, identity_matrix


def test_init_list_with_relation():
    """Creating relation list with one relation contains the provided
    relation after instantiation."""
    rel_list = RelationList(['X0', 'X1', 'X2'])
    [first_relation] = rel_list.relations

    assert len(rel_list.relations) == 1
    assert first_relation.variables == ['X0', 'X1', 'X2']
    assert first_relation.matrix == init_matrix(3)


def test_init_list_with_many_relations():
    """Creating a relation list contains all provided relations after
    instantiation."""
    r1 = Relation(['X0', 'X1'])
    r2 = Relation(['X0', 'X1', 'X2'])
    r3 = Relation(['X0', 'X1', 'X2', 'X3'])
    many_relations = RelationList(relation_list=[r1, r2, r3])
    [rl_r1, rl_r2, rl_r3] = many_relations.relations

    assert len(many_relations.relations) == 3
    assert rl_r1 == r1
    assert rl_r2 == r2
    assert rl_r3 == r3


def test_init_list_with_identity():
    """Creating identity relation list also creates an identity matrix, and
    holds specified variables."""
    rel_list = RelationList.identity(['X0', 'X1', 'X2'])
    expect_matrix = identity_matrix(3)
    [first_relation] = rel_list.relations

    assert first_relation.variables == ['X0', 'X1', 'X2']
    assert first_relation.matrix == expect_matrix


def test_contains_matrix_finds_match():
    """Method finds identity matrix in a list of matrices."""
    r1 = Relation.identity(['X0', 'X1', 'X2'])
    r2 = Relation(['X0', 'X1', 'X2'])
    r3 = Relation.identity(['X0', 'X1', 'X2', 'X3'])
    expected_matrix = identity_matrix(4)
    search_list = [r1, r2, r3]

    assert RelationList.contains_matrix(search_list, expected_matrix) is True


def test_contains_matrix_finds_polynomial_match():
    """When matrix of polynomials is in list, method returns true."""
    search_list = [Relation(matrix=init_matrix(3, Polynomial('p')))]
    search_value = init_matrix(3, Polynomial('p'))

    assert RelationList.contains_matrix(search_list, search_value) is True


def test_contains_matrix_no_match():
    """When matrix is not in list, method returns false."""
    search_list = [
        Relation.identity(['X0', 'X1']),
        Relation(matrix=init_matrix(3, Polynomial('p')))
    ]
    search_value = init_matrix(3)

    assert RelationList.contains_matrix(search_list, search_value) is False
