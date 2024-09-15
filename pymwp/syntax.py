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
from abc import ABC, abstractmethod
from collections import Counter
from copy import deepcopy
from typing import List, Any, Callable, Tuple, Optional

from .parser import Parser as pr

logger = logging.getLogger(__name__)


class BaseAnalysis(ABC):
    """Base implementation for AST analysis."""

    INC_DEC = {'p++', '++', 'p--', '--'}
    U_OPS = INC_DEC | {'+', '-', '!', 'sizeof'}
    BIN_OPS = {"+", "-", "*"}

    @abstractmethod
    def handler(self, node: Any, *args, **kwargs) -> None:
        """Handle AST nodes that meets some (abstract) criteria."""
        pass

    def recurse(self, node: Any, *args, **kwargs) -> None:
        """Recursively traverse AST nodes."""
        if isinstance(node, pr.Constant):
            return self.constant(node, *args, **kwargs)
        if isinstance(node, pr.ID):
            return self.id_(node, *args, **kwargs)
        if isinstance(node, pr.Decl):
            return self.decl(node, *args, **kwargs)
        if isinstance(node, pr.DeclList):
            return self.decl_list(node, *args, **kwargs)
        if isinstance(node, pr.Assignment):
            return self.assign(node, *args, **kwargs)
        if isinstance(node, pr.UnaryOp):
            return self.unary(node, *args, **kwargs)
        if isinstance(node, pr.BinaryOp):
            return self.binop(node, *args, **kwargs)
        if isinstance(node, pr.Compound):
            return self.compound(node, *args, **kwargs)
        if isinstance(node, pr.ExprList):
            return self.expr_list(node, *args, **kwargs)
        if isinstance(node, pr.If):
            return self.if_(node, *args, **kwargs)
        if isinstance(node, pr.While):
            return self.while_(node, *args, **kwargs)
        if isinstance(node, pr.DoWhile):
            return self.do_while(node, *args, **kwargs)
        if isinstance(node, pr.For):
            return self.for_(node, *args, **kwargs)
        if isinstance(node, pr.ArrayRef):
            return self.array_ref(node, *args, **kwargs)
        if isinstance(node, pr.Cast):
            return self.cast(node, *args, **kwargs)
        if isinstance(node, pr.TernaryOp):
            return self.ternary(node, *args, **kwargs)
        if isinstance(node, pr.Return):
            return self.return_(node, *args, **kwargs)
        if isinstance(node, pr.Break):
            return self.break_(node, *args, **kwargs)
        if isinstance(node, pr.Continue):
            return self.continue_(node, *args, **kwargs)
        if isinstance(node, pr.FuncCall):
            if isinstance(node.name, pr.ID) and node.name.name == 'assert':
                return self.assert_(node, *args, **kwargs)
            return self.func_call(node, *args, **kwargs)
        if isinstance(node, pr.FuncDef):
            return self.func_def(node, *args, **kwargs)
        if isinstance(node, pr.Switch):
            return self.switch_(node, *args, **kwargs)
        if isinstance(node, pr.ParamList):
            return self.param_list(node, *args, **kwargs)
        self.handler(node, *args, **kwargs)

    def _recurse_attr(self, node: Any, attr: str, *args, **kwargs) -> None:
        """Analyze child at node.attribute.

        Arguments:
            node: AST node.
            attr: node attribute to analyze.
        """
        if hasattr(node, attr) and getattr(node, attr):
            self.recurse(getattr(node, attr), *args, **kwargs)

    def _iter_attr(self, node: Any, attr: str, *args, **kwargs) -> None:
        """Iteratively analyze children at `node.attribute`,
        where the attribute is an iterable.

        Arguments:
            node: AST node.
            attr: node attribute to analyze.
        """
        if hasattr(node, attr) and getattr(node, attr):
            for n in getattr(node, attr):
                self.recurse(n, *args, **kwargs)

    @staticmethod
    def _array_name(node: pr.ArrayRef) -> str:
        """Find array name for array node. If multidimensional,
        will iterate to find the nested node with name.

        Arguments:
            node: array AST node.

        Returns:
            Array name.
        """
        name_node = node.name
        while not isinstance(name_node, pr.ID):
            name_node = name_node.name
        return name_node.name

    def array_ref(self, node: pr.ArrayRef, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def assert_(self, node: pr.Assert, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def assign(self, node: pr.Assignment, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def binop(self, node: pr.BinaryOp, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def break_(self, node: pr.Break, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def cast(self, node: pr.Cast, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def compound(self, node: pr.Compound, *args, **kwargs):
        self._iter_attr(node, 'block_items', *args, **kwargs)

    def constant(self, node: pr.Constant, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def continue_(self, node: pr.Continue, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def decl(self, node: pr.Decl, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def decl_list(self, node: pr.DeclList, *args, **kwargs):
        self._iter_attr(node, 'decls', *args, **kwargs)

    def do_while(self, node: pr.DoWhile, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def expr_list(self, node: pr.ExprList, *args, **kwargs):
        self._iter_attr(node, 'exprs', *args, **kwargs)

    def for_(self, node: pr.For, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def func_call(self, node: pr.FuncCall, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def func_def(self, node: pr.FuncDef, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def id_(self, node: pr.ID, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def if_(self, node: pr.If, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def param_list(self, node: pr.ParamList, *args, **kwargs):
        self._iter_attr(node, 'params', *args, **kwargs)

    def return_(self, node: pr.Return, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def switch_(self, node: pr.Switch, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def ternary(self, node: pr.TernaryOp, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def unary(self, node: pr.UnaryOp, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def while_(self, node: pr.While, *args, **kwargs):
        self.handler(node, *args, **kwargs)


class Variables(BaseAnalysis):
    """Locate and analyze variables in an AST.

    Attributes:
        vars (List[str]): List of variables.
    """

    def __init__(self, *nodes: Any):
        self.vars = []
        [self.recurse(node) for node in nodes]
        self.vars = sorted(self.vars)

    def handler(self, node: Any, *args, **kwargs):
        if hasattr(node, 'name') and node.name:
            if node.name not in self.vars:
                self.vars.append(node.name)

    def array_ref(self, node: pr.ArrayRef, *args, **kwargs):
        self._recurse_attr(node, 'subscript', *args, **kwargs)

    def assert_(self, node: pr.FuncCall, *args, **kwargs):
        return

    def assign(self, node: pr.Assignment, *args, **kwargs):
        self._recurse_attr(node, 'lvalue', *args, **kwargs)
        self._recurse_attr(node, 'rvalue', *args, **kwargs)

    def binop(self, node: pr.BinaryOp, *args, **kwargs):
        self._recurse_attr(node, 'left', *args, **kwargs)
        self._recurse_attr(node, 'right', *args, **kwargs)

    def break_(self, node: pr.Break, *args, **kwargs):
        return

    def cast(self, node: pr.Cast, *args, **kwargs):
        self._recurse_attr(node, 'expr', *args, **kwargs)

    def constant(self, node: pr.Constant, *args, **kwargs):
        return

    def continue_(self, node: pr.Continue, *args, **kwargs):
        return

    def decl(self, node: pr.Decl, *args, **kwargs):
        self.handler(node, *args, **kwargs)
        self._recurse_attr(node, 'init', *args, **kwargs)

    def do_while(self, node: pr.DoWhile, *args, **kwargs):
        self._recurse_attr(node, 'cond', *args, **kwargs)
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def for_(self, node: pr.For, *args, **kwargs):
        # skip control block in general
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def func_call(self, node: pr.FuncCall, *args, **kwargs):
        self._iter_attr(node, 'args', *args, **kwargs)

    def func_def(self, node: pr.FuncDef, *args, **kwargs):
        self.recurse(node.decl.type.args, *args, **kwargs)
        self.recurse(node.body, *args, **kwargs)

    def id_(self, node: pr.ID, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def if_(self, node: pr.If, *args, **kwargs):
        self._recurse_attr(node, 'iftrue', *args, **kwargs)
        self._recurse_attr(node, 'iffalse', *args, **kwargs)

    def return_(self, node: pr.Return, *args, **kwargs):
        self._recurse_attr(node, 'expr', *args, **kwargs)

    def switch_(self, node: pr.Switch, *args, **kwargs):
        return  # uncovered anyway

    def ternary(self, node: pr.TernaryOp, *args, **kwargs):
        self._recurse_attr(node, 'cond', *args, **kwargs)
        self._recurse_attr(node, 'iftrue', *args, **kwargs)
        self._recurse_attr(node, 'iffalse', *args, **kwargs)

    def unary(self, node: pr.UnaryOp, *args, **kwargs):
        self._recurse_attr(node, 'expr', *args, **kwargs)

    def while_(self, node: pr.While, *args, **kwargs):
        self._recurse_attr(node, 'cond', *args, **kwargs)
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    @staticmethod
    def loop_control(node: pr.For) -> Tuple[List[str], List[str]]:
        """Find variables in a for loop control block.

        Arguments:
            node: for-loop node.

        Returns:
            Two lists of variables: (loop controls, body variables).
        """
        iters, decls, srcs = [], [], []

        def id_(node_, tgt):
            if isinstance(node_, pr.ID):
                tgt += [node_.name]

        # init is an assignment (x=e; ...)
        def asgn(node_, itrs, values):
            if isinstance(node_, pr.Assignment) and node_.op == '=':
                id_(node_.lvalue, itrs)
                id_(node_.rvalue, values)
                return True

        if not asgn(node.init, iters, srcs):
            # init is a declaration (int i=0; ...)
            if isinstance(node.init, pr.DeclList):
                for decl in node.init.decls:
                    decls += [decl.name]
                    id_(decl.init, srcs)
            # init is a list (i=0, j=x; ...)
            elif isinstance(node.init, pr.ExprList):
                for expr in node.init.exprs:
                    asgn(expr, iters, srcs)

        conds = Variables(node.cond).vars
        body = Variables(node.stmt).vars
        nxt = Variables(node.next).vars
        iters = list(set(iters) | set(nxt))

        # control expr + source-vars from initialization
        loop_vars = list(set(conds) | set(srcs))
        # loop_vars - declarations - iterators
        loop_x = list(set(loop_vars) - set(decls) - set(iters))

        info = [('iters', iters), ('decl', decls), ('maybe', loop_vars),
                ('control', loop_x), ('\n  body', body)]
        info = [f"{lbl}: {', '.join(v) or '?'}" for lbl, v in info]
        logger.debug(f"loop variables\n  {'; '.join(info)}")
        return loop_x, body


class Coverage(BaseAnalysis):
    """Simple analysis of AST syntax to determine if AST contains
    only supported language features.

    Attributes:
        node(Any): AST node.
        omit(List[str]): List of _unsupported commands.
        to_clear(List[Callable]): Anonymous functions to remove
            _unsupported commands.
    """

    def __init__(self, node: Any):
        self.node = node
        self.omit = []
        self.to_clear = []
        self.recurse(self.node)

    @property
    def full(self) -> bool:
        """True if entire syntax tree is fully covered by analysis."""
        return len(self.omit) == 0

    def report(self) -> Coverage:
        """Display syntax coverage for AST node."""
        if len(self.omit):
            self._unsupported(self.omit)
        return self

    def ast_mod(self) -> Coverage:
        """Removes unsupported AST nodes in place."""
        n = len(self.omit)
        assert (n == len(self.to_clear))
        [callable_() for callable_ in self.to_clear]
        self.omit, self.to_clear = [], []
        logger.warning(f"removed _unsupported syntax: {n} node(s)")
        return self

    @staticmethod
    def _fmt(idx: int, count: int, desc: str) -> str:
        """Formatter for displaying _unsupported nodes.

        Arguments:
            idx: ranked order (1., 2., 3....).
            count: number of occurrences.
            desc: node description.

        Returns:
              Formatted string expression for display.
        """
        order = f"{(str(idx) + '.'):<4}"
        times = f" {(str(count) + 'x ')}" if count > 1 else ' '
        return f"{order}{times}{desc}"

    @staticmethod
    def _unsupported(omits: List[str]) -> None:
        """Display _unsupported nodes as an ordered list.

        Arguments:
            omits: list of _unsupported AST nodes.
        """
        if len(omits) < 2:
            if len(omits) == 1:
                logger.debug(f'Unsupported syntax: {omits[0]}')
            return

        codes = [(cnt, code) for (code, cnt) in Counter(omits).items()]
        codes = sorted(codes, key=lambda x: (-x[0], x[1]))
        lines = [Coverage._fmt(i + 1, *cv) for i, cv in enumerate(codes)]
        om, uq = len(omits), len(lines)
        logger.debug(f'Unsupported syntax {om}x, {uq} unique')
        [logger.debug(line) for line in lines]

    @staticmethod
    def _clearer(node: Any, attr: str, child: Any) -> Callable:
        """Construct a callable function to clear a child node.

        Using a callable allows flagging tree nodes for removal, while
        iterating a tree, then applying the removals afterward.

        Arguments:
            node: parent node.
            attr: parent's attribute name that contains child, e.g., stmt.
            child: child node.

        Returns:
            A callable function.
        """
        return lambda: getattr(node, attr).remove(child) \
            if child in getattr(node, attr) else None

    def _clear_stmt(self, node: Any, *args, **kwargs):
        """Remove statement attribute of an unhandled node."""
        node_ = deepcopy(node)
        node_.stmt = None
        self.handler(node_, *args, **kwargs)

    def _iter_attr(self, node: Any, attr: str, *args, **kwargs):
        """Iteratively analyze children at node.attribute."""
        if hasattr(node, attr) and getattr(node, attr):
            for n in getattr(node, attr):
                cl = Coverage._clearer(node, attr, n)
                self.recurse(n, *args, **{**kwargs, 'clear': cl})

    @staticmethod
    def loop_compat(node: pr.For) -> Tuple[bool, Optional[str]]:
        r"""Check if C-language for loop is compatible with an "mwp-loop".

        The mwp-loop has form `loop X { C }`. Try to identify if C-language
        `for` loop has a similar form, "repeat command X times". The
        variable `X` is not allowed to occur in the body `C` of the loop.

        Arguments:
            node: AST node to inspect.

        Returns:
            A tuple containing <bool, string>. The first is a compatibility
                result: True if for loop is mwp-loop compatible, otherwise
                False. The second is the name of iteration variable `X`,
                possibly `None`.
        """
        loop_x, body = Variables.loop_control(node)
        if len(loop_x) != 1:  # exactly one control variable
            logger.debug(
                f"Too many loop control variables: ({', '.join(loop_x)})"
                if len(loop_x) > 1 else "Unknown loop control variable")
            return False, None
        x_var = loop_x[0]
        if x_var in body:
            logger.warning(f"Variable {x_var} occurs in loop body")
            return False, None
        return True, x_var

    def handler(self, node: Any, *args, **kwargs):
        """Make a list of uncovered nodes."""
        self.omit.append(pr.to_c(node, compact=True))
        self.to_clear.append(kwargs['clear'])  # should always exist

    def recurse(self, node: Any, *args, **kwargs):
        skips = (pr.ID, pr.Constant, pr.Break, pr.Continue, pr.Return)
        if next((s for s in skips if isinstance(node, s)), None) is None:
            return super().recurse(node, *args, **kwargs)

    def array_ref(self, node: pr.ArrayRef, *args, **kwargs):
        node_ = deepcopy(node)
        node_.name = pr.ID(BaseAnalysis._array_name(node))
        node_.subscript = pr.Constant('String', '…')
        self.handler(node_, *args, **kwargs)

    def assert_(self, node: pr.FuncCall, *args, **kwargs):
        return

    def assign(self, node: pr.Assignment, *args, **kwargs):
        if node.op != "=":  # only = is an allowed operator
            return self.handler(node, *args, **kwargs)
        self.recurse(node.lvalue, *args, **kwargs)
        self.recurse(node.rvalue, *args, **kwargs)

    def binop(self, node: pr.BinaryOp, *args, **kwargs):
        # only truly binary ops are allowed, not n-ary.
        if (node.op not in self.BIN_OPS or not (
                (isinstance(node.left, pr.Constant) or
                 isinstance(node.left, pr.ID)) and
                (isinstance(node.right, pr.Constant) or
                 isinstance(node.right, pr.ID)))):
            self.handler(node, *args, **kwargs)

    def cast(self, node: pr.Cast, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def decl(self, node: pr.Decl, *args, **kwargs):
        init = node.init if hasattr(node, 'init') else None
        type_ = node.type if hasattr(node, 'type') else None
        if not (isinstance(type_, pr.TypeDecl) and init is None):
            self.handler(node, *args, **kwargs)

    def do_while(self, node: pr.DoWhile, *args, **kwargs):
        self._recurse_attr(node, 'stmt', *args, **kwargs)

    def for_(self, node: pr.For, *args, **kwargs):
        compat, _ = self.loop_compat(node)
        self._clear_stmt(node, *args, **kwargs) \
            if not compat else \
            self._recurse_attr(node, 'stmt', *args, **kwargs)

    def func_call(self, node: pr.FuncCall, *args, **kwargs):
        node_ = deepcopy(node)
        if len(node_.args.exprs):
            node_.args = pr.ExprList([pr.Constant('String', '…')])
        self.handler(node_, *args, **kwargs)

    def func_def(self, node: pr.FuncDef, *args, **kwargs):
        self.recurse(node.decl.type.args, *args, **kwargs)
        self.recurse(node.body, *args, **kwargs)

    def if_(self, node: pr.If, *args, **kwargs):
        self._recurse_attr(node, 'iftrue', *args, **kwargs)
        self._recurse_attr(node, 'iffalse', *args, **kwargs)

    def switch_(self, node: pr.Switch, *args, **kwargs):
        self._clear_stmt(node, *args, **kwargs)

    def ternary(self, node: pr.TernaryOp, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def unary(self, node: pr.UnaryOp, *args, **kwargs):
        self.handler(node, *args, **kwargs) \
            if node.op not in self.U_OPS \
            else self._recurse_attr(node, 'expr', *args, **kwargs)

    def while_(self, node: pr.While, *args, **kwargs):
        self._recurse_attr(node, 'stmt', *args, **kwargs)
