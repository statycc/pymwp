import json
import logging
import os

from pymwp import Result

logger = logging.getLogger(__name__)


def loc(input_file: str) -> int:
    """Get number of lines is a file"""
    with open(input_file, 'r') as fp:
        return len(fp.readlines())


def default_file_out(input_file: str) -> str:
    """Generates default output file.

    Arguments:
        input_file: input filename (with or without path)

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
        file_name: filename where to write
        analysis_result: A [`Result`](result.md) object.
    """
    # JSON serializable object
    file_content = analysis_result.serialize()

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
    [`save_relation`](file_io.md#pymwp.file_io.save_relation)
    and assumes the input matches the output of that method.

    Arguments:
        file_name: file to read

    Raises:
          Exception: if `file_name` does not exist or cannot be read.

    Returns:
        Parsed result from file
    """
    # read the file
    with open(file_name) as file_object:
        data = json.load(file_object)

    return Result.deserialize(**data)
