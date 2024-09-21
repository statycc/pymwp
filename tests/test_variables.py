from pymwp import Variables, Parser as pr
from .mocks.ast_mocks import *

# examples indices in var_tests.c
[EX_LOOP, EX_CALL, EX_PNT, EX_LOOP2, EX_SWH, EX_IFDO, EX_CAST] = range(7)


def nth_func(ast, nth=0):
    return [f for f in ast if pr.is_func(f)][nth]


def nth_loop(func, nth=0):
    return [lp for lp in func.body.block_items if pr.is_loop(lp)][nth]


def test_vars_find_expected_body_variables():
    expect = ['X1', 'X2', 'X3', 'X4']
    assert Variables(nth_func(VARIABLE_IGNORED)).vars == expect


def test_vars_find_expected_params():
    assert Variables(nth_func(PARAMS)).vars == ['x1', 'x2', 'x3']


def test_detecting_vars_in_loops():
    func = nth_func(VAR_TESTS, EX_LOOP)
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == body == ['X1']
    assert x == []  # unable to infer guard


def test_ignore_function_call_vars():
    func = nth_func(VAR_TESTS, EX_CALL)
    assert Variables(func).vars == ['X1', 'X2']


def test_ignore_pointer_vars():
    func = nth_func(VAR_TESTS, EX_PNT)
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == body == ['z']
    assert x == []


def test_find_right_loop_variables():
    func = nth_func(VAR_TESTS, EX_LOOP2)
    x, body = Variables.loop_guard(nth_loop(func))
    assert Variables(func).vars == ['x', 'y', 'z']  # x is in params
    assert body == ['y', 'z']
    assert x == ['x']


def test_ignores_variables_in_skipped_stmts():
    assert Variables(nth_func(VAR_TESTS, EX_SWH)).vars == []


def test_find_right_nested_variables():
    assert Variables(nth_func(VAR_TESTS, EX_IFDO)).vars == ['x', 'y', 'z']


def test_finds_casted_variables():
    assert Variables(nth_func(VAR_TESTS, EX_CAST)).vars == ['count', 'sum']
