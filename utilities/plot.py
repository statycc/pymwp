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
    --help (): Command help.
"""

import argparse
import glob
import sys
from json import JSONDecodeError
from os.path import join, isdir, abspath, dirname
from typing import Dict, Union, List

# noinspection PyPackageRequirements
from pytablewriter import SpaceAlignedTableWriter
# noinspection PyProtectedMember,PyPackageRequirements
from pytablewriter.writer.text._latex import LatexWriter

# run relative to repository root
cwd = abspath(join(dirname(__file__), '../'))
sys.path.insert(0, cwd)

# flake8: noqa: E402
from pymwp import Result
from pymwp.bound import MwpBound
from pymwp.file_io import load_result


def cmd_args(parser):
    """Define available arguments."""
    parser.add_argument(
        "-i", "--in",
        dest="in_dir",
        metavar="IN",
        default=join(cwd, 'output'),
        help='Path to analysis results directory (default: output)',
    )
    parser.add_argument(
        "-o", "--out",
        action='store',
        default=join(cwd, 'output'),
        help="Directory to save generated plot (default: output)"
    )
    parser.add_argument(
        "-f", '--fmt',
        action="store",
        default="plain",
        metavar="FORMAT",
        help='output format: {tex, plain} (default: plain)'
    )
    return parser.parse_args()


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


class Plot:
    """Main plotting routine."""

    def __init__(self, src_path: str, out_dir: str, table_format: str):
        self.src = src_path
        self.out_dir = out_dir
        self.format = table_format
        self.results: Dict[str, Result] = {}
        # parse the input data
        for file in glob.glob(join(self.src, "*.json")):
            try:
                res = load_result(file)
            except JSONDecodeError:
                continue
            if res.program.name:
                self.results[res.program.name] = res
        self.has_data = len(self.results) > 0
        if not self.has_data:
            print('Found no results to plot.')

    def filename(self, extra='') -> str:
        """Generate table file name based on format."""
        ext = 'tex' if self.format == 'tex' else 'txt'
        return f'__table{extra}.{ext}'

    def writer(self) -> Union[MyLatexTableWriter, SpaceAlignedTableWriter]:
        """Gets the choice table writer."""
        return MyLatexTableWriter() if self.format == 'tex' \
            else SpaceAlignedTableWriter()

    @staticmethod
    def texify_bound(bound):
        """An attempt to latex-format of a bound expression."""

        def var_format(txt):
            return r'\texttt{' + str(txt) + '}'

        def bound_format(mwp):
            mwp.z.op = r'\times'
            mwp.x.var_fmt = mwp.y.var_fmt = mwp.z.var_fmt = var_format
            return str(MwpBound.bound_poly(mwp)) \
                .replace('max', r'\text{max}')

        # construct formatted bounds expressions for each variable
        leq = r'\leq'
        var_bounds = [f"{var_format(k)}' {leq} {bound_format(v)}"
                      for k, v in bound.bound_dict.items()
                      if str(k) != str(v)]  # only keep "significant"

        # separator between bound expressions
        # separate the "and" to allow easier line breaks
        bound_exp = (r'$ $\land$ $'.join(var_bounds))
        return f'${bound_exp}$'  # in math mode

    @staticmethod
    def headers() -> List[str]:
        """Specify table headers."""
        return ['#', 'Benchmark', 'loc', 'time', 'vars', 'bounds']

    @staticmethod
    def text_fmt(bound, pad, wrap_at):
        return bound if len(bound) < wrap_at else \
            bound.replace('∧', f'\n{" " * pad}∧')

    def build_matrix(self):
        """Construct table data."""

        inputs = [e for sublist in [[
            (ex, ex.get_func(f_name)) for f_name in ex.relations.keys()]
            for (_, ex) in sorted(self.results.items())] for e in sublist]

        bound_dict = [
            (i + 1, (Plot.texify_bound(f.bound), p))
            for i, f, p in [(i, f, f.bound.show(True, True)
            if f.bound else None) for (i, (_, f)) in enumerate(inputs)]
            if f.n_bounds > 0 and len(p) > 0]

        return [(i + 1, (f'{ex.program.name}: {fun.name}'
                         if ex.n_functions > 1 else ex.program.name),
                 ex.program.n_lines, fun.dur_ms, fun.n_vars, fun.n_bounds)
                for i, (ex, fun) in enumerate(inputs)], dict(bound_dict)

    def generate(self) -> None:
        """Generate a table plot, then show it, and save it to file."""
        if not self.has_data:
            return
        fn = join(self.out_dir, self.filename())
        mn = join(self.out_dir, self.filename('_map'))

        t1_writer = SpaceAlignedTableWriter()
        f1_writer, f2_writer = self.writer(), self.writer()

        f1_writer.headers = t1_writer.headers = self.headers()
        f1_writer.value_matrix, _ = t1_values, bounds = self.build_matrix()
        f1_writer.dump(fn)  # write to file

        f2_writer.headers = ['#', 'bound']
        f2_writer.value_matrix = [
            (k, tex if self.format == 'tex' else str_b)
            for k, (tex, str_b) in bounds.items()]
        f2_writer.dump(mn)

        # display text tables
        pad, wrap_at = len(str(list(bounds)[-1])) + 2, 52
        t1_writer.value_matrix = t1_values
        t1_writer.write_table()
        print()
        [print(f'{k:<{pad}}' + self.text_fmt(v, pad, wrap_at))
         for k, (_, v) in bounds.items()]
        print()
        print(f'Wrote tables to: {fn}\nand to: {mn}')


if __name__ == '__main__':
    args = cmd_args(argparse.ArgumentParser())
    if not isdir(args.in_dir):
        print(f"Non-existent directory {args.in_dir}")
    else:
        Plot(args.in_dir, args.out, args.fmt).generate()
