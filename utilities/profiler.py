#!/usr/bin/env python3

# noinspection PyUnresolvedReferences
"""
Profiling reveals how many times different functions are called during
analysis. Profiling is based on Python cProfile.

cProfile: https://docs.python.org/3/library/profile.html

## Profiling a single file

Single-file profiling works on both pymwp installed from package registry or
when running pymwp from source, because it requires only the standard Python
module cProfile.

<h4>Usage:</h4>

=== "Distributed version"

    ```
    python -m cProfile pymwp --silent -s ncalls INPUT_FILE
    ```

=== "Running from source"

    ```
    python -m cProfile -m pymwp --silent -s ncalls INPUT_FILE
    ```

Arguments:
    INPUT_FILE (str): Path to input C file.

Note:
    * Argument `--silent` mutes pymwp analysis output.
    * Argument `-s` specifies cProfile output sort order.
    * Additional arguments of cProfile or pymwp can be appended similarly.

cProfile output sort orders:
https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats

## Multi-file profile

Profiler utility module is a wrapper for cProfile. It enables profiling
directories of C files. The results of each execution are stored in
corresponding output files.

One outputs is displayed for each profiled file:

: _**done-ok**_ profiling subprocess terminated without error, note: even if
    pymwp analysis ends with non-0 exit code, it falls into this category
    if it does not crash the subprocess.
: _**error**_ profiling subprocess terminated in error.
: _**timeout**_ profiling subprocess did not terminate within time limit and
    was forced to quit.

<h4>Usage:</h4>

Profile all repository examples:

```
make profile
```

Run with custom arguments:

```
python utilities/profiler.py --in IN --out OUT --sort SORT --timeout SEC
       --lines LINES --skip SKIP --only ONLY --extern --callers --save --help
```

Arguments:
    --in (str): Directory path to C-files [default: c_files].
    --out (str): Directory path for storing results
        [default: `output/profile`].
    --sort (str): Property to sort by [default: `calls`].
    --timeout (int): Max. timeout in seconds for one execution [default: 10].
    --lines (int): Number lines of profiler stats to collect,
        <br/>e.g. to profile top 10 methods, use `--lines 10`.
    --skip (str): Space-separated list of files to exclude,
        <br/>e.g., `--skip dense infinite_2` will not profile matching files.
    --only (str): Space-separated list of files to include,
        <br/>e.g., `--only dense empty` will profile only matching files.
    --extern (): Exclude package external methods from cProfile results
    --callers (): Include function caller statistics.
    --save (): Save pymwp analysis results [default: False].
    --help (): Command help.
"""

import argparse
import asyncio
import os
import pstats
import signal
import subprocess
import time
from argparse import RawTextHelpFormatter
from os import listdir, makedirs, remove
from os.path import abspath, join, dirname, basename, splitext, exists, isfile

from runtime import write_file, machine_info

cwd = abspath(join(dirname(__file__), '../'))  # repository root


def parse_args(parser):
    """Define available arguments."""
    parser.add_argument(
        '--in',
        action='store',
        dest="in_",
        metavar="IN",
        default=join(cwd, 'c_files'),
        help='Directory path to C-files.',
    )
    parser.add_argument(
        "--out",
        action="store",
        default=join(cwd, 'output', 'profile'),
        help="Directory path for storing results.",
    )
    parser.add_argument(
        "--sort",
        action="store",
        default='calls',
        help="Property to sort by.",
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        metavar="SEC",
        help='Max. timeout in seconds for one execution.')
    parser.add_argument(
        '--lines',
        type=int,
        default=-1,
        help='Number of lines of profiler stats to collect\n' +
             'e.g. to profile top 10 methods use --lines 10')
    parser.add_argument(
        '--skip',
        nargs='+',
        default=[],
        metavar="FL",
        help='Space-separated list of files to exclude\n' +
             'e.g. `--skip if dense` skips matching files.'
    )
    parser.add_argument(
        '--only',
        nargs='+',
        default=[],
        metavar="FL",
        help='Space-separated list of files to include\n' +
             'e.g. `--only dense empty` profiles only matching files.'
    )
    parser.add_argument(
        "--extern",
        dest="no_external",
        action='store_true',
        help="Exclude package-external methods from cProfile."
    )
    parser.add_argument(
        "--callers",
        action='store_true',
        help="Include caller stats in profile."
    )
    parser.add_argument(
        "--save",
        action='store_true',
        help="Save pymwp analysis results to file."
    )
    return parser.parse_args()


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
        self.divider_len = 72
        self.no_external = args.no_external
        self.callers = args.callers
        self.save = args.save

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
    def build_cmd(file_in, file_out, save=False):
        """Build cProfile command"""
        return ' '.join([
            'python3 -m cProfile',
            f'-o {file_out}',
            '-m pymwp --silent',
            '--no_save' if not save else '',
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
        write_file(machine_info(), self.output)
        self.post_log()

    async def profile_file(self, c_file):
        """Profile single C file"""
        file_name = Profiler.filename_only(c_file)
        out_file = join(self.output, file_name)
        cmd = Profiler.build_cmd(c_file, out_file, self.save)

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
            message = 'done-ok'
        else:
            message = 'error'
        self.write_stats(out_file)

        print(f'{file_name.ljust(self.pad)} ... '
              f'{message.ljust(7)} : ' +
              f'{(end_time - start_time):.2f}s')

    def pre_log(self):
        """Print info before running profiler."""
        self.__log(f'Profiling {self.file_count} C files... ' +
                   f'(limit: {self.timeout} sec)')
        print(f'{"EXAMPLE".ljust(self.pad + 5)}'
              f'{"RESULT".ljust(7)}   TIME  ')

    def post_log(self):
        """Print info after running profiler."""
        self.__log(f'Finished all after {self.total_time:.2f} seconds.')

    def __log(self, msg):
        """Log something using print and visual dividers."""
        divider = '=' * self.divider_len
        print(f'\n{divider}\n{msg}\n{divider}')


if __name__ == '__main__':
    """Run profiler using provided args."""
    args = parse_args(argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter))
    Profiler(args.in_, args.out, args).run()
