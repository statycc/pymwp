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
from typing import Optional, Dict, Union, List, Any, Callable

from pymwp import Relation, Bound, MwpBound, Choices
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

    def __str__(self):
        if not self.infinite and not self.bound:
            return 'Some bound exists'
        txt = f'function: {self.name}'
        txt += f' • time: {self.dur_ms:,} ms\n'
        txt += f'variables: {len(self.vars)}'
        txt += ' • num-bounds: '
        if self.infinite:
            txt += '0 (infinite)'
            if self.inf_flows:
                txt += f'\nProblematic flows: {self.inf_flows}'
        else:
            txt += f'{self.n_bounds:,}\n'
            txt += f'{Bound.show(self.bound, True, True)}'
        return txt

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


class LoopResult(Timeable, Serializable):
    """Analysis result for loop.

    Attributes:
        func_name (str): Containing function name.
        loop_code (str): The analyzed loop.
        variables (Dict[str, VResult]): Results by variable.
    """

    def __init__(
            self, func_name: str = None,
            loop_code: str = None):
        super().__init__()
        self.func_name: str = func_name
        self.loop_code: str = loop_code
        self.variables: Dict[str, VResult] = {}

    def __str__(self):
        txt = f'function: {self.func_name}'
        txt += f'\nloop: {self.loop_desc}'
        txt += f'\nvariables: {len(self.variables)}'
        txt += f' • time: {self.dur_ms:,} ms'
        txt += f'\nlinear: {", ".join(self.linear) or "—"}'
        txt += f'\nindependent: {", ".join(self.weak) or "—"}'
        txt += f'\npolynomial: {", ".join(self.poly) or "—"}'
        txt += f'\ninfinity: {", ".join(self.exp) or "—"}'
        txt += f'\n{self.as_bound().show(True, True)}'
        return txt

    @property
    def attrs(self) -> List[str]:
        return 'func_name,start_time,end_time,loop_code'.split(',')

    @property
    def n_vars(self) -> int:
        """Number of variables."""
        return len(self.variables)

    @property
    def n_bounded(self) -> int:
        """Number of variables with a known bound."""
        exp = filter(lambda x: x.exponential, self.variables.values())
        return self.n_vars - len(list(exp))

    @property
    def n_lines(self) -> int:
        """Number of code lines in a loop."""
        return self.loop_code.strip().count('\n')

    @property
    def loop_desc(self) -> str:
        """Loop description => header block."""
        header = self.loop_code.split('\n')[:1][0].strip()
        return (header[:40] if len(header) > 40 else header) + '…'

    @property
    def linear(self) -> List[str]:
        """All variables with a linear bound."""
        return self.var_sat(lambda r: r.is_m)

    @property
    def weak(self) -> List[str]:
        """All variables with a weak polynomial bound."""
        return self.var_sat(lambda r: r.is_w and not r.is_m)

    @property
    def poly(self) -> List[str]:
        """All variables with a polynomial bound."""
        return self.var_sat(lambda r: r.is_p and not r.is_w)

    @property
    def exp(self) -> List[str]:
        """All variables with an unknown bound."""
        return self.var_sat(lambda r: r.exponential)

    def as_bound(self) -> Bound:
        """Combines variable results to a Bound-type."""
        return Bound(dict([
            (v, res.bound.bound_str) for v, res in
            self.variables.items() if res.bound]))

    def var_sat(self, cond: Callable[[VResult], bool]) -> List[str]:
        """List of variables satisfying condition."""
        return [v for v, r in self.variables.items() if cond(r)]

    def to_dict(self) -> dict[str, Union[str, int, dict]]:
        """Serialize a function result."""
        result = super().to_dict()
        variables = {'variables': dict([
            (name, v.to_dict()) for (name, v) in
            self.variables.items()])} if self.variables else {}
        return {**result, **variables}

    @staticmethod
    def from_dict(**kwargs) -> LoopResult:
        """Deserialize a function result."""
        result = LoopResult()
        Serializable._from_dict(result, **kwargs)
        variables = LoopResult.try_get('variables', **kwargs)
        if variables:
            result.variables = dict([
                (name, VResult.from_dict(**value))
                for name, value in variables.items()])
        return result


class VResult(Serializable):
    """Analysis result for a single variable.

    Attributes:
        name (str): Variable name.
        is_m (bool): Has maximal linear bound.
        is_w (bool): Has weak polynomial bound.
        is_p (bool): Has polynomial bound.
        bound (Optional[MwpBound]): A bound (if exists).
        choices (Optional[Choice]): Choice for bound.
    """

    def __init__(self, name: str = None, is_m: bool = False,
                 is_w: bool = False, is_p: bool = False,
                 bound: MwpBound = None, choices: Choices = None):
        self.name = name
        self._is_m = False
        self._is_w = False
        self._is_p = False
        self.bound = bound
        self.choices = choices
        self.is_m = is_m
        self.is_w = is_w
        self.is_p = is_p

    @property
    def exponential(self):
        """Variable has no known bound (polynomial or less)."""
        return self.is_p is False

    @property
    def is_m(self) -> bool:
        """Variable has a max of linear bound."""
        return self._is_m

    @is_m.setter
    def is_m(self, value: bool):
        if value:
            self._is_m = self._is_w = self._is_p = True
        else:
            self._is_m = False

    @property
    def is_w(self) -> bool:
        """Variable has a weak polynomial bound."""
        return self._is_w

    @is_w.setter
    def is_w(self, value: bool):
        if value:
            self._is_w = self._is_p = True
        else:
            self._is_m = self._is_w = False

    @property
    def is_p(self) -> bool:
        """Variable has a polynomial bound."""
        return self._is_p

    @is_p.setter
    def is_p(self, value: bool):
        if value:
            self._is_p = True
        else:
            self._is_m = self._is_w = self._is_p = False

    @property
    def attrs(self) -> List[str]:
        return 'name,is_m,is_w,is_p'.split(',')

    def to_dict(self) -> dict[str, str, int, dict]:
        """Serialize a loop variable analysis result."""
        result = super().to_dict()
        if self.choices:
            result['choices'] = self.choices.valid
        if self.bound:
            result['bound'] = self.bound.bound_str
        return result

    @staticmethod
    def from_dict(**kwargs) -> VResult:
        """Reverse of serialize.

        Returns:
            Result: Initialized Result object.
        """
        r = VResult()
        Serializable._from_dict(r, **kwargs)
        choices = VResult.try_get('choices', **kwargs)
        if choices:
            r.choices = Choices(choices)
        bound = VResult.try_get('bound', **kwargs)
        if bound:
            r.bound = MwpBound(bound)
        return r


class Result(Timeable, Serializable):
    """Captures analysis result and details about the analysis process.

    Attributes:
        program (Program): Information about analyzed C File.
        relations (Dict[str, FuncResult]): Dictionary of function results.
        loops ([LoopResult]: List of analyzed loops.
    """

    def __init__(self):
        super().__init__()
        self.program: Program = Program()
        self.relations: Dict[str, FuncResult] = {}
        self.loops = []

    @property
    def n_functions(self) -> int:
        """Number of functions in analyzed program."""
        return len(self.relations.keys())

    @property
    def n_loops(self) -> int:
        """Number of loops in analyzed program."""
        return len(self.loops)

    @property
    def attrs(self) -> List[str]:
        """List of attribute names."""
        return ['start_time', 'end_time']

    def add_relation(self, func_result: FuncResult) -> None:
        """Appends function analysis to result."""
        self.relations[func_result.name] = func_result
        Result.pretty_print_result(str(func_result))

    def add_loop(self, loop_result: LoopResult) -> None:
        """Append loop analysis to result."""
        self.loops.append(loop_result)
        Result.pretty_print_result(str(loop_result))

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

    def log_result(self) -> Result:
        """Display here all interesting stats about analysis result."""
        if self.n_functions == 0 and self.n_loops == 0:
            logger.warning("Nothing was analyzed")
        logger.info(f'Total time: {self.dur_s} s ({self.dur_ms} ms)')
        return self

    def to_dict(self) -> dict[str, Union[str, dict]]:
        """JSON serialize a result object.

        Returns:
            dict: dictionary representation.
        """
        result = super().to_dict()
        prog = {'program': self.program.to_dict()}
        loop = {'loops': [lp.to_dict() for lp in self.loops]} \
            if self.loops else {}
        rest = {'relations': dict([
            (name, v.to_dict()) for (name, v) in
            self.relations.items()])} if self.relations else {}
        return {**result, **prog, **loop, **rest}

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
        loops = Result.try_get('loops', **kwargs)
        if loops:
            r.loops = [LoopResult.from_dict(**loop) for loop in loops]
        relations = Result.try_get('relations', **kwargs)
        if relations:
            for value in relations.values():
                r.add_relation(FuncResult.from_dict(**value))
        return r
