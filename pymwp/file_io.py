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

import json
import logging
import os

from . import Result

logger = logging.getLogger(__name__)


def loc(input_file: str) -> int:
    """Get number of lines is a file.

    Arguments:
        input_file: Path to input file.

    Returns:
        Number of non-empty lines in input file.
    """
    with open(input_file, 'r') as fp:
        lines = fp.readlines()
    lines = [1 for line in lines if line and len(line.strip())]
    return sum(lines)


def default_file_out(input_file: str) -> str:
    """Generates default output file.

    Arguments:
        input_file: input filename (with or without path).

    Returns:
        Generated output filename with path.
    """
    file_only = os.path.splitext(input_file)[0]
    file_name = os.path.basename(file_only)
    return os.path.join("output", f"{file_name}.json")


def save_result(file_name: str, analysis_result: Result) -> None:
    """Save analysis result to file as JSON.

    Expected behavior:

    - if path to output file does not exist it will be created
    - if output file does not exist it will be created
    - if output file exists it will be overwritten

    Arguments:
        file_name: Filename where to write.
        analysis_result: Result object.
    """
    # JSON serializable object
    file_content = analysis_result.to_dict()

    # ensure directory path exists
    dir_path, _ = os.path.split(file_name)
    if len(dir_path) > 0 and not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # write to file
    with open(file_name, "w") as outfile:
        json.dump(file_content, outfile, indent=4)

    logger.info(f'saved result in {file_name}')


def load_result(file_name: str) -> Result:
    """Load previous analysis result from file.

    This method is the reverse of
    [`save_result`](file_io.md#pymwp.file_io.save_result)
    and assumes the input matches the output of that method.

    Arguments:
        file_name: File to read.

    Raises:
        Exception: if `file_name` does not exist or cannot be read.

    Returns:
        Parsed result from file.
    """
    # read the file
    with open(file_name) as file_object:
        data = json.load(file_object)

    return Result.from_dict(**data)
