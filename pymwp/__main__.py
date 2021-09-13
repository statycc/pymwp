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
import sys
import logging
from typing import List, Optional
from pycparser import parse_file, c_ast
from subprocess import CalledProcessError

from .analysis import Analysis
from .version import __version__
from .file_io import default_file_out


def main():
    """Implementation of MWP analysis on C code in Python."""
    parser = argparse.ArgumentParser(prog='pymwp', description=main.__doc__)
    args = _parse_args(parser)

    if not args.file:
        parser.print_help()
        sys.exit(1)

    log_level = 0 if args.silent else 40
    log_filename = args.logfile
    logger = setup_logger(logging.FATAL - log_level, log_filename=log_filename)
    file_out = args.out or default_file_out(args.file)
    use_cpp, cpp_path, cpp_args = not args.no_cpp, args.cpp, args.cpp_args

    logger.info(f'Starting analysis of {args.file}')
    ast = parse_c_file(args.file, use_cpp, cpp_path, cpp_args, logger)
    Analysis.run(ast, file_out, args.no_save)


def _parse_args(
        parser: argparse.ArgumentParser,
        args: Optional[List] = None) -> argparse.Namespace:
    """Setup available program arguments."""
    parser.add_argument(
        "file",
        help="Path to C source code file",
        nargs="?"
    )
    parser.add_argument(
        "--outfile",
        action="store",
        dest="out",
        help="file for storing analysis result",
    )
    parser.add_argument(
        "--logfile",
        action="store",
        help="save log messages into a file",
    )
    parser.add_argument(
        "--no-save",
        action='store_true',
        help="skip writing result to file"
    )
    parser.add_argument(
        "--no-cpp",
        action='store_true',
        help="disable execution of C pre-processor on the input file"
    )
    parser.add_argument(
        '--cpp',
        action='store',
        default='gcc',
        help='path to C pre-processor on your system (default: gcc)',
    )
    parser.add_argument(
        '--cpp-args',
        action='store',
        default='-E',
        help='arguments to pass to C pre-processor (default: -E)',
    )
    parser.add_argument(
        "--silent",
        action='store_true',
        help="silence logging; only show fatal errors"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    return parser.parse_args(args)


def setup_logger(
        level: int = logging.ERROR,
        log_filename: Optional[str] = None) -> logging.Logger:
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
    return logger


def parse_c_file(
        file: str, use_cpp: bool, cpp_path: str, cpp_args: str,
        logger: logging.Logger
) -> c_ast:
    """Parse C file using pycparser.

    Arguments:
        file: path to C file
        use_cpp: Set to True if you want to execute the C pre-processor
            on the file prior to parsing it.
        cpp_path: If use_cpp is True, this is the path to 'cpp' on your
            system. If no path is provided, it attempts to just execute
            'cpp', so it must be in your PATH.
        cpp_args: If use_cpp is True, set this to the command line
            arguments strings to cpp. Be careful with quotes - it's best
            to pass a raw string (r'') here. If several arguments are
            required, pass a list of strings.
        logger: logger instance

    Returns:
        Generated AST
    """
    try:
        ast = parse_file(file, use_cpp, cpp_path, cpp_args)
        if use_cpp:
            info = f'parsed with preprocessor: {cpp_path} {cpp_args}'
        else:
            info = 'parsed without preprocessor'
        logger.debug(info)
        validate_ast(ast, logger)
        return ast
    except CalledProcessError:
        logger.error('Failed to parse C file. Terminating.')
        sys.exit(1)


def validate_ast(ast: c_ast, logger: logging.Logger) -> None:
    """Check if successfully parsed AST can be analyzed.

    Here we check that the C input file contains some source code
    (has body) and that that body is not empty (has block_items).
    These types of inputs do not cause the parser to error, so we
    need to check these separately from parse error.

    If the input is invalid terminate immediately.

    Ref: [issue #4](https://github.com/seiller/pymwp/issues/4)

    Arguments:
        ast: AST object
        logger: logger instance
    """

    invalid = ast is None or ast.ext is None or len(ast.ext) == 0
    invalid = invalid or ast.ext[0].body is None or ast.ext[
        0].body.block_items is None

    if invalid:
        logger.error('Input C file is invalid or empty.')
        sys.exit(1)


if __name__ == '__main__':
    main()
