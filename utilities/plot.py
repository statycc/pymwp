#!/usr/bin/env python3

"""
Makes a table plot of analysis results.

# Usage

python3 utilities/plot.py [ARGS]

Run python3 utilities/plot.py --help for assistance
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

from pymwp import Result
from pymwp.bound import MwpBound
from pymwp.file_io import load_result


class MyLatexTableWriter(LatexWriter):
    @property
    def format_name(self) -> str:
        return "latex_table"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.char_right_side_row = r" \\"

    def _get_opening_row_items(self) -> List[str]:
        return ["".join([
            r"\begin{tabular}{",
            "{:s}".format("".join(self._get_col_align_char_list())),
            r"}", ])]

    @staticmethod
    def _str_escape(str):
        return str.replace('_', '\_').replace('#', '\#')

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
        var_bounds = [f"{var_format(k)}' \leq {bound_format(v)}"
                      for k, v in bound.bound_dict.items()
                      if str(k) != str(v)]  # only keep "significant"

        # separator between bound expressions
        # separate the "and" to allow easier line breaks
        bound_exp = ('$ $\land$ $'.join(var_bounds))

        return f'${bound_exp}$'  # in math mode

    @staticmethod
    def headers() -> List[str]:
        """Specify table headers."""
        return ['#', 'Benchmark', 'loc', 'time', 'vars', 'bounds']

    def build_matrix(self):
        """Construct table data."""

        inputs = [e for sublist in [[
            (ex, ex.get_func(f_name)) for f_name in ex.relations.keys()]
            for (_, ex) in sorted(self.results.items())] for e in sublist]

        bound_dict = [
            (i + 1, Plot.texify_bound(f.bound) if self.format == 'tex' else p)
            for i, f, p in [(i, f, f.bound.show_poly(True, True)
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

        txt_writer = SpaceAlignedTableWriter()
        f1_writer, f2_writer = self.writer(), self.writer()

        f1_writer.headers = txt_writer.headers = self.headers()
        f1_writer.value_matrix, bd = self.build_matrix()
        f1_writer.dump(fn)  # write to file

        f2_writer.headers = ['#', 'bound']
        f2_writer.value_matrix = [(k, v) for k, v in bd.items()]
        f2_writer.dump(mn)

        txt_writer.value_matrix, _ = self.build_matrix()
        txt_writer.write_table()  # show the table

        print(f'Wrote tables to: {fn}\nand to: {mn}')


def cmd_args(parser):
    """Define available arguments."""
    parser.add_argument(
        '-r', '--in',
        action='store',
        dest="in_",
        default=join(cwd, 'output'),
        help='path to analysis results directory (default: output)',
    )
    parser.add_argument(
        "-o", "--out",
        action='store',
        default=join(cwd, 'output'),
        help="directory to save generated plot (default: output)"
    )
    parser.add_argument(
        "-f", '--fmt',
        action="store",
        default="plain",
        help='output format: {tex, plain} (default: plain)'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = cmd_args(argparse.ArgumentParser())
    if not isdir(args.in_):
        print(f"Non-existent directory {args.in_}")
    else:
        Plot(args.in_, args.out, args.fmt).generate()
