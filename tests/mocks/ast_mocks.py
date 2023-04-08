# noinspection DuplicatedCode

"""
Sample ASTs for unit testing Analysis

here we mock the outputs of pycparser.parse_file

These ASTs match the examples in c_files by name, or tests/test_examples
"""

# noinspection PyUnresolvedReferences
from pycparser.c_ast import *


def load_ast(fp):
    with open(fp, "r+") as f:
        # yes, but it is needed here.
        return eval(f.read())


INFINITE_2C = load_ast('tests/mocks/infinite_2.txt')
INFINITE_8C = load_ast('tests/mocks/infinite_8.txt')
IF_WO_BRACES = load_ast('tests/mocks/if_wo_braces.txt')
IF_WITH_BRACES = load_ast('tests/mocks/if_with_braces.txt')
NOT_INFINITE_2C = load_ast('tests/mocks/notinfinite_2.txt')
NOT_INFINITE_3C = load_ast('tests/mocks/notinfinite_3.txt')
VARIABLE_IGNORED = load_ast('tests/mocks/variable_ignored.txt')
BRACES_ISSUES = load_ast('tests/mocks/braces_issues.txt')
PARAMS = load_ast('tests/mocks/params.txt')
FUNCTION_CALL = load_ast('tests/mocks/example14.txt')
TYPEDEF = load_ast('tests/mocks/typedefs.txt')
EMPTY = load_ast('tests/mocks/empty.txt')
