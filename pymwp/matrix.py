# flake8: noqa: W605

import logging
from functools import reduce
from typing import Any, Optional, List

from .polynomial import Polynomial
from .monomial import Monomial
from .semiring import ZERO_MWP, UNIT_MWP

ZERO = Polynomial(ZERO_MWP)

UNIT = Polynomial(UNIT_MWP)

logger = logging.getLogger(__name__)


def init_matrix(size: int, init_value: Optional[Any] = None) -> List[list]:
    """Create empty matrix of specified size.

    Example:

    Generate 5 x 5 size zero-matrix

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
    value = init_value if init_value is not None else ZERO
    return [[value for _ in range(size)] for _ in range(size)]


def identity_matrix(size: int) -> List[list]:
    """Create identity matrix of specified size.

    Example:

    Generate 5 x 5 size identity matrix:

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
    return [[UNIT if i == j else ZERO
             for j in range(size)] for i in range(size)]


def encode(matrix: List[List[Polynomial]]) -> List[List[List[dict]]]:
    """Converts a matrix of polynomials to a matrix of dictionaries.

    This function is useful when preparing to write a matrix of polynomials to
    a file. The same matrix can later be restored using matrix
    [decode](matrix.md#pymwp.matrix.decode).

    Arguments:
        matrix: matrix to encode

    Raises:
        AttributeError: If the matrix does not contain polynomials.

    Returns:
        Encoded matrix.
    """
    return [[
        [mono.to_dict() for mono in polynomial.list]
        for polynomial in row]
        for (i, row) in enumerate(matrix)]


def decode(matrix: List[List[List[dict]]]) -> List[List[Polynomial]]:
    """Converts matrix of dictionaries to a matrix of polynomials.

    Primary use case of this function is for restoring a matrix of
     polynomials from a file (assuming [encode](matrix.md#pymwp.matrix.encode)
     was used to generate that file).

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
        Polynomial(*[Monomial(
            scalar=monomial["scalar"],
            deltas=monomial["deltas"])
            for monomial in polynomial])
        for polynomial in row]
        for (i, row) in enumerate(matrix)]


def matrix_sum(
        matrix1: List[List[Any]], matrix2: List[List[Any]]
) -> List[List[Any]]:
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


def matrix_prod(
        matrix1: List[List[Polynomial]], matrix2: List[List[Polynomial]]
) -> List[List[Polynomial]]:
    """Compute the product of two polynomial matrices.

    Arguments:
        matrix1: first polynomial matrix.
        matrix2: second polynomial matrix.

    Returns:
        new matrix that represents the product of the two inputs.
    """

    return [[

        reduce(lambda total, k:
               total + (matrix1[i][k] * matrix2[k][j]),
               range(len(matrix1)), ZERO)

        for j in range(len(matrix2))]
        for i in range(len(matrix1))]


def resize(matrix: List[List[Polynomial]], new_size: int) \
        -> List[List[Polynomial]]:
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


def show(matrix: List[List[Any]], **kwargs) -> None:
    """Pretty print a matrix at the screen.

    Using the keyword arguments it is possible display additional text
    before or after the matrix.

    Example:

    Display matrix only:

    ```python
    my_matrix = identity_matrix(3)
    show(my_matrix)

    # displays:
    #
    # ['  +m', '  +o', '  +o']
    # ['  +o', '  +m', '  +o']
    # ['  +o', '  +o', '  +m']
    ```

    Display matrix and some extra text before it

    ```python
    my_matrix = identity_matrix(3)
    header = '|   x1   |   x2  |  x3 |'
    show(my_matrix, prefix=header)

    # displays:
    #
    # |   x1   |   x2  |  x3 |
    # ['  +m', '  +o', '  +o']
    # ['  +o', '  +m', '  +o']
    # ['  +o', '  +o', '  +m']
    ```

    Arguments:
        matrix: the matrix to display.

    Kwargs:

    - `prefix` (`str`): display some text before displaying matrix
    - `postfix` (`str`): display some text after displaying matrix

    Raises:
        TypeError: If the matrix is not iterable (type list of lists)
    """
    if 'prefix' in kwargs:
        print(kwargs['prefix'])
    for row in matrix:
        print([str(r) for r in row])
    if 'postfix' in kwargs:
        print(kwargs['postfix'])
    print(' ')


def equals(matrix1: List[List[Any]], matrix2: List[List[Any]]) -> bool:
    """Determine if two matrices are equal.

    This function performs element-wise equality comparisons on values of
    two matrices. The two matrices must be the same size. For any two matrices
    of different size the result is always `False`.

    This function can evaluate values that are comparable by equals `==`
    operator.

    Arguments:
        matrix1: first matrix.
        matrix2: second matrix.

    Raises:
        TypeError: If the matrix value is not iterable

    Returns:
        `True` if matrices are equal element-wise and `False` otherwise.
    """
    # equal size
    if [len(row) for row in matrix1] != [len(row) for row in matrix2]:
        return False

    # element-wise comparison
    for row_index, column in enumerate(matrix1):
        for col_index, value in enumerate(column):
            if matrix2[row_index][col_index] != value:
                return False

    return True


def fixpoint(matrix: List[List[Any]]) -> List[List[Any]]:
    """Computes the star operation $1 + M + M^2 + M^3 + …$

    This function assumes provided input is a square matrix.

    Arguments:
        matrix: for which to compute fixpoint

    Returns:
        $M^*$
    """
    _1_ = identity_matrix(len(matrix))
    previous = matrix
    next_matrix = matrix
    result = matrix_sum(_1_, matrix)

    while not equals(previous, result):
        previous = result
        next_matrix = matrix_prod(next_matrix, matrix)  # M^2, M^3, M^4....
        result = matrix_sum(result, next_matrix)

    return result
