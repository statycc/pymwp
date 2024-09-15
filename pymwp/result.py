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
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, Dict, Union, List, Any

from pymwp import Relation, Bound, Choices
from .matrix import decode

logger = logging.getLogger(__name__)


class Timeable:
    """Represents an entity whose runtime can be measured.

    Attributes:
        start_time (int): recorded start time.
        end_time (int): recorded end time.
    """

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


class Serializable(ABC):
    """General utilities for converting results to JSON-writable
    objects and vice versa."""

    @property
    @abstractmethod
    def attrs(self) -> List[str]:
        """List of relevant attribute names."""
        pass

    @staticmethod
    def try_set(target: object, attr: str, *keys: str, **kwargs) -> None:
        """Try set target.attr from kwargs matching keys."""
        keys_ = (attr,) if not keys else keys
        ob = Serializable.try_get(*keys_, **kwargs)
        setattr(target, attr, ob) if ob else None

    @staticmethod
    def try_get(*keys: str, **kwargs) -> Any:
        """Try to get a kwargs value that matches keys."""
        ob = kwargs
        for i, key in enumerate(keys):
            ob = ob[key] if (ob and key in ob) else None
        return ob

    def to_dict(self) -> Dict[str, Any]:
        """Convert an object to a dictionary.

        Returns:
            Dictionary version of implementing class.
        """
        values = map(self.__getattribute__, self.attrs)
        return dict(zip(self.attrs, values))

    @staticmethod
    def _from_dict(obj: Serializable, **kwargs) -> None:
        """Initialize Serializable object from kwargs.

        Arguments:
            obj: initialized object.
        """
        [obj.try_set(obj, key, **kwargs) for key in obj.attrs]


class Program(Serializable):
    """Details about analyzed C-language input file.

    Attributes:
        n_lines (int): Lines of code in input program.
        program_path (str): Path to program file.
    """

    def __init__(self, n_lines: int = -1, program_path: str = None):
        self.n_lines: int = n_lines
        self.program_path: str = program_path

    @property
    def attrs(self) -> List[str]:
        """List of attributes."""
        return ['n_lines', 'program_path']

    @property
    def name(self) -> Optional[str]:
        """Get name of program, from file name, without path and extension.

        Returns:
            Program name or `None` if not set.
        """
        return Path(self.program_path).stem if self.program_path else None

    @staticmethod
    def from_dict(**kwargs) -> Program:
        """Initialize Program object from kwargs.

        Returns:
            Program: initialized Program object.
        """
        prog = Program()
        Serializable._from_dict(prog, **kwargs)
        return prog


# noinspection PyShadowingBuiltins
class FuncResult(Timeable, Serializable):
    """Analysis results for one function of the input program.

    Attributes:
        name (str): Function name.
        infinite (bool): (optional) True if no valid derivation exists.
        vars (List[str]): (optional) List of program variables.
        relation (Relation): (optional) Relation object; does not
        choices (Choices): (optional) a choice vector-object; does not
            exist if analysis terminated early or no choice exists.
        bound (Bound): (optional) mwp-bounds; does not
            exist if analysis terminated early or no choice exists.
        inf_flows (str): (optional) Description of problematic flows.
            exist if analysis terminated early.
        index (int): (optional) Degree of derivation choice [default: 0].
        func_code (str): (optional) Function source code, if the AST required
            modification.
    """

    def __init__(
            self,
            name: str,
            infinite: bool = False,
            vars: Optional[List[str]] = None,
            relation: Optional[Relation] = None,
            choices: Optional[Choices] = None,
            bound: Optional[Bound] = None,
            inf_flows: Optional[str] = None,
            index: int = 0,
            func_code: str = None):
        super().__init__()
        self.name: str = name
        self.infinite: bool = infinite
        self.vars: List[str] = vars or []
        self.relation: Relation = relation
        self.choices: Choices = choices
        self.bound: Bound = bound
        self.inf_flows: str = inf_flows
        self.index: int = index
        self.func_code: str = func_code

    @property
    def n_vars(self) -> int:
        """Number of variables."""
        return len(self.vars)

    @property
    def n_bounds(self) -> int:
        """Number of bounds."""
        return self.choices.n_bounds if self.choices else 0

    @property
    def attrs(self) -> List[str]:
        """List of attribute names."""
        return 'name,infinite,start_time,end_time,vars,' \
               'inf_flows,index,func_code'.split(',')

    def to_dict(self) -> dict:
        """Serialize a function result."""
        result = super().to_dict()
        if self.relation:
            result['relation'] = self.relation.to_dict()
        if self.choices:
            result['choices'] = self.choices.valid
        if self.bound:
            result['bound'] = self.bound.to_dict()
        return result

    @staticmethod
    def from_dict(name: str = None, infinite: bool = False, **kwargs) \
            -> FuncResult:
        """Deserialize a function result."""
        func = FuncResult(name, infinite)
        Serializable._from_dict(func, **kwargs)
        matrix = FuncResult.try_get('relation', 'matrix', **kwargs)
        if matrix:
            func.relation = Relation(func.vars, decode(matrix))
        choices = FuncResult.try_get('choices', **kwargs)
        if choices:
            func.choices = Choices(choices, func.index)
        bound = FuncResult.try_get('bound', **kwargs)
        if bound:
            func.bound = Bound(bound)
        return func


class Result(Timeable, Serializable):
    """Captures analysis result and details about the analysis process.

    Attributes:
        program (Program): Information about analyzed C File.
        relations (Dict[str, FuncResult]): Dictionary of function results.
    """

    def __init__(self):
        super().__init__()
        self.program: Program = Program()
        self.relations: Dict[str, FuncResult] = {}

    @property
    def n_functions(self) -> int:
        """Number of functions in analyzed program."""
        return len(self.relations.keys())

    @property
    def attrs(self) -> List[str]:
        """List of attribute names."""
        return ['start_time', 'end_time']

    def add_relation(self, func_result: FuncResult) -> None:
        """Appends function analysis outcome to result.

        Attributes:
            func_result: function analysis to append to Result.
        """
        self.relations[func_result.name] = f = func_result
        if not f.infinite and not f.bound:
            logger.info('Some bound exists')
            return
        txt = f'function: {f.name}'
        txt += f' • time: {func_result.dur_ms:,} ms\n'
        txt += f'variables: {len(f.vars)}'
        txt += ' • num-bounds: '
        if f.infinite:
            txt += '0 (infinite)'
            if f.inf_flows:
                txt += f'\nProblematic flows: {f.inf_flows}'
        else:
            txt += f'{f.n_bounds:,}\n'
            txt += f'{Bound.show(f.bound)}'
        Result.pretty_print_result(txt)

    @staticmethod
    def pretty_print_result(txt: str) -> None:
        """Draws a colored box around text before display.

        Arguments:
            txt: some text to display.
        """
        color, endc, line_w, hb = '\033[96m', '\033[0m', 50, '─'
        top_bar = (hb * (line_w + 3))
        bot_bar = top_bar[:]
        land, i_bar = Bound.LAND, Relation.INFTY_BAR
        lines, fst_land = [], True
        for vals in txt.split('\n'):
            while vals:
                # don't wrap if bound expr fits in one line
                fits = fst_land and len(vals) < line_w
                # find ideal line break index
                if land in vals[:line_w] and not fits:
                    split_at = 1 + vals[:line_w].index(land)
                elif i_bar in vals[:line_w] and len(vals) > line_w:
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

    def get_func(self, name: Optional[str] = None) \
            -> Union[FuncResult, Dict[str, FuncResult]]:
        """Returns analysis result for function(s).

        * If `name` argument is provided and key exists, returns function
          result for exact value match.
        * If program contained exactly 1 function, returns result for that
          function.
        * Otherwise, returns a dictionary of results for each analyzed
          function, as in: `<function_name, analysis_result>`

        Arguments:
            name: name of function,

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
        logger.info(f'Total time: {self.dur_s} s ({self.dur_ms} ms)')

    def to_dict(self) -> dict:
        """JSON serialize a result object.

        Returns:
            dict: dictionary representation.
        """
        result = super().to_dict()
        rels = [(name, v.to_dict()) for (name, v) in self.relations.items()]
        rest = {'program': self.program.to_dict(), 'relations': dict(rels)}
        return {**result, **rest}

    @staticmethod
    def from_dict(**kwargs) -> Result:
        """Reverse of serialize.

        Returns:
            Result: Initialized Result object.
        """
        r = Result()
        Serializable._from_dict(r, **kwargs)
        program = Result.try_get('program', **kwargs)
        if program:
            r.program = Program.from_dict(**program)
        relations = Result.try_get('relations', **kwargs)
        if relations:
            for value in relations.values():
                r.add_relation(FuncResult.from_dict(**value))
        return r
