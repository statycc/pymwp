from pymwp import Polynomial, Monomial
from pymwp.relation import Relation
from pymwp.relation_list import RelationList
from pymwp.matrix import init_matrix, identity_matrix


def test_init_list_with_relation():
    rel_list = RelationList(['X0', 'X1', 'X2'])
    expect_matrix = init_matrix(3)

    assert len(rel_list.relations) == 1
    assert rel_list.relations[0].variables == ['X0', 'X1', 'X2']
    assert rel_list.relations[0].matrix == expect_matrix


def test_init_list_with_many_relations():
    r1 = Relation(['X0', 'X1'])
    r2 = Relation(['X0', 'X1', 'X2'])
    r3 = Relation(['X0', 'X1', 'X2', 'X3'])

    many_relations = RelationList(relation_list=[r1, r2, r3])

    assert len(many_relations.relations) == 3
    assert many_relations.relations[0] == r1
    assert many_relations.relations[1] == r2
    assert many_relations.relations[2] == r3


def test_init_list_with_identity():
    rel_list = RelationList.identity(['X0', 'X1', 'X2'])
    expect_matrix = identity_matrix(3)

    assert rel_list.relations[0].variables == ['X0', 'X1', 'X2']
    assert rel_list.relations[0].matrix == expect_matrix


def test_contains_matrix_finds_match():
    r1 = Relation.identity(['X0', 'X1', 'X2'])
    r2 = Relation(['X0', 'X1', 'X2'])
    r3 = Relation.identity(['X0', 'X1', 'X2', 'X3'])
    search_list = [r1, r2, r3]

    expected_matrix = identity_matrix(4)
    search_result = RelationList.contains_matrix(search_list, expected_matrix)

    assert search_result is True


def test_contains_matrix_finds_polynomial_match():
    m = init_matrix(3, Polynomial([Monomial('p')]))
    search_list = [Relation(matrix=m)]
    search_value = init_matrix(3, Polynomial([Monomial('p')]))

    search_result = RelationList.contains_matrix(search_list, search_value)

    assert search_result is True


def test_contains_matrix_no_match():
    search_list = [
        Relation.identity(['X0', 'X1']),
        Relation(matrix=init_matrix(3, Polynomial([Monomial('p')])))
    ]
    search_value = init_matrix(3)
    search_result = RelationList.contains_matrix(search_list, search_value)

    assert search_result is False
