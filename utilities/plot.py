#!/usr/bin/env python3

# noinspection PyUnresolvedReferences
"""
Makes a table plot of analysis results.

<h4>Usage:</h4>

```
python3 utilities/plot.py  --in IN --out OUT --fmt FORMAT
```

Arguments:
    --in (str): Directory of analysis results.
    --out (str): Directory where to save generated plot.
    --fmt (str): Plot format: `tex` or `plain`.
"""

import argparse
import glob
import sys
from json import JSONDecodeError
from os.path import join, isdir, abspath, dirname
from typing import Dict, Union, List, Tuple, Optional, Any

# noinspection PyPackageRequirements
from pytablewriter import SpaceAlignedTableWriter as SpaceTable
# noinspection PyProtectedMember,PyPackageRequirements
from pytablewriter.writer.text._latex import LatexWriter

# run relative to repository root
cwd = abspath(join(dirname(__file__), '../'))
sys.path.insert(0, cwd)

# flake8: noqa: E402
from pymwp import Bound, MwpBound
from pymwp.result import Result, FuncResult, FuncLoops, LoopResult
from pymwp.file_io import load_result


def cmd_args(parser):
    """Define available arguments."""
    parser.add_argument(
        '-i', '--in',
        dest='in_dir',
        metavar='IN',
        default=join(cwd, 'output'),
        help='Directory of analysis results.')
    parser.add_argument(
        '-o', '--out',
        action='store',
        default=join(cwd, 'output'),
        help='Directory where to save generated plot.')
    parser.add_argument(
        '-f', '--fmt',
        action='store',
        default='plain',
        metavar='FMT',
        type=str.lower,
        help='Plot format: tex or plain.')
    return parser.parse_args()


def parse_files(src) -> Dict[str, Result]:
    results = {}
    for file in glob.glob(join(src, "*.json")):
        try:
            res = load_result(file)
        except JSONDecodeError:
            continue
        if res.program.name:
            results[res.program.name] = res
    return results


class MyLatexTableWriter(LatexWriter):
    """Custom LaTeX table writer."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.char_right_side_row = r" \\"

    @property
    def format_name(self) -> str:
        return "latex_table"

    def _get_opening_row_items(self) -> List[str]:
        return ["".join([
            r"\begin{tabular}{",
            "{:s}".format("".join(self._get_col_align_char_list())),
            r"}", ])]

    @staticmethod
    def _str_escape(txt):
        return txt.replace('_', r'\_').replace('#', r'\#')

    def _to_header_item(self, col_dp, value_dp) -> str:
        return MyLatexTableWriter._str_escape(
            super()._to_header_item(col_dp, value_dp))

    def _to_row_item(self, row_idx: int, col_dp, value_dp) -> str:
        row_item = MyLatexTableWriter._str_escape(
            super()._to_row_item(row_idx, col_dp, value_dp))
        if self._is_math_parts(value_dp):
            return self._to_math_parts(row_item)
        return row_item

    def _get_header_row_separator_items(self) -> List[str]:
        return [""]

    def _get_closing_row_items(self) -> List[str]:
        return [r"\end{tabular}"]

    @staticmethod
    def texify_var(txt) -> str:
        """LaTeX format a variable"""
        return r'\texttt{' + str(txt) + '}'

    @staticmethod
    def texify_mwp(var: str, mwp: MwpBound):
        """LaTeX-format an mwp-bound."""
        # An attempt to latex-format of a bound expression
        # construct formatted bounds expressions for each variable
        leq, mwp.z.op = r'\leq', r'\times'
        fmt = MyLatexTableWriter.texify_var
        mwp.x.var_fmt = mwp.y.var_fmt = mwp.z.var_fmt = fmt
        bound = str(MwpBound.bound_poly(mwp)).replace('max', r'\text{max}')
        return f"{fmt(var)}' {leq} {bound}"

    @staticmethod
    def texify_bound(bound: Bound):
        """LaTeX-format a bound."""
        var_bounds = [MyLatexTableWriter.texify_mwp(k, v) for k, v
                      in bound.bound_dict.items() if str(k) != str(v)]
        # separate the "and" to allow easier line breaks
        bound_exp = r'$ $\land$ $'.join(var_bounds)
        return f'${bound_exp}$'


class Plot:
    """Main plotting routine."""

    def __init__(self, src_path: str, out_dir: str, table_format: str):
        self.src = src_path
        self.out_dir = out_dir
        self.format = table_format
        self.results = parse_files(src_path)
        self.has_data = len(self.results) != 0
        if not self.has_data:
            print('Found no results to plot.')

    def filename(self, extra: str = '') -> str:
        """Generate table file name based on format."""
        ext = 'tex' if self.format == 'tex' else 'txt'
        return f'__table{extra}.{ext}'

    def writer(self) -> Union[MyLatexTableWriter, SpaceTable]:
        """Gets the choice table writer."""
        return MyLatexTableWriter() if self.format == 'tex' \
            else SpaceTable()

    @property
    def relations(self) -> List[Tuple[Result, FuncResult]]:
        """Flat list of relation results."""
        items = [[(ex, ex.get_func(f_name))
                  for f_name in ex.relations.keys()]
                 for (_, ex) in sorted(self.results.items())]
        return [e for sub in items for e in sub]

    @property
    def loops(self) -> List[Tuple[int, Result, FuncLoops, LoopResult]]:
        """Flat list of loop analysis results."""
        result = []
        for (_, ex) in sorted(self.results.items()):
            for f_name in ex.loops.keys():
                loop_n = 1
                for loop in ex.loops[f_name].loops:
                    result.append((loop_n, ex, ex.loops[f_name], loop))
                    loop_n += 1
        return result

    @property
    def pad(self) -> int:
        """Get table display leftpad by number of table items."""
        items = len(self.relations) + len(self.loops)
        return len(str(items)) + 2

    @staticmethod
    def table_format_bound(n: int, bound: Bound, pad=5) \
            -> Optional[Tuple[int, Tuple[str, str, str]]]:
        """Convert a bound to various display-formats."""
        plain = bound.show(True, True) if bound else ''
        if len(plain) == 0:
            return None
        tex = MyLatexTableWriter.texify_bound(bound)
        wrapped = (plain if len(plain) < 52 else
                   plain.replace('∧', f'\n{" " * pad}∧'))
        terminal = f'{n:<{pad}}{wrapped}'
        return n, (tex, plain, terminal)

    @staticmethod
    def fun_name(ex: Result, fun: FuncResult) -> str:
        """Formatted benchmark name for a function result."""
        endf = f': {fun.name}' if ex.n_functions > 1 else ''
        return f'{ex.program.name}{endf}'

    @staticmethod
    def loop_name(res: Result, lf: FuncLoops, n: int):
        """Formatted benchmark name for a loop result."""
        mid = f', {lf.name}' if res.program.name != lf.name else ''
        return f'{res.program.name}{mid}: L{n}'

    def loop_data(self, offset=1):
        """Construct table data of loop analyses results."""
        return [((i + offset, Plot.loop_name(ex, fun, n),
                  lp.n_lines, lp.dur_ms, lp.n_vars, lp.n_bounded),
                 Plot.table_format_bound(i + offset, lp.as_bound, self.pad))
                for i, (n, ex, fun, lp) in enumerate(self.loops)]

    def func_data(self, offset=1):
        """Construct table data of function analyses results."""
        return [((i + offset, Plot.fun_name(ex, fun), ex.program.n_lines,
                  fun.dur_ms, fun.n_vars, fun.n_bounds),
                 Plot.table_format_bound(i + offset, fun.bound, self.pad))
                for i, (ex, fun) in enumerate(self.relations)]

    def build_loop_table(self, offset=1) -> Tuple[List, Dict]:
        """Construct table data of loop analyses results."""
        relation_data, bounds = list(zip(*self.loop_data(offset)))
        bounds = dict([b for b in bounds if b])
        return relation_data, bounds

    def build_table(self) -> Tuple[List, List, Dict]:
        """Construct table data of function analyses results."""
        relations, loops, bounds1, bounds2 = [], [], {}, {}
        if self.relations:
            relations, bounds = list(zip(*self.func_data()))
            bounds1 = dict([b for b in bounds if b])
        if self.loops:
            loops, bounds = list(zip(*self.loop_data(len(relations))))
            bounds2 = dict([b for b in bounds if b])
        return relations, loops, {**bounds1, **bounds2}

    def write_table(self, file_name, data, headers, writes) -> None:
        """Generate, display, and save a data table."""
        if data:
            fn = join(self.out_dir, self.filename(file_name))
            t_writer, f_writer = SpaceTable(), self.writer()
            t_writer.headers = f_writer.headers = headers
            f_writer.value_matrix = t_writer.value_matrix = data
            t_writer.write_table()  # display table
            f_writer.dump(fn)  # write to file
            writes.append(fn)
            print()

    def write_bounds(self, bounds, writes) -> None:
        """Generate and display bounds table."""
        if bounds:
            mn = join(self.out_dir, self.filename('_map'))
            b_writer = self.writer()
            b_writer.headers = ['#', 'bound']
            tex, plain, term = list(zip(*bounds.values()))
            f2_values = tex if self.format == 'tex' else plain
            b_writer.value_matrix = list(zip(bounds, f2_values))
            print('\n'.join(term))  # display table
            b_writer.dump(mn)  # write to file
            writes.append(mn)
            print()

    def generate(self) -> None:
        """Generate and plot all relevant tables."""
        writes = []
        if self.has_data:
            fun_data, loop_data, bounds = self.build_table()
            head1 = '#,Benchmark,loc,time,vars,bounds'.split(',')
            self.write_table('', fun_data, head1, writes)
            head2 = '#,Benchmark,loc,time,vars,vb'.split(',')
            self.write_table('_loops', loop_data, head2, writes)
            self.write_bounds(bounds, writes)
        if writes:
            print(f'Wrote tables to:\n+ ' + '\n+ '.join(writes))


if __name__ == '__main__':
    args = cmd_args(argparse.ArgumentParser())
    if not isdir(args.in_dir):
        print(f"Non-existent directory {args.in_dir}")
    else:
        Plot(args.in_dir, args.out, args.fmt).generate()
