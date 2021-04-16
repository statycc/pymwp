# flake8: noqa: W605

from typing import Any, Optional, List
from functools import reduce

from polynomial import Polynomial
from monomial import Monomial
from semiring import ZERO_MWP, UNIT_MWP

_ZERO = Polynomial([Monomial(ZERO_MWP)])

_UNIT = Polynomial([Monomial(UNIT_MWP)])


def init_matrix(size: int, init_value: Optional[Any] = None) -> List[list]:
    """Create empty matrix of specified size.

    Example:

    ```python
    init_matrix(5)

    # generates:
    #
    # [[+o, +o, +o, +o, +o],
    #  [+o, +o, +o, +o, +o],
    #  [+o, +o, +o, +o, +o],
    #  [+o, +o, +o, +o, +o],
    #  [+o, +o, +o, +o, +o]]
    ```

    Arguments:
        size: matrix size
        init_value: value to place at each index. If not provided,
            will default to 0-polynomial.

    Returns:
        Initialized matrix.
    """
    value = init_value if init_value is not None else _ZERO
    return [[value for _ in range(size)] for _ in range(size)]


def identity_matrix(size: int) -> List[list]:
    """Create identity matrix of specified size.

    Example:

    ```python
    identity_matrix(5)

    # generates:
    #
    # [[+m, +o, +o, +o, +o],
    #  [+o, +m, +o, +o, +o],
    #  [+o, +o, +m, +o, +o],
    #  [+o, +o, +o, +m, +o],
    #  [+o, +o, +o, +o, +m]]
    ```

    Arguments:
        size: matrix size

    Returns:
        New identity matrix.
    """
    return [[_UNIT if i == j else _ZERO
             for j in range(size)] for i in range(size)]


def encode(matrix: List[List[Polynomial]]) -> List[List[List[dict]]]:
    """Convert matrix of polynomials to a matrix of dictionaries.

    Arguments:
        matrix: matrix to encode

    Raises:
        AttributeError: If the matrix does not contain polynomials
        calling this method will raise this exception.

    Returns:
        Encoded matrix.
    """
    return [[[mon.to_dict()
              for mon in polynomial.list]
             for polynomial in row]
            for (i, row) in enumerate(matrix)]


def decode(matrix: List[List[List[dict]]]) -> List[List[Polynomial]]:
    """Convert matrix of dictionaries to a matrix of polynomials.

    Arguments:
        matrix: matrix to decode

    Raises:
        TypeError: If the matrix value is not iterable
        AttributeError: If the matrix elements are not
            valid encoded polynomials.

    Returns:
        Decoded matrix of polynomials.
    """
    return [[
        Polynomial(monomials=[Monomial(
            scalar=monomial["scalar"],
            deltas=["deltas"])
            for monomial in polynomial])
        for polynomial in row]
        for (i, row) in enumerate(matrix)]


def matrix_sum(matrix1: List[List[Any]], matrix2: List[List[Any]]) -> List[List[Any]]:
    """Compute the sum of two matrices.

    Arguments:
        matrix1: first matrix.
        matrix2: second matrix.

    Returns:
        new matrix that represents the sum of the two inputs.
    """

    return [[matrix1[i][j] + matrix2[i][j]
             for j in range(len(matrix1))]
            for i in range(len(matrix1))]


def matrix_prod(matrix1: List[List[Polynomial]],
                matrix2: List[List[Polynomial]]) -> List[List[Polynomial]]:
    """Compute the product of two polynomial matrices.

    Arguments:
        matrix1: first polynomial matrix.
        matrix2: second polynomial matrix.

    Returns:
        new matrix that represents the product of the two inputs.
    """

    return [[

        reduce(lambda total, k:
               total + matrix1[i][k] * matrix2[k][j],
               range(len(matrix1)), _ZERO)

        for j in range(len(matrix2))]
        for i in range(len(matrix1))]


def resize(matrix: List[List[Polynomial]], new_size: int) -> List[List[Polynomial]]:
    """Create a new matrix of polynomials of specified size.

    The resized matrix is initialized as an identity matrix
    then filled with values from the original matrix.

    Arguments:
        matrix: original matrix
        new_size: width/height of new matrix

    Returns:
        New matrix of specified size, filled with values from
            the original matrix.
    """

    res = identity_matrix(new_size)
    bound = min(new_size, len(matrix))

    for i in range(bound):
        for j in range(bound):
            res[i][j] = matrix[i][j]
    return res
