from pymwp import FindLoops, Parser as pr
from .mocks.ast_mocks import *


def f(ast, name):
    return ([f_ for f_ in ast if pr.is_func(f_)
             and f_.decl.name == name][0])


def test_find_loop_locates_expected_for_loop():
    loops = FindLoops(f(FOR_LOOP, 'main')).loops
    assert len(loops) == 1
    assert isinstance(loops[0], pr.For)


def test_find_loop_locates_expected_while_loop():
    loops = FindLoops(f(INFINITE_8, 'foo')).loops
    assert len(loops) == 1
    assert isinstance(loops[0], pr.While)


def test_find_loop_locates_nested_loops():
    loops = FindLoops(f(SINGLE_LINK_CLUSTER, 'SingleLinkCluster')).loops
    assert len(loops) == 3
    assert isinstance(loops[0], pr.While)
    assert isinstance(loops[1], pr.While)
    assert isinstance(loops[2], pr.While)


def test_find_loop_locates_non_top_level_loops():
    loops = FindLoops(f(VAR_TESTS, 'fun_do_wh')).loops
    assert len(loops) == 1
    assert isinstance(loops[0], pr.DoWhile)


def test_find_loop_skips_invalid_guard():
    loops = FindLoops(f(FOR_INVALID, 'main'))
    assert len(loops.loops) == 1


def test_find_loop_skips_invalid_body():
    loops = FindLoops(f(FOR_BODY, 'main'))
    assert len(loops.loops) == 1
