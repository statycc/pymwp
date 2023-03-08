from pymwp.delta_graphs import DeltaGraph
from pymwp.monomial import Monomial


def test_insert_mono():
    m1 = Monomial('m', (0, 0), (0, 1), (1, 2), (2, 3))
    m2 = Monomial('m', (1, 0), (2, 1))
    m3 = Monomial('m', (1, 0), (1, 1))
    dg = DeltaGraph(m1, m2, m3)

    assert ((1, 0), (2, 1)) in dg.graph_dict[2]
    assert ((1, 0), (1, 1)) in dg.graph_dict[2]
    assert ((0, 0), (0, 1), (1, 2), (2, 3)) in dg.graph_dict[4]


def test_insert_tuple():
    m1 = ((0, 0), (0, 1))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 2), (1, 3), (2, 4))
    m4 = ((0, 2), (1, 3), (3, 4))
    m5 = ((0, 2), (1, 3), (3, 4))
    m6 = ((0, 2), (2, 3), (2, 4))

    lm = [m1, m2, m3, m4, m5, m6]

    dg = DeltaGraph()

    for m in lm:
        dg.insert_node(m)

    assert dg.node_diff(m3, m4) == (True, 4)
    assert dg.graph_dict[3][m3][m4] == 4
    assert dg.graph_dict[3][m4][m3] == 4
    assert dg.graph_dict[3][m3][m6] == 3


def test_remove_index():
    m1 = ((0, 0), (0, 1))
    m1_ = ((0, 1),)
    m2 = ((0, 1), (1, 2))
    m2_ = ((0, 1),)
    m3 = ((0, 2), (1, 3), (2, 4))
    m3_ = ((0, 2), (1, 3))
    m4 = ((0, 2), (1, 3), (2, 3))
    m4_ = ((0, 2),)

    assert DeltaGraph.remove_index(m1, 0) == m1_
    assert DeltaGraph.remove_index(m2, 2) == m2_
    assert DeltaGraph.remove_index(m3, 4) == m3_
    assert DeltaGraph.remove_index(m4, 3) == m4_


def test_remove_tuple():
    m1 = ((0, 0), (0, 1))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 2), (1, 3), (2, 4))
    m4 = ((0, 2), (1, 3), (3, 4))
    m5 = ((0, 2), (2, 3), (3, 4))
    m6 = ((0, 2), (2, 3), (2, 4))

    # m1 --1--m2
    # m3 --4--m4--3-- m5
    #   \           /
    #    \         /
    #     3       4
    #      \     /
    #       \   /
    #         m6
    lm = [m1, m2, m3, m4, m5, m6]

    dg = DeltaGraph()

    for m in lm:
        dg.insert_node(m)

    assert dg.graph_dict[2][m1] == {}
    assert dg.graph_dict[2][m2] == {}
    assert dg.graph_dict[3][m3][m4] == 4
    assert dg.graph_dict[3][m4][m3] == 4
    assert dg.graph_dict[3][m4][m5] == 3
    assert dg.graph_dict[3][m3][m6] == 3
    assert dg.graph_dict[3][m5][m6] == 4
    assert dg.graph_dict[3][m6][m5] == 4

    # Should remove m6 and m5
    dg.remove_node(m6, 4)

    assert dg.graph_dict[2][m1] == {}
    assert dg.graph_dict[2][m2] == {}

    assert dg.graph_dict[3][m3][m4] == 4
    assert dg.graph_dict[3][m4][m3] == 4
    assert m5 not in dg.graph_dict[3]
    assert m5 not in dg.graph_dict[3][m4]
    assert m6 not in dg.graph_dict[3]
    assert m6 not in dg.graph_dict[3][m3]


def test_diff():
    m1 = ((0, 0), (0, 2))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 2), (1, 3), (2, 4))
    m4 = ((0, 2), (1, 3), (3, 4))
    m5 = ((0, 2), (2, 3), (3, 4))

    assert DeltaGraph.node_diff(m3, m4) == (True, 4)
    assert DeltaGraph.node_diff(m4, m3) == (True, 4)
    assert DeltaGraph.node_diff(m1, m2) == (False, 0)
    assert DeltaGraph.node_diff(m2, m1) == (False, 1)
    assert DeltaGraph.node_diff(m3, m5) == (False, 3)


def test_is_full2():
    m1 = ((0, 1), (0, 2))
    m2 = ((0, 1), (1, 2))
    dg2 = DeltaGraph(m1, m2, degree=2)
    dg3 = DeltaGraph(m1, m2, degree=3)

    # m1 --2-- m2
    assert dg3.is_full(m1, 2, 2) is False
    assert dg3.is_full(m2, 2, 2) is False
    assert dg2.is_full(m1, 2, 2) is True
    assert dg2.is_full(m2, 2, 2) is True


def test_is_full3():
    m3 = ((0, 1), (2, 2), (0, 3))
    m4 = ((0, 1), (2, 2), (1, 3))
    m5 = ((0, 1), (2, 2), (2, 3))
    dg = DeltaGraph(m3, m4, m5, degree=3)

    # m3 --3-- m4
    #   \       |
    #    \      |
    #     3     3
    #      \    |
    #       \   |
    #         m5

    assert dg.is_full(m3, 3, 3) is True
    assert dg.is_full(m4, 3, 3) is True
    assert dg.is_full(m5, 3, 3) is True


def test_fusion():
    m1 = ((0, 1), (0, 2))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 1), (2, 2), (0, 3))
    m4 = ((0, 1), (2, 2), (1, 3))
    m5 = ((0, 1), (2, 2), (2, 3))

    lm = (m1, m2, m3, m4, m5)

    dg = DeltaGraph()

    for m in lm:
        dg.insert_node(m)

    dg.fusion()

    assert dg.graph_dict[3] == {}
    assert dg.graph_dict[2] == {}
    assert dg.graph_dict[1] == {((0, 1),): {}}
