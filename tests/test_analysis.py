from pytest import raises
from pymwp import Analysis
from .mocks.ast_mocks import \
    EMPTY_MAIN, INFINITE_2C, NOT_INFINITE_2C, \
    IF_WO_BRACES, IF_WITH_BRACES, VARIABLE_IGNORED

PARSE_METHOD = 'pymwp.analysis.Analysis.parse_c_file'


def test_analyze_empty_file(mocker):
    """Empty C file raises non-zero system exit"""
    mocker.patch(PARSE_METHOD, return_value=None)
    with raises(SystemExit):
        Analysis.run('empty input')


def test_analyze_empty_main(mocker):
    """Empty main method raises non-zero system exit"""
    mocker.patch(PARSE_METHOD, return_value=EMPTY_MAIN)
    with raises(SystemExit):
        Analysis.run('empty main')


def test_analyze_simple_infinite(mocker):
    """Check analysis result for infinite/infinite_2.c"""
    mocker.patch(PARSE_METHOD, return_value=INFINITE_2C)
    relation, combinations = Analysis.run("infinite 2", no_save=True)

    # no combinations since it is infinite
    assert combinations == []
    # expected these variables
    assert relation.variables == ['X0', 'X1']
    # check that *some* deltas match expected outputs
    try:
        assert str(relation.matrix[0][0].list[0]) == 'm'
        assert str(relation.matrix[0][0].list[1]) == 'i.delta(0,0)'
        assert str(relation.matrix[0][0].list[2]) == 'i.delta(1,0)'
        assert str(relation.matrix[0][0].list[3]) == 'i.delta(2,0)'
    except AssertionError:
        relation.show()
        raise


def test_analyze_simple_non_infinite(mocker):
    """Check analysis result for not_infinite/notinfinite_2.c"""
    mocker.patch(PARSE_METHOD, return_value=NOT_INFINITE_2C)
    relation, combinations = Analysis.run("not infinite 2", no_save=True)

    # match expected choices and variables
    assert relation.variables == ['X0', 'X1']
    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    # match *some* deltas from the matrix
    assert str(relation.matrix[0][0].list[0]) == 'w.delta(0,0)'
    assert str(relation.matrix[0][0].list[1]) == 'w.delta(1,0)'
    assert str(relation.matrix[0][0].list[2]) == 'w.delta(2,0)'


def test_analyze_if_with_braces(mocker):
    """If...else program using curly braces; result is 0-matrix."""
    mocker.patch(PARSE_METHOD, return_value=IF_WITH_BRACES)
    relation, combinations = Analysis.run("if_braces", no_save=True)

    # match choices and variables
    assert relation.variables == ['x', 'x1', 'x2', 'x3', 'y']
    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    # all monomials are 0s
    try:
        for i, _ in enumerate(relation.variables):
            for j, _ in enumerate(relation.variables):
                assert relation.matrix[i][j].list[0].scalar == 'o'
    except AssertionError:
        relation.show()
        raise


def test_analyze_if_without_braces(mocker):
    """If...else program NOT using curly braces; result is 0-matrix, expect
    exact same output as previous test."""
    mocker.patch(PARSE_METHOD, return_value=IF_WO_BRACES)
    relation, combinations = Analysis.run("if_wo_braces", no_save=True)

    # match choices and variables
    assert relation.variables == ['x', 'x1', 'x2', 'x3', 'y']
    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    # all monomials are 0s
    try:
        for i, _ in enumerate(relation.variables):
            for j, _ in enumerate(relation.variables):
                assert relation.matrix[i][j].list[0].scalar == 'o'
    except AssertionError:
        relation.show()
        raise


def test_analyze_variable_ignore(mocker):
    """Analysis picks up variable one left of assignment,
    see issue #11: https://github.com/seiller/pymwp/issues/11 """
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
