from pymwp.bound import Bound, MwpBound


def test_bound_triple():
    mwp = MwpBound()
    mwp.append('m', 'X0')
    mwp.append('w', 'X1')
    mwp.append('p', 'X2')

    assert mwp.bound_triple == (('X0',), ('X1',), ('X2',))


def test_mwp_bound_equals():
    mwp = MwpBound()
    mwp.append('m', 'X0')
    mwp.append('m', 'X2')
    mwp.append('m', 'X1')
    mwp.append('w', 'X4')
    mwp.append('p', 'X8')
    mwp.append('p', 'X5')
    mwp.append('p', 'X6')

    assert mwp == MwpBound("X1,X0,X2;X4;X6,X5,X8")


def test_bound_not_equals():
    b1 = Bound({'X3': "X3,X5;;X1,X2",
                'X4': "X4;;X1,X5"})
    b2 = Bound({'X3': "X3,X2;;X1,X5",
                'X4': "X4;;X1,X5"})
    assert b1.variables == b2.variables
    assert b1.bound_dict['X4'] == b2.bound_dict['X4']
    assert b1.bound_dict['X3'] != b2.bound_dict['X3']
    assert b1 != b2


def test_bound_str_format():
    mwp = MwpBound()
    mwp.x.add('X0', 'X1')
    mwp.z.add('X3', 'X4', 'X2')

    assert mwp.bound_str == "X0,X1;;X2,X3,X4"


def test_bound_load():
    bound = Bound({"X0": "X0;X1;X2,X3",
                   "X1": "X1;;X2",
                   "X2": "X2;;X3", "X3": "X3;;"})

    assert bound.bound_dict['X0'].x.vars == ['X0']
    assert bound.bound_dict['X0'].y.vars == ['X1']
    assert bound.bound_dict['X0'].z.vars == ['X2', 'X3']
    assert bound.bound_dict['X1'].x.vars == ['X1']
    assert bound.bound_dict['X1'].z.vars == ['X2']
    assert bound.bound_dict['X2'].x.vars == ['X2']
    assert bound.bound_dict['X2'].z.vars == ['X3']


def test_bound_unload():
    bd = Bound({"X0": "X0;X1;", "X1": ";;X0"}).to_dict()

    assert 'X0' in bd and 'X1' in bd
    assert bd['X0'] == "X0;X1;"
    assert bd['X1'] == ";;X0"
