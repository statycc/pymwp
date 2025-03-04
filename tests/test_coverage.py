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
           "void invalid_body(int x, int y) { }"

def test_clears_invalid_while_body():
    func = f(VAR_TESTS, 'invalid_body2')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           ("void invalid_body2(int x, int i, int k) { int i; int j; int k; "
            "if (((0 <= n) && (0 <= m)) && (0 <= N)) { i = 0; "
            "while ((nondet() > 0) && (i < n)) { j = 0; "
            "while ((nondet() > 0) && (j < m)) { k = i; i = k; } ++i; } } }")

def test_clears_partially_invalid_loop_body():
    func = f(VAR_TESTS, 'partially_invalid_body')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "void partially_invalid_body(int x, int y) " \
           "{ for (int i = 0; i < x; i++) { y = y + 1; } }"


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


def test_if_true_branch_invalid():
    after = Coverage(f(IF_INVALID_TESTS, 'invalid_true')).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "void invalid_true(int x, int y, int z) " \
           "{ if (true) ; else w = z + 1; }"


def test_if_true_branch_partly_invalid():
    func = f(IF_INVALID_TESTS, 'partially_invalid_true')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "void partially_invalid_true(int x, int y, int z) { " \
           "if (true) { y = x + y; } else w = z + 1; }"


def test_if_else_branch_invalid():
    func = f(IF_INVALID_TESTS, 'invalid_else')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "void invalid_else(int x, int y, int z) { " \
           "if (true) x = x + 1; else ; }"


def test_if_else_branch_partly_invalid():
    func = f(IF_INVALID_TESTS, 'partially_invalid_else')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "void partially_invalid_else(int x, int y, int z) { " \
           "if (true) x = x + 1; else { z = z + 1; } }"


def test_if_both_branches_invalid():
    func = f(IF_INVALID_TESTS, 'invalid_branches')
    after = Coverage(func).ast_mod().node
    assert pr.to_c(after, compact=True).strip() == \
           "void invalid_branches(int x, int y, int z)" \
           " { if (true) ; else ; }"
