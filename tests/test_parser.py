import pycparser

from pymwp import Parser
from .mocks.ast_mocks import INFINITE_2C, INFINITE_8C, FUNCTION_CALL

"""
Test imported external dependencies that are being used.

The goal of these tests is to enable checking that dependency updates 
do not break expected and existing behavior that is currently in use.

To see what functionality is being used see parser interface in
pymwp/parser.py
"""

PARSER_KWARGS = {'use_cpp': True, 'cpp_path': 'gcc', 'cpp_args': '-E'}


def __compare__(a, b):
    """ignores newlines"""
    return a.replace('\n', '') == b.replace('\n', '')


def test_ast_node_types():
    """Test for existence of different AST node types."""
    assert hasattr(pycparser.c_ast, 'Assignment')
    assert hasattr(pycparser.c_ast, 'BinaryOp')
    assert hasattr(pycparser.c_ast, 'Break')
    assert hasattr(pycparser.c_ast, 'Compound')
    assert hasattr(pycparser.c_ast, 'Constant')
    assert hasattr(pycparser.c_ast, 'Continue')
    assert hasattr(pycparser.c_ast, 'Decl')
    assert hasattr(pycparser.c_ast, 'DoWhile')
    assert hasattr(pycparser.c_ast, 'For')
    assert hasattr(pycparser.c_ast, 'FuncCall')
    assert hasattr(pycparser.c_ast, 'FuncDef')
    assert hasattr(pycparser.c_ast, 'ID')
    assert hasattr(pycparser.c_ast, 'If')
    assert hasattr(pycparser.c_ast, 'Node')
    assert hasattr(pycparser.c_ast, 'NodeVisitor')
    assert hasattr(pycparser.c_ast, 'ParamList')
    assert hasattr(pycparser.c_ast, 'UnaryOp')
    assert hasattr(pycparser.c_ast, 'While')


def test_parse():
    """Ensure parse function exists."""
    assert hasattr(pycparser, 'parse_file')
    assert callable(getattr(pycparser, 'parse_file'))


def test_ast_structure_infty2c():
    """Parser should match mock result used for unit tests

    If this (or subsequent similar tests) fails after parser version bump,
    update the mock AST trees.
    """
    ast = Parser.parse('c_files/infinite/infinite_2.c', **PARSER_KWARGS)

    assert str(ast) == str(INFINITE_2C)


def test_ast_structure_infty8c():
    ast = Parser.parse('c_files/infinite/infinite_8.c', **PARSER_KWARGS)

    assert str(ast) == str(INFINITE_8C)


def test_ast_structure_func_call():
    ast = Parser.parse('c_files/implementation_paper/example14.c',
                       **PARSER_KWARGS)

    assert str(ast) == str(FUNCTION_CALL)
