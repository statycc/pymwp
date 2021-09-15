import os
import sys
import json
import logging

from typing import List, Tuple
from pycparser import parse_file, c_ast
from subprocess import CalledProcessError

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
    return os.path.join("output", f"{file_name}.json")


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


def parse(
        file: str, use_cpp: bool = True, cpp_path: str = 'cpp',
        cpp_args: str = '-E'
) -> c_ast:
    """Parse C file using pycparser.

    Pycparser can parse files that cannot be analyzed in any meaningful way,
    e.g. empty main, no main, etc. This method will also check that AST
    has some meaningful content before returning the AST.

    Arguments:
        file: path to C file
        use_cpp: (optional) Set to True if you want to execute the C
            pre-processor on the file prior to parsing it; default: `True`
        cpp_path: (optional) If use_cpp is True, this is the path to 'cpp' on
            your system. If no path is provided, it attempts to just execute
            'cpp', so it must be in your PATH, default: `cpp`
        cpp_args: (optional) If use_cpp is True, set this to the command line
            arguments strings to cpp. Be careful with quotes - it's best
            to pass a raw string (r'') here. If several arguments are
            required, pass a list of strings. default: `-E`

    Raises:
        System.exit: if file cannot be parsed or it appears invalid/
        un-analyzable.

    Returns:
        Generated AST
    """
    try:
        ast = parse_file(file, use_cpp, cpp_path, cpp_args)

        invalid = ast is None or ast.ext is None or \
                  len(ast.ext) == 0 or \
                  ast.ext[0].body is None or \
                  ast.ext[0].body.block_items is None  # noqa: E127

        if not invalid:
            return ast

        sys.exit('FATAL: Input C file is invalid or empty. Terminating.')

    except CalledProcessError:
        sys.exit('FATAL: Failed to parse C file. Terminating.')
