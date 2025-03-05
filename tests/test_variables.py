from pymwp import Variables, Parser as pr
from .mocks.ast_mocks import *


def f(ast, name):
    return [f_ for f_ in ast if pr.is_func(f_)
            and f_.decl.name == name][0]


def nth_loop(func, nth=0):
    return [lp for lp in func.body.block_items if pr.is_loop(lp)][nth]


def test_vars_find_expected_body_variables():
    expect = ['X1', 'X2', 'X3', 'X4']
    assert Variables(f(VARIABLE_IGNORED, 'foo')).vars == expect


def test_vars_find_expected_params():
    assert Variables(f(PARAMS, 'foo')).vars == ['x1', 'x2', 'x3']


def test_detecting_vars_in_loops():
    func = f(VAR_TESTS, 'loop')
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == ['X1','i']
    assert body == ['X1']
    assert x == []  # unable to infer guard


def test_ignore_function_call_vars():
    func = f(VAR_TESTS, 'fcall')
    assert Variables(func).vars == ['X1', 'X2']


def test_ignore_pointer_vars():
    func = f(VAR_TESTS, 'pointer_loop')
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == ['j','z']
    assert body == ['z']
    assert x == []


def test_find_right_loop_variables():
    func = f(VAR_TESTS, 'ok_loop')
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == ['x', 'y', 'z']  # x is in params
    assert body == ['y', 'z']
    assert x == ['x']


def test_ignores_variables_in_skipped_stmts():
    assert Variables(f(VAR_TESTS, 'fun_do_wh')).vars == []


def test_find_right_nested_variables():
    assert Variables(f(VAR_TESTS, 'fun_if')).vars == ['x', 'y', 'z']


def test_finds_casted_variables():
    assert Variables(f(VAR_TESTS, 'cast')).vars == ['count', 'sum']


def test_ignore_true_false():
    assert Variables(f(VAR_TESTS, 'ignore_tf')).vars == ['X1', 'X2']
