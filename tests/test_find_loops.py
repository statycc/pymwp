from pymwp import FindLoops, Parser as pr
from .mocks.ast_mocks import *


def nth_func(ast, nth=0):
    return [f for f in ast if pr.is_func(f)][nth]


def test_find_loop_locates_expected_for_loop():
    loops = FindLoops(nth_func(FOR_LOOP)).loops
    assert len(loops) == 1
    assert isinstance(loops[0], pr.For)


def test_find_loop_locates_expected_while_loop():
    loops = FindLoops(nth_func(INFINITE_8)).loops
    assert len(loops) == 1
    assert isinstance(loops[0], pr.While)


def test_find_loop_locates_nested_loops():
    loops = FindLoops(nth_func(SINGLE_LINK_CLUSTER)).loops
    assert len(loops) == 3
    assert isinstance(loops[0], pr.While)
    assert isinstance(loops[1], pr.While)
    assert isinstance(loops[2], pr.While)


def test_find_loop_locates_non_top_level_loops():
    loops = FindLoops(nth_func(VAR_TESTS, 4)).loops
    assert len(loops) == 1
    assert isinstance(loops[0], pr.DoWhile)
