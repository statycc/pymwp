# -----------------------------------------------------------------------------
# Copyright (c) 2020-2024 C. Aubert, T. Rubiano, N. Rusch and T. Seiller.
#
# This file is part of pymwp.
#
# pymwp is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pymwp is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pymwp. If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from __future__ import annotations

import logging
from abc import abstractmethod
from collections import Counter
from copy import deepcopy
from typing import List, Callable, Tuple, Optional, Union

# noinspection PyPep8Naming
from .parser import Parser as pr, NodeHandler

logger = logging.getLogger(__name__)


class SyntaxUtils:
    """Various helpful syntax-related utility methods."""

    @staticmethod
    def array_name(node: pr.ArrayRef) -> str:
        """Find array identifier.

        Arguments:
            node (pr.ArrayRef): Array AST node.

        Returns:
            Find array name from node.
        """
        name_node = node.name
        while not isinstance(name_node, pr.ID):
            name_node = name_node.name
        return name_node.name

    @staticmethod
    def init_vars(node: Union[pr.Assignment, pr.DeclList, pr.ExprList]) \
            -> Tuple[List[str], List[str]]:
        """Find and group variables in an init-block.

        Looks for declarations/iterators `int i=…,…` on left
        and "source" variables `…=y` on right.

        Arguments:
            node: Node to inspect.

        Returns:
            Discovered variable lists of declarations and sources.
        """

        def att(lst, attr):
            return [getattr(e, attr) for e in lst]

        def names(lst):
            return [e.name for e in lst if isinstance(e, (pr.ID, pr.Decl))]

        # int i=0,… one or more declarations
        if isinstance(node, pr.DeclList):
            return names(node.decls), names(att(node.decls, 'init'))

        # i=0, j=x,… one or more assignments
        exp = node.exprs if hasattr(node, 'exprs') else [node]
        return names(att(exp, 'lvalue')), names(att(exp, 'rvalue'))

    @staticmethod
    def rm_child(node: pr.Node, attr: str, child: pr.Node) -> Callable:
        """Construct a callable function to remove a child node.

        Using a callable allows performing the actual removal later.

        Arguments:
            node (pr.Node): Parent node.
            attr (str): Parent's attribute that contains child, e.g., stmt.
            child (pr.Node): Child node.

        Returns:
            A callable function.
        """
        return lambda: getattr(node, attr).remove(child) \
            if child in getattr(node, attr) else None

    @staticmethod
    def rm_attr(node: pr.Node, attr: str) -> Callable:
        """Construct a callable function to clear an attribute.

        Arguments:
            node (pr.Node): AST node.
            attr (str): Attribute to remove.

        Returns:
            A callable function.
        """
        return lambda: setattr(node, attr, pr.EmptyStatement())

    @staticmethod
    def _fmt(idx: int, count: int, desc: str) -> str:
        """Formatter for displaying unsupported nodes.

        Arguments:
            idx (int): Ranked order (1., 2., 3.…).
            count (int): Number of occurrences.
            desc (str): Node description.

        Returns:
            Formatted string expression for display.
        """
        order = f"{(str(idx) + '.'):<4}"
        times = f" {(str(count) + 'x ')}" if count > 1 else ' '
        return f"{order}{times}{desc}"

    @staticmethod
    def unsupported(omits: List[str]) -> None:
        """Display unsupported nodes as an ordered list.

        Arguments:
            omits (List[str]): List of unsupported AST nodes.
        """
        n = len(omits)
        if n == 1:
            logger.debug(f'Unsupported syntax: {omits[0]}')
        elif n > 1:
            codes = [(cnt, code) for (code, cnt) in Counter(omits).items()]
            codes = sorted(codes, key=lambda x: (-x[0], x[1]))
            logger.debug(f'Unsupported syntax {n}x, {len(codes)} unique')
            for i, cv in enumerate(codes):
                logger.debug(SyntaxUtils._fmt(i, *cv))

    @staticmethod
    def print_mod(node: pr.Node) -> pr.Node:
        """Prepare AST node for display as string.

        For example, for long blocks the body statement is removed.
        The original node is never modified; if some edit is applied, it is
        always applied to a copy of the AST node.

        Arguments:
            node (pr.Node): AST node.

        Returns:
            AST node conditionally formatted for display.
        """
        if isinstance(node, pr.ArrayRef):
            node = deepcopy(node)
            node.name = pr.ID(SyntaxUtils.array_name(node))
            node.subscript = pr.Constant('String', '…')
        elif hasattr(node, 'args') and hasattr(node.args, 'exprs'):
            node = deepcopy(node)
            node.args = pr.ExprList([pr.Constant('String', '…')])
        elif hasattr(node, 'stmt'):
            node = deepcopy(node)
            node.stmt = None
        return node


# noinspection PyPep8Naming
class BaseAnalysis(NodeHandler):
    """Base implementation for AST analysis."""

    PLUS, MINUS, MULT = '+', '-', '*'
    NEG, SIZEOF = '!', 'sizeof'

    BIN_OPS = {PLUS, MINUS, MULT}
    """Supported binary operators."""

    SIGN = {'+', '-'}
    PREFIX = {'++', '--'}
    INC, DEC = {'p++', '++'}, {'p--', '--'}
    INC_DEC = INC | DEC
    U_OPS = INC | DEC | {PLUS, MINUS, NEG, SIZEOF}
    """Supported unary operators."""

    @abstractmethod
    def handler(self, node: pr.Node, *args, **kwargs) \
            -> None:  # pragma: no cover
        """Handler for AST nodes that meet some abstract criteria."""
        pass

    def node_handler(self, node: pr.Node) -> Callable:
        # Maps node type to method to call.
        t_name = type(node).__name__
        return getattr(self, t_name) if hasattr(self, t_name) \
            else self.handler

    def recurse(self, node: pr.Node, *args, **kwargs) -> None:
        """Traverse AST nodes."""
        return (self.FCall(node, *args, **kwargs)
                if isinstance(node, pr.FuncCall) else
                self.node_handler(node)(node, *args, **kwargs))

    def _recurse_attr(self, node: pr.Node, attr: str, *args, **kwargs):
        """Analyze node's child at attribute, if exists."""
        if hasattr(node, attr) and getattr(node, attr):
            self.recurse(getattr(node, attr), *args, **kwargs)

    def _iter_attr(self, node: pr.Node, attr: str, *args, **kwargs):
        """Analyze node's children at attribute, if any exist."""
        if hasattr(node, attr) and getattr(node, attr):
            for n in getattr(node, attr):
                self.recurse(n, *args, **kwargs)

    def Assert(self, node: pr.FuncCall, *args, **kwargs):
        pass

    def Assume(self, node: pr.FuncCall, *args, **kwargs):
        pass

    def FCall(self, node: pr.FuncCall, *args, **kwargs):
        # Routes function call to the correct handler
        if isinstance(node.name, pr.ID):
            if node.name.name == 'assert':
                return self.Assert(node, *args, **kwargs)
            if node.name.name == 'assume':
                return self.Assume(node, *args, **kwargs)
        return self.FuncCall(node, *args, **kwargs)

    def Case(self, node: pr.Case, *args, **kwargs):
        self._iter_attr(node, 'stmts', *args, **kwargs)

    def Compound(self, node: pr.Compound, *args, **kwargs):
        self._iter_attr(node, 'block_items', *args, **kwargs)

    def DeclList(self, node: pr.DeclList, *args, **kwargs):
        self._iter_attr(node, 'decls', *args, **kwargs)

    def Default(self, node: pr.Default, *args, **kwargs):
        self._iter_attr(node, 'stmts', *args, **kwargs)

    def ExprList(self, node: pr.ExprList, *args, **kwargs):
        self._iter_attr(node, 'exprs', *args, **kwargs)

    def ParamList(self, node: pr.ParamList, *args, **kwargs):
        self._iter_attr(node, 'params', *args, **kwargs)


class Coverage(BaseAnalysis):
    """Simple analysis of AST syntax to determine if AST contains
    only supported language features.

    Attributes:
        node(pr.Node): AST node.
        omit(List[str]): List of unsupported commands.
        clear_list(List[Callable]): Functions to clear unsupported syntax.
    """

    def __init__(self, node: pr.Node):
        self.node = node
        self.omit = []
        self.clear_list = []
        self.recurse(self.node)

    @property
    def full(self) -> bool:
        """True if entire syntax tree is fully covered by analysis."""
        return len(self.omit) == 0

    def report(self) -> Coverage:
        """Display syntax coverage for inspected AST node."""
        SyntaxUtils.unsupported(self.omit)
        return self

    def ast_mod(self) -> Coverage:
        """Removes unsupported AST nodes in place."""
        n = len(self.omit)
        assert (n == len(self.clear_list))
        [callable_() for callable_ in self.clear_list]
        self.omit, self.clear_list = [], []
        logger.debug(f"Removed unsupported syntax: {n} node(s)")
        return self

    @staticmethod
    def loop_compat(node: pr.For) -> Tuple[bool, Optional[str]]:
        r"""Check if C-language for loop is compatible with an "mwp-loop".

        The mwp-loop has form $\text{loop} \; \texttt{X} \; \{ \texttt{C} \}$.
        Try to identify if C-language `for` loop has a similar form,
        _repeat X times command C_. The variable X is not allowed to
        occur in the body C of the loop.

        Arguments:
            node: AST node to inspect.

        Returns:
            A tuple where the first item is a compatibility result: True if
                for loop is mwp-loop compatible, otherwise False. The second
                is the name of iteration guard variable X, possibly `None`.
        """
        loop_x, body = Variables.loop_guard(node)
        if len(loop_x) != 1:  # exactly one guard variable
            logger.debug(f"Unknown loop guard variable in {loop_x}")
            return False, None
        x_var = loop_x[0]
        if x_var in body:
            logger.warning(f"Variable {x_var} occurs in loop body")
            return False, None
        return True, x_var

    def handler(self, node: pr.Node, *args, **kwargs):
        """Make a list of uncovered nodes."""
        # add to clear list
        self.clear_list.append(kwargs['clear'])  # should always exist
        # display edit, then add to list of issues to display
        node = SyntaxUtils.print_mod(node)
        self.omit.append(pr.to_c(node, compact=True))

    def recurse(self, node: pr.Node, *args, **kwargs):
        if isinstance(node, (pr.TernaryOp, pr.ArrayRef, pr.Switch)):
            self.handler(node, *args, **kwargs)
        else:
            super().recurse(node, *args, **kwargs)

    def _iter_attr(self, node: pr.Node, attr: str, *args, **kwargs):
        if hasattr(node, attr) and getattr(node, attr):
            for n in getattr(node, attr):
                cl = SyntaxUtils.rm_child(node, attr, n)
                self.recurse(n, *args, **{**kwargs, 'clear': cl})

    def FuncCall(self, node: pr.FuncCall, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def Assignment(self, node: pr.Assignment, *args, **kwargs):
        allow = pr.BinaryOp, pr.Constant, pr.ID, pr.UnaryOp
        right = (node.rvalue.expr if isinstance(node.rvalue, pr.Cast)
                 else node.rvalue)
        if not (node.op == "=" and isinstance(node.lvalue, pr.ID) and
                isinstance(right, allow)):
            self.handler(node, *args, **kwargs)
        else:
            self.recurse(node.lvalue, *args, **kwargs)
            self.recurse(right, *args, **kwargs)

    def BinaryOp(self, node: pr.BinaryOp, *args, **kwargs):
        left, right = node.left, node.right
        lf = left.expr if isinstance(left, pr.Cast) else left
        rt = right.expr if isinstance(right, pr.Cast) else right
        allow = pr.Constant, pr.ID
        if not (node.op in self.BIN_OPS and isinstance(lf, allow) and
                isinstance(rt, allow)):
            self.handler(node, *args, **kwargs)

    def Cast(self, node: pr.Cast, *args, **kwargs):
        self._recurse_attr(node, 'expr', *args, **kwargs)

    def Decl(self, node: pr.Decl, *args, **kwargs):
        init = node.init if hasattr(node, 'init') else None
        type_ = node.type if hasattr(node, 'type') else None
        if not (isinstance(type_, pr.TypeDecl) and init is None):
            self.handler(node, *args, **kwargs)

    def DoWhile(self, node: pr.DoWhile, *args, **kwargs):
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def For(self, node: pr.For, *args, **kwargs):
        if not self.loop_compat(node)[0]:
            self.handler(node, *args, **kwargs)
        else:
            self._recurse_attr(node, 'stmt', *args, **kwargs)

    def FuncDef(self, node: pr.FuncDef, *args, **kwargs):
        self._recurse_attr(node.decl.type, 'args', *args, **kwargs)
        self._recurse_attr(node, 'body', *args, **kwargs)

    def If(self, node: pr.If, *args, **kwargs):
        t_kwargs = {**kwargs, 'clear': SyntaxUtils.rm_attr(node, 'iftrue')}
        self._recurse_attr(node, 'iftrue', *args, **t_kwargs)
        e_kwargs = {**kwargs, 'clear': SyntaxUtils.rm_attr(node, 'iffalse')}
        self._recurse_attr(node, 'iffalse', *args, **e_kwargs)

    def Return(self, node: pr.Return, *args, **kwargs):
        self._recurse_attr(node, 'expr', *args, **kwargs)

    def UnaryOp(self, node: pr.UnaryOp, *args, **kwargs):
        if not (node.op in self.U_OPS and isinstance(
                node.expr, (pr.ID, pr.Constant, pr.Cast, pr.UnaryOp))):
            self.handler(node, *args, **kwargs)
        else:
            self._recurse_attr(node, 'expr', *args, **kwargs)

    def While(self, node: pr.While, *args, **kwargs):
        self._recurse_attr(node, 'stmt', *args, **kwargs)


class FindLoops(BaseAnalysis):
    """Finds all loop nodes in an AST.

    Attributes:
        loops (List[pr.LoopT]): Loop nodes.
    """

    def __init__(self, node: pr.Node):
        self.loops: List[pr.LoopT] = []
        self.recurse(node)

    def handler(self, node: pr.LoopT, *args, **kwargs) -> None:
        """Make a (flat) list of the discovered loops."""
        self.loops.append(node)

    def DoWhile(self, node: pr.DoWhile, *args, **kwargs):
        self.handler(node, *args, **kwargs)
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def For(self, node: pr.For, *args, **kwargs):
        if Coverage.loop_compat(node)[0]:
            self.handler(node, *args, **kwargs)
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def FuncDef(self, node: pr.FuncDef, *args, **kwargs):
        self._recurse_attr(node, 'body', *args, **kwargs)

    def If(self, node: pr.If, *args, **kwargs):
        self._recurse_attr(node, 'iftrue', *args, **kwargs)
        self._recurse_attr(node, 'iffalse', *args, **kwargs)

    def Switch(self, node: pr.Switch, *args, **kwargs):
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def While(self, node: pr.While, *args, **kwargs):
        self.handler(node, *args, **kwargs)
        self._recurse_attr(node, 'stmt', *args, **kwargs)


class Variables(BaseAnalysis):
    """Find variables in an AST.

    Attributes:
        vars (List[str]): List of variables.
    """

    RESERVED = ['true', 'false']
    """List of reserved names that are not variables;
    see [issue #150](https://github.com/statycc/pymwp/issues/150)."""

    def __init__(self, *nodes: pr.Node):
        self.vars = []
        [self.recurse(node) for node in nodes]
        self.vars = sorted(self.vars)

    @staticmethod
    def loop_guard(node: pr.For) -> Tuple[List[str], List[str]]:
        """Find variables in a for loop.

        Arguments:
            node (pr.For): A for-loop AST node.

        Returns:
            Two lists of variables: `(loop_guard, body_variables)`.
        """
        iters, srcs = SyntaxUtils.init_vars(node.init)
        conds = Variables(node.cond).vars
        nxt = Variables(node.next).vars
        iters = list(set(iters) | set(nxt))
        body = Variables(node.stmt).vars

        loop_vars = set(conds) | set(srcs)
        loop_x = list(loop_vars - set(iters))

        info = [('guard', loop_x), ('body', body)]
        info = [f"{lbl}: {' '.join(v) or '?'}" for lbl, v in info]
        logger.debug(f"for-loop {', '.join(info)}")
        return loop_x, body

    def handler(self, node: pr.Node, *args, **kwargs):
        """Record the name of a discovered variable."""
        if hasattr(node, 'name') and node.name:
            if node.name not in self.vars:
                self.vars.append(node.name)

    def Assignment(self, node: pr.Assignment, *args, **kwargs):
        self._recurse_attr(node, 'lvalue', *args, **kwargs)
        self._recurse_attr(node, 'rvalue', *args, **kwargs)

    def BinaryOp(self, node: pr.BinaryOp, *args, **kwargs):
        self._recurse_attr(node, 'left', *args, **kwargs)
        self._recurse_attr(node, 'right', *args, **kwargs)

    def Cast(self, node: pr.Cast, *args, **kwargs):
        self._recurse_attr(node, 'expr', *args, **kwargs)

    def Decl(self, node: pr.Decl, *args, **kwargs):
        # skip when not TypeDecl => PtrDecl is ignored
        if hasattr(node, 'type') and isinstance(node.type, pr.TypeDecl):
            self.handler(node, *args, **kwargs)
        self._recurse_attr(node, 'init', *args, **kwargs)

    def DoWhile(self, node: pr.DoWhile, *args, **kwargs):
        self._recurse_attr(node, 'cond', *args, **kwargs)
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def For(self, node: pr.For, *args, **kwargs):
        # generally skip control block => use loop_guard
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def FuncDef(self, node: pr.FuncDef, *args, **kwargs):
        self._recurse_attr(node.decl.type, 'args', *args, **kwargs)
        self._recurse_attr(node, 'body', *args, **kwargs)

    def ID(self, node: pr.ID, *args, **kwargs):
        if node.name not in Variables.RESERVED:
            self.handler(node, *args, **kwargs)

    def If(self, node: pr.If, *args, **kwargs):
        self._recurse_attr(node, 'iftrue', *args, **kwargs)
        self._recurse_attr(node, 'iffalse', *args, **kwargs)

    def Return(self, node: pr.Return, *args, **kwargs):
        # Search return because could be a single-line expr
        self._recurse_attr(node, 'expr', *args, **kwargs)

    def UnaryOp(self, node: pr.UnaryOp, *args, **kwargs):
        if node.op in self.U_OPS:
            self._recurse_attr(node, 'expr', *args, **kwargs)

    def While(self, node: pr.While, *args, **kwargs):
        self._recurse_attr(node, 'cond', *args, **kwargs)
        self._recurse_attr(node, 'stmt', *args, **kwargs)
