from itertools import product
from pymwp.delta_graphs import DeltaGraph
from pytest import raises

def test_insert_tuple():
    m1 = ((0, 0), (0, 1))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 2), (1, 3), (2, 4))
    m4 = ((0, 2), (1, 3), (3, 4))
    m5 = ((0, 2), (1, 3), (3, 4))
    m6 = ((0, 2), (2, 3), (2, 4))

    lm = [m1,m2,m3,m4,m5,m6]

    dg = DeltaGraph()
    # dg.import_monomials(lm)

    for m in lm:
        dg.insert_tuple(m)


    try:
        assert dg.mono_diff(m3,m4) == (True,4)
        assert dg.graph_dict[3][m3][m4] == 4
        assert dg.graph_dict[3][m4][m3] == 4
        with raises(KeyError):
            dg.graph_dict[3][m4][m5]
        assert dg.graph_dict[3][m3][m6] == 3
    except AssertionError:
        print(dg.graph_dict[3][m4])
        raise


def test_remove_index():
    m1 = ((0, 0), (0, 1))
    m1_ = ((0, 1),)
    m2 = ((0, 1), (1, 2))
    m2_ = ((0, 1),)
    m3 = ((0, 2), (1, 3), (2, 4))
    m3_ = ((0, 2), (1, 3))
    m4 = ((0, 2), (1, 3), (2, 3))
    # FIXME Should remove all deltas with index 3 ?
    m4_ = ((0, 2),)

    try:
        assert DeltaGraph.remove_index(m1,0) == m1_
        assert DeltaGraph.remove_index(m2,2) == m2_
        assert DeltaGraph.remove_index(m3,4) == m3_
        assert DeltaGraph.remove_index(m4,3) == m4_
    except AssertionError:
        raise

def test_remove_tuple():
    m1 = ((0, 0), (0, 1))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 2), (1, 3), (2, 4))
    m4 = ((0, 2), (1, 3), (3, 4))
    m5 = ((0, 2), (2, 3), (3, 4))
    m6 = ((0, 2), (2, 3), (2, 4))

    # m1 --1-- m2
    # m3 --4--m4--3-- m5
    #   \           /
    #    \         /
    #     3       4
    #      \     /
    #       \   /
    #         m6
    lm = [m1,m2,m3,m4,m5,m6]

    dg = DeltaGraph()

    for m in lm:
        dg.insert_tuple(m)

    try:

        assert dg.graph_dict[2][m1] == {}
        assert dg.graph_dict[2][m2] == {}

        assert dg.graph_dict[3][m3][m4] == 4
        assert dg.graph_dict[3][m4][m3] == 4
        assert dg.graph_dict[3][m4][m5] == 3
        assert dg.graph_dict[3][m3][m6] == 3
        assert dg.graph_dict[3][m5][m6] == 4
        assert dg.graph_dict[3][m6][m5] == 4
    except AssertionError:
        raise

    # Should remove m6 and m5
    dg.remove_tuple(m6,4)

    try:
        assert dg.graph_dict[2][m1] == {}
        assert dg.graph_dict[2][m2] == {}

        assert dg.graph_dict[3][m3][m4] == 4
        assert dg.graph_dict[3][m4][m3] == 4
        assert m5 not in dg.graph_dict[3]
        assert m5 not in dg.graph_dict[3][m4]
        assert m6 not in dg.graph_dict[3]
        assert m6 not in dg.graph_dict[3][m3]
    except AssertionError:
        raise

def test_mono_diff():
    m1 = ((0, 0), (0, 2))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 2), (1, 3), (2, 4))
    m4 = ((0, 2), (1, 3), (3, 4))
    m5 = ((0, 2), (2, 3), (3, 4))


    assert DeltaGraph.mono_diff(m3,m4) == (True,4)
    assert DeltaGraph.mono_diff(m4,m3) == (True,4)
    assert DeltaGraph.mono_diff(m1,m2) == (False,0)
    assert DeltaGraph.mono_diff(m2,m1) == (False,1)
    assert DeltaGraph.mono_diff(m3,m5) == (False,3)

def test_isfull():
    m1 = ((0, 1), (0, 2))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 1), (2, 2), (0, 3))
    m4 = ((0, 1), (2, 2), (1, 3))
    m5 = ((0, 1), (2, 2), (2, 3))

    # m1 --2-- m2
    # m3 --3-- m4
    #   \       |
    #    \      |
    #     3     3
    #      \    |
    #       \   |
    #         m5

    lm = (m1,m2,m3,m4,m5)

    dg = DeltaGraph()

    for m in lm:
        dg.insert_tuple(m)

    try:
        assert dg.is_full(3, m3, 3, 3) == True
        assert dg.is_full(3, m4, 3, 3) == True
        assert dg.is_full(3, m5, 3, 3) == True
        assert dg.is_full(2, m1, 2, 3) == False
        assert dg.is_full(2, m2, 2, 3) == False
        assert dg.is_full(2, m1, 2, 2) == True
        assert dg.is_full(2, m2, 2, 2) == True
    except AssertionError:
        raise

def test_fusion():
    m1 = ((0, 1), (0, 2))
    m2 = ((0, 1), (1, 2))
    m3 = ((0, 1), (2, 2), (0, 3))
    m4 = ((0, 1), (2, 2), (1, 3))
    m5 = ((0, 1), (2, 2), (2, 3))

    lm = (m1,m2,m3,m4,m5)

    dg = DeltaGraph()

    for m in lm:
        dg.insert_tuple(m)

    # list_of_max = [3,3,3,3]

    dg.fusion()

    try:
        assert dg.graph_dict[3] == {}
        assert dg.graph_dict[2] == {}
        assert dg.graph_dict[1] == {((0,1),):{}}
    except AssertionError:
        raise
