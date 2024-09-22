# noinspection DuplicatedCode

"""
Sample ASTs for unit testing Analysis.
We mock the outputs of pycparser.parse_file.
These ASTs match the examples in tests/test_examples.

How add a new example:
1. add .c file to test_examples
2. run `make compute-ast`
3. add a new variable here that loads the AST .txt file
4. import the variable in a unit test
"""

# noinspection PyUnresolvedReferences
from pycparser.c_ast import *


def load_ast(fp):
    with open(fp, "r+") as f:
        # yes, but it is needed here.
        return eval(f.read())


BRACES_ISSUES = load_ast('tests/mocks/braces_issues.txt')
CASTS = load_ast('tests/mocks/casts.txt')
EMPTY = load_ast('tests/mocks/empty.txt')
EMPTY_FUNCTION = load_ast('tests/mocks/empty_function.txt')
FOR_BODY = load_ast('tests/mocks/for_body.txt')
FOR_INVALID = load_ast('tests/mocks/for_invalid.txt')
FOR_LOOP = load_ast('tests/mocks/for_loop.txt')
FOR_SUBST = load_ast('tests/mocks/for_subst.txt')
FUNCTION_CALL = load_ast('tests/mocks/function_call.txt')
IF_EMPTY_BRACES = load_ast('tests/mocks/braces_empty.txt')
IF_INVALID_TESTS = load_ast('tests/mocks/if_invalid_tests.txt')
IF_WITH_BRACES = load_ast('tests/mocks/if_with_braces.txt')
IF_WO_BRACES = load_ast('tests/mocks/if_wo_braces.txt')
INFINITE_2 = load_ast('tests/mocks/infinite_2.txt')
INFINITE_8 = load_ast('tests/mocks/infinite_8.txt')
NOT_INFINITE_2 = load_ast('tests/mocks/notinfinite_2.txt')
NOT_INFINITE_3 = load_ast('tests/mocks/notinfinite_3.txt')
PARAMS = load_ast('tests/mocks/params.txt')
SINGLE_LINK_CLUSTER = load_ast('tests/mocks/SingleLinkCluster.txt')
TYPEDEFS = load_ast('tests/mocks/typedefs.txt')
UNARY_EQ = load_ast('tests/mocks/unary_eq.txt')
UNARY_OPS = load_ast('tests/mocks/unary_ops.txt')
VARIABLE_IGNORED = load_ast('tests/mocks/variable_ignored.txt')
VAR_TESTS = load_ast('tests/mocks/var_tests.txt')
VERIFICATION = load_ast('tests/mocks/verification.txt')
