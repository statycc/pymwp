from pymwp import LoopAnalysis
from .mocks.ast_mocks import *


def test_single_link_loop_analysis():
    result = LoopAnalysis.run(SINGLE_LINK_CLUSTER, strict=True) \
        .get_func('SingleLinkCluster')

    assert result.n_loops == 3
    assert result.loops[0].n_bounded == 2
    assert result.loops[1].n_bounded == 2
    assert result.loops[2].n_bounded == 1
    assert len(result.loops[0].linear) == 1
    assert len(result.loops[1].linear) == 1
    assert len(result.loops[2].linear) == 1


def test_not_infinite3_has_independent():
    result = LoopAnalysis.run(NOT_INFINITE_3, strict=True)
    loop = result.get_func('foo').loops[0]
    assert result.n_loops == 1
    assert loop.n_vars == 4
    assert loop.variables['X0'].is_w
    assert loop.variables['X1'].is_m
    assert loop.variables['X2'].is_m


def test_infinite8_has_one_ok_variable():
    result = LoopAnalysis.run(INFINITE_8, strict=True).get_func('foo')
    loop = result.loops[0]
    assert result.n_loops == 1
    assert loop.n_vars == 6
    assert loop.n_bounded == 2
    assert len(loop.exp) == 4
    assert loop.variables['X5'].is_m


def test_for_subst_loop_analysis():
    result = LoopAnalysis.run(FOR_SUBST, strict=True).get_func('main')
    loop = result.loops[0]
    assert result.n_loops == 1
    assert loop.n_vars == 3  # include guard
    assert loop.n_bounded == 3
    assert loop.variables['x_'].is_m
    assert loop.variables['x'].is_m
    assert loop.variables['y'].is_p
