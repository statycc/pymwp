from pytest import raises
from pymwp import Analysis
from .sample_ast import EMPTY_MAIN, INFINITE_2C, NOT_INFINITE_2C, \
    IF_WO_BRACES, IF_WITH_BRACES, VARIABLE_IGNORED

PARSE_METHOD = 'pymwp.analysis.Analysis.parse_c_file'


def test_analyze_empty_file(mocker):
    mocker.patch(PARSE_METHOD, return_value=None)
    # should return non-zero exit
    with raises(SystemExit):
        Analysis.run('empty input')


def test_analyze_empty_main(mocker):
    mocker.patch('pymwp.analysis.Analysis.parse_c_file',
                 return_value=EMPTY_MAIN)
    with raises(SystemExit):
        # should return non-zero exit
        Analysis.run('empty main')


def test_analyze_simple_infinite(mocker):
    mocker.patch(PARSE_METHOD, return_value=INFINITE_2C)
    relation, combinations = Analysis.run("infinite 2", no_save=True)

    assert combinations == []  # no combinations since it is infinite
    assert relation.variables == ['X0', 'X1']  # expected these variables
    # check that some deltas match expected
    try:
        assert str(relation.matrix[0][0].list[0]) == 'm'
        assert str(relation.matrix[0][0].list[1]) == 'i.delta(0,0)'
        assert str(relation.matrix[0][0].list[2]) == 'i.delta(1,0)'
        assert str(relation.matrix[0][0].list[3]) == 'i.delta(2,0)'
    except AssertionError:
        relation.show()
        raise


def test_analyze_simple_non_infinite(mocker):
    mocker.patch(PARSE_METHOD, return_value=NOT_INFINITE_2C)
    relation, combinations = Analysis.run("not infinite 2", no_save=True)

    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    assert relation.variables == ['X0', 'X1']
    assert str(relation.matrix[0][0].list[0]) == 'w.delta(0,0)'
    assert str(relation.matrix[0][0].list[1]) == 'w.delta(1,0)'
    assert str(relation.matrix[0][0].list[2]) == 'w.delta(2,0)'


def test_analyze_if_with_braces(mocker):
    mocker.patch(PARSE_METHOD, return_value=IF_WITH_BRACES)
    relation, combinations = Analysis.run("if_braces", no_save=True)

    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    assert relation.variables == ['x', 'x1', 'x2', 'x3', 'y']
    # Should we have `m` on diag for x3 ? don't think so
    # since X3 is constant in all cases…
    try:
        for i in range(len(relation.variables)):
            for j in range(len(relation.variables)):
                assert str(relation.matrix[i][j].list[0]) == 'o'
    except AssertionError:
        relation.show()
        raise


def test_analyze_if_without_braces(mocker):
    mocker.patch(PARSE_METHOD, return_value=IF_WO_BRACES)
    relation, combinations = Analysis.run("if_wo_braces", no_save=True)

    # should have exact same result as previous test...
    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    assert relation.variables == ['x', 'x1', 'x2', 'x3', 'y']
    # Should we have `m` on diag for x3 ? don't think so
    # since X3 is constant in all cases…
    try:
        for i in range(len(relation.variables)):
            for j in range(len(relation.variables)):
                assert str(relation.matrix[i][j].list[0]) == 'o'
    except AssertionError:
        relation.show()
        raise


def test_analyze_variable_ignore(mocker):
    mocker.patch(PARSE_METHOD, return_value=VARIABLE_IGNORED)
    relation, combinations = Analysis.run("variable_ignored", no_save=True)

    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    assert relation.variables == ['X2', 'X3', 'X1', 'X4']

    wmp = '+w.delta(0,0)+m.delta(1,0)+p.delta(2,0)'
    wpm = '+w.delta(0,0)+p.delta(1,0)+m.delta(2,0)'
    o = '+o'
    m = '+m'
    res = [
        [o, o, o, o],
        [wmp, m, o, wmp],
        [wpm, o, m, wpm],
        [o, o, o, o],
    ]

    try:
        for i in range(len(relation.variables)):
            for j in range(len(relation.variables)):
                assert str(relation.matrix[i][j]).strip() == res[i][j]
    except AssertionError:
        relation.show()
        raise
