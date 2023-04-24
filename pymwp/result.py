from __future__ import annotations

import logging
import time
from typing import Optional, Dict, Tuple

from pymwp import Relation, Choices, Bound
from pymwp.choice import CHOICES

logger = logging.getLogger(__name__)

FUNC_RESULT = Tuple[Optional[Relation], Optional[CHOICES], bool]
"""Type hint for function analysis result."""


class Program(object):
    """Details about analyzed program."""

    def __init__(self):
        self.n_lines: int = -1
        self.program_path: Optional[str] = None
        self.raw_source: Optional[str] = None


class Result:
    """Captures analysis result."""

    def __init__(self):
        self.program: Program = Program()
        self.relations: Dict[str, FUNC_RESULT] = {}
        self.start_time: int = -1
        self.end_time: int = -1

    @property
    def n_functions(self):
        return len(self.relations.keys())

    def add_relation(
            self, name: str, matrix: Optional[Relation],
            choices: Optional[Choices], infinite: bool
    ):
        """Appends function analysis outcome to result."""
        self.relations[name] = (matrix, choices, infinite)
        if not infinite:
            if choices:
                simple = matrix.apply_choice(*choices.first_choice)
                bound = Bound.calculate(simple.variables, simple.matrix)
                logger.info(f'BOUND: {Bound.show(bound)}')
            else:
                logger.info('Some bound exists')
        if infinite:
            logger.info(f'{name} is infinite')
            if matrix:
                logger.info(f'Problematic flows: {matrix.show_infty_pairs()}')

    def get_result(self):
        """Returns the analysis result.

        If program contained exactly 1 function, returns
        matrix, choices, infinity-flag for that function.

        Otherwise, returns a dictionary of results for each
        analyzed function, as in: <function_name, analysis_result>
        """
        if self.n_functions == 1:
            key = next(iter(self.relations))
            return self.relations[key]
        return self.relations

    def on_start(self):
        """Called immediately before analysis of AST."""
        self.start_time = time.time_ns()

    def on_end(self):
        """Called immediately after analysis of AST has completed."""
        self.end_time = time.time_ns()

    def log_result(self):
        """Display here all interesting stats."""
        if self.n_functions == 0:
            logger.warning("Input C file contained no analyzable functions!")

        time_diff = self.end_time - self.start_time
        dur_sc = round(time_diff / 1e9, 1)
        dur_ms = int(time_diff / 1e6)
        logger.info(f'Total time: {dur_sc} s ({dur_ms} ms)')
