import json
import logging
import os
from typing import Dict

from pymwp import Result, Relation, Choices
from .matrix import decode

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


def save_relation(file_name: str, analysis_result: Result) -> None:
    """Save analysis result to file as JSON.

    Expected behavior:

    - if path to output file does not exist it will be created
    - if output file does not exist it will be created
    - if output file exists it will be overwritten

    Arguments:
        file_name: filename where to write
        analysis_result: A [`Result`](result.md) object.
    """

    file_content = {}

    for function_name, result in analysis_result.relations.items():
        file_content[function_name] = {
            "relation": result.relation.to_dict() if result.relation else None,
            "choices": result.choices.valid if result.choices else None,
            "bound": result.bound.to_dict() if result.bound else None,
            "infinity": result.infinite
        }

    # ensure directory path exists
    dir_path, _ = os.path.split(file_name)
    if len(dir_path) > 0 and not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # write to file
    with open(file_name, "w") as outfile:
        json.dump(file_content, outfile, indent=4)

    logger.info(f'saved result in {file_name}')


def load_relation(file_name: str) -> Dict[str, any]:
    """Load previous analysis result from file.

    This method is the reverse of
    [`save_relation`](file_io.md#pymwp.file_io.save_relation)
    and assumes the input matches the output of that method.

    Arguments:
        file_name: file to read

    Raises:
          Exception: if `file_name` does not exist or cannot be read.

    Returns:
        parsed result from file where:

        - `key`: name of analyzed function
        - `value`: triple with following positional values:

            - `[0]`: final relation produced by analysis
            - `[1]`: list of non-infinity choices
            - `[2]`: `True` when function does not have polynomial bounds
    """
    # read the file
    with open(file_name) as file_object:
        data = json.load(file_object)

    result = {}

    for function_name, value in data.items():
        relation = None
        # parse its data
        if value["relation"]:
            matrix = value["relation"]["matrix"]
            variables = value["relation"]["variables"]
            relation = Relation(variables, decode(matrix))
        combinations = Choices(value["choices"]) \
            if "choices" in value else None
        infinity = value["infinity"]

        # generate objects
        result[function_name] = relation, combinations, infinity

    return result
