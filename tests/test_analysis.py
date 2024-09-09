from pymwp import Analysis, Polynomial
from pymwp.semiring import ZERO_MWP, UNIT_MWP
from .mocks.ast_mocks import \
    INFINITE_2C, INFINITE_8C, NOT_INFINITE_2C, NOT_INFINITE_3C, \
    IF_WO_BRACES, IF_WITH_BRACES, VARIABLE_IGNORED, BRACES_ISSUES, \
    PARAMS, FUNCTION_CALL, EMPTY, IF_EMPTY_BRACES, FOR_LOOP, FOR_SUBST

o = ZERO_MWP
m = UNIT_MWP
w, p = 'w', 'p'


def test_analyze_infinite2():
    """Check analysis result for infinite/infinite_2.c"""
    foo = Analysis.run(INFINITE_2C, save=False).get_func()
    relation, combinations = foo.relation, foo.choices

    assert foo.infinite  # result should be infinite
    assert combinations is None  # no combinations since it is infinite
    assert relation is None  # no relation since infinite


def test_analyze_infinite_8():
    """Check analysis result for infinite/infinite_8.c"""
    assert Analysis.run(INFINITE_8C, save=False).get_func().infinite


def test_analyze_non_infinite_2():
    """Check analysis result for not_infinite/notinfinite_2.c"""
    foo = Analysis.run(NOT_INFINITE_2C, save=False).get_func()
    relation, combinations = foo.relation, foo.choices

    assert not foo.infinite

    # match expected choices and variables
    assert set(relation.variables) == {'X0', 'X1'}
    assert combinations.is_valid(0, 0)
    assert combinations.is_valid(0, 1)
    assert combinations.is_valid(0, 2)
    assert combinations.is_valid(1, 0)
    assert combinations.is_valid(1, 1)
    assert combinations.is_valid(1, 2)
    assert combinations.is_valid(2, 0)
    assert combinations.is_valid(2, 1)
    assert combinations.is_valid(2, 2)

    # match *some* deltas from the matrix
    assert relation.matrix[0][0].list[0].scalar == \
           relation.matrix[0][0].list[1].scalar == \
           relation.matrix[0][0].list[2].scalar == w
    assert relation.matrix[0][0].list[0].deltas == [(0, 0)]
    assert relation.matrix[0][0].list[1].deltas == [(1, 0)]
    assert relation.matrix[0][0].list[2].deltas == [(2, 0)]


def test_analyze_non_infinite_3():
    """Check analysis result for not_infinite/notinfinite_3.c"""
    foo = Analysis.run(NOT_INFINITE_3C, save=False).get_func()
    assert not foo.infinite
    assert len(foo.choices.valid) == 1
    assert foo.choices.valid[0] == [[0, 1, 2], [0, 1, 2], [2]]


def test_analyze_infinite_to_completion():
    """Check analysis completion for infinite program"""
    relation = Analysis.run(INFINITE_2C, save=False, fin=True) \
        .get_func().relation
    assert relation
    assert relation.matrix
    assert not relation.is_empty


def test_analyze_if_braces_do_not_matter():
    """If...else block with single-statement, with or without curly braces,
     should give the same analysis result."""
    res1 = Analysis.run(IF_WITH_BRACES, save=False).get_func()
    rel_with, choices_with = res1.relation, res1.choices
    res2 = Analysis.run(IF_WO_BRACES, save=False).get_func()
    rel_wo, choices_wo = res2.relation, res2.choices

    all_valid_choices = [
        [0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1],
        [0, 1, 2], [0, 2, 0], [0, 2, 1], [0, 2, 2], [1, 0, 0],
        [1, 0, 1], [1, 0, 2], [1, 1, 0], [1, 1, 1], [1, 1, 2],
        [1, 2, 0], [1, 2, 1], [1, 2, 2], [2, 0, 0], [2, 0, 1],
        [2, 0, 2], [2, 1, 0], [2, 1, 1], [2, 1, 2], [2, 2, 0],
        [2, 2, 1], [2, 2, 2]]

    # match choices and variables
    assert set(rel_with.variables) == set(rel_wo.variables) == \
           {'x', 'x1', 'x2', 'x3', 'y'}
    # both results accept same & all choices
    for choice in all_valid_choices:
        assert choices_with.is_valid(*choice) and choices_wo.is_valid(*choice)


def test_analyze_variable_ignore():
    """Analysis picks up variable on left of assignment,
    see issue #11: https://github.com/statycc/pymwp/issues/11 """
    result = Analysis.run(VARIABLE_IGNORED, save=False).get_func()
    relation, combinations = result.relation, result.choices
    non_infinity_choices = [[0, 0], [0, 1], [0, 2],
                            [1, 0], [1, 1], [1, 2],
                            [2, 0], [2, 1], [2, 2]]

    for choice in non_infinity_choices:
        assert combinations.is_valid(*choice)
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

    for i in range(len(relation.variables)):
        for j in range(len(relation.variables)):
            assert str(relation.matrix[i][j]).strip() == res[i][j]


def test_extra_braces_are_ignored():
    """Analysis ignores superfluous braces in C program,
    see issue: #25: https://github.com/statycc/pymwp/issues/25"""
    result = Analysis.run(BRACES_ISSUES, save=False).get_func()
    relation = result.relation
    assert set(relation.variables) == {'x', 'y'}
    assert relation.matrix[0][0] == Polynomial(m)
    assert relation.matrix[0][1] == Polynomial(o)
    assert relation.matrix[1][0] == Polynomial(m)
    assert relation.matrix[1][1] == Polynomial(m)


def test_analysis_identifies_function_params():
    """Analysis will identify variables from function declaration
    issue #51: https://github.com/statycc/pymwp/issues/51
    """
    relation = Analysis.run(PARAMS, save=False).get_func().relation
    assert set(relation.variables) == {'x1', 'x2', 'x3'}


def test_analysis_returns_all_functions():
    """If input file contains multiple functions result contains
    evaluation of each function (example 5a)
    """
    f = Analysis.run(FUNCTION_CALL, save=False).get_func('f')
    foo = Analysis.run(FUNCTION_CALL, save=False).get_func('foo')

    assert not f.infinite
    assert set(foo.relation.variables) == {'X1', 'X2'}


def test_analysis_handles_empty_program():
    result = Analysis.run(EMPTY, save=False)
    assert result.relations == {}


def test_analysis_handles_empty_decision_body():
    result = Analysis.run(IF_EMPTY_BRACES, save=False).get_func('foo')
    assert not result.infinite


def test_analysis_loop():
    """
    The matrix for loop x{y = y + z;}

    Loop body y = y + z =>  m p / p m / w w
    Last two derivations fail because need all m's on the diagonal.
    Loop correction: M* has p at row=2 col=1 => add p to row ℓ=0 col=1.
    Only one valid derivation.

        x   y   z
    x | m | p | o |
    y | o | m | o |
    z | o | p | m |
    """
    result = Analysis.run(FOR_LOOP, save=False).get_func('foo')
    simple_mat = result.relation.apply_choice(*result.choices.first)
    assert result.choices.n_bounds == 1
    assert simple_mat.matrix[0][0] == \
           simple_mat.matrix[1][1] == \
           simple_mat.matrix[2][2] == m
    assert simple_mat.matrix[0][1] == \
           simple_mat.matrix[2][1] == p
    assert simple_mat.matrix[0][2] == \
           simple_mat.matrix[1][0] == \
           simple_mat.matrix[1][2] == \
           simple_mat.matrix[2][0] == o


def test_analysis_loop_subst():
    """If loop variable occurs in body, substitute.
       x_ = x; loop x { y = y + x_; }
    """
    result = Analysis.run(FOR_SUBST, save=False).get_func('foo')
    simple_mat = result.relation.apply_choice(*result.choices.first)
    assert result.relation.variables == ['x', 'x_', 'y']
    assert result.choices.n_bounds == 3
    assert simple_mat.matrix[0][0] == m
    assert simple_mat.matrix[1][0] == \
           simple_mat.matrix[2][0] == o
    assert simple_mat.matrix[0][1] == m
    assert simple_mat.matrix[1][1] == \
           simple_mat.matrix[2][0] == o
    assert simple_mat.matrix[0][2] == p
    assert simple_mat.matrix[1][2] == o
    assert simple_mat.matrix[2][2] == m
