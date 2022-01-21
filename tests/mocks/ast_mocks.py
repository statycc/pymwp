"""
Sample ASTs for unit testing Analysis

here we mock the outputs of pycparser.parse_file

These ASTs match the examples in c_files by name, or tests/test_examples
"""

from pycparser.c_ast import FileAST, FuncDef, Decl, FuncDecl, TypeDecl, \
    IdentifierType, Compound, Constant, While, BinaryOp, ID, Assignment, If, \
    ParamList, FuncCall, Return, ExprList

# c_files/infinite/infinite_2.c
INFINITE_2C = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='X0', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X0', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None,
    body=Compound(block_items=[While(cond=BinaryOp(
        op='<', left=ID(name='X1'),
        right=Constant(type='int', value='10')),
        stmt=Compound(block_items=[
            Assignment(op='=', lvalue=ID(name='X0'),
                       rvalue=BinaryOp(op='*', left=ID(name='X1'),
                                       right=ID(name='X0'))),
            Assignment(op='=', lvalue=ID(name='X1'),
                       rvalue=BinaryOp(op='+', left=ID(name='X1'),
                                       right=ID(name='X0')))]))]))])

# c_files/infinite/infinite_8.c
INFINITE_8C = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='X0', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X0', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X2', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X2', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X3', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X3', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X4', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X4', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X5', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X5', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[If(cond=BinaryOp(
            op='==', left=ID(name='X3'),
            right=Constant(type='int', value='0')),
            iftrue=Compound(block_items=[
                Assignment(op='=', lvalue=ID(name='X1'),
                           rvalue=BinaryOp(op='+', left=ID(name='X2'),
                                           right=ID(name='X1')))]),
            iffalse=None), While(
            cond=BinaryOp(op='<', left=ID(name='X4'),
                          right=Constant(type='int', value='100')),
            stmt=Compound(block_items=[
                Assignment(op='=', lvalue=ID(name='X2'),
                           rvalue=BinaryOp(
                               op='+', left=ID(name='X3'),
                               right=ID(name='X5'))),
                Assignment(op='=', lvalue=ID(name='X3'),
                           rvalue=BinaryOp(op='+', left=ID(
                               name='X4'), right=ID(name='X5'))),
                Assignment(op='=', lvalue=ID(name='X4'),
                           rvalue=BinaryOp(op='+', left=ID(
                               name='X2'), right=ID(name='X5'))),
                If(cond=BinaryOp(op='==', left=ID(name='X3'),
                                 right=Constant(type='int', value='0')),
                   iftrue=Compound(block_items=[
                       Assignment(op='=', lvalue=ID(name='X0'),
                                  rvalue=BinaryOp(op='+', left=ID(
                                      name='X2'), right=ID(name='X2')))]),
                   iffalse=Compound(block_items=[
                       Assignment(op='=', lvalue=ID(name='X2'),
                                  rvalue=BinaryOp(
                                      op='+', left=ID(name='X3'),
                                      right=ID(name='X4')))]))])),
            If(cond=BinaryOp(op='==', left=ID(name='X3'),
                             right=Constant(type='int', value='0')),
               iftrue=Compound(block_items=[
                   Assignment(op='=', lvalue=ID(name='X1'),
                              rvalue=BinaryOp(op='+',
                                              left=ID(name='X2'),
                                              right=ID(name='X1')))]),
               iffalse=Compound(block_items=[
                   Assignment(op='=', lvalue=ID(name='X2'),
                              rvalue=BinaryOp(op='+',
                                              left=ID(name='X3'),
                                              right=ID(
                                                  name='X1')))]))]))])

# tests/test_examples/if_wo_braces.c
IF_WO_BRACES = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='x', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='y', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='y', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x2', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x2', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x3', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x3', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[If(cond=BinaryOp(op='>', left=ID(name='x'),
                                      right=Constant(type='int', value='0')),
                        iftrue=Assignment(op='=', lvalue=ID(name='x3'),
                                          rvalue=ID(name='x1')),
                        iffalse=Assignment(op='=', lvalue=ID(name='x3'),
                                           rvalue=ID(name='x2'))),
                     Assignment(op='=', lvalue=ID(name='y'),
                                rvalue=ID(name='x3'))]))])

# tests/test_examples/if_with_braces.c
IF_WITH_BRACES = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='x', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='y', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='y', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x2', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x2', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x3', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x3', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[If(cond=BinaryOp(op='>', left=ID(name='x'),
                                      right=Constant(type='int', value='0')),
                        iftrue=Compound(block_items=[
                            Assignment(op='=', lvalue=ID(name='x3'),
                                       rvalue=ID(name='x1'))]),
                        iffalse=Compound(block_items=[
                            Assignment(op='=', lvalue=ID(name='x3'),
                                       rvalue=ID(name='x2'))])),
                     Assignment(op='=', lvalue=ID(name='y'),
                                rvalue=ID(name='x3'))]))])

# c_files/not_infinite/notinfinite_2.c
NOT_INFINITE_2C = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='X0', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X0', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[Assignment(op='=', lvalue=ID(name='X0'),
                                rvalue=BinaryOp(op='*', left=ID(name='X1'),
                                                right=ID(name='X0'))),
                     Assignment(op='=', lvalue=ID(name='X1'),
                                rvalue=BinaryOp(op='+', left=ID(name='X1'),
                                                right=ID(name='X0')))]))])

# tests/test_examples/variable_ignored.c
VARIABLE_IGNORED = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='X1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X2', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X2', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X3', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X3', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X4', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X4', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[Assignment(op='=', lvalue=ID(name='X2'),
                                rvalue=BinaryOp(op='+', left=ID(name='X3'),
                                                right=ID(name='X1'))),
                     Assignment(op='=', lvalue=ID(name='X4'),
                                rvalue=ID(name='X2'))]))])

# tests/test_examples/braces_issues.c
BRACES_ISSUES = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='x', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='y', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='y', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[Compound(block_items=[
            If(cond=BinaryOp(op='>', left=ID(name='x'), right=ID(name='y')),
               iftrue=Compound(block_items=[
                   Assignment(op='=', lvalue=ID(name='x'),
                              rvalue=ID(name='y'))]), iffalse=None)])]))])

# tests/test_examples/params.c
PARAMS = FileAST(ext=[FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='x1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x2', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x2', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='x3', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='x3', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[
            Assignment(op='=', lvalue=ID(name='x1'), rvalue=ID(name='x2'))]))])

# c_files/implementation_paper/example5_a.c
FUNCTION_CALL = FileAST(ext=[FuncDef(
    decl=Decl(name='f', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='X1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X2', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X2', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='f', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[While(cond=ID(name='X1'), stmt=Compound(block_items=[
            Assignment(op='=', lvalue=ID(name='X2'),
                       rvalue=BinaryOp(op='+', left=ID(name='X1'),
                                       right=ID(name='X1')))])),
                     Return(expr=ID(name='X2'))])), FuncDef(
    decl=Decl(name='foo', quals=[], align=[], storage=[], funcspec=[],
              type=FuncDecl(args=ParamList(params=[
                  Decl(name='X1', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X1', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None),
                  Decl(name='X2', quals=[], align=[], storage=[], funcspec=[],
                       type=TypeDecl(declname='X2', quals=[], align=None,
                                     type=IdentifierType(names=['int'])),
                       init=None, bitsize=None)]),
                  type=TypeDecl(declname='foo', quals=[], align=None,
                                type=IdentifierType(names=['int']))),
              init=None, bitsize=None), param_decls=None, body=Compound(
        block_items=[Assignment(
            op='=', lvalue=ID(name='X2'),
            rvalue=BinaryOp(op='+', left=ID(name='X1'), right=ID(name='X1'))),
            Assignment(op='=', lvalue=ID(name='X1'),
                       rvalue=FuncCall(name=ID(name='f'), args=ExprList(
                           exprs=[ID(name='X2'), ID(name='X2')])))]))])
