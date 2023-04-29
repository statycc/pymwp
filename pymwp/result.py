from __future__ import annotations

import logging
import time
from typing import Optional, Dict, Union, List
from pathlib import Path

from pymwp import Relation, Bound, Choices
from .matrix import decode

logger = logging.getLogger(__name__)


class Timeable:
    """Represents an entity whose runtime can be measured."""

    def __init__(self):
        self.start_time = 0
        self.end_time = 0

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

    def on_start(self) -> Timeable:
        """At start of function analysis"""
        self.start_time = time.time_ns()
        return self

    def on_end(self) -> Timeable:
        """Called immediately after function analysis"""
        self.end_time = time.time_ns()
        return self


class Program(object):
    """Details about analyzed C program."""

    def __init__(self, n_lines: int = -1, program_path: str = None):
        self.n_lines: int = n_lines
        self.program_path: Optional[str] = program_path

    def to_dict(self):
        return {
            'n_lines': self.n_lines,
            'program_path': self.program_path}

    @property
    def name(self) -> Optional[str]:
        return Path(self.program_path).stem if self.program_path else None

    @staticmethod
    def from_dict(**kwargs):
        return Program(kwargs['n_lines'], kwargs['program_path'])


class FuncResult(Timeable):
    """Capture details of analysis result for one function."""

    def __init__(
            self, name: str, infinite: bool = False,
            variables: Optional[List[str]] = None,
            relation: Optional[Relation] = None,
            choices: Optional[Choices] = None,
            bound: Optional[Bound] = None):
        super().__init__()
        self.name = name
        self.vars = variables or []
        self.infinite = infinite
        self.relation = relation
        self.choices = choices
        self.bound = bound

    @property
    def n_vars(self) -> int:
        return len(self.vars)

    @property
    def n_bounds(self) -> int:
        return self.choices.n_bounds if self.choices else 0

    def to_dict(self) -> dict:
        """Serialize function result."""
        return {
            "name": self.name,
            "infinity": self.infinite,
            "variables": self.vars,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "relation": self.relation.to_dict() if self.relation else None,
            **({"choices": self.choices.valid if self.choices else None,
                "bound": self.bound.to_dict() if self.bound else None}
               if not self.infinite else
               {"infty_vars": self.relation.infty_vars()}
               if self.relation else {})}

    @staticmethod
    def from_dict(**kwargs):
        """Deserialize function result."""
        st, et = 'start_time', 'end_time'
        func = FuncResult(kwargs['name'], kwargs['infinity'])
        func.start_time = int(kwargs[st]) if st in kwargs else 0
        func.end_time = int(kwargs[et]) if et in kwargs else 0
        if 'variables' in kwargs:
            func.vars = kwargs['variables']
        if kwargs['relation']:
            matrix = kwargs['relation']['matrix']
            if func.vars:
                func.relation = Relation(func.vars, decode(matrix))
        if 'choices' in kwargs:
            func.choices = Choices(kwargs['choices'])
        if 'bound' in kwargs and func.choices and func.relation:
            func.bound = Bound(kwargs['bound'])
        return func


class Result(Timeable):
    """Captures analysis result and details about the process."""

    def __init__(self):
        super().__init__()
        self.program: Program = Program()
        self.relations: Dict[str, FuncResult] = {}

    @property
    def n_functions(self) -> int:
        """number of functions in analyzed program"""
        return len(self.relations.keys())

    def add_relation(self, func_result: FuncResult) -> None:
        """Appends function analysis outcome to result."""
        self.relations[func_result.name] = func_result
        if not func_result.infinite:
            if func_result.bound:
                logger.info(f'Bound: {Bound.show_poly(func_result.bound)}')
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

        - If `name` argument is provided and key exists, returns value match.
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

    def log_result(self):
        """Display here all interesting stats."""
        if self.n_functions == 0:
            logger.warning("Input C file contained no analyzable functions!")

        dur_sc = round(self.time_diff / 1e9, 1)
        dur_ms = int(self.time_diff / 1e6)
        logger.info(f'Total time: {dur_sc} s ({dur_ms} ms)')

    def serialize(self):
        """JSON serialize result object."""
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'program': self.program.to_dict(),
            'relations': [v.to_dict() for v in self.relations.values()]}

    @staticmethod
    def deserialize(**kwargs) -> Result:
        """Reverse of serialize."""
        st, et, r = 'start_time', 'end_time', Result()
        r.start_time = int(kwargs[st]) if st in kwargs else 0
        r.end_time = int(kwargs[et]) if et in kwargs else 0
        if 'program' in kwargs:
            r.program = Program.from_dict(**kwargs['program'])
        if 'relations' in kwargs:
            for value in kwargs['relations']:
                r.add_relation(FuncResult.from_dict(**value))
        return r
