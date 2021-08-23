from pymwp.polynomial import Polynomial, Comparison

"""Unit tests for Polynomial.compare method"""


def test_compare_empty_list_is_smaller_than_nonempty():
    m1 = []
    m2 = [(0, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_nonempty_list_is_larger_than_empty():
    m1 = [(0, 0)]
    m2 = []
    assert Polynomial.compare(m1, m2) == Comparison.LARGER


def test_compare_two_empty_lists_are_equal():
    m1 = []
    m2 = []
    assert Polynomial.compare(m1, m2) == Comparison.EQUAL


def test_compare_same_deltas_of_same_length_are_equal():
    m1 = [(0, 0), (1, 1), (0, 2)]
    m2 = [(0, 0), (1, 1), (0, 2)]
    assert Polynomial.compare(m1, m2) == Comparison.EQUAL


def test_compare_equals_shorter_list_is_smaller():
    m1 = [(0, 1)]
    m2 = [(0, 1), (1, 2)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_equals_longer_list_is_larger():
    m1 = [(0, 1), (1, 2)]
    m2 = [(0, 1)]
    assert Polynomial.compare(m1, m2) == Comparison.LARGER


def test_compare_diff_smaller_when_i_less_than_m():
    m1 = [(0, 0)]
    m2 = [(1, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_diff_larger_when_i_greater_than_m():
    m1 = [(1, 0)]
    m2 = [(0, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.LARGER


def test_compare_diff_smaller_when_j_less_than_n():
    m1 = [(0, 0)]
    m2 = [(0, 1)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_diff_larger_when_j_greater_than_n():
    m1 = [(0, 1)]
    m2 = [(0, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.LARGER
