#!/usr/bin/env python3

"""
This is a utility script for running cProfile on a bunch of C files.

USAGE: see docs/utilities.md
"""

import os
import asyncio
import pstats
import logging
import argparse
import subprocess
import signal
import time

from os import listdir, makedirs, remove
from os.path import abspath, join, dirname, basename, splitext, exists, isfile

logger = logging.getLogger(__name__)
cwd = abspath(join(dirname(__file__), '../'))  # repository root


class Profiler:

    def __init__(self, src, dest, args):
        """Initialize profiler utility"""
        self.output = dest
        self.sort = args.sort
        self.timeout = args.timeout
        self.start_time = self.end_time = 0
        self.lines = args.lines if args.lines > 0 else None
        self.file_list = Profiler.find_c_files(src, args.skip, args.only)
        self.pad = Profiler.longest_file_name(self.file_list)
        self.ignore = ".gitignore"
        self.divider_len = 50
        self.no_external = args.no_external
        self.callers = args.callers

    @property
    def file_count(self):
        """Number of C files to profile."""
        return len(self.file_list)

    @property
    def total_time(self):
        """Total time to run profile on all files."""
        return self.end_time - self.start_time

    @staticmethod
    def find_c_files(src, skip_list, incl_list):
        """Recursively look for C files in src directory."""
        files = []
        for parent_path, _, filenames in os.walk(src):
            for f in filenames:
                name = Profiler.filename_only(f)
                extension = basename(splitext(f)[1])
                if extension == '.c' and \
                        name not in skip_list and \
                        (len(incl_list) == 0 or name in incl_list):
                    files.append(join(parent_path, f))
        return files

    @staticmethod
    def filename_only(file):
        """Get file name without path or extension."""
        return basename(splitext(file)[0])

    @staticmethod
    def longest_file_name(file_list):
        """Compute length of longest filename in src directory, excluding
        path."""
        if file_list is None or len(file_list) == 0:
            return 0
        return len(max([
            Profiler.filename_only(c)
            for c in file_list], key=len))

    def ensure_output_dir(self):
        """Make sure output directory exists."""
        # make output directory
        if not exists(self.output):
            makedirs(self.output)
        # add .gitignore file
        if not exists(join(self.output, self.ignore)):
            with open(join(self.output, self.ignore), 'w') as ignore:
                ignore.write("*")

    def clear_temp_files(self):
        """Remove temporary files from output directory."""
        # for all files in output directory
        for f in [join(self.output, f) for f in listdir(self.output)]:
            # must be a file, not txt file, and not .gitignore
            clean_it = isfile(join(self.output, f)) \
                       and '.txt' not in f \
                       and self.ignore not in f
            if clean_it:
                remove(f)

    def write_stats(self, out_file):
        """convert cProfile to plain text and saves to txt file."""
        if exists(out_file) and isfile(out_file):
            with open(out_file + ".txt", 'w') as stream:
                ps = pstats.Stats(out_file, stream=stream)
                # write profile stats
                if self.no_external:
                    ps.sort_stats(self.sort) \
                        .print_stats('pymwp/pymwp', self.lines)
                else:
                    ps.strip_dirs() \
                        .sort_stats(self.sort) \
                        .print_stats(self.lines)
                # top 10 caller stats
                if self.callers:
                    ps.strip_dirs() \
                        .sort_stats(self.sort) \
                        .print_callers(10)
            remove(out_file)

    @staticmethod
    def build_cmd(file_in, file_out):
        """Build cProfile command"""
        return ' '.join([
            'python3 -m cProfile',
            f'-o {file_out}',
            '-m pymwp --no-save --silent',
            file_in
        ])

    def run(self):
        """Run cProfile on all discovered files"""
        self.pre_log()
        self.ensure_output_dir()
        self.start_time = time.monotonic()
        for file in sorted(self.file_list):
            asyncio.run(self.profile_file(file))
        self.end_time = time.monotonic()
        self.clear_temp_files()
        self.post_log()

    async def profile_file(self, c_file):
        """Profile single C file"""
        file_name = Profiler.filename_only(c_file)
        out_file = join(self.output, file_name)
        cmd = Profiler.build_cmd(c_file, out_file)

        timeout = False
        start_time = time.monotonic()
        proc = subprocess.Popen(
            [cmd], cwd=cwd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        try:
            proc.communicate(timeout=self.timeout)
            end_time = time.monotonic()
        except subprocess.TimeoutExpired:
            end_time = time.monotonic()
            proc.send_signal(signal.SIGINT)  # raise stop signal
            time.sleep(2)  # give some time to terminate to capture stats
            proc.kill()  # now force kill it
            timeout = True

        if timeout:
            message = 'timeout'
        elif proc.returncode == 0:
            message = 'done'
        else:
            message = 'error'
        self.write_stats(out_file)

        logger.info(f'{file_name.ljust(self.pad)}... {message}: ' +
                    f'{(end_time - start_time):.2f}s')

    def pre_log(self):
        """Print info before running profiler."""
        self.__log(f'Profiling {self.file_count} C files... ' +
                   f'(limit: {self.timeout} sec)')

    def post_log(self):
        """Print info after running profiler."""
        self.__log(f'Finished after {self.total_time:.2f} seconds.')

    def __log(self, msg):
        """Log something using print and visual dividers."""
        divider = '=' * self.divider_len
        logger.info(f'\n{divider}\n{msg}\n{divider}')


def main():
    """Run profiler using provided args."""
    setup_logger()
    args = _args(argparse.ArgumentParser())
    Profiler(args.in_, args.out, args).run()


def setup_logger():
    """Initialize logger."""
    fmt = "[%(asctime)s]: %(message)s"
    date_fmt = "%H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)
    logger.setLevel(logging.FATAL - 40)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def _args(parser, args=None):
    """Define available arguments."""
    parser.add_argument(
        '--in',
        action='store',
        dest="in_",
        default='c_files',
        help='directory path to C-files (default: c_files)',
    )
    parser.add_argument(
        "--out",
        action="store",
        default=join(cwd, 'profile'),
        help="directory path for storing results (default: profile)",
    )
    parser.add_argument(
        "--sort",
        action="store",
        default='calls',
        help="property to sort by (default: calls)",
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='max. timeout in seconds for one execution (default: 10)')
    parser.add_argument(
        '--lines',
        type=int,
        default=-1,
        help='how many lines of profiler stats to collect ' +
             'e.g. to profile top 10 methods, set this value to 10.')
    parser.add_argument(
        '--skip',
        nargs='+',
        default=[],
        help='space separated list of files to exclude ' +
             '(e.g. --skip dense infinite_2) will not profile matching files'
    )
    parser.add_argument(
        '--only',
        nargs='+',
        default=[],
        help='space separated list of files to include ' +
             '(e.g. --only dense empty) will profile only matching files'
    )
    parser.add_argument(
        "--no-external",
        action='store_true',
        help="exclude package external methods from cProfile results"
    )
    parser.add_argument(
        "--callers",
        action='store_true',
        help="include caller stats"
    )
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
