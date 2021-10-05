"""
Sample ASTs for unit testing Analysis

here we mock the outputs of pycparser.parse_file

These ASTs match the examples in c_files by name, or tests/mocks
"""

from pycparser.c_ast import FileAST, FuncDef, Decl, FuncDecl, TypeDecl, \
    IdentifierType, Compound, Constant, While, BinaryOp, ID, Assignment, If, \
    ParamList, FuncCall, Return, ExprList

INFINITE_2C = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='X0', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(
                     declname='X0', quals=[],
                     type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(
            declname='foo', quals=[], type=IdentifierType(names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[While(cond=BinaryOp(
        op='<', left=ID(name='X1'), right=Constant(type='int', value='10')),
        stmt=Compound(block_items=[
            Assignment(op='=', lvalue=ID(name='X0'), rvalue=BinaryOp(
                op='*', left=ID(name='X1'), right=ID(name='X0'))),
            Assignment(op='=', lvalue=ID(name='X1'), rvalue=BinaryOp(
                op='+', left=ID(name='X1'), right=ID(name='X0')))]))]))])

IF_WO_BRACES = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='x', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='y', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='y', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x2', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x2', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x3', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x3', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(declname='foo', quals=[],
                                                type=IdentifierType(
                                                    names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[If(cond=BinaryOp(
        op='>', left=ID(name='x'), right=Constant(type='int', value='0')),
        iftrue=Assignment(op='=', lvalue=ID(name='x3'), rvalue=ID(name='x1')),
        iffalse=Assignment(op='=', lvalue=ID(name='x3'),
                           rvalue=ID(name='x2'))),
        Assignment(op='=', lvalue=ID(name='y'), rvalue=ID(name='x3'))]))])

IF_WITH_BRACES = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='x', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='y', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='y', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x2', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x2', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x3', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x3', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(declname='foo', quals=[],
                                                type=IdentifierType(
                                                    names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[If(cond=BinaryOp(
        op='>', left=ID(name='x'), right=Constant(type='int', value='0')),
        iftrue=Compound(block_items=[
            Assignment(op='=', lvalue=ID(name='x3'), rvalue=ID(name='x1'))]),
        iffalse=Compound(block_items=[
            Assignment(op='=', lvalue=ID(name='x3'), rvalue=ID(name='x2'))])),
        Assignment(op='=', lvalue=ID(name='y'), rvalue=ID(name='x3'))]))])

NOT_INFINITE_2C = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='X0', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X0', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(declname='foo', quals=[],
                                                type=IdentifierType(
                                                    names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[
        Assignment(op='=', lvalue=ID(name='X0'),
                   rvalue=BinaryOp(op='*', left=ID(name='X1'),
                                   right=ID(name='X0'))),
        Assignment(op='=', lvalue=ID(name='X1'),
                   rvalue=BinaryOp(op='+', left=ID(name='X1'),
                                   right=ID(name='X0')))]))])

VARIABLE_IGNORED = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='X1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X2', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X2', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X3', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X3', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X4', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X4', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(
            declname='foo', quals=[], type=IdentifierType(names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[
        Assignment(op='=', lvalue=ID(name='X2'),
                   rvalue=BinaryOp(op='+', left=ID(name='X3'),
                                   right=ID(name='X1'))),
        Assignment(op='=', lvalue=ID(name='X4'), rvalue=ID(name='X2'))]))])

OTHER_BRACES_ISSUES = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='x', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='y', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='y', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(
            declname='foo', quals=[], type=IdentifierType(names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[Compound(block_items=[
        If(cond=BinaryOp(op='>', left=ID(name='x'), right=ID(name='y')),
           iftrue=Compound(block_items=[
               Assignment(op='=', lvalue=ID(name='x'),
                          rvalue=ID(name='y'))]),
           iffalse=None)])]))])

BASICS_ASSIGN_VALUE = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='y', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='y', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(
            declname='foo', quals=[], type=IdentifierType(names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[
        Assignment(op='=', lvalue=ID(name='y'),
                   rvalue=Constant(type='int', value='0'))]))])

PARAMS = FileAST(ext=[FuncDef(decl=Decl(
    name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='x1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x2', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x2', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='x3', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='x3', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(declname='foo', quals=[],
                                                type=IdentifierType(
                                                    names=['int']))),
    init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[
        Assignment(op='=', lvalue=ID(name='x1'), rvalue=ID(name='x2'))]))])

FUNCTION_CALL = FileAST(ext=[FuncDef(decl=Decl(
    name='f', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='X1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X2', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X2', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(declname='f', quals=[],
                                                type=IdentifierType(
                                                    names=['int']))),
    init=None, bitsize=None), param_decls=None, body=Compound(block_items=[
    While(cond=ID(name='X1'), stmt=Compound(block_items=[
        Assignment(op='=', lvalue=ID(name='X2'),
                   rvalue=BinaryOp(op='+', left=ID(name='X2'),
                                   right=ID(name='X2')))])),
    Return(expr=ID(name='X2'))])), FuncDef(
    decl=Decl(name='foo', quals=[], storage=[], funcspec=[], type=FuncDecl(
        args=ParamList(params=[
            Decl(name='X1', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X1', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X2', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X2', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None),
            Decl(name='X3', quals=[], storage=[], funcspec=[],
                 type=TypeDecl(declname='X3', quals=[],
                               type=IdentifierType(names=['int'])), init=None,
                 bitsize=None)]), type=TypeDecl(declname='foo', quals=[],
                                                type=IdentifierType(
                                                    names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[Assignment(op='=', lvalue=ID(name='X3'),
                                rvalue=BinaryOp(op='+', left=ID(name='X1'),
                                                right=ID(name='X1'))),
                     Assignment(op='=', lvalue=ID(name='X2'),
                                rvalue=BinaryOp(op='+', left=ID(name='X3'),
                                                right=ID(name='X1'))),
                     Assignment(op='=', lvalue=ID(name='X1'),
                                rvalue=FuncCall(name=ID(name='f'),
                                                args=ExprList(
                                                    exprs=[ID(name='X2'), ID(
                                                        name='X2')])))]))])
