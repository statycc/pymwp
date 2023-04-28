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
from typing import Dict

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
    def filename(self):
        ext = 'tex' if self.format == 'tex' else 'txt'
        return f'table.{ext}'

    @property
    def get_writer(self):
        return LatexTableWriter() if self.format == 'tex' \
            else SpaceAlignedTableWriter()

    @staticmethod
    def headers():
        return ['Benchmark', 'func', 'LOC', 't/ms', '#var', 'bound']

    @staticmethod
    def table_entry(r, f, first, max_char=50):
        loc_time = (r.program.n_lines, r.dur_ms) if first else ('', '')
        b_format = f.bound.show(True) if f.bound else '∞'
        b_format = b_format[:max_char] + '...' \
            if len(b_format) > max_char else b_format
        return (r.program.name, f.name, *loc_time, f.n_vars, b_format)

    def build_matrix(self):
        return [e for sublist in [[
            self.table_entry(ex, ex.get_func(f_name), i == 0)
            for i, f_name in enumerate(ex.relations.keys())]
            for _,ex in sorted(self.results.items())] for e in sublist]

    def generate(self):
        if not self.has_data:
            return
        fn = join(self.out_dir, self.filename)
        writer = self.get_writer
        print('generating table!')
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
        sys.exit()
    Plot(args.in_, args.out, args.fmt).generate()
