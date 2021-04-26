from matrix import init_matrix, identity_matrix, encode, decode, matrix_sum, matrix_prod, resize
from matrix import ZERO as o, UNIT as m
from monomial import Monomial
from polynomial import Polynomial


def test_init_matrix_creates_zero_matrix():
    matrix = init_matrix(2)

    assert matrix[0][0] == o
    assert matrix[1][0] == o
    assert matrix[0][1] == o
    assert matrix[1][1] == o


def test_identity_matrix_creates_expected_matrix():
    matrix = identity_matrix(3)

    assert matrix[0][0] == m
    assert matrix[0][1] == o
    assert matrix[0][2] == o
    assert matrix[1][0] == o
    assert matrix[1][1] == m
    assert matrix[1][2] == o
    assert matrix[2][0] == o
    assert matrix[2][1] == o
    assert matrix[2][2] == m


def test_resize_modifies_matrix_size():
    poly = Polynomial([Monomial('m')])
    before_resize = init_matrix(2, poly)
    after_resize = resize(before_resize, 5)

    # correctly changes matrix dimensions
    assert len(before_resize) == len(before_resize[0]) == 2
    assert len(after_resize) == len(after_resize[0]) == 5

    # copies content
    assert after_resize[0][0] == poly
    assert after_resize[0][1] == poly
    assert after_resize[1][0] == poly
    assert after_resize[1][1] == poly
    assert after_resize[0][2] == o
    assert after_resize[0][3] == o
    assert after_resize[0][4] == o
    assert after_resize[2][2] == m
    assert after_resize[3][3] == m
    assert after_resize[4][4] == m


def test_matrix_sum():
    expected = Polynomial([Monomial('m', [(0, 0)]), Monomial('w', [(1, 1)])])

    mat_a = init_matrix(2, Polynomial([Monomial('m', [(0, 0)])]))
    mat_b = init_matrix(2, Polynomial([Monomial('w', [(1, 1)])]))
    result = matrix_sum(mat_a, mat_b)

    assert result[0][0] == expected
    assert result[0][1] == expected
    assert result[1][0] == expected
    assert result[1][1] == expected


def test_matrix_prod():
    p1 = Polynomial([Monomial('p', [(0, 1)]), Monomial('w', [(1, 1)])])
    p2 = Polynomial([Monomial('m', [(0, 1)]), Monomial('w', [(1, 1)])])
    p3 = Polynomial([Monomial('m', [(0, 2)]), Monomial('w', [(1, 2)])])
    p4 = Polynomial([Monomial('p', [(0, 2)]), Monomial('w', [(1, 2)])])

    mat_a = [[m, o, p1], [o, m, p2], [o, o, o]]
    mat_b = [[m, p3, o], [o, m, o], [o, p4, m]]
    result = matrix_prod(mat_a, mat_b)

    assert result[0][0] == (m * m) + (o * o) + (p1 * o)
    assert result[0][1] == (m * p3) + (o * m) + (p1 * p4)
    assert result[0][2] == (m * o) + (o * o) + (p1 * m)

    assert result[1][0] == (o * m) + (m * o) + (p2 * o)
    assert result[1][1] == (o * p3) + (m * m) + (p2 * p4)
    assert result[1][2] == (o * o) + (m * o) + (p2 * m)

    assert result[2][0] == (o * m) + (o * o) + (o * o)
    assert result[2][1] == (o * p3) + (o * m) + (o * p4)
    assert result[2][2] == (o * o) + (o * o) + (o * m)


def test_encode():
    p = Polynomial([Monomial('m', [(0, 1)])])
    mat = init_matrix(2, p)
    encoded = encode(mat)
    expected = [
        [[{'scalar': 'm', 'deltas': [(0, 1)]}], [{'scalar': 'm', 'deltas': [(0, 1)]}]],
        [[{'scalar': 'm', 'deltas': [(0, 1)]}], [{'scalar': 'm', 'deltas': [(0, 1)]}]]
    ]

    assert encoded == expected


def test_decode():
    sample = [
        [[{'scalar': 'm', 'deltas': [(0, 1)]}], [{'scalar': 'm', 'deltas': [(0, 1)]}]],
        [[{'scalar': 'm', 'deltas': [(0, 1)]}], [{'scalar': 'm', 'deltas': [(0, 1)]}]]
    ]

    decoded = decode(sample)
    expected = init_matrix(2, Polynomial([Monomial('m', [(0, 1)])]))

    assert decoded == expected
