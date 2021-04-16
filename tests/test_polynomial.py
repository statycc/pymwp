from semiring import ZERO_MWP
from pymwp.polynomial import Polynomial
from pymwp.monomial import Monomial


def test_polynomial_copy():
    p = Polynomial([Monomial('m', [(0, 0), (1, 1)])])
    poly_copy = p.copy()
    # their data is identical
    assert poly_copy == p
    # different reference
    assert poly_copy is not p


def test_polynomial_times_empty():
    z = Polynomial([Monomial(ZERO_MWP, [])])
    p = Polynomial([Monomial('m', [(0, 0), (1, 1)])])
    c = p * z
    assert c == Polynomial()


def test_polynomial_times_by_non_empty():
    mono1 = Monomial('m', [(2, 2)])
    mono2 = Monomial('m', [(0, 0), (1, 1)])
    m = Polynomial([mono1])
    p = Polynomial([mono2])
    c = p * m
    expected = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])
    assert c == expected


def test_polynomial_equals_empty_are_equal():
    p1 = Polynomial()
    p2 = Polynomial()
    assert p1.equal(p2) is True


def test_polynomial_equals_same_returns_true():
    p1 = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])
    p2 = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])
    assert p1.equal(p2) is True


def test_polynomial_equals_different_returns_false():
    p1 = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])
    p2 = Polynomial([Monomial('m', [(1, 1), (3, 3)])])
    assert p1.equal(p2) is False


def test_polynomial_sort_1():
    m1 = Monomial('m', [(0, 1), (1, 6)])
    m2 = Monomial('m', [(2, 4), (1, 5)])
    m3 = Monomial('m', [(0, 1), (1, 2), (1, 9)])
    p = Polynomial.sort_monomials([m1, m2, m3])
    assert p[0].deltas == [(0, 1), (1, 2), (1, 9)]
    assert p[1].deltas == [(0, 1), (1, 6)]
    assert p[2].deltas == [(2, 4), (1, 5)]


def test_polynomial_sort_2():
    monomials = [Monomial('m', [(1, 4)]),
                 Monomial('m', [(1, 2), (1, 3)]),
                 Monomial('m', [(1, 1), (1, 2)]),
                 Monomial()]
    p = Polynomial.sort_monomials(monomials)
    assert p[0].deltas == []
    assert p[1].deltas == [(1, 1), (1, 2)]
    assert p[2].deltas == [(1, 2), (1, 3)]
    assert p[3].deltas == [(1, 4)]
