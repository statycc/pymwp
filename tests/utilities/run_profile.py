#!/usr/bin/env python

import os
import asyncio
import pstats
import logging
import time

from os import listdir, makedirs, remove
from functools import reduce

logger = logging.getLogger(__name__)
cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# max timeout, in seconds
TIMEOUT = 30

# number of lines to include in profile
STAT_LINES = 50

# examples directory
EXAMPLES_DIR = 'c_files'

# output directory
OUTPUT_DIR = os.path.join(cwd, 'profile')

# .git ignore file name
IGNORE = ".gitignore"

CPROFILE = 'python3 -m cProfile'

# pymwp analysis command
ANALYSIS_CMD = '-m pymwp --no-save '

# list of C files to profile
# finds all files in subdirectories of examples directory
C_FILES = list(reduce(lambda x, y: x + y, [[
    os.path.join(cwd, EXAMPLES_DIR, d, f)
    for f in listdir(os.path.join(cwd, EXAMPLES_DIR, d)) if
    os.path.isfile(os.path.join(cwd, EXAMPLES_DIR, d, f))]
    for d in listdir(os.path.join(cwd, EXAMPLES_DIR)) if
    os.path.isdir(os.path.join(cwd, EXAMPLES_DIR, d))
]))

# measure longest example filename
LONGEST_FILENAME = len(max([
    os.path.basename(os.path.splitext(c)[0])
    for c in C_FILES], key=len))


def setup_logger(level=logging.DEBUG):
    """Initialize logger."""
    fmt = "[%(asctime)s]: %(message)s"
    date_fmt = "%H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def ensure_output_dir_exist():
    if not os.path.exists(OUTPUT_DIR):
        makedirs(OUTPUT_DIR)
    if not os.path.exists(os.path.join(OUTPUT_DIR, IGNORE)):
        with open(os.path.join(OUTPUT_DIR, IGNORE), 'w') as ignore:
            ignore.write("*")


def clear_temp_files():
    for f in [os.path.join(OUTPUT_DIR, f) for f in listdir(OUTPUT_DIR)
              if os.path.isfile(os.path.join(OUTPUT_DIR, f)) \
                 and '.txt' not in f and IGNORE not in f]:
        remove(f)


def plain_profile(out_file):
    """convert cProfile to plain text"""
    with open(out_file + ".txt", 'w') as stream:
        pstats.Stats(out_file, stream=stream) \
            .sort_stats(pstats.SortKey.TIME) \
            .print_stats(STAT_LINES)

    if os.path.isfile(out_file):
        remove(out_file)


async def profile(c_file):
    """Profile single c file"""
    file_only = os.path.splitext(c_file)[0]
    file_name = os.path.basename(file_only)
    out_file = os.path.join(OUTPUT_DIR, file_name)
    start_time = time.monotonic()
    output = f'-o {out_file}'  # if True else ''
    sort = '-s tottime'

    cmd = ' '.join([CPROFILE, sort, output, ANALYSIS_CMD, c_file])
    proc = await asyncio.create_subprocess_shell(
        cmd, cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    task = asyncio.Task(proc.communicate())
    done, pending = await asyncio.wait([task], timeout=TIMEOUT)
    if pending:
        message = 'timeout'
        proc.kill()
    await task
    if proc.returncode not in [0, -9]:
        message = 'error'
    if proc.returncode == 0:
        message = 'done'
        plain_profile(out_file)

    logger.info(
        f'{file_name.ljust(LONGEST_FILENAME)}... {message} ' +
        f': {(time.monotonic() - start_time):.2f}s')


def main():
    """Profile examples"""
    start_time = time.monotonic()
    setup_logger(logging.FATAL - 40)
    ensure_output_dir_exist()
    for file in sorted(C_FILES):
        asyncio.run(profile(file))
    clear_temp_files()
    end = time.monotonic() - start_time
    print(
        f'{"=" * 50}' +
        f'\nProfiled {len(C_FILES)} examples.' +
        f'\nFinished after {end:.2f} seconds.'
        f'\n{"=" * 50}'
    )


if __name__ == '__main__':
    main()
