#!/usr/bin/env python3

"""
This is a utility script for running cProfile on a bunch of C files.

USAGE: see docs/utilities.md
"""

import os
import asyncio
import pstats
import logging
import time
import argparse
import subprocess

from os import listdir, makedirs, remove
from os.path import abspath, join, dirname, basename, splitext, exists, isfile

logger = logging.getLogger(__name__)
cwd = abspath(join(dirname(__file__), '../'))  # set cwd to repository root


class Profiler:

    def __init__(self, src, dest, lines, timeout, sort):
        """Initialize profiler utility"""
        self._output_dir = dest
        self._timeout = timeout
        self._sort = sort
        self._start_time = self._end_time = 0
        self._lines = lines if lines > 0 else None
        self._file_list = Profiler.find_c_files(src)
        self._pad = Profiler.longest_file_name(self._file_list)
        self.ignore = ".gitignore"
        self.divider_len = 50

    @property
    def file_list(self):
        """List of files to profile"""
        return self._file_list

    @property
    def file_count(self):
        """Number of C files to profile."""
        return len(self._file_list)

    @property
    def output(self):
        """Directory where to store results"""
        return self._output_dir

    @property
    def timeout(self):
        """Max timeout, per file"""
        return self._timeout

    @property
    def lines(self):
        """Number of pstat lines to output"""
        return self._lines

    @property
    def pad(self):
        """Longest file name in file_list"""
        return self._pad

    @property
    def sort(self):
        """cProfile stats sort order."""
        return self._sort

    @property
    def total_time(self):
        """Total time to run profile on all files."""
        return self._end_time - self._start_time

    @staticmethod
    def find_c_files(src):
        """Recursively look for C files in src directory."""
        files = []
        for parent_path, _, filenames in os.walk(src):
            for f in filenames:
                extension = basename(splitext(f)[1])
                if extension == '.c':
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

    def plain_profile(self, out_file):
        """convert cProfile to plain text."""
        with open(out_file + ".txt", 'w') as stream:
            pstats.Stats(out_file, stream=stream) \
                .sort_stats(pstats.SortKey.TIME) \
                .print_stats(self.lines)

        if isfile(out_file):
            remove(out_file)

    def build_cmd(self, file_in, file_out):
        """Build cProfile command"""
        return ' '.join([
            'python3 -m cProfile',
            f'-s {self.sort}',
            f'-o {file_out}',
            '-m pymwp --no-save --silent',
            file_in
        ])

    def run(self):
        """Run cProfile on all discovered files"""
        self.pre_log()
        self.ensure_output_dir()
        self._start_time = time.monotonic()
        for file in sorted(self.file_list):
            asyncio.run(self.profile_file(file))
        self._end_time = time.monotonic()
        self.clear_temp_files()
        self.post_log()

    async def profile_file(self, c_file):
        """Profile single C file"""
        file_name = Profiler.filename_only(c_file)
        out_file = join(self.output, file_name)
        start_time = time.monotonic()
        cmd = self.build_cmd(c_file, out_file)
        message = ''

        proc = subprocess.Popen(
            [cmd], cwd=cwd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        try:
            proc.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            message = 'timeout'

        end_time = time.monotonic()

        if proc.returncode not in [0, -9]:
            message = 'error'

        if proc.returncode == 0:
            message = 'done'
            self.plain_profile(out_file)

        logger.info(
            f'{file_name.ljust(self.pad)}... {message} ' +
            f': {(end_time - start_time):.2f}s')

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
    Profiler(
        src=args.in_,
        dest=args.out,
        timeout=args.timeout,
        lines=args.lines,
        sort=args.sort
    ).run()


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
        help="directory path for storing results",
    )
    parser.add_argument(
        "--sort",
        action="store",
        default='tottime',
        help="cProfile property to sort by",
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Max. timeout for profiling single example')
    parser.add_argument(
        '--lines',
        type=int,
        default=-1,
        help='How many lines of cProfiler output to include, ' +
             'e.g. to profile top 10 methods, set this value to 10.')

    return parser.parse_args(args)


if __name__ == '__main__':
    main()
