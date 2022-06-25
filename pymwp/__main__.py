#!/usr/bin/env python3

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
from typing import List, Optional

from pymwp import Parser, Analysis, __version__
from .file_io import default_file_out


def main():
    """Implementation of MWP analysis on C code in Python."""
    parser = argparse.ArgumentParser(prog='pymwp', description=main.__doc__)
    args = __parse_args(parser)

    if not args.input_file:
        parser.print_help()
        sys.exit(1)

    # setup logger
    log_level = logging.FATAL - (0 if args.silent else 40)
    __setup_logger(log_level, args.logfile)

    # get parser args then get AST
    parser_kwargs = {'use_cpp': not args.no_cpp}
    # these options only apply when use_cpp is set to True
    if not args.no_cpp:
        parser_kwargs['cpp_path'] = args.cpp_path
        parser_kwargs['cpp_args'] = args.cpp_args
    ast = Parser.parse(args.input_file, **(parser_kwargs or {}))

    # run analysis
    Analysis.run(ast,
                 file_out=args.out or default_file_out(args.input_file),
                 no_save=args.no_save,
                 no_eval=args.no_eval)


def __parse_args(
        parser: argparse.ArgumentParser,
        args: Optional[List] = None) -> argparse.Namespace:
    """Setup available program arguments."""
    parser.add_argument(
        'input_file',
        help="Path to C source code file you want to analyze",
        nargs="?"
    )
    parser.add_argument(
        '-o', '--out',
        action="store",
        dest="out",
        help="output filename (with path) for storing analysis result",
    )
    parser.add_argument(
        "--logfile",
        action="store",
        help="write analysis log messages to a file",
    )
    parser.add_argument(
        '--cpp_path',
        action='store',
        default='gcc',
        help='path to C pre-processor on your system (default: gcc)',
    )
    parser.add_argument(
        '--cpp_args',
        action='store',
        default='-E',
        help='arguments to pass to C pre-processor (default: -E)',
    )
    parser.add_argument(
        "--no_cpp",
        action='store_true',
        help="disable execution of C pre-processor on input file"
    )
    parser.add_argument(
        "--no_eval",
        action="store_true",
        help="skip evaluation (no impact if bound does not exist)",
    )
    parser.add_argument(
        "--no_save",
        action='store_true',
        help="skip writing result to file"
    )
    parser.add_argument(
        '-s', "--silent",
        action='store_true',
        help="disable debug logging, only fatal errors will be displayed"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    return parser.parse_args(args)


def __setup_logger(
        level: int = logging.ERROR, log_filename: Optional[str] = None
) -> None:
    """Create a configured instance of logger.

    Arguments:
        level: Describe the severity level of the logs to handle.
            see: https://docs.python.org/3/library/logging.html#levels
        log_filename: Write logging info to a file
    """
    fmt = "[%(asctime)s] %(levelname)s (%(module)s): %(message)s"
    date_fmt = "%H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    logger = logging.getLogger("pymwp")
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
