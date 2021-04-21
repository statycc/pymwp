import argparse
import sys
import logging
from typing import List, Optional

from .analysis import Analysis
from .version import __version__


def main():
    """Implementation of MWP analysis on C code in Python."""
    parser = argparse.ArgumentParser(prog='pymwp', description=main.__doc__)
    args = _parse_args(parser)

    if args.verbosity:
        if args.verbosity:
            log_filename = None
            log_level = min(args.verbosity, 4) * 10
            if args.logfile:
                log_filename = args.logfile
            setup_logger(logging.FATAL - log_level,
                         log_filename=log_filename)

    if not args.file:
        parser.print_help()
        sys.exit(1)
    else:
        Analysis(args.file, args.out)


def _parse_args(
        parser: argparse.ArgumentParser,
        args: Optional[List] = None) -> argparse.Namespace:
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
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbosity",
        help="verbosity level, use up to 4 to increase logging -vvvv",
    )
    parser.add_argument(
        "--logfile",
        action="store",
        help="logging debug and error messages into a log file",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    return parser.parse_args(args)


def setup_logger(
        level: int = logging.ERROR,
        log_filename: Optional[str] = None) -> None:
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
