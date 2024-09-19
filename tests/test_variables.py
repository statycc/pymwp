from pymwp import Variables, Parser as pr
from .mocks.ast_mocks import *


def nth_func(ast, nth=0):
    functions = [f for f in ast if pr.is_func(f)]
    return functions[nth]


def nth_loop(func, nth=0):
    return [lp for lp in func.body.block_items if pr.is_loop(lp)][nth]


def test_vars_find_expected_body_variables():
    assert Variables(nth_func(VARIABLE_IGNORED)).vars == \
           ['X1', 'X2', 'X3', 'X4']


def test_vars_find_expected_params():
    assert Variables(nth_func(PARAMS)).vars == ['x1', 'x2', 'x3']


def test_detecting_vars_in_loops():
    func = nth_func(VAR_TESTS, 0)
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == body == ['X1']
    assert x == []  # unable to infer guard


def test_ignore_function_call_vars():
    func = nth_func(VAR_TESTS, 1)
    assert Variables(func).vars == ['X1', 'X2']


def test_ignore_pointer_vars():
    func = nth_func(VAR_TESTS, 2)
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == body == ['z']
    assert x == []


def test_find_right_loop_variables():
    func = nth_func(VAR_TESTS, 3)
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == ['x', 'y', 'z']  # x is in params
    assert body == ['y', 'z']
    assert x == ['x']
