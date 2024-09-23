#!/usr/bin/env python3

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

"""
Provides command line interface to executing pymwp analysis with arguments.

This method enables executing MWP analysis through command line.

If user has installed pymwp through pip, this will be the entry point
of that command when calling:  `pymwp c/file/path --args`

The command behavior is to run the analysis on the specified file,
applying the optional flags.

The available arguments are specified below in `_parse_args` -method.

This method also initializes the program logger that displays debugging
information on the screen. The logger default to log level DEBUG. Analysis
output can be muted by specifying command line argument `--silent`.
"""

import argparse
import logging
import sys
from argparse import RawTextHelpFormatter
from typing import List, Optional, Type, Union

from . import __version__, __title__ as pymwp
from . import __notice__, __warranty__, __conditions__
from . import Parser, Result, Analysis, LoopAnalysis
from .file_io import default_file_out, loc, save_result


def main():
    """Implementation of MWP analysis on C code in Python."""
    parser = argparse.ArgumentParser(
        prog=pymwp, description=main.__doc__ + '\n\n' + __notice__,
        formatter_class=RawTextHelpFormatter)
    args = __parse_args(parser)

    if args.license:
        import shutil
        shell_size = shutil.get_terminal_size((50, 20))
        text = __conditions__ if args.license == 'C' else __warranty__
        print(Result.pretty_print(text, shell_size.columns - 5))
        sys.exit(0)

    if not args.input_file:
        parser.print_help()
        sys.exit(1)

    # setup logger
    level = 0 if args.silent else 30 if args.info else 40
    __setup_logger(logging.FATAL - level, args.logfile, args.no_time)

    # get parser args then get AST
    parser_kwargs = {'use_cpp': not args.no_cpp}
    if not args.no_cpp:  # only when use_cpp is True
        parser_kwargs['cpp_path'] = args.cpp_path
        parser_kwargs['cpp_args'] = args.cpp_args
    c_headers = args.headers.split(',') if args.headers else None
    ast = Parser.parse(args.input_file, c_headers, **(parser_kwargs or {}))

    # setup arguments
    result = Result()
    result.program.program_path = args.input_file
    result.program.n_lines = loc(args.input_file)

    analyzer: Type[Union[Analysis, LoopAnalysis]] = \
        LoopAnalysis if args.mode == 'L' else Analysis
    result = analyzer.run(ast, result, fin=args.fin, strict=args.strict)

    if not args.no_save:
        file_out = args.out or default_file_out(args.input_file)
        save_result(file_out, result)


def __parse_args(
        parser: argparse.ArgumentParser, args: Optional[List] = None
) -> argparse.Namespace:
    """Setup available program arguments."""
    parser.add_argument(
        'input_file',
        help="C source code file to analyze",
        nargs="?"
    )
    parser.add_argument(
        '-v', "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    parser.add_argument(
        "--license",
        action='store',
        dest='license',
        type=str.upper,
        metavar="opt",
        choices=['W', 'C'],
        help="show warranty (W) or conditions (C) and exit"
    )

    analysis = parser.add_argument_group('Analysis options')
    analysis.add_argument(
        "--mode", '-m',
        action='store',
        dest='mode',
        default='F',
        type=str.upper,
        metavar="opt",
        choices=['F', 'L'],
        help="analyze functions (F) or loops (L) [default: F]"
    )
    analysis.add_argument(
        '--out', '-o',
        action="store",
        dest="out",
        metavar="FILE",
        help="file where to store analysis result",
    )
    analysis.add_argument(
        "--no_save",
        action='store_true',
        help="do not write analysis result to a file"
    )
    analysis.add_argument(
        "--fin",
        action='store_true',
        help="ensure analysis always runs to completion"
    )
    analysis.add_argument(
        "--strict",
        action='store_true',
        help="enforce input file must be syntax-compliant"
    )

    compiler = parser.add_argument_group('C compiler options')
    compiler.add_argument(
        '--cpp_path',
        action='store',
        default='gcc',
        metavar="PATH",
        help='pre-processor [default: gcc]',
    )
    compiler.add_argument(
        '--cpp_args',
        action='store',
        default='-E',
        metavar="ARGS",
        help='pre-processor arguments [default: -E]',
    )
    compiler.add_argument(
        "--headers",
        action="store",
        metavar="DIR",
        help="headers dir paths, separate by comma",
    )
    compiler.add_argument(
        "--no_cpp",
        action='store_true',
        help="disable pre-processor"
    )

    log_group = parser.add_argument_group('Terminal log options')
    log_group.add_argument(
        "--logfile",
        action="store",
        metavar="FILE",
        help="write console output to a file",
    )
    log_group.add_argument(
        "--no_time",
        action='store_true',
        help="omits timestamps from log output"
    )
    log_group.add_argument(
        '--info',
        action='store_true',
        help="set logging level to info"
    )
    log_group.add_argument(
        "--silent",
        action='store_true',
        help="disable all terminal output"
    )

    return parser.parse_args(args)


def __setup_logger(
        level: int = logging.ERROR, log_filename: Optional[str] = None,
        hide_time: bool = False
) -> None:
    """Create a configured instance of logger.

    Arguments:
        level: Describe the severity level of the logs to handle.
            see: https://docs.python.org/3/library/logging.html#levels
        log_filename: Write logging info to a file
    """
    fmt = "%(levelname)s (%(module)s): %(message)s" if hide_time else \
        "[%(asctime)s] %(levelname)s (%(module)s): %(message)s"
    date_fmt = "%H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    logger = logging.getLogger(pymwp)
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_filename is not None:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


if __name__ == '__main__':
    main()
