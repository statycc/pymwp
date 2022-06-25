import pycparser

"""
Test imported external dependencies that are being used.

The goal of these tests is to enable checking that dependency updates 
do not break expected and existing behavior that is currently in use.

To see what functionality is being used see parser interface in
pymwp/parser.py
"""


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
