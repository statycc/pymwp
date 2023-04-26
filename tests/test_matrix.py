import builtins

from pymwp.matrix import init_matrix, identity_matrix, encode, decode, \
    matrix_sum, matrix_prod, resize, equals, fixpoint, show
from pymwp.matrix import ZERO as o, UNIT as m
from pymwp import Monomial, Polynomial


def test_init_matrix_creates_zero_matrix():
    """Creates matrix of 0s everywhere."""
    matrix = init_matrix(2)

    assert matrix[0][0] == o
    assert matrix[1][0] == o
    assert matrix[0][1] == o
    assert matrix[1][1] == o


def test_identity_matrix_creates_expected_matrix():
    """m at diagonal and 0 everywhere else."""
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
    """Resizing matrix changes matrix size correctly, it preserves the
    polynomials from the input matrix, and when enlarging, the newly added
    positions are filled with identity matrix values."""
    poly = Polynomial(Monomial('m'))
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
    """Matrix sum should add two matrices element-wise."""
    expected = Polynomial(Monomial('m', [(0, 0)]), Monomial('w', [(1, 1)]))

    mat_a = init_matrix(2, Polynomial(Monomial('m', (0, 0))))
    mat_b = init_matrix(2, Polynomial(Monomial('w', (1, 1))))
    result = matrix_sum(mat_a, mat_b)

    assert result[0][0] == expected
    assert result[0][1] == expected
    assert result[1][0] == expected
    assert result[1][1] == expected


def test_matrix_prod():
    """Matrix product test -- here we check using an elaborate test case
    that the product is what it should be, at each position."""
    p1 = Polynomial(Monomial('p', [(0, 1)]), Monomial('w', [(1, 1)]))
    p2 = Polynomial(Monomial('m', [(0, 1)]), Monomial('w', [(1, 1)]))
    p3 = Polynomial(Monomial('m', [(0, 2)]), Monomial('w', [(1, 2)]))
    p4 = Polynomial(Monomial('p', [(0, 2)]), Monomial('w', [(1, 2)]))

    #          m p3 o
    #          o m  o
    #          o p4 m
    # m o p1
    # o m p2
    # o o o
    mat_a = [[m, o, p1], [o, m, p2], [o, o, o]]
    mat_b = [[m, p3, o], [o, m, o], [o, p4, m]]
    result = matrix_prod(mat_a, mat_b)

    try:
        assert result[0][0] == (m * m) + (o * o) + (p1 * o)
        assert result[0][1] == (m * p3) + (o * m) + (p1 * p4)
        assert result[0][2] == (m * o) + (o * o) + (p1 * m)

        assert result[1][0] == (o * m) + (m * o) + (p2 * o)
        assert result[1][1] == (o * p3) + (m * m) + (p2 * p4)
        assert result[1][2] == (o * o) + (m * o) + (p2 * m)

        assert result[2][0] == (o * m) + (o * o) + (o * o)
        assert result[2][1] == (o * p3) + (o * m) + (o * p4)
        assert result[2][2] == (o * o) + (o * o) + (o * m)
    except AssertionError:
        print(result[0][1])
        print("Should be :")
        print((m * p3) + (o * m) + (p1 * p4))
        raise


def test_encode():
    """Encoding converts matrix of polynomials to a list of dictionaries."""
    p = Polynomial(Monomial('m', [(0, 1)]))
    mat = init_matrix(2, p)
    encoded = encode(mat)
    expected = [
        [[{'scalar': 'm', 'deltas': [(0, 1)]}],
         [{'scalar': 'm', 'deltas': [(0, 1)]}]],
        [[{'scalar': 'm', 'deltas': [(0, 1)]}],
         [{'scalar': 'm', 'deltas': [(0, 1)]}]]
    ]

    assert encoded == expected


def test_decode():
    """Decode converts dictionary object to matrix of polynomials."""
    sample = [
        [[{'scalar': 'm', 'deltas': [(0, 1)]}],
         [{'scalar': 'm', 'deltas': [(0, 1)]}]],
        [[{'scalar': 'm', 'deltas': [(0, 1)]}],
         [{'scalar': 'm', 'deltas': [(0, 1)]}]]
    ]

    decoded = decode(sample)
    expected = init_matrix(2, Polynomial(Monomial('m', (0, 1))))

    assert decoded == expected


def test_matrix_equals():
    """Two polynomial matrices are equal when their monomials match exactly."""
    p1 = Polynomial(Monomial('m', [(0, 1), (1, 1)]))
    p2 = Polynomial(Monomial('m', [(0, 1), (1, 1)]))
    p3 = Polynomial(Monomial('m', [(0, 0)]))
    p4 = Polynomial(Monomial('m', [(0, 0)]))
    p5 = Polynomial(Monomial('m', [(1, 1), (2, 2)]))
    p6 = Polynomial(Monomial('m', [(1, 1), (2, 2)]))

    m1 = [[o, p1, o], [p3, o, o], [o, o, p5]]
    m2 = [[o, p2, o], [p4, o, o], [o, o, p6]]

    assert equals(m1, m2) is True


def test_matrix_not_equals():
    """Two matrices where monomials differ by deltas are not equal."""
    p1 = Polynomial(Monomial('m', [(0, 1)]))
    p2 = Polynomial(Monomial('m', [(1, 1)]))
    m1 = [[o, o, o], [o, o, o], [o, o, p1]]
    m2 = [[o, o, o], [o, o, o], [o, o, p2]]

    assert equals(m1, m2) is False


def test_matrix_size_not_equals():
    """Two matrices of different size are not equal."""
    m1 = [[o, o, o], [o, o, o], [o, o, o]]
    m2 = [[o, o], [o, o]]

    assert equals(m1, m2) is False


def test_fixpoint():
    """M^* of zero matrix is identity matrix."""
    before = [[o, o, o], [o, o, o], [o, o, o]]
    after = fixpoint(before)

    assert after[0][0] == m
    assert after[0][1] == o
    assert after[0][2] == o
    assert after[1][0] == o
    assert after[1][1] == m
    assert after[1][2] == o
    assert after[2][0] == o
    assert after[2][1] == o
    assert after[2][2] == m


def test_show(mocker):
    """Matrix show calls print for N times, where N is number of rows
    to display each row."""
    my_matrix = [[o, o, o], [o, o, o], [o, o, o]]
    mocker.patch('builtins.print')
    show(my_matrix)
    expected = 4  # print each row and new line
    assert builtins.print.call_count == expected


def test_show_with_extras(mocker):
    """Matrix show calls print per each row, and 2 more times to print
    header and footer when those arguments are provided."""
    my_matrix = [[o, o, o], [o, o, o], [o, o, o]]
    mocker.patch('builtins.print')
    show(my_matrix, prefix="foo", postfix="bar")
    assert builtins.print.call_count == 6
