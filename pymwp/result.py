from __future__ import annotations

import logging
import time
from typing import Optional, Dict, Union

from pymwp import Relation, Bound, Choices

logger = logging.getLogger(__name__)


class FuncResult:
    """Analysis result for one function."""

    def __init__(
            self, name: str, infinite: bool,
            relation: Optional[Relation] = None,
            choices: Optional[Choices] = None,
            bound: Optional[Bound] = None,
    ):
        self.name = name
        self.infinite = infinite
        self.relation = relation
        self.choices = choices
        self.bound = bound


class Program(object):
    """Details about analyzed program."""

    def __init__(self):
        self.n_lines: int = -1
        self.program_path: Optional[str] = None
        self.raw_source: Optional[str] = None


class Result:
    """Captures analysis result and details about the process."""

    def __init__(self):
        self.program: Program = Program()
        self.relations: Dict[str, FuncResult] = {}
        self.start_time: int = -1
        self.end_time: int = -1

    @property
    def n_functions(self) -> int:
        """number of functions in analyzed program"""
        return len(self.relations.keys())

    @property
    def time_diff(self) -> int:
        """Time delta between analysis start and end time."""
        return self.end_time - self.start_time

    @property
    def dur_s(self) -> float:
        """Duration in seconds."""
        return round(self.time_diff / 1e9, 1)

    @property
    def dur_ms(self) -> int:
        """Duration in milliseconds."""
        return int(self.time_diff / 1e6)

    def add_relation(self, func_result: FuncResult) -> None:
        """Appends function analysis outcome to result."""
        self.relations[func_result.name] = func_result
        if not func_result.infinite:
            if func_result.bound:
                logger.info(f'Bound: {Bound.show(func_result.bound)}')
            else:
                logger.info('Some bound exists')
        if func_result.infinite:
            logger.info(f'{func_result.name} is infinite')
            if func_result.relation:
                logger.info('Possibly problematic flows:')
                logger.info(func_result.relation.infty_pairs())

    def get_func(self, name: Optional[str] = None) \
            -> Union[FuncResult, Dict[str, FuncResult]]:
        """Returns the analysis result.

        - If `name` argument is provided and the key exists, returns value match.
        - If program contained 1 function, returns result for that function.

        Otherwise, returns a dictionary of results for each
        analyzed function, as in: `<function_name, analysis_result>`

        Arguments:
            name - name of function

        Returns:
            Function analysis result, or dictionary of results.
        """
        if name and name in self.relations:
            return self.relations[name]
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

        dur_sc = round(self.time_diff / 1e9, 1)
        dur_ms = int(self.time_diff / 1e6)
        logger.info(f'Total time: {dur_sc} s ({dur_ms} ms)')
