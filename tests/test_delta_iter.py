from pymwp.delta_graphs import DeltaGraph
from pymwp.delta_iter import create_delta_list, Deltaiter
from pytest import raises

def test_create_delta_list():
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

    dl = create_delta_list(4,dg)

    assert (dl[0] == [])
    assert (dl[1] == [list(m1)])
    assert (dl[2] == [list(m2)])
    assert (dl[3] == [])
    assert (dl[4] == list(map(list,[m3,m4,m6])))

def test_delta_iter_no_dg():
    dg = DeltaGraph()
    dl = create_delta_list(2,dg)

    assert (dl[0] == [])

    delta_i = Deltaiter([3,3],dl)

    print(delta_i.value())
    assert (delta_i.value() == [0,0])
    delta_i.next()
    assert (delta_i.value() == [0,1])
    delta_i.next()
    assert (delta_i.value() == [0,2])
    delta_i.next()
    assert (delta_i.value() == [1,0])
    delta_i.next()
    assert (delta_i.value() == [1,1])
    delta_i.next()
    assert (delta_i.value() == [1,2])
    delta_i.next()
    assert (delta_i.value() == [2,0])
    delta_i.next()
    assert (delta_i.value() == [2,1])
    delta_i.next()
    assert (delta_i.value() == [2,2])

def test_delta_iter_with_dg():
    m1 = ((0, 0), (1, 1))
    m2 = ((2, 0), (1, 1))

    lm = [m1,m2]

    dg = DeltaGraph()

    for m in lm:
        dg.insert_tuple(m)

    dl = create_delta_list(2,dg)

    assert (dl[0] == [])

    delta_i = Deltaiter([3,3],dl)

    assert (delta_i.value() == [0,0])
    delta_i.next()
    assert (delta_i.value() != [0,1])
    # delta_i.next()
    assert (delta_i.value() == [0,2])
    delta_i.next()
    assert (delta_i.value() == [1,0])
    delta_i.next()
    assert (delta_i.value() == [1,1])
    delta_i.next()
    assert (delta_i.value() == [1,2])
    delta_i.next()
    assert (delta_i.value() == [2,0])
    delta_i.next()
    assert (delta_i.value() != [2,1])
    # delta_i.next()
    assert (delta_i.value() == [2,2])
    assert (delta_i.next() == False)

