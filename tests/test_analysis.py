from pymwp import Analysis, Polynomial
from .mocks.ast_mocks import \
    INFINITE_2C, NOT_INFINITE_2C, IF_WO_BRACES, IF_WITH_BRACES, \
    VARIABLE_IGNORED, EXTRA_BRACES


def test_analyze_simple_infinite():
    """Check analysis result for infinite/infinite_2.c"""
    relation, combinations = Analysis.run(INFINITE_2C, no_save=True)

    assert combinations == []  # no combinations since it is infinite
    assert relation.variables == []  # expected these variables


def test_analyze_simple_non_infinite():
    """Check analysis result for not_infinite/notinfinite_2.c"""
    relation, combinations = Analysis.run(NOT_INFINITE_2C, no_save=True)

    # match expected choices and variables
    assert relation.variables == ['X0', 'X1']
    assert combinations == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]
    # match *some* deltas from the matrix
    assert str(relation.matrix[0][0].list[0]) == 'w.delta(0,0)'
    assert str(relation.matrix[0][0].list[1]) == 'w.delta(1,0)'
    assert str(relation.matrix[0][0].list[2]) == 'w.delta(2,0)'


def test_analyze_if_with_braces():
    """If...else program using curly braces; result is 0-matrix."""
    relation, combinations = Analysis.run(IF_WITH_BRACES, no_save=True)

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


def test_analyze_if_without_braces():
    """If...else program NOT using curly braces; result is 0-matrix, expect
    exact same output as previous test."""
    relation, combinations = Analysis.run(IF_WO_BRACES, no_save=True)

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


def test_analyze_variable_ignore():
    """Analysis picks up variable on left of assignment,
    see issue #11: https://github.com/seiller/pymwp/issues/11 """
    relation, combinations = Analysis.run(VARIABLE_IGNORED, no_save=True)

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


def test_extra_braces_are_ignored():
    """Analysis ignores superfluous braces in C program,
    see issue: #25: https://github.com/seiller/pymwp/issues/25"""
    relation, combinations = Analysis.run(EXTRA_BRACES, no_save=True)

    assert set(relation.variables) == {'x', 'y'}
    assert relation.matrix[0][0] == Polynomial('m')
    assert relation.matrix[0][1] == Polynomial('o')
    assert relation.matrix[1][0] == Polynomial('m')
    assert relation.matrix[1][1] == Polynomial('m')
