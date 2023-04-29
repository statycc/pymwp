from pymwp import Monomial
from pymwp.constants import SetInclusion

"""Unit test Monomial class methods."""


def test_create_monomial_without_deltas():
    mono = Monomial('o', [])
    assert mono.scalar == 'o'
    assert mono.deltas == []


def test_create_monomial_with_duplicated_deltas():
    mono = Monomial('m', [(0, 0), (0, 0), (0, 0)])
    assert mono.scalar == 'm'
    assert mono.deltas == [(0, 0)]


def test_create_monomial_with_invalid_deltas():
    mono = Monomial('m', [(0, 2), (1, 2), (1, 1), (0, 0)])
    assert mono.scalar == 'o'
    assert mono.deltas == []


def test_monomial_decl_equivalence():
    mono1 = Monomial('m', [(0, 0), (2, 1), (1, 2)])
    mono2 = Monomial('m', (0, 0), (2, 1), (1, 2))
    assert mono1.scalar == mono2.scalar
    assert mono1.deltas == mono2.deltas


def test_monomial_product_non_empty():
    a = Monomial('m', [(0, 0)])
    b = Monomial('m', [(0, 0), (1, 1)])
    p = a * b
    assert p.scalar == 'm'
    assert p.deltas == [(0, 0), (1, 1)]


def test_monomial_product_empty_arg():
    a = Monomial('m', [(0, 0)])
    b = Monomial('o', [])
    p = a * b
    assert p.scalar == 'o'
    assert p.deltas == []


def test_monomial_product_empty_self():
    a = Monomial('o', [])
    b = Monomial('m', [(0, 0)])
    p = a * b
    assert p.scalar == 'o'
    assert p.deltas == []


def test_monomial_copy():
    m = Monomial('m', [(0, 0), (1, 1)])
    n = m.copy()
    assert m.scalar == n.scalar  # same scalar
    assert m.deltas == n.deltas  # same deltas
    assert m is not n  # different reference


def test_valid_insert_to_empty():
    deltas = []
    delta = (0, 0)
    deltas = Monomial.insert_delta(deltas, delta)
    assert delta in deltas
    assert deltas == [(0, 0)]


def test_valid_insert_to_nonempty():
    deltas = [(0, 0), (1, 1), (2, 2)]
    delta = (1, 3)
    deltas = Monomial.insert_delta(deltas, delta)
    assert delta in deltas
    assert deltas == [(0, 0), (1, 1), (2, 2), (1, 3)]


def test_insert_ignores_duplicate():
    deltas = [(0, 0), (1, 1), (2, 2)]
    delta = (0, 0)
    deltas = Monomial.insert_delta(deltas, delta)
    assert deltas == [(0, 0), (1, 1), (2, 2)]


def test_insert_return_empty_on_conflict():
    deltas = [(0, 0), (1, 1), (2, 2)]
    delta = (0, 1)
    deltas = Monomial.insert_delta(deltas, delta)
    assert deltas == []


def test_contains_true():
    deltas1 = [(0, 0), (1, 1), (2, 2)]
    deltas2 = [(0, 0), (1, 1), (2, 2)]
    m1 = Monomial('m', deltas1)
    m2 = Monomial('m', deltas2)
    assert m1.contains(m2)
    assert m2.contains(m1)


def test_contains_true_2():
    deltas1 = [(0, 0), (2, 2)]
    deltas2 = [(0, 0), (1, 1), (2, 2)]
    m1 = Monomial('m', deltas1)
    m2 = Monomial('m', deltas2)
    assert m2.contains(m1)
    assert not m1.contains(m2)


def test_inclusion_1():
    deltas1 = [(0, 0), (2, 2)]
    deltas2 = [(0, 0), (1, 1), (2, 2)]
    m1 = Monomial('m', deltas1)
    m2 = Monomial('m', deltas2)
    assert m2.inclusion(m1) == SetInclusion.CONTAINS
    assert m1.inclusion(m2) == SetInclusion.INCLUDED


def test_inclusion_2():
    deltas1 = [(0, 0), (2, 2), (3, 3)]
    deltas2 = [(0, 0), (1, 1), (2, 2)]
    m1 = Monomial('m', deltas1)
    m2 = Monomial('m', deltas2)
    assert m2.inclusion(m1) == SetInclusion.EMPTY
    assert m1.inclusion(m2) == SetInclusion.EMPTY


def test_inclusion_3():
    deltas1 = [(0, 0), (2, 2)]
    deltas2 = [(0, 0), (1, 1), (2, 2)]
    m1 = Monomial('w', deltas1)
    m2 = Monomial('m', deltas2)
    assert m1.inclusion(m2) == SetInclusion.INCLUDED
    assert m2.inclusion(m1) == SetInclusion.CONTAINS


def test_inclusion_4():
    deltas1 = [(0, 0), (2, 2)]
    deltas2 = [(0, 0), (1, 1), (2, 2)]
    m1 = Monomial('m', deltas1)
    m2 = Monomial('w', deltas2)
    assert m2.inclusion(m1) == SetInclusion.EMPTY
    assert m1.inclusion(m2) == SetInclusion.EMPTY
