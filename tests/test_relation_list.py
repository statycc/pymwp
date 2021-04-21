from relation import Relation
from relation_list import RelationList
from matrix import init_matrix, identity_matrix


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
