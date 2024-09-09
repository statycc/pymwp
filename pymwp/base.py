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

# noinspection DuplicatedCode
import logging
from collections import Counter
from copy import deepcopy
from typing import List, Any, Callable, Tuple, Optional

from .parser import Parser as pr

logger = logging.getLogger(__name__)


class BaseAnalysis:
    """Base implementation for AST analysis."""

    INC_DEC = {'p++', '++', 'p--', '--'}
    U_OPS = INC_DEC | {'+', '-', '!', 'sizeof'}
    BIN_OPS = {"+", "-", "*"}

    def handler(self, node: Any, *args, **kwargs):
        pass  # do something with node

    def recurse(self, node: Any, *args, **kwargs):
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
            return self.func_call(node, *args, **kwargs)
        if isinstance(node, pr.FuncDef):
            return self.func_def(node, *args, **kwargs)
        if isinstance(node, pr.Switch):
            return self.switch_(node, *args, **kwargs)
        if isinstance(node, pr.ParamList):
            return self.param_list(node, *args, **kwargs)
        self.handler(node, *args, **kwargs)

    def recurse_attr(self, node: Any, attr: str, *args, **kwargs):
        """Analyze child at node.attribute."""
        if hasattr(node, attr) and getattr(node, attr):
            self.recurse(getattr(node, attr), *args, **kwargs)

    def iter_attr(self, node: Any, attr: str, *args, **kwargs):
        """Iteratively analyze children at node.attribute."""
        if hasattr(node, attr) and getattr(node, attr):
            for n in getattr(node, attr):
                self.recurse(n, *args, **kwargs)

    @staticmethod
    def array_name(node: pr.ArrayRef) -> str:
        name_node = node.name
        while not isinstance(name_node, pr.ID):
            name_node = name_node.name
        return name_node.name

    def array_ref(self, node: pr.ArrayRef, *args, **kwargs):
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
        self.handler(node, *args, **kwargs)

    def constant(self, node: pr.Constant, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def continue_(self, node: pr.Continue, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def decl(self, node: pr.Decl, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def decl_list(self, node: pr.DeclList, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def do_while(self, node: pr.DoWhile, *args, **kwargs):
        self.handler(node, *args, **kwargs)

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
        self.handler(node, *args, **kwargs)

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
    """Locate and analyze variables in an AST."""

    def __init__(self, *nodes: Any):
        self.vars = []
        [self.recurse(node) for node in nodes]
        self.vars = sorted(self.vars)

    def handler(self, node: Any, *args, **kwargs):
        if hasattr(node, 'name') and node.name:
            if node.name not in self.vars:
                self.vars.append(node.name)

    def array_ref(self, node: pr.ArrayRef, *args, **kwargs):
        self.recurse_attr(node, 'subscript', *args, **kwargs)

    def assign(self, node: pr.Assignment, *args, **kwargs):
        self.recurse_attr(node, 'lvalue', *args, **kwargs)
        self.recurse_attr(node, 'rvalue', *args, **kwargs)

    def binop(self, node: pr.BinaryOp, *args, **kwargs):
        self.recurse_attr(node, 'left', *args, **kwargs)
        self.recurse_attr(node, 'right', *args, **kwargs)

    def break_(self, node: pr.Break, *args, **kwargs):
        return

    def compound(self, node: pr.Compound, *args, **kwargs):
        self.iter_attr(node, 'block_items', *args, **kwargs)

    def constant(self, node: pr.Constant, *args, **kwargs):
        return

    def continue_(self, node: pr.Continue, *args, **kwargs):
        return

    def decl(self, node: pr.Decl, *args, **kwargs):
        self.handler(node, *args, **kwargs)
        self.recurse_attr(node, 'init', *args, **kwargs)

    def decl_list(self, node: pr.DeclList, *args, **kwargs):
        self.iter_attr(node, 'decls', *args, **kwargs)

    def do_while(self, node: pr.DoWhile, *args, **kwargs):
        self.recurse_attr(node, 'cond', *args, **kwargs)
        self.recurse_attr(node, 'stmt', *args, **kwargs)

    def for_(self, node: pr.For, *args, **kwargs):
        # skip control block in general
        self.recurse_attr(node, 'stmt', *args, **kwargs)

    def func_call(self, node: pr.FuncCall, *args, **kwargs):
        self.iter_attr(node, 'args', *args, **kwargs)

    def func_def(self, node: pr.FuncDef, *args, **kwargs):
        self.recurse(node.decl.type.args, *args, **kwargs)
        self.recurse(node.body, *args, **kwargs)

    def id_(self, node: pr.ID, *args, **kwargs):
        self.handler(node, *args, **kwargs)

    def if_(self, node: pr.If, *args, **kwargs):
        self.recurse_attr(node, 'iftrue', *args, **kwargs)
        self.recurse_attr(node, 'iffalse', *args, **kwargs)

    def param_list(self, node: pr.ParamList, *args, **kwargs):
        self.iter_attr(node, 'params', *args, **kwargs)

    def return_(self, node: pr.Return, *args, **kwargs):
        self.recurse_attr(node, 'expr', *args, **kwargs)

    def switch_(self, node: pr.Switch, *args, **kwargs):
        return  # uncovered anyway

    def unary(self, node: pr.UnaryOp, *args, **kwargs):
        self.recurse_attr(node, 'expr', *args, **kwargs)

    def while_(self, node: pr.While, *args, **kwargs):
        self.recurse_attr(node, 'cond', *args, **kwargs)
        self.recurse_attr(node, 'stmt', *args, **kwargs)

    @staticmethod
    def loop_control(node: pr.For):
        it, dc, vl = [], [], []
        if isinstance(node.init, pr.Assignment) and node.init.op == "=":
            if isinstance(node.init.lvalue, pr.ID):
                it += [node.init.lvalue.name]
            if isinstance(node.init.rvalue, pr.ID):
                vl += [node.init.rvalue.name]
        elif isinstance(node.init, pr.DeclList):
            for decl in node.init.decls:
                if isinstance(decl, pr.Decl):
                    dc += [decl.name]
                    if isinstance(decl.init, pr.ID):
                        vl += [decl.init.name]
        elif isinstance(node.init, pr.ExprList):
            for expr in node.init.exprs:
                if isinstance(expr, pr.Assignment) and expr.op == "=":
                    if isinstance(expr.lvalue, pr.ID):
                        it += [expr.lvalue.name]
                    if isinstance(expr.rvalue, pr.ID):
                        vl += [expr.rvalue.name]
        cv = Variables(node.cond).vars
        body = Variables(node.stmt).vars
        it = list(set(it) | set(Variables(node.next).vars))
        # loop_x is (control expr U init vars) - decl - iterators
        loop_x = list((set(cv) | set(vl)) - set(dc) - set(it))
        logger.debug(f"loop iterators: {it}")
        logger.debug(f"loop declarations: {dc}")
        logger.debug(f"loop variables: {list(set(cv) | set(vl))}")
        logger.debug(f"loop control: {loop_x}")
        logger.debug(f"loop body: {body}")
        return loop_x, body


class SyntaxCover(BaseAnalysis):
    """Determine if C-lang AST is fully covered by analysis syntax.

    Optionally, remove unsupported AST nodes from the tree;
    set `modify` to `True` to permit the modification.
    """

    def __init__(self, node: Any, modify: bool = False):
        self.omit = []
        self.to_clear = []
        self.recurse(node)
        self.unsupported(self.omit)
        self.apply_mod(self.to_clear, self.omit) if modify else None

    @property
    def is_full(self):
        """True if entire syntax tree is covered by analysis."""
        return len(self.omit) == 0

    @staticmethod
    def fmt(idx: int, count: int, desc: str):
        """Formatter for displaying unsupported nodes.

        Arguments:
            idx: ranked order (1., 2., 3....)
            count: number of occurrences
            desc: node description

        Returns:
              Formatted string expression for display.
        """
        order = f"{str(idx) + '.':<4}"
        times = f"{str(count) + 'x':<4}"
        return f"{order} {times} {desc}"

    @staticmethod
    def unsupported(omits: List[str]):
        """Display unsupported nodes as an ordered list."""
        codes = sorted([
            (cnt, code) for (code, cnt) in
            Counter(omits).items()], key=lambda x: (-x[0], x[1]))
        lines = '\n'.join([
            SyntaxCover.fmt(i + 1, c, v) for i, (c, v)
            in enumerate(codes)])
        tot = len(omits)
        if lines:
            logger.warning(f'Unsupported syntax ({tot}x)\n{lines}')

    @staticmethod
    def clearer(node: Any, attr: str, child: Any):
        """Construct a callable function to clear a child node.

        Using a callable allows flagging tree nodes for removal, while
        iterating a tree, then applying the removals afterward.

        Arguments:
            node: parent node
            attr: parent's attribute name that contains child, e.g., stmt
            child: child node

        Returns:
            A callable function.
        """
        return lambda: getattr(node, attr).remove(child) \
            if child in getattr(node, attr) else None

    @staticmethod
    def apply_mod(to_clear: list[Callable], omits: list[str]) -> None:
        """Remove encountered, unsupported AST-nodes from tree, in place.

        Arguments:
            to_clear: list of callable functions that clear nodes.
            omits: list of detected unsupported syntax
        """
        assert (len(omits) == len(to_clear))
        [callable_() for callable_ in to_clear]
        logger.info(f"Skipping unsupported syntax: {len(omits)} nodes")

    @staticmethod
    def loop_compat(node: pr.For) -> Tuple[bool, Optional[str]]:
        """Check if C-language for loop is compatible with a "mwp-loop".

        The mwp-loop has form loop X { C }. Try to identify C-language
        for loops that have similar form ("repeat command X times").
        The variable X is not allowed to occur in the body C of the
        iteration loop X {C}.

        Arguments:
            node: AST node to inspect.

        Returns:
            A tuple containing (1) compatibility result -- true if for
        loop is mwp-loop compatible, otherwise false -- and (2) name of
        iteration variable `X`, possibly `None`.
        """
        loop_x, body = Variables.loop_control(node)
        if len(loop_x) != 1:  # exactly one control variable
            logger.warning(f"Too many loop control variables: "
                           f"({', '.join(loop_x)})")
            return False, None
        x_var = loop_x[0]
        if x_var in body:
            logger.warning(f"Control variable ({x_var}) cannot "
                           f"occur in loop body")
            return False, None
        return True, x_var

    def iter_attr(self, node: Any, attr: str, *args, **kwargs):
        """Iteratively analyze children at node.attribute."""
        if hasattr(node, attr) and getattr(node, attr):
            for n in getattr(node, attr):
                self.recurse(n, *args, **{
                    **kwargs, 'clear': SyntaxCover.clearer(node, attr, n)})

    def clear_stmt(self, node: Any, *args, **kwargs):
        """Remove statement attribute of an unhandled node."""
        node_ = deepcopy(node)
        node_.stmt = None
        self.handler(node_, *args, **kwargs)

    def handler(self, node: Any, *args, **kwargs):
        """Make a list of uncovered nodes."""
        self.omit.append(pr.to_c(node, compact=True))
        self.to_clear.append(kwargs['clear'])  # should always exist

    def array_ref(self, node: pr.ArrayRef, *args, **kwargs):
        """All arrays are out of scope."""
        node_ = deepcopy(node)
        node_.name = pr.ID(BaseAnalysis.array_name(node))
        node_.subscript = pr.Constant('String', '…')
        self.handler(node_, *args, **kwargs)

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

    def break_(self, node: pr.Break, *args, **kwargs):
        return

    def compound(self, node: pr.Compound, *args, **kwargs):
        self.iter_attr(node, 'block_items', *args, **kwargs)

    def constant(self, node: pr.Constant, *args, **kwargs):
        return

    def continue_(self, node: pr.Continue, *args, **kwargs):
        return

    def decl(self, node: pr.Decl, *args, **kwargs):
        init = node.init if hasattr(node, 'init') else None
        type_ = node.type if hasattr(node, 'type') else None
        if not (isinstance(type_, pr.TypeDecl) and init is None):
            self.handler(node, *args, **kwargs)

    def decl_list(self, node: pr.DeclList, *args, **kwargs):
        self.iter_attr(node, 'decls', *args, **kwargs)

    def do_while(self, node: pr.DoWhile, *args, **kwargs):
        self.recurse_attr(node, 'stmt', *args, **kwargs)

    def for_(self, node: pr.For, *args, **kwargs):
        compat, _ = self.loop_compat(node)
        self.clear_stmt(node, *args, **kwargs) if not compat else \
            self.recurse_attr(node, 'stmt', *args, **kwargs)

    def func_call(self, node: pr.FuncCall, *args, **kwargs):
        node_ = deepcopy(node)
        if len(node_.args.exprs):
            node_.args = pr.ExprList([pr.Constant('String', '…')])
        self.handler(node_, *args, **kwargs)

    def func_def(self, node: pr.FuncDef, *args, **kwargs):
        self.recurse(node.decl.type.args, *args, **kwargs)
        self.recurse(node.body, *args, **kwargs)

    def id_(self, node: pr.ID, *args, **kwargs):
        return

    def if_(self, node: pr.If, *args, **kwargs):
        self.recurse_attr(node, 'iftrue', *args, **kwargs)
        self.recurse_attr(node, 'iffalse', *args, **kwargs)

    def param_list(self, node: pr.ParamList, *args, **kwargs):
        self.iter_attr(node, 'params', *args, **kwargs)

    def return_(self, node: pr.Return, *args, **kwargs):
        return

    def switch_(self, node: pr.Switch, *args, **kwargs):
        self.clear_stmt(node, *args, **kwargs)

    def unary(self, node: pr.UnaryOp, *args, **kwargs):
        self.handler(node, *args, **kwargs) \
            if node.op not in self.U_OPS \
            else self.recurse_attr(node, 'expr', *args, **kwargs)

    def while_(self, node: pr.While, *args, **kwargs):
        self.recurse_attr(node, 'stmt', *args, **kwargs)
