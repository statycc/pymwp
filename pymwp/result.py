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
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Union, List, Tuple, Any, Callable, Type

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
    def _attrs(self) -> List[str]:
        """List of simple attribute names."""
        return []

    @property
    def _ser_attrs(self) -> List[Tuple[str, Type[Serializable]]]:
        """Attributes of type Serializable."""
        return []

    @property
    def _ser_dict(self) -> List[Tuple[str, str, Type[Serializable]]]:
        """Dictionaries attributes where values are of Serializable type."""
        return []

    @property
    def _ser_list(self) -> List[Tuple[str, Type[Serializable]]]:
        """List attributes where values are of Serializable type."""
        return []

    def to_dict(self) -> Dict[str, Any]:
        """Convert an object to a JSON-compatible dictionary."""
        # simple type attributes
        sv = map(self.__getattribute__, self._attrs)
        simple = dict(zip(self._attrs, sv))

        # serializable types
        ok = [k for k, _ in self._ser_attrs]
        ov = [self.__getattribute__(k).to_dict() for k in ok]
        objs = dict(zip(ok, ov))

        # lists of serializable types
        lk = [k for k, _ in self._ser_list if getattr(self, k)]
        lv = [[v.to_dict() for v in getattr(self, k)] for k in lk]
        lists = dict(zip(lk, lv))

        # dictionary types
        dk = [n for n, _, _ in self._ser_dict if getattr(self, n)]
        dicts = dict(zip(dk, [dict([
            (n, v.to_dict()) for n, v in getattr(self, k).items()])
            for k in dk]))

        return {**simple, **objs, **lists, **dicts}

    @staticmethod
    @abstractmethod
    def from_dict(**kwargs) -> Serializable:
        """Restore object from a dictionary; reverses `to_dict()`."""
        pass

    @staticmethod
    def _load(obj: Serializable, **kwargs) -> Any:
        """Initializes a Serializable object from kwargs.

        Arguments:
            obj: Initialized object.
            *kwargs: Object data.

        Returns:
            Loaded object.
        """
        for key in obj._attrs:
            obj._try_set(obj, key, **kwargs)
        for attr, objT in obj._ser_attrs:
            values = Serializable._try_get(attr, **kwargs)
            setattr(obj, attr, objT.from_dict(**values) if values else None)
        for attr, objT in obj._ser_list:
            values = Serializable._try_get(attr, **kwargs) or []
            setattr(obj, attr, [objT.from_dict(**v) for v in values])
        for attr, key, objT in obj._ser_dict:
            items = Result._try_get(attr, **kwargs) or {}
            values = [objT.from_dict(**value) for value in items.values()]
            keys = [getattr(obj, key) for obj in values]
            setattr(obj, attr, dict(zip(keys, values)))
        return obj

    @staticmethod
    def _try_set(target: object, attr: str, *keys: str, **kwargs) -> None:
        """Try set target.attr from kwargs matching keys."""
        keys_ = (attr,) if not keys else keys
        ob = Serializable._try_get(*keys_, **kwargs)
        setattr(target, attr, ob) if ob else None

    @staticmethod
    def _try_get(*keys: str, **kwargs) -> Any:
        """Try to get a kwargs value that matches keys."""
        ob = kwargs
        for i, key in enumerate(keys):
            ob = ob[key] if (ob and key in ob) else None
        return ob


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
    def _attrs(self) -> List[str]:
        """List of attributes."""
        return ['n_lines', 'program_path']

    @property
    def name(self) -> Optional[str]:
        """Get program name without path and extension."""
        return Path(self.program_path).stem if self.program_path else None

    @staticmethod
    def from_dict(**kwargs) -> Program:
        """Restore Program object."""
        return Serializable._load(Program(), **kwargs)


class FuncResult(Timeable, Serializable):
    """Analysis results for one function of the input program.

    Attributes:
        name (str): Function name.
        infinite (bool): True if no valid derivation exists.
        variables (List[str]): List of program variables.
        relation (Relation): Relation object; does not
        choices (Choices): A choice vector-object.
        bound (Bound): A bound of mwp-bounds.
        inf_flows (str): Description of problematic flows.
        index (int): Degree of derivation choice.
        func_code (str): Function source code.
    """

    def __init__(self, name: str, infinite: bool = False,
                 variables: Optional[List[str]] = None,
                 relation: Optional[Relation] = None,
                 choices: Optional[Choices] = None,
                 bound: Optional[Bound] = None,
                 inf_flows: Optional[str] = None,
                 index: int = -1, func_code: str = None):
        super().__init__()
        self.name: str = name
        self.infinite: bool = infinite
        self.variables: List[str] = variables or []
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
        txt += f'variables: {len(self.variables)}'
        if self.infinite:
            txt += ' • num-bounds: '
            txt += '0 (infinite)'
            if self.inf_flows:
                txt += f'\nProblematic flows: {self.inf_flows}'
        elif len(self.variables):
            txt += ' • num-bounds: '
            txt += f'{self.n_bounds:,}\n'
            txt += f'{Bound.show(self.bound, True, True)}'
        return txt

    @property
    def _attrs(self) -> List[str]:
        """List of attribute names."""
        return 'name,infinite,start_time,end_time,variables,' \
               'inf_flows,index,func_code'.split(',')

    @property
    def n_vars(self) -> int:
        """Number of variables."""
        return len(self.variables)

    @property
    def n_bounds(self) -> int:
        """Number of bounds."""
        return self.choices.n_bounds if self.choices else 0

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
    def from_dict(name: str = None, **kwargs) -> FuncResult:
        """Deserialize a function result."""
        func = Serializable._load(FuncResult(name), **kwargs)
        matrix = FuncResult._try_get('relation', 'matrix', **kwargs)
        if matrix:
            func.relation = Relation(func.variables, decode(matrix))
        choices = FuncResult._try_get('choices', **kwargs)
        if choices:
            func.choices = Choices(choices)
        bound = FuncResult._try_get('bound', **kwargs)
        if bound:
            func.bound = Bound(bound)
        return func


class FuncLoops(Timeable, Serializable):
    """Analysis result for a function with loops, when running
    loop analysis mode. `FuncLoops` captures the results for all loops
    inside their parent function.

    Attributes:
        name (str): Containing function name.
        loops (Dict[str, LoopResult]): Function loop analysis results.
    """

    def __init__(self, name: str = None):
        super().__init__()
        self.name: str = name
        self.loops: List[LoopResult] = []

    def __str__(self):
        loops = [f'{i}. {lp}' for i, lp in enumerate(self.loops)]
        lp_str = ('\n# ' + '\n# '.join(loops)) if loops else ''
        return (f'function: {self.name} • loops: {self.n_loops}'
                f' • time: {self.dur_ms:,} ms{lp_str}')

    @property
    def _attrs(self) -> List[str]:
        return ['name', 'start_time', 'end_time']

    @property
    def _ser_list(self) -> List[Tuple[str, Type[Serializable]]]:
        return [('loops', LoopResult)]

    @property
    def n_loops(self) -> int:
        """Number of analyzed loops"""
        return len(self.loops)

    @staticmethod
    def from_dict(**kwargs) -> FuncLoops:
        """Restore FuncLoops object."""
        return Serializable._load(FuncLoops(), **kwargs)


class LoopResult(Timeable, Serializable):
    """Analysis result for one loop.

    Attributes:
        loop_code (str): The analyzed loop.
        variables (Dict[str, VResult]): Results by variable.
    """

    def __init__(self, loop_code: str = None):
        super().__init__()
        self.loop_code: str = loop_code
        self.variables: Dict[str, VResult] = {}

    def __str__(self):
        txt = f'{self.loop_desc}'
        if not self.variables:
            txt += f'\nvariables: {len(self.variables)}'
        else:
            txt += f'\nlinear: {", ".join(self.linear) or "—"}'
            txt += f'\nindependent: {", ".join(self.weak) or "—"}'
            txt += f'\npolynomial: {", ".join(self.poly) or "—"}'
            txt += f'\ninfinity: {", ".join(self.exp) or "—"}'
            txt += f'\n{self.as_bound.show(True, True)}'
        return txt

    @property
    def _attrs(self) -> List[str]:
        return ['loop_code', 'start_time', 'end_time']

    @property
    def _ser_dict(self) -> List[Tuple[str, str, Type[Serializable]]]:
        return [('variables', 'name', VResult)]

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
        header = self.loop_code.split('\n', 1)[0].strip()
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

    @property
    def as_bound(self) -> Bound:
        """Combines variable results to a Bound-type."""
        return Bound(dict([
            (v, res.bound.bound_str) for v, res in
            sorted(self.variables.items()) if res.bound]))

    def var_sat(self, cond: Callable[[VResult], bool]) -> List[str]:
        """List of variables satisfying a condition."""
        return [v for v, r in self.variables.items() if cond(r)]

    @staticmethod
    def from_dict(**kwargs) -> LoopResult:
        """Restore LoopResult object."""
        return Serializable._load(LoopResult(), **kwargs)


class VResult(Serializable):
    """Analysis result for a single variable.

    Attributes:
        name (str): Variable name.
        is_m (bool): Has maximal linear bound.
        is_w (bool): Has weak polynomial bound.
        is_p (bool): Has polynomial bound.
        bound (Optional[MwpBound]): A bound (if exists).
        choices (Optional[Choice]): Bound choices.
    """

    def __init__(self, name: str = None, is_m: bool = False,
                 is_w: bool = False, is_p: bool = False,
                 bound: MwpBound = None, choices: Choices = None):
        self.name = name
        self.bound = bound
        self.choices = choices
        self._is_m = False
        self._is_w = False
        self._is_p = False
        self.is_m = is_m
        self.is_w = is_w
        self.is_p = is_p

    @property
    def _attrs(self) -> List[str]:
        return 'name,is_m,is_w,is_p'.split(',')

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

    def to_dict(self) -> dict:
        """Serialize a VResult object."""
        result = super().to_dict()
        if self.choices:
            result['choices'] = self.choices.valid
        if self.bound:
            result['bound'] = self.bound.bound_str
        return result

    @staticmethod
    def from_dict(**kwargs) -> VResult:
        """Restore VResult object."""
        r = Serializable._load(VResult(), **kwargs)
        choices = VResult._try_get('choices', **kwargs)
        r.choices = Choices(choices) if choices else None
        bound = VResult._try_get('bound', **kwargs)
        r.bound = MwpBound(bound) if bound else None
        return r


class Result(Timeable, Serializable):
    """Captures analysis result and details about the analysis process.

    Attributes:
        program (Program): Information about analyzed C File.
        relations (Dict[str, FuncResult]): Dictionary of function results.
        loops (Dict[str, FuncLoops]): Dictionary of function loop results.
    """

    def __init__(self):
        super().__init__()
        self.program: Program = Program()
        self.relations: Dict[str, FuncResult] = {}
        self.loops: Dict[str, FuncLoops] = {}

    @property
    def _attrs(self) -> List[str]:
        """List of attribute names."""
        return ['start_time', 'end_time']

    @property
    def _ser_attrs(self) -> List[Tuple[str, Type[Serializable]]]:
        return [('program', Program)]

    @property
    def _ser_dict(self) -> List[Tuple[str, str, Type[Serializable]]]:
        return [('loops', 'name', FuncLoops),
                ('relations', 'name', FuncResult)]

    @property
    def n_functions(self) -> int:
        """Number of functions in analyzed program."""
        return len(self.relations.keys())

    @property
    def n_loops(self) -> int:
        """Number of loops in functions of analyzed program."""
        return sum([lp.n_loops for lp in self.loops.values()])

    def add_relation(self, result: FuncResult) -> None:
        """Appends function analysis to result."""
        self.relations[result.name] = result
        Result.pretty_print(str(result))

    def add_loop(self, result: FuncLoops) -> None:
        """Append loop analysis to result."""
        self.loops[result.name] = result
        Result.pretty_print(str(result))

    @staticmethod
    def pretty_print(txt: str, line_w: int = 50, hb: str = '─') -> str:
        """Draws a colored box around text before display.

        Arguments:
            txt: Some text to display.
            line_w: Formatted text line width.
            hb: Horizontal bar box-drawing character

        Returns:
             Formatted text.
        """
        color, endc = '\033[96m', '\033[0m'
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
                elif ' ' in vals[:line_w] and len(vals) > line_w:
                    split_at = 1 + vals[:line_w].rindex(' ')
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
        return parts

    def get_func(self, name: Optional[str] = None) \
            -> Union[FuncResult, FuncLoops, Dict[str, FuncResult],
                     Dict[str, FuncLoops]]:
        """Returns analysis result for function(s).

        Here "analysis" means either whole-function analysis, or loop
        analysis, based on executed analysis mode; they cannot co-exist in
        the same result.

        * If `name` argument is provided and key exists, returns a result
         for exact value match.
        * If program contained exactly 1 function, returns result for that
          function.
        * Otherwise, returns a dictionary of results for each analyzed
          function, as in: `<function_name, analysis_result>`

        Arguments:
            name: Name of function.

        Returns:
            A function analysis result, or a dictionary of results.
        """
        if name:
            if name in self.relations:
                return self.relations[name]
            if name in self.loops:
                return self.loops[name]
        if self.n_functions == 1:
            key = next(iter(self.relations))
            return self.relations[key]
        if self.n_loops == 1:
            key = next(iter(self.loops))
            return self.loops[key]
        return self.relations if self.relations else self.loops

    def log_result(self) -> Result:
        """Display here all interesting stats about analysis result."""
        if self.n_functions == 0 and self.n_loops == 0:
            logger.warning("Nothing was analyzed")
        logger.info(f'Total time: {self.dur_s} s ({self.dur_ms} ms)')
        return self

    @staticmethod
    def from_dict(**kwargs) -> Result:
        """Restore Result object."""
        return Serializable._load(Result(), **kwargs)
