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
    def get_writer(self) -> Union[LatexTableWriter, SpaceAlignedTableWriter]:
        """Choose table writer."""
        return LatexTableWriter() if self.format == 'tex' \
            else SpaceAlignedTableWriter()

    @staticmethod
    def headers() -> List[str]:
        """Specify table headers."""
        return ['Benchmark', 'func', 'LOC', 't/ms',
                '#var', '#bound', 'bound value']

    @staticmethod
    def table_entry(result, func_result, first, max_char=500) \
            -> Tuple[any, ...]:
        """Generate one table row.

        Arguments:
            result: a result object (covers entire C file)
            func_result: analysis result of one function (possibly 1 of N)
            first: True if this is the first function of the C file
            max_char: clip table text, if it exceeds max_chars value.

        Returns:
            Formatted table row.
        """
        loc_time = (result.program.n_lines, result.dur_ms) \
            if first else ('', '')
        b_format = func_result.bound.show(True) if func_result.bound else '∞'
        b_format = b_format[:max_char] + '...' \
            if len(b_format) > max_char else b_format
        return (result.program.name, func_result.name, *loc_time,
                func_result.n_vars, func_result.n_bounds, b_format)

    def build_matrix(self) -> List[Tuple[any]]:
        """Construct table data."""
        return [e for sublist in [[
            self.table_entry(ex, ex.get_func(f_name), i == 0)
            for i, f_name in enumerate(ex.relations.keys())]
            for _, ex in sorted(self.results.items())] for e in sublist]

    def generate(self) -> None:
        """Generate a table plot, then show it and save it to file."""
        if not self.has_data:
            return
        fn = join(self.out_dir, self.filename)
        writer = self.get_writer
        writer.headers = self.headers()
        writer.value_matrix = self.build_matrix()
        writer.write_table()
        writer.dump(fn)
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
        print(f"Invalid directory {args.in_}")
    else:
        Plot(args.in_, args.out, args.fmt).generate()
