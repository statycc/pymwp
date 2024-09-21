from pymwp import Coverage, Parser as pr
from .mocks.ast_mocks import *
from copy import deepcopy


def nth_func(ast, name):
    return deepcopy([f for f in ast if pr.is_func(f)
                     and f.decl.name == name][0])


def test_full_cover_remains_unchanged():
    func = nth_func(SINGLE_LINK_CLUSTER, 'SingleLinkCluster')
    before = deepcopy(func)
    cover = Coverage(func)
    assert cover.full
    after = cover.ast_mod().node
    assert str(before) == str(after)


def test_removes_function_call():
    func = nth_func(FUNCTION_CALL, 'foo')
    cover = Coverage(func)
    assert not cover.full
    after = cover.ast_mod().node
    assert Coverage(after).full
    assert pr.to_c(after, compact=True).strip() == \
           "int foo(int X1, int X2) { X2 = X1 + X1; }"


def test_assert_and_assume_are_ok():
    before = nth_func(VERIFICATION, 'main')
    cover = Coverage(deepcopy(before))
    assert cover.full
