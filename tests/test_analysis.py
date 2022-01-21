from pymwp import Analysis, Polynomial
from .mocks.ast_mocks import \
    INFINITE_2C, NOT_INFINITE_2C, IF_WO_BRACES, IF_WITH_BRACES, \
    VARIABLE_IGNORED, BRACES_ISSUES, PARAMS, FUNCTION_CALL, INFINITE_8C


def test_analyze_infinite2():
    """Check analysis result for infinite/infinite_2.c"""
    relation, combinations, infty = Analysis.run(INFINITE_2C, no_save=True)

    assert infty  # result should be infinite
    assert combinations is None  # no combinations since it is infinite
    assert relation is None  # no relation since infinite


def test_analyze_non_infinite_2():
    """Check analysis result for not_infinite/notinfinite_2.c"""
    relation, combinations, infty = Analysis.run(NOT_INFINITE_2C, no_save=True)

    assert not infty

    # match expected choices and variables
    assert set(relation.variables) == {'X0', 'X1'}
    assert combinations == [[0, 0], [0, 1], [0, 2],
                            [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]

    # match *some* deltas from the matrix
    assert str(relation.matrix[0][0].list[0]) == 'w.delta(0,0)'
    assert str(relation.matrix[0][0].list[1]) == 'w.delta(1,0)'
    assert str(relation.matrix[0][0].list[2]) == 'w.delta(2,0)'


def test_analyze_infinite_8():
    """Check analysis result for infinite/infinite_8.c"""
    _, _, infty = Analysis.run(INFINITE_8C, no_save=True)
    assert infty


def test_analyze_if_braces_do_not_matter():
    """If...else block with single-statement, with or without curly braces,
     should give the same analysis result."""
    rel_with, choices_with = Analysis.run(IF_WITH_BRACES, no_save=True)[:2]
    rel_wo, choices_wo = Analysis.run(IF_WO_BRACES, no_save=True)[:2]

    # match choices and variables
    assert set(rel_with.variables) == set(rel_wo.variables) == \
           {'x', 'x1', 'x2', 'x3', 'y'}
    # should give same choices
    assert choices_with == choices_wo == \
           [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1],
            [0, 1, 2], [0, 2, 0], [0, 2, 1], [0, 2, 2], [1, 0, 0],
            [1, 0, 1], [1, 0, 2], [1, 1, 0], [1, 1, 1], [1, 1, 2],
            [1, 2, 0], [1, 2, 1], [1, 2, 2], [2, 0, 0], [2, 0, 1],
            [2, 0, 2], [2, 1, 0], [2, 1, 1], [2, 1, 2], [2, 2, 0],
            [2, 2, 1], [2, 2, 2]]


def test_analyze_variable_ignore():
    """Analysis picks up variable on left of assignment,
    see issue #11: https://github.com/statycc/pymwp/issues/11 """
    relation, combinations = Analysis.run(VARIABLE_IGNORED, no_save=True)[:2]

    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    assert set(relation.variables) == {'X2', 'X3', 'X1', 'X4'}

    mpw = '+m.delta(0,0)+p.delta(1,0)+w.delta(2,0)'
    pmw = '+p.delta(0,0)+m.delta(1,0)+w.delta(2,0)'
    o = '+o'
    m = '+m'
    res = [
        [m, pmw, o, pmw],
        [o, o, o, o],
        [o, mpw, m, mpw],
        [o, o, o, o],
    ]

    try:
        for i in range(len(relation.variables)):
            for j in range(len(relation.variables)):
                assert str(relation.matrix[i][j]).strip() == res[i][j]
    except AssertionError:
        relation.show()
        raise


def test_extra_braces_are_ignored():
    """Analysis ignores superfluous braces in C program,
    see issue: #25: https://github.com/statycc/pymwp/issues/25"""
    relation, combinations = Analysis.run(BRACES_ISSUES, no_save=True)[
                             :2]

    assert set(relation.variables) == {'x', 'y'}
    assert relation.matrix[0][0] == Polynomial('m')
    assert relation.matrix[0][1] == Polynomial('o')
    assert relation.matrix[1][0] == Polynomial('m')
    assert relation.matrix[1][1] == Polynomial('m')


def test_analysis_identifies_function_params():
    """Analysis will identify variables from function declaration
    issue #51: https://github.com/statycc/pymwp/issues/51
    """
    relation = Analysis.run(PARAMS, no_save=True)[0]

    assert set(relation.variables) == {'x1', 'x2', 'x3'}


def test_analysis_returns_all_functions():
    """If input file contains multiple functions result contains
    evaluation of each function (example 5a)
    """
    result = Analysis.run(FUNCTION_CALL, no_save=True)
    _, _, f_infty = result['f']
    foo, _, _ = result['foo']

    assert not f_infty
    assert set(foo.variables) == {'X1', 'X2'}
