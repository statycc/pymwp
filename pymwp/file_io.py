import os
import json
import logging

from typing import List, Tuple

from .relation_list import RelationList
from .relation import Relation
from .matrix import decode

logger = logging.getLogger(__name__)


def default_file_out(input_file: str) -> str:
    """Generates default output file.

    Arguments:
        input_file: input filename (with or without path)

    Returns:
        Generated output filename with path.
    """
    file_only = os.path.splitext(input_file)[0]
    file_name = os.path.basename(file_only)
    # TODO: we save/load json but save as .txt, why?
    return os.path.join("output", f"{file_name}.txt")


def save_relation(file_name: str, relation: Relation,
                  choices: List[List[int]]) -> None:
    """Save analysis result to file as JSON.

    Expected behavior:

    - if path to output file does not exist it will be created
    - if output file does not exist it will be created
    - if output file exists it will be overwritten

    Arguments:
        file_name: filename where to write
        relation: analysis result relation
        choices: non-infinity choices
    """
    info = {
        "relation": relation.to_dict(),
        "choices": choices
    }

    # ensure directory path exists
    dir_path, _ = os.path.split(file_name)
    if len(dir_path) > 0 and not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # write to file
    with open(file_name, "w") as outfile:
        json.dump(info, outfile, indent=4)

    logger.info(f'saved result in {file_name}')


def load_relation(file_name: str) -> Tuple[RelationList, List[List[int]]]:
    """Load previous analysis result from file.

    This method is the reverse of
    [`save_relation`](file_io.md#pymwp.file_io.save_relation)
    and assumes the input matches the output of that method.

    Arguments:
        file_name: file to read

    Raises:
          Exception: if `file_name` does not exist or cannot be read.

    Returns:
        parsed relation list and combinations

    """
    # read the file
    with open(file_name) as file_object:
        data = json.load(file_object)

    # parse its data
    matrix = data["relation"]["matrix"]
    variables = data["relation"]["variables"]
    combinations = data["combinations"]

    # generate objects
    relation = Relation(variables, decode(matrix))
    relation_list = RelationList(relation_list=[relation])
    return relation_list, combinations
