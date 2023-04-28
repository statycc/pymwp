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
from typing import Dict, Union, List, Tuple

# noinspection PyPackageRequirements
from pytablewriter import SpaceAlignedTableWriter, LatexTableWriter

# run relative to repository root
cwd = abspath(join(dirname(__file__), '../'))
sys.path.insert(0, cwd)

from pymwp import Result
from pymwp.file_io import load_result


class LatexTableWriterExt(LatexTableWriter):
    """Overrides some LaTeX table writer behavior"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.char_right_side_row = r" \\"

    def _get_opening_row_items(self) -> List[str]:
        return ["".join([
            r"\begin{tabular}{",
            "{:s}".format("".join(self._get_col_align_char_list())),
            r"}", ])]

    def _get_header_row_separator_items(self) -> List[str]:
        return [r"\toprule"]

    def _get_closing_row_items(self) -> List[str]:
        return [r"\end{tabular}"]

    def __is_requre_verbatim(self, value_dp) -> bool:
        return False

    def __verbatim(self, value: str) -> str:
        return f"{value:s}"

    def _to_header_item(self, col_dp, value_dp) -> str:
        return super()._to_header_item(col_dp, value_dp) \
            .replace('\\verb|', '').replace('|', '').strip()

    def _to_row_item(self, row_idx: int, col_dp, value_dp) -> str:
        row_item = super()._to_row_item(row_idx, col_dp, value_dp)
        if self._is_math_parts(value_dp):
            return self._to_math_parts(row_item)
        return row_item.replace('\\verb|', '').replace('|', '').strip()


class Plot:

    def __init__(self, src_path: str, out_dir: str, table_format: str):
        self.src = src_path
        self.out_dir = out_dir
        self.format = table_format
        self.results: Dict[str, Result] = {}
        json_files = glob.glob(join(self.src, "*.json"))
        for file in json_files:
            try:
                res = load_result(file)
            except JSONDecodeError:
                continue
            if res.program.name:
                self.results[res.program.name] = res
        self.has_data = len(self.results) > 0
        if not self.has_data:
            print('Found no results to plot.')

    @property
    def filename(self) -> str:
        """generate table file name based on format."""
        ext = 'tex' if self.format == 'tex' else 'txt'
        return f'table.{ext}'

    @property
    def get_writer(self) \
            -> Union[LatexTableWriterExt, SpaceAlignedTableWriter]:
        """Choose table writer."""
        return LatexTableWriterExt() if self.format == 'tex' \
            else SpaceAlignedTableWriter()

    @staticmethod
    def headers() -> List[str]:
        """Specify table headers."""
        return ['Benchmark', 'loc', 'func', 't.ms',
                'vars', 'bounds', 'bound']

    @staticmethod
    def table_entry(result, func_result) -> Tuple[any, ...]:
        """Generate one table row (plain text optimized).

        Arguments:
            result: a result object (covers entire C file)
            func_result: analysis result of one function (possibly 1 of N)

        Returns:
            Formatted table row.
        """
        return (result.program.name, result.program.n_lines,
                func_result.name, func_result.dur_ms,
                func_result.n_vars, func_result.n_bounds,
                func_result.bound.show(compact=True, significant=True)
                if func_result.bound else '∞')

    @staticmethod
    def tex_entry(result, func_result) -> Tuple[any, ...]:
        """Generate one table for latex table

        Arguments:
            result: a result object (covers entire C file)
            func_result: analysis result of one function (possibly 1 of N)

        Returns:
            Formatted table row.
        """
        prime = "'"
        prog_name = result.program.name.replace('_', '\_')
        tt = lambda v: "\scriptsize \\texttt{" + str(v) + "}"
        bound_fmt = lambda b: ' $\land$ '.join([
            f"{tt(str(k) + prime)}$\leq${v}" for k, v in b.items()
            if str(k) != str(v)])

        return (prog_name, result.program.n_lines,
                func_result.name, func_result.dur_ms,
                func_result.n_vars, func_result.n_bounds,
                bound_fmt(func_result.bound.bound_dict)
                if func_result.bound else '$\infty$')

    def build_matrix(self, fmt_func) -> List[Tuple[any]]:
        """Construct table data."""
        return [e for sublist in [[fmt_func(
            ex, ex.get_func(f_name))
            for f_name in ex.relations.keys()]
            for _, ex in sorted(self.results.items())] for e in sublist]

    def generate(self) -> None:
        """Generate a table plot, then show it and save it to file."""
        if not self.has_data:
            return
        fn = join(self.out_dir, self.filename)
        # file writer, screen-writer, screen is always plain text
        f_writer, s_writer = self.get_writer, SpaceAlignedTableWriter()
        f_writer.headers = s_writer.headers = self.headers()
        f_writer.value_matrix = self.build_matrix(self.tex_entry)
        s_writer.value_matrix = self.build_matrix(self.table_entry)
        s_writer.write_table()  # show the table
        f_writer.dump(fn)  # write to file
        print(f'Saved to {fn}')


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
