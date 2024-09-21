import logging
from copy import deepcopy

from pymwp import Coverage, Parser as pr
from .mocks.ast_mocks import *


def f(ast, name):
    return deepcopy(
        [f_ for f_ in ast if pr.is_func(f_)
         and f_.decl.name == name][0])


def loop(func, nth=0):
    return [lp for lp in func.body.block_items
            if pr.is_loop(lp)][nth]


def test_assert_and_assume_are_allowed():
    assert Coverage(f(VERIFICATION, 'main')).full


def test_allow_cast():
    assert Coverage(f(VAR_TESTS, 'cast')).full


def test_nary_not_supported():
    assert not Coverage(f(VAR_TESTS, 'triple')).full


def test_allow_do_while():
    assert Coverage(f(VAR_TESTS, 'fun_if')).full


def test_casts_maybe_supported():
    cover = Coverage(f(CASTS, 'foo'))
    assert len(cover.omit) == 5


def test_fully_supported_ast_remains_unchanged():
    func = f(SINGLE_LINK_CLUSTER, 'SingleLinkCluster')
    before = deepcopy(func)
    cover = Coverage(func)
    assert cover.full
    after = cover.ast_mod().node
    assert str(before) == str(after)


def test_removes_top_level_function_call():
    func = f(FUNCTION_CALL, 'foo')
    cover = Coverage(func)
    assert not cover.full
    after = cover.ast_mod().node
    assert Coverage(after).full
    assert pr.to_c(after, compact=True).strip() == \
           "int foo(int X1, int X2) { X2 = X1 + X1; }"


def test_clears_incompatible_loop():
    func = f(FOR_INVALID, 'main')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "int main(int x, int y, int z) { }"


def test_clears_invalid_loop_body():
    func = f(VAR_TESTS, 'invalid_body')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "void invalid_body(int x, int y) " \
           "{ for (int i = 0; i < x; i++) ; }"


def test_reports_nothing_on_full_cover(caplog):
    with caplog.at_level(logging.DEBUG):
        Coverage(f(INFINITE_2, 'foo')).report()
        assert not caplog.records


def test_reports_unsupported(caplog):
    with caplog.at_level(logging.DEBUG):
        Coverage(f(VAR_TESTS, 'arr')).report()
        assert len(caplog.records) == 3
        assert 'my_arrC[x][x]' in caplog.records[-1].message


def test_loop_compat_rejects_invalid_guard():
    compat, guard = Coverage.loop_compat(loop(f(FOR_INVALID, 'main')))
    assert guard is None
    assert not compat


def test_loop_compat_rejects_invalid_body():
    compat, guard = Coverage.loop_compat(loop(f(FOR_BODY, 'main')))
    assert guard is None
    assert not compat
