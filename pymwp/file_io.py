import os
import json

from typing import List, Tuple

from .relation_list import RelationList
from .relation import Relation
from .matrix import decode


def default_file_out(input_file: str) -> str:
    """Generates default output file.

    Arguments:
        input_file: input filename (with or without path)

    Returns:
        Generated output filename with path.
    """
    file_only = os.path.splitext(input_file)[0]
    file_name = os.path.basename(file_only)
    return os.path.join("output", f"{file_name}.txt")


def save_relation(
        file_name: str, relation: Relation, combinations: List[List[int]]
) -> None:
    """Save analysis result to file.

    Arguments:
        file_name: file to write
        relation: result relation
        combinations: non-infinity choices
    """
    info = {
        "relation": relation.to_dict(),
        "combinations": combinations
    }

    # ensure directory path exists
    dir_path, _ = os.path.split(file_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # write to file
    with open(file_name, "w") as outfile:
        json.dump(info, outfile, indent=4)


def load_relation(file_name: str) -> Tuple[RelationList, List[List[int]]]:
    """Load previous analysis result from file.

    Arguments:
        file_name: file to read

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
