# flake8: noqa: W605

from __future__ import annotations

import logging
import math
import progressbar
from itertools import product
from typing import Optional, Tuple, List

from . import matrix as matrix_utils
from .delta_graphs import DeltaGraph

logger = logging.getLogger(__name__)


class Relation:
    """
    A relation is made of a list of variables and a 2D-matrix:

    - Variables of a relation represent the variables of the input
    program under analysis, for example: $X_0, X_1, X_2$.

    - Matrix holds [`Polynomials`](polynomial.md#pymwp.polynomial)
    and represents the current state of the analysis.

    """

    def __init__(self, variables: Optional[List[str]] = None,
                 matrix: Optional[List[List]] = None):
        """Create a relation.

        When constructing a relation, provide a list of variables
        and an initial matrix.

        If matrix is not provided, the relation matrix will be initialized to
        zero matrix of size matching the number of variables.

        Also see: [`Relation.identity()`](relation.md#pymwp.relation
        .Relation.identity) for creating a relation whose matrix is an
        identity matrix.

        Example:

        Create a new relation from a list of variables:

        ```python
        r = Relation(['X0', 'X1', 'X2'])

        # Creates relation with 0-matrix with and specified variables:
        #
        #  X0  |  0  0  0
        #  X1  |  0  0  0
        #  X2  |  0  0  0
        ```

        Arguments:
            variables: program variables
            matrix: relation matrix
        """
        self.variables = (variables or [])[:]
        self.matrix = matrix or matrix_utils \
            .init_matrix(len(self.variables))

    @staticmethod
    def identity(variables: List) -> Relation:
        """Create an identity relation.

        This method allows creating a relation whose
        matrix is an identity matrix.

        This is an alternative way to construct a relation.

        Example:

        Create a new identity relation from a list of variables:

        ```python
        r = Relation.identity(['X0', 'X1', 'X2', 'X3'])

        # Creates relation with identity matrix with and specified variables:
        #
        #  X0  |  m  0  0  0
        #  X1  |  0  m  0  0
        #  X2  |  0  0  m  0
        #  X3  |  0  0  0  m
        ```

        Arguments:
            variables: list of variables

        Returns:
             Generated relation of given variables and an identity matrix.
        """
        matrix = matrix_utils.identity_matrix(len(variables))
        return Relation(variables, matrix)

    @property
    def is_empty(self):
        return not self.variables or not self.matrix

    def __str__(self):
        right_pad = len(max(self.variables, key=len)) \
            if self.variables else 0
        return '\n'.join(
            [var.ljust(right_pad) + '  |' + ''.join(poly) for var, poly in
             [(var, [str(self.matrix[i][j]) for j in range(len(self.matrix))])
              for i, var in enumerate(self.variables)]])

    def __add__(self, other):
        return self.sum(other)

    def __mul__(self, other):
        return self.composition(other)

    def replace_column(self, vector: List, variable: str) -> Relation:
        """Replace identity matrix column by a vector.

        Arguments:
            vector: vector by which a matrix column will be replaced.
            variable: program variable, column replacement
                will occur at the index of this variable.

        Raises:
              ValueError: if variable is not found in this relation.

        Returns:
            new relation after applying the column replacement.
        """
        new_relation = Relation.identity(self.variables)
        j = self.variables.index(variable)

        for idx, value in enumerate(vector):
            new_relation.matrix[idx][j] = value

        return new_relation

    def while_correction(self, dg: DeltaGraph) -> None:
        """Replace invalid scalars in a matrix by $\\infty$.

        Following the computation of fixpoint for a while loop node, this
        method checks the resulting matrix and replaces all invalid scalars
        with $\\infty$ (W rule in MWP paper):

        - scalar $p$ anywhere in the matrix becomes $\\infty$
        - scalar $w$ at the diagonal becomes $\\infty$

        Example:

        ```text
           Before:                After:

           | m  o  o  o  o |      | m  o  o  o  o |
           | o  w  o  p  o |      | o  i  o  i  o |
           | o  o  m  o  o |      | o  o  m  o  o |
           | w  o  o  m  o |      | w  o  o  m  o |
           | o  o  o  o  p |      | o  o  o  o  i |
        ```

        This method is where $\\infty$ is introduced in a matrix.

        Related discussion: [issue #14](
        https://github.com/statycc/pymwp/issues/14).

        Arguments:
            dg: DeltaGraph instance
        """
        for i, vector in enumerate(self.matrix):
            for j, poly in enumerate(vector):
                for mon in poly.list:
                    if mon.scalar == "p" or (mon.scalar == "w" and i == j):
                        mon.scalar = "i"
                        dg.import_monomial(mon)

    def sum(self, other: Relation) -> Relation:
        """Sum two relations.

        Calling this method is equivalent to syntax `relation + relation`.

        Arguments:
            other: Relation to sum with self.

        Returns:
           A new relation that is a sum of inputs.
        """
        er1, er2 = Relation.homogenisation(self, other)
        new_matrix = matrix_utils.matrix_sum(er1.matrix, er2.matrix)
        return Relation(er1.variables, new_matrix)

    def composition(self, other: Relation) -> Relation:
        """Composition of current and another relation.

        Calling this method is equivalent to syntax `relation * relation`.

        Composition will:

        1. combine the variables of two relations, and
        2. produce a single matrix that is the product of matrices of
            the two input relations.

        Arguments:
            other: Relation to compose with current

        Returns:
           a new relation that is a product of inputs.
        """

        logger.debug("starting composition...")
        er1, er2 = Relation.homogenisation(self, other)
        logger.debug("composing matrix product...")
        new_matrix = matrix_utils.matrix_prod(er1.matrix, er2.matrix)
        logger.debug("...relation composition done!")
        return Relation(er1.variables, new_matrix)

    def equal(self, other: Relation) -> bool:
        """Determine if two relations are equal.

        For two relations to be equal they must have:

        1. the same variables (independent of order), and
        2. matrix polynomials must be equal element-wise.

        See [`polynomial#equal`](
        polynomial.md#pymwp.polynomial.Polynomial.equal)
        for details on how to determine equality of two polynomials.

        Arguments:
            other: relation to compare

        Returns:
            true when two relations are equal
            and false otherwise.
        """

        # must have same variables in same order
        if set(self.variables) != set(other.variables):
            return False

        # not sure homogenisation is necessary here
        # --> yes we need it
        er1, er2 = Relation.homogenisation(self, other)

        for row1, row2 in zip(er1.matrix, er2.matrix):
            for poly1, poly2 in zip(row1, row2):
                if poly1 != poly2:
                    return False
        return True

    def fixpoint(self) -> Relation:
        """
        Compute sum of compositions until no changes occur.

        Returns:
            resulting relation.
        """
        fix_vars = self.variables
        matrix = matrix_utils.identity_matrix(len(fix_vars))
        fix = Relation(fix_vars, matrix)
        prev_fix = Relation(fix_vars, matrix)
        current = Relation(fix_vars, matrix)

        logger.debug(f"computing fixpoint for variables {fix_vars}")

        while True:
            prev_fix.matrix = fix.matrix
            current = current * self
            fix = fix + current
            if fix.equal(prev_fix):
                logger.debug(f"fixpoint done {fix_vars}")
                return fix

    def eval(self, choices: List[int], dg: DeltaGraph) -> bool:
        """Evaluate relation matrix against a list of choices to
            determine if any of them results in infinity.

        This method iterates all monomials of all polynomials
        and performs `eval()` on each object.

        For implementations see:

        - [`polynomial.eval()`](polynomial.md#pymwp.polynomial.Polynomial.eval)
        - [`monomial.eval()`](monomial.md#pymwp.monomial.Monomial.eval)

        Example:

        ```python
        choices = [0, 1, 2, 0, 1, 0]
        relation.eval(choices)
        ```

        Arguments:
            choices: a list of indices to select for each monomial.
            dg: DeltaGraph instance

        Returns:
           `False` if infinity occurs during evaluation of choices and `True`
           otherwise.
        """

        if dg.contains_combination(choices):
            return False

        for row in self.matrix:
            for poly in row:
                if poly.eval(choices) == 'i':
                    return False
        return True

    def non_infinity(self, choices: List[int], index: int, dg: DeltaGraph) -> \
            List[list[int]]:
        """Find all combinations of choices that do not evaluate to infinity.

        This method computes the Cartesian product of input iterables and
        evaluates each combination against the current relation.

        If the evaluation determines that no infinity will occur, that
        combination will be included in the return value.

        Reference: [itertools.product](
        https://docs.python.org/3/library/itertools.html#itertools.product)

        Example:

        ```
        rel.non_infinity(choices=[0, 1], index=2)

        # internally generates combinations: [[0, 0], [0, 1], [1, 0], [1, 1]]
        # and of those returns the ones that do not evaluate to infinity
        # against current relation.
        ```

        Arguments:
            choices: integer list of choices
            index: length of generated product
            dg: DeltaGraph instance

        Returns:
            All combinations that do not result in $\\infty$ when evaluated
            against the this relation.
        """
        logger.debug(f"evaluating choices: {choices}, index: {index}")
        logger.debug(f"relation variables: {self.variables}")

        # uses itertools.product to generate all possible assignments
        combinations = product(choices, repeat=index)

        size = math.pow(len(choices), index)

        logger.debug(f"number of assignments to evaluate {size}")

        res = []
        for combination in progressbar.progressbar(
                combinations, max_value=size):
            # append when result is non-empty list
            if self.eval(list(combination), dg) and combination:
                res.append(list(combination))

        return res

    def to_dict(self) -> dict:
        """Get dictionary representation of a relation."""
        return {
            "variables": self.variables,
            "matrix": matrix_utils.encode(self.matrix)
        }

    def show(self):
        """Display relation."""
        print(str(self))

    @staticmethod
    def homogenisation(r1: Relation, r2: Relation) \
            -> Tuple[Relation, Relation]:
        """Performs homogenisation on two relations.

        After this operation both relations will have same
        variables and their matrices of the same size.

        This operation will internally resize matrices as needed.

        Arguments:
            r1: first relation to homogenise
            r2: second relation to homogenise

        Returns:
            Homogenised versions of the 2 inputs relations
        """

        # check equality
        if r1.variables == r2.variables:
            return r1, r2

        # check empty cases
        if r1.is_empty:
            return Relation.identity(r2.variables), r2

        if r2.is_empty:
            return r1, Relation.identity(r1.variables)

        logger.debug("matrix homogenisation...")

        # build a list of all distinct variables; maintain order
        extended_vars = r1.variables + [v for v in r2.variables
                                        if v not in r1.variables]

        # resize matrices to match new number of variables
        new_matrix_size = len(extended_vars)

        # first matrix: just resize -> this one is now done
        matrix1 = matrix_utils.resize(r1.matrix, new_matrix_size)

        # second matrix: create and initialize as identity matrix
        matrix2 = matrix_utils.identity_matrix(new_matrix_size)

        # index of each extended_vars iff variable exists in r2.
        # we will use this to mapping from old -> new matrix to fill
        # the new matrix; the indices may be in different order.
        index_dict = {index: r2.variables.index(var)
                      for index, var in enumerate(extended_vars)
                      if var in r2.variables}

        # generate a list of all valid <row, column> combinations
        index_map = [t1 + t2 for t1 in index_dict.items()
                     for t2 in index_dict.items()]

        # fill the resized matrix with values from original matrix
        for mj, rj, mi, ri in index_map:
            matrix2[mi][mj] = r2.matrix[ri][rj]

        return Relation(extended_vars, matrix1), Relation(extended_vars,
                                                          matrix2)
