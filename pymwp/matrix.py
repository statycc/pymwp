# -----------------------------------------------------------------------------
# Copyright (c) 2020-2024 C. Aubert, T. Rubiano, N. Rusch and T. Seiller.
#
# This file is part of pymwp.
#
# pymwp is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pymwp is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pymwp. If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

# flake8: noqa: W605

import logging
from functools import reduce
from typing import Any, Optional, List, Callable

from . import Monomial, Polynomial, MATRIX
from .semiring import ZERO_MWP, UNIT_MWP

ZERO = Polynomial(ZERO_MWP)

UNIT = Polynomial(UNIT_MWP)

logger = logging.getLogger(__name__)


def init_matrix(size: int, init_value: Optional[Any] = None) -> List[list]:
    """Create empty matrix of specified size.

    Example:
        Generate 5 x 5 size zero-matrix.

        ```python
        init_matrix(5)
        ```

        Generates:

        ```python
        [[o, o, o, o, o],
         [o, o, o, o, o],
         [o, o, o, o, o],
         [o, o, o, o, o],
         [o, o, o, o, o]]
        ```

    Arguments:
        size: matrix size.
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
        ```

        Generates:

        ```python
        [[m, o, o, o, o],
         [o, m, o, o, o],
         [o, o, m, o, o],
         [o, o, o, m, o],
         [o, o, o, o, m]]
        ```

    Arguments:
        size: matrix size

    Returns:
        New identity matrix.
    """
    return [[UNIT if i == j else ZERO
             for j in range(size)] for i in range(size)]


def encode(matrix: MATRIX) -> List[List[List[dict]]]:
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


def decode(matrix: List[List[List[dict]]]) -> MATRIX:
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


def matrix_sum(matrix1: MATRIX, matrix2: MATRIX) -> MATRIX:
    """Compute the sum of two polynomial matrices.

    Arguments:
        matrix1: First polynomial matrix.
        matrix2: Second polynomial matrix.

    Returns:
        A new matrix that represents the sum of the two inputs.
    """

    return [[matrix1[i][j] + matrix2[i][j]
             for j in range(len(matrix1))]
            for i in range(len(matrix1))]


def matrix_prod(matrix1: MATRIX, matrix2: MATRIX) -> MATRIX:
    """Compute the product of two polynomial matrices.

    Arguments:
        matrix1: First polynomial matrix.
        matrix2: Second polynomial matrix.

    Returns:
        A new matrix that represents the product of the two inputs.
    """

    return [[
        reduce(lambda total, k:
               total + (matrix1[i][k] * matrix2[k][j]),
               range(len(matrix1)), ZERO)
        for j in range(len(matrix2))]
        for i in range(len(matrix1))]


def resize(matrix: MATRIX, new_size: int) -> MATRIX:
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


def show(matrix: MATRIX, prefix: str = None, postfix: str = None,
         fmt:Callable[[Any],str]=None) -> None:
    """Pretty print a matrix at the screen.

    Using the keyword arguments to display additional text before or
    after the matrix.

    Example:
        === "Matrix only"

            ```python
            my_matrix = identity_matrix(3)
            show(my_matrix)
            ```

            Displays:

            ```
            +m  +o  +o
            +o  +m  +o
            +o  +o  +m
            ```

        === "Matrix with text"

            ```python
            my_matrix = identity_matrix(3)
            header = ' x1  x2  x3'
            show(my_matrix, prefix=header)
            ```

            Displays:

            ```
            x1  x2  x3
            +m  +o  +o
            +o  +m  +o
            +o  +o  +m
            ```

    Arguments:
        matrix: The matrix to display.
        prefix: display some text before displaying matrix
        postfix: display some text after displaying matrix
        fmt: Optional element formatter function.

    Raises:
        TypeError: If the matrix is not iterable (type list of lists)
    """
    fmt_ = fmt or str
    if prefix:
        print(prefix)
    for row in matrix:
        print(' '.join([fmt_(r) for r in row]))
    if postfix:
        print(postfix)
    print(' ')


def equals(matrix1: MATRIX, matrix2: MATRIX) -> bool:
    """Determine if two matrices are equal.

    This function performs element-wise equality comparisons on values of
    two matrices. The two matrices must be the same size. For any two matrices
    of different size the result is always `False`.

    This function can evaluate values that are comparable by equals `==`
    operator.

    Arguments:
        matrix1: First matrix.
        matrix2: Second matrix.

    Raises:
        TypeError: If the matrix value is not iterable.

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


def fixpoint(matrix: MATRIX) -> MATRIX:
    """Computes the star operation $1 + M + M^2 + M^3 + …$

    This function assumes provided input is a square matrix.

    Arguments:
        matrix: Matrix for which to compute fixpoint.

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
