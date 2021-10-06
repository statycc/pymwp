from pymwp.semiring import ZERO_MWP
from pymwp import Polynomial, Monomial


def test_polynomial_copy():
    """Copying a polynomial returns different reference but of identical
    content."""
    p = Polynomial([Monomial('m', [(0, 0), (1, 1)])])
    poly_copy = p.copy()

    assert poly_copy == p  # their data is identical
    assert poly_copy is not p  # different reference


def test_polynomial_times_empty():
    """Multiplying two polynomials where one is 0-monomial, results in 0."""
    z = Polynomial(ZERO_MWP)
    p = Polynomial([Monomial('m', [(0, 0), (1, 1)])])

    assert (p * z) == Polynomial(ZERO_MWP)


def test_contains_filter():
    """Contains correctly identifies when a monomial is contained by
    another."""
    m1 = Monomial('m', [(0, 0), (0, 1)])
    m2 = Monomial('w', [(0, 1), (1, 2)])
    m3 = Monomial('p', [(0, 2), (1, 3), (2, 4)])
    new_list = [m1, m2, m3]
    new_list2 = [m1, m2, m3]
    m0 = Monomial('p', [(0, 1)])
    m0_ = Monomial('m', [(0, 1), (1, 2), (1, 3)])

    assert Polynomial.inclusion(new_list, m0, 1) == (True, 0)
    assert new_list == [m3]
    assert Polynomial.inclusion(new_list2, m0_, 1) == (False, 1)


def test_polynomial_add_by_non_empty():
    """Adding two polynomials with monomials with deltas, returns expected
    result."""
    mono1 = Monomial('m', [(2, 2)])
    mono2 = Monomial('m', [(0, 0), (1, 1)])
    m = Polynomial([mono1])
    p = Polynomial([mono2])
    c = p + m
    expected = Polynomial(
        [Monomial('m', [(0, 0), (1, 1)]), Monomial('m', [(2, 2)])])

    assert c == expected


def test_polynomial_add_simpl():
    """Result of polynomial add is simplified."""
    mono1 = Monomial('m', [(0, 1), (0, 2), (0, 3)])
    mono2 = Monomial('w', [(0, 2), (0, 3), (0, 4)])
    mono3 = Monomial('p', [(0, 2), (0, 3), (0, 5)])
    m = Polynomial(Polynomial.sort_monomials([mono1, mono2, mono3]))
    print(m)
    mono0 = Monomial('w', [(0, 2), (0, 3)])
    p = Polynomial([mono0])
    c = p.add(m)
    expected = Polynomial([mono0, mono3])

    assert c == expected


def test_polynomial_times_by_non_empty():
    """Multiplying two polynomials with monomials with deltas gives expected
     result."""
    p1 = Polynomial([Monomial('m', [(2, 2)])])
    p2 = Polynomial([Monomial('m', [(0, 0), (1, 1)])])
    expected = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])

    assert (p1 * p2) == expected

def test_polynomial_times_by_non_empty2():
    mono1 = Monomial('m', [(2, 2)])
    mono12 = Monomial('m', [(1, 1)])
    mono2 = Monomial('m', [(0, 0)])
    mono22 = Monomial('m', [(3, 3)])
    m = Polynomial([mono1,mono12])
    p = Polynomial([mono2,mono22])
    c = p * m
    expected = Polynomial([
        Monomial('m', [(0, 0), (1, 1)]),
        Monomial('m', [(0, 0), (2, 2)]),
        Monomial('m', [(1, 1), (3, 3)]),
        Monomial('m', [(2, 2), (3, 3)])])
    try:
        assert c == expected
    except AssertionError:
        print("expected:")
        print(expected)
        print("prod:")
        print(c)
        raise

def test_polynomial_equals_empty_are_equal():
    """Two default polynomials are equal."""
    p1 = Polynomial()
    p2 = Polynomial()
    assert p1.equal(p2) is True


def test_polynomial_equals_same_returns_true():
    """equal returns true when two polynomials are the same."""
    p1 = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])
    p2 = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])
    assert p1.equal(p2) is True


def test_polynomial_equals_different_returns_false():
    """equal returns false when two polynomials are different."""
    p1 = Polynomial([Monomial('m', [(0, 0), (1, 1), (2, 2)])])
    p2 = Polynomial([Monomial('m', [(1, 1), (3, 3)])])

    assert p1.equal(p2) is False


def test_polynomial_sort_1():
    """Sorting monomials with deltas gives expected order."""
    m1 = Monomial('m', [(0, 1), (1, 6)])
    m2 = Monomial('m', [(2, 4), (1, 5)])
    m3 = Monomial('m', [(0, 1), (1, 2), (1, 9)])
    [m1, m2, m3] = Polynomial.sort_monomials([m1, m2, m3])

    assert m1.deltas == [(0, 1), (1, 2), (1, 9)]
    assert m2.deltas == [(0, 1), (1, 6)]
    assert m3.deltas == [(2, 4), (1, 5)]


def test_polynomial_sort_2():
    """Sorting monomials with duplicate deltas returns expected order."""
    sorted_mono = Polynomial.sort_monomials(
        [Monomial('m', [(1, 4)]),
         Monomial('m', [(1, 1), (1, 2)]),
         Monomial('w', [(1, 1), (1, 2)]),
         Monomial('p', [(1, 1), (1, 2)]),
         Monomial('w')])
    [m0, m1, m2] = sorted_mono

    assert len(sorted_mono) == 3
    assert m0.scalar == 'w' and m0.deltas == []
    assert m1.scalar == 'p' and m1.deltas == [(1, 1), (1, 2)]
    assert m2.scalar == 'm' and m2.deltas == [(1, 4)]


def test_polynomial_remove_zeros_with_deltas():
    """Adding two polynomials where one contains 0-monomial and another
    contains non-0 monomial -AND- some deltas, after addition, only the
    non-zero monomial remains in the result.

    see: https://github.com/statycc/pymwp/issues/16
    """
    zero = Polynomial([Monomial('o')])
    poly = Polynomial([Monomial('m', [(0, 0), (1, 1)])])
    after_add = zero + poly

    assert len(after_add.list) == 1
    assert 'm' == after_add.list[0].scalar


def test_polynomial_remove_zeros_no_deltas():
    """Adding two polynomials where one contains 0-monomial and another
    contains non-0 monomial without deltas, after addition, only the
    non-zero monomial remains in the result."""
    zero = Polynomial([Monomial('o')])
    poly = Polynomial([Monomial('w')])
    after_add = zero + poly

    assert len(after_add.list) == 1
    assert 'w' == after_add.list[0].scalar


def test_polynomial_remove_zeros_empty():
    """For a polynomial that contains only 0-monomials, only one 0-monomial
    remains after removing zeros."""
    poly = Polynomial([Monomial('o'), Monomial('o'), Monomial('o')])
    poly.remove_zeros()

    assert len(poly.list) == 1
    assert poly.list[0].scalar == 'o'


def test_polynomial_init_shorthand_syntax():
    """Shorthand syntax gives equivalent polynomial as the longer syntax."""
    assert Polynomial('m') == Polynomial([Monomial('m')])
    assert Polynomial('w') == Polynomial([Monomial('w')])
    assert Polynomial('p') == Polynomial([Monomial('p')])
