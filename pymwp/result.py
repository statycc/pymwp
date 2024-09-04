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
        """Called at start of timeable entity."""
        self.start_time = time.time_ns()
        return self

    def on_end(self) -> Timeable:
        """Called at end of timeable entity."""
        self.end_time = time.time_ns()
        return self


class Program(object):
    """Details about analyzed C file."""

    def __init__(self, n_lines: int = -1, program_path: str = None):
        """Create program object.

        Attributes:
            n_lines (int): number of lines.
            program_path (str): path to program file.
        """
        self.n_lines: int = n_lines
        self.program_path: Optional[str] = program_path

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """Convert Program object to a dictionary."""
        return {
            'n_lines': self.n_lines,
            'program_path': self.program_path}

    @property
    def name(self) -> Optional[str]:
        """Get name of program, without path and extension.

        Returns:
            Program name or `None` if not set.
        """
        return Path(self.program_path).stem if self.program_path else None

    @staticmethod
    def from_dict(**kwargs) -> Program:
        """Initialize Program object from kwargs.

        Returns:
            Program: initialized program object.

        Raises:
            KeyError: if all Program attributes are not included as kwargs.
        """
        return Program(kwargs['n_lines'], kwargs['program_path'])


class FuncResult(Timeable):
    """Capture details of analysis result for one program (function in C)."""

    def __init__(
            self, name: str, infinite: bool = False,
            variables: Optional[List[str]] = None,
            relation: Optional[Relation] = None,
            choices: Optional[Choices] = None,
            bound: Optional[Bound] = None,
            inf_flows: Optional[str] = None):
        """
        Create a function result.

        Attributes:
            name: function name
            infinite: True if result is infinite.
            variables: list of variables.
            relation: corresponding [`Relation`](relation.md)
            choices: choice object [`Choice`](choice.md)
            bound: bound object [`Bound`](bound.md)
            inf_flows: description of problematic flows
        """
        super().__init__()
        self.name = name
        self.vars = variables or []
        self.infinite = infinite
        self.inf_flows = inf_flows
        self.relation = relation
        self.choices = choices
        self.bound = bound

    @property
    def n_vars(self) -> int:
        """Number of variables."""
        return len(self.vars)

    @property
    def n_bounds(self) -> int:
        """Number of bounds."""
        return self.choices.n_bounds if self.choices else 0

    def to_dict(self) -> dict:
        """Serialize function result."""
        return {
            "name": self.name,
            "infinity": self.infinite,
            "inf_flows": self.inf_flows,
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
        if 'inf_flows' in kwargs:
            func.inf_flows = kwargs['inf_flows']
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
    """Captures analysis result and details about the process.

    This result contains

    - program: information about analyzed C File:
        type [`Program`](result.md#pymwp.result.Program)
    - relations: dictionary of function results:
        type [`FuncResult`](result.md#pymwp.result.FuncResult)
    - analysis time: measured from before any function
        has been analyzed, until all functions have been analyzed.
        It excludes time to write result to file.
    """

    def __init__(self):
        super().__init__()
        self.program: Program = Program()
        self.relations: Dict[str, FuncResult] = {}

    @property
    def n_functions(self) -> int:
        """Number of functions in analyzed program."""
        return len(self.relations.keys())

    def add_relation(self, func_result: FuncResult) -> None:
        """Appends function analysis outcome to result.

        Attributes:
            func_result: function analysis to append to Result.
        """
        self.relations[func_result.name] = f = func_result
        if not f.infinite and not f.bound:
            logger.info('Some bound exists')
            return
        txt = (('num-bounds: 0 (infinite)' + (
            ('\nProblematic flows: ' + f.inf_flows)
            if f.inf_flows else '')) if f.infinite else (
                f'num-bounds: {f.n_bounds:,}\n' +
                f'{Bound.show_poly(f.bound)}'))
        Result.pretty_print_result(f'Function: {f.name} • {txt}')

    @staticmethod
    def pretty_print_result(txt: str) -> None:
        """Draws a colored box around text before display.

        Arguments:
            txt: some text to display.
        """
        color, endc, line_w = '\033[96m', '\033[0m', 50
        # box-drawing, but a full box is not good for copy-paste.
        # flake8: noqa: F841
        tl, tr, bl, br, vb, hb = '─', '─', '─', '─', '│', '─'
        top_bar = tl + (hb * (line_w + 1)) + tr
        bot_bar = bl + (hb * (line_w + 1)) + br
        land, i_bar = Bound.LAND, Relation.INFTY_BAR
        lines, fst_land = [], True
        for vals in txt.split('\n'):
            while vals:
                # don't wrap if bound expr fits in one line
                fits = fst_land and len(vals) < line_w
                # find ideal line break index
                if land in vals[:line_w] and not fits:
                    split_at = 1 + vals[:line_w].index(land)
                elif i_bar in vals[:line_w] and not fits:
                    split_at = 1 + vals[:line_w].rindex(i_bar)
                else:
                    split_at = line_w
                # split to current...remaining
                part = vals[:split_at].strip()
                vals = vals[split_at:].strip()
                fst_land = fst_land and (
                        land not in part and i_bar not in part)
                # format line and append
                lines += [f' {part:<{line_w}}']
        parts = '\n'.join([top_bar, '\n'.join(lines), bot_bar])
        logger.info(f'\n{color}{parts}{endc}')

    def get_func(
            self, name: Optional[str] = None
    ) -> Union[FuncResult, Dict[str, FuncResult]]:
        """Returns analysis result for function(s).

        * If `name` argument is provided and key exists,
          returns function result for exact value match.
        * If program contained exactly 1 function,
          returns result for that function.
        * Otherwise, returns a dictionary of results for each
          analyzed function, as in: `<function_name, analysis_result>`

        Arguments:
            name: name of function

        Returns:
            Function analysis result, or dictionary of results.
        """
        if name and name in self.relations:
            return self.relations[name]
        if self.n_functions == 1:
            key = next(iter(self.relations))
            return self.relations[key]
        return self.relations

    def log_result(self) -> None:
        """Display here all interesting stats."""
        if self.n_functions == 0:
            logger.warning("Input C file contained no analyzable functions!")

        dur_sc = round(self.time_diff / 1e9, 1)
        dur_ms = int(self.time_diff / 1e6)
        logger.info(f'Total time: {dur_sc} s ({dur_ms} ms)')

    def serialize(self) -> dict:
        """JSON serialize a result object.

        Returns:
            dict: dictionary representation.
        """
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'program': self.program.to_dict(),
            'relations': [v.to_dict() for v in self.relations.values()]}

    @staticmethod
    def deserialize(**kwargs) -> Result:
        """Reverse of serialize.

        Returns:
            Result: Initialized Result object.
        """
        st, et, r = 'start_time', 'end_time', Result()
        r.start_time = int(kwargs[st]) if st in kwargs else 0
        r.end_time = int(kwargs[et]) if et in kwargs else 0
        if 'program' in kwargs:
            r.program = Program.from_dict(**kwargs['program'])
        if 'relations' in kwargs:
            for value in kwargs['relations']:
                r.add_relation(FuncResult.from_dict(**value))
        return r
