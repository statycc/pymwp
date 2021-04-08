from pymwp.polynomial import Polynomial, Comparison


def test_compare_empty_first_list():
    m1 = []
    m2 = [(0, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_empty_second_list():
    m1 = [(0, 0)]
    m2 = []
    assert Polynomial.compare(m1, m2) == Comparison.LARGER


def test_compare_two_empty_lists():
    m1 = []
    m2 = []
    assert Polynomial.compare(m1, m2) == Comparison.EQUAL


def test_compare_equals_same_length():
    m1 = [(0, 0), (1, 1), (0, 2)]
    m2 = [(0, 0), (1, 1), (0, 2)]
    assert Polynomial.compare(m1, m2) == Comparison.EQUAL


def test_compare_equals_first_list_shorter():
    m1 = [(0, 1)]
    m2 = [(0, 1), (1, 2)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_equals_first_list_longer():
    m1 = [(0, 1), (1, 2)]
    m2 = [(0, 1)]
    assert Polynomial.compare(m1, m2) == Comparison.LARGER


def test_compare_diff_i_less_than_m():
    m1 = [(0, 0)]
    m2 = [(1, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_diff_i_greater_than_m():
    m1 = [(1, 0)]
    m2 = [(0, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.LARGER


def test_compare_diff_j_less_than_n():
    m1 = [(0, 0)]
    m2 = [(0, 1)]
    assert Polynomial.compare(m1, m2) == Comparison.SMALLER


def test_compare_diff_j_greater_than_n():
    m1 = [(0, 1)]
    m2 = [(0, 0)]
    assert Polynomial.compare(m1, m2) == Comparison.LARGER
