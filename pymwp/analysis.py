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
from typing import List, Tuple, Optional

from pymwp import DeltaGraph, Polynomial, RelationList, Result, Bound
from pymwp import Coverage, Variables
from pymwp.result import FuncResult
from .file_io import save_result
# noinspection PyPep8Naming
from .parser import Parser as pr

logger = logging.getLogger(__name__)

ComRes = Tuple[int, RelationList, bool]
"""Predicate is a function from seq R -> bool."""


class Analysis:
    """MWP analysis implementation."""

    @staticmethod
    def run(ast: pr.AST, res: Result = None, file_out: str = None,
            save: bool = True, evaluate: bool = True, fin: bool = False,
            strict: bool = False) \
            -> Result:
        """Run MWP analysis on specified input file.

        Arguments:
            ast: parsed C source code AST
            res: pre-initialized result object
            file_out: file to save result [default: None]
            save: save result to file_out [default: True]
            evaluate: do bound evaluation [default: True]
            fin: always run to completion [default: False]
            strict: require supported syntax [default: False]

        Returns:
            A [`Result`](result.md) object.
        """
        result: Result = res or Result()
        logger.debug("started analysis")

        result.on_start()
        for f_node in [f for f in ast if pr.is_func(f)]:
            func_res = Analysis.func(f_node, not fin, evaluate, strict)
            if func_res:
                result.add_relation(func_res)
        result.on_end()
        result.log_result()

        if save and file_out:
            save_result(file_out, res)
        return result

    @staticmethod
    def func(node: pr.FuncDef, stop: bool, evaluate: bool, strict: bool) \
            -> Optional[FuncResult]:
        """Analyze a function.

        Arguments:
            node: parsed C source code function node
            stop: terminate if no bound exists
            evaluate: do not calculate choices and evaluate bound
            strict: skip function if it contains unsupported syntax

        Returns:
              Analysis result for provided function. When running strict
              mode, the result will be None if function is not analyzable.
        """
        assert pr.is_func(node)
        name = node.decl.name
        logger.info(f"Analyzing {name}")
        result = FuncResult(name)

        # preliminary syntax check
        cover = Coverage(node).report()
        if not cover.full and strict:
            logger.info(f"{name} is not analyzable")
            return None
        if not cover.full:
            cover.ast_mod()
            logger.warning(f"{name} syntax was modified")
            if len(node.body.block_items) == 0:
                logger.warning("nothing left to analyze")
                return None

        # setup for function analysis
        index, options, choices = 0, [0, 1, 2], []
        evaluated, bound = False, None
        delta_infty, dg = False, DeltaGraph()
        variables = Variables(node).vars
        total = len(node.body.block_items)
        relations = RelationList.identity(variables=variables)
        logger.debug(f"{name} variables: {', '.join(variables)}")
        logger.debug(f"{total} top-level commands to analyze")

        # analyze body commands
        result.on_start()
        for i, node in enumerate(node.body.block_items):
            logger.debug(f'computing relation...{i} of {total}')
            index, rel_list, delta_infty_ = Analysis \
                .compute_relation(index, node, dg)
            delta_infty = delta_infty or delta_infty_  # cannot erase
            if stop and delta_infty:
                logger.debug('delta_graphs: infinite -> Exit now')
                break
            logger.debug(f'computing composition...{i} of {total}')
            relations.composition(rel_list)

        # evaluate choices + calculate a bound
        if evaluate and not delta_infty:
            choices = relations.first.eval(options, index)
            if not choices.infinite:
                bound = Bound().calculate(
                    relations.first.apply_choice(*choices.first))
            evaluated = True

        # infinite by delta graph or by choice
        infinite = delta_infty or (
                relations.first.variables and index > 0 and
                evaluated and choices.infinite)

        # record results
        result.index = index
        result.infinite = infinite
        result.vars = relations.first.variables
        if not (infinite and stop):
            result.relation = relations.first
        if infinite and not stop:
            var_choices = relations.first.var_eval(options, index)
            result.inf_flows = relations.first.infty_pairs(
                [v for v, c in var_choices.items() if c.infinite])
        if not infinite:
            result.bound = bound
            result.choices = choices
        result.on_end()
        return result

    @staticmethod
    def compute_relation(index: int, node: pr.Node, dg: DeltaGraph) -> ComRes:
        """Create a relation list corresponding for all possible matrices
        of an AST node.

        Arguments:
            index: delta index
            node: AST node to analyze
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """

        logger.debug("in compute_relation")
        if isinstance(node, pr.Decl):
            return index, RelationList(), False
        if isinstance(node, pr.Assignment) and \
                isinstance(node.lvalue, pr.ID):
            if isinstance(node.rvalue, pr.BinaryOp):
                return Analysis.binary_op(index, node)
            if isinstance(node.rvalue, pr.Constant):
                return Analysis.constant(index, node.lvalue.name)
            if isinstance(node.rvalue, pr.UnaryOp):
                return Analysis.unary_asgn(index, node)
            if isinstance(node.rvalue, pr.ID):
                return Analysis.id(index, node)
        if isinstance(node, pr.UnaryOp):
            return Analysis.unary_op(index, node, dg)
        if isinstance(node, pr.If):
            return Analysis.if_(index, node, dg)
        if isinstance(node, pr.While):
            return Analysis.while_(index, node, dg)
        if isinstance(node, pr.DoWhile):
            return Analysis.while_(index, node, dg)
        if isinstance(node, pr.For):
            return Analysis.for_(index, node, dg)
        if isinstance(node, pr.Compound):
            return Analysis.compound_(index, node, dg)
        if isinstance(node, pr.Break):  # => skip
            return index, RelationList(), False
        if isinstance(node, pr.Continue):  # => skip
            return index, RelationList(), False
        if isinstance(node, pr.Return):  # => skip
            return index, RelationList(), False
        if (isinstance(node, pr.FuncCall)
                and isinstance(node.name, pr.ID)
                and node.name.name == 'assert'):
            return index, RelationList(), False

        Analysis.unsupported(pr.to_c(node))
        return index, RelationList(), False

    @staticmethod
    def id(index: int, node: pr.Assignment) -> ComRes:
        """Analyze x = y, where data flows between two variables.

        Arguments:
            index: delta index
            node: AST node representing a simple assignment

        Returns:
            Updated index value, relation list, and an exit flag.
        """

        # ensure we have distinct variables on both sides of x = y
        if not isinstance(node.lvalue, pr.ID) \
                or isinstance(node.rvalue, pr.Constant) \
                or node.lvalue.name == node.rvalue.name:
            return index, RelationList(), False

        logger.debug('Computing Relation x = y')
        x = node.lvalue.name
        vars_list = [[x], [node.rvalue.name]]

        # create a vector of polynomials based on operator type
        #     x   y
        # x | o   o
        # y | m   m
        vector = [  # because x != y
            Polynomial('o'), Polynomial('m')]

        # build a list of unique variables
        variables = vars_list[0]
        for var in vars_list[1]:
            if var not in variables:
                variables.append(var)

        # create relation list
        rel_list = RelationList.identity(variables)
        rel_list.replace_column(vector, x)

        return index, rel_list, False

    @staticmethod
    def binary_op(index: int, node: pr.Assignment) -> ComRes:
        """Analyze binary operation, e.g. `x = y + z`.

        Arguments:
            index: delta index
            node: AST node representing a binary operation

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('Computing Relation: binary op')
        x, y, z = node.lvalue, node.rvalue.left, node.rvalue.right
        non_constants = tuple([v.name if hasattr(v, 'name') else None
                               for v in [x, y, z]])
        if not ((isinstance(y, pr.Constant) or isinstance(y, pr.ID)) and
                (isinstance(z, pr.Constant) or isinstance(z, pr.ID))):
            Analysis.unsupported(pr.to_c(node))
            return index, RelationList(), False

        # create a vector of polynomials based on operator type
        index, vector = Analysis.create_vector(
            index, node.rvalue.op, non_constants)

        # build a list of unique variables but maintain order
        variables = list(dict.fromkeys(non_constants))

        # create relation list
        rel_list = RelationList.identity(variables)
        if hasattr(x, 'name'):
            rel_list.replace_column(vector, x.name)

        return index, rel_list, False

    @staticmethod
    def constant(index: int, variable_name: str) -> ComRes:
        """Analyze a constant assignment of form `x = c` where x is some
        variable and c is constant.

        !!! info "From \"A Flow Calculus of mwp-Bounds...\""

            To deal with constants, just replace the program’s constants by
            variables and regard the replaced constants as input to these
            variables.

        Arguments:
            index: delta index
            variable_name: name of variable to which constant is being assigned

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('Constant value node')
        return index, RelationList([variable_name]), False

    @staticmethod
    def unary_asgn(index: int, node: pr.Assignment) -> ComRes:
        """Assignment where right-hand-size is a unary op e.g. `x = y++`.

        Arguments:
            index: delta index
            node: Assignment, where the right-side is a unary operation.

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('Computing Relation: unary')
        tgt, unary, op = node.lvalue, node.rvalue, node.rvalue.op
        if isinstance(unary.expr, pr.Constant):
            return Analysis.constant(index, tgt.name)
        if isinstance(unary.expr, pr.ID):
            exp = unary.expr.name
            if op in Coverage.INC_DEC:
                # expand unary incr/decr to a binary op
                # this ignores the +1/-1 applied to exp, but this is ok since
                # constants are irrelevant
                op_code = '+' if op in ('p++', '++') else '-'
                dsp = op.replace('p', exp) if ('p' in op) else f'{op}{exp}'
                logger.debug(f'{dsp} converted to {exp}{op_code}1')
                r_node = pr.BinaryOp(
                    op_code, pr.ID(exp), pr.Constant('int', 1))
                return Analysis.binary_op(
                    index, pr.Assignment('=', tgt, r_node))
            if op == '!':
                # negation ! of an integer gives either 0 or 1
                logger.debug(f'int negation of {exp} is a constant')
                return Analysis.id(index, pr.Assignment(
                    '=', tgt, pr.Constant('int', 1)))
            if op == 'sizeof':
                # sizeof gets variable's size in bytes
                # for all integers, the value is 8--64
                # https://en.wikipedia.org/wiki/C_data_types
                logger.debug(f'sizeof({exp}) is a constant')
                return Analysis.id(index, pr.Assignment(
                    '=', tgt, pr.Constant('int', 64)))
            if op == '+':  # does nothing; just an explicit sign
                return Analysis.id(index, pr.Assignment('=', tgt, unary.expr))
            if op == '-':  # flips variable sign
                r_node = pr.BinaryOp('*', pr.ID(exp), pr.Constant('int', -1))
                logger.debug(f'{op}{exp} converted to -1*{exp}')
                return Analysis.binary_op(
                    index, pr.Assignment('=', tgt, r_node))

        # unary address of "&" will fall through
        # expr not in {ID, Constant} will fall through
        Analysis.unsupported(type(node))
        return index, RelationList(), False

    @staticmethod
    def unary_op(index: int, node: pr.UnaryOp, dg: DeltaGraph) -> ComRes:
        """Analyze a standalone unary operation.

        Arguments:
            index: delta index
            node: unary operation AST node
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        if not (isinstance(node.expr, pr.Constant) or
                isinstance(node.expr, pr.ID)):
            return Analysis.compute_relation(index, node.expr, dg)

        op, exp = node.op, node.expr.name
        if op in Coverage.INC_DEC:
            # expand unary incr/decr to a binary op
            op_code = '+' if op in ('p++', '++') else '-'
            dsp = op.replace('p', exp) if ('p' in op) else f'{op}{exp}'
            logger.debug(f'{dsp} expanded to {exp}={exp}{op_code}1')
            r_node = pr.BinaryOp(op_code, pr.ID(exp), pr.Constant('int', 1))
            return Analysis.binary_op(index, pr.Assignment('=', exp, r_node))
        # all other unary ops do nothing ("skip") without assignment.
        return index, RelationList(), False

    @staticmethod
    def if_(index: int, node: pr.If, dg: DeltaGraph) -> ComRes:
        """Analyze an if statement.

        Arguments:
            index: delta index
            node: if-statement AST node
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('computing relation (conditional case)')
        true_relation, false_relation = RelationList(), RelationList()

        index, exit_ = Analysis.if_branch(
            index, node.iftrue, true_relation, dg)
        if exit_:
            return index, true_relation, True
        index, exit_ = Analysis.if_branch(
            index, node.iffalse, false_relation, dg)
        if exit_:
            return index, false_relation, True

        relations = false_relation + true_relation
        return index, relations, False

    @staticmethod
    def if_branch(index: int, node: pr.If, relation_list: RelationList,
                  dg: DeltaGraph) -> Tuple[int, bool]:
        """Analyze `if` or `else` branch of a conditional statement.

        This method will analyze the body of the statement and update
        the provided relation. It can handle blocks with or without surrounding
        braces. It will return the updated index value.

        If branch does not exist (when else case is omitted) this
        method does nothing and returns the original index value without
        modification.

        Arguments:
            index: current delta index value
            node: AST if statement branch node
            relation_list: current relation list state
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        if node is not None:
            for child in (node.block_items or []) \
                    if hasattr(node, 'block_items') else [node]:
                index, rel_list, exit_ = Analysis \
                    .compute_relation(index, child, dg)
                if exit_:
                    return index, exit_
                relation_list.composition(rel_list)
        return index, False

    @staticmethod
    def while_(index: int, node: pr.While, dg: DeltaGraph) -> ComRes:
        """Analyze a while loop.

        Arguments:
            index: delta index
            node: while loop node
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug("analysing while")

        relations = RelationList()
        for child in node.stmt.block_items \
                if hasattr(node, 'block_items') else [node.stmt]:
            index, rel_list, exit_ = Analysis.compute_relation(
                index, child, dg)
            if exit_:
                return index, rel_list, exit_
            relations.composition(rel_list)

        logger.debug('while loop fixpoint')
        relations.fixpoint()
        relations.while_correction(dg)
        dg.fusion()

        return index, relations, dg.is_empty

    @staticmethod
    def for_(index: int, node: pr.For, dg: DeltaGraph) -> ComRes:
        """Analyze for loop node.

        The mwp-loop has form loop X { C }. The method supports C-language
        for loops that have similar form ("repeat command X times").
        The variable X is not allowed to occur in the body C of the
        iteration loop X {C}. If it is not possible to infer similar loop
        control format, analysis skips the loop.

        Arguments:
            index: delta index
            node: for loop node
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        comp, x_var = Coverage.loop_compat(node)
        if not comp:
            return index, RelationList(), False
        relations = RelationList(variables=[x_var])
        for child in node.stmt.block_items \
                if hasattr(node, 'block_items') else [node.stmt]:
            index, rel_list, exit_ = Analysis.compute_relation(
                index, child, dg)
            if exit_:
                return index, rel_list, True
            relations.composition(rel_list)

        logger.debug('loop fixpoint')
        relations.fixpoint()
        relations.loop_correction(x_var, dg)
        dg.fusion()
        return index, relations, dg.is_empty

    @staticmethod
    def compound_(index: int, node: pr.Compound, dg: DeltaGraph) -> ComRes:
        """Compound AST node contains zero or more children and is
        created by braces in source code.

        We analyze such compound node by recursively analysing its children.

        Arguments:
            index: delta index
            node: compound AST node
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        relations = RelationList()

        if node.block_items:
            for node in node.block_items:
                index, rel_list, exit_ = Analysis.compute_relation(
                    index, node, dg)
                relations.composition(rel_list)
                if exit_:
                    return index, relations, True
        return index, relations, False

    @staticmethod
    def create_vector(index: int, op: str, variables: Tuple[str, ...]) \
            -> Tuple[int, List[Polynomial]]:
        """Build a polynomial vector based on operator and the operands
        of a binary operation statement that has form `x = y (operator) z`.

        For an AST node that represents a binary operation, this method
        generates a vector of polynomials based on the properties of that
        operation. The returned vector depends on the type of operator,
        how many operands are constants, and if the operands are equal.

        Arguments:
            index: delta index
            op: operator
            variables: variables in this operation `x = y (op) z` in order,
                where `y` or `z` is `None` if constant

        Returns:
             Updated index, list of Polynomial vectors
        """

        x, y, z = variables
        supported_op = Coverage.BIN_OPS
        vector = []

        if op not in supported_op:
            Analysis.unsupported(f'{op} operator')
            return index, []

        # when left variable does not occur on right side of assignment
        # x = … (if x not in …), i.e. when left side variable does not
        # occur on the right side of assignment, we prepend 0 to vector
        if x != y and x != z:
            vector.append(Polynomial('o'))

        if op in supported_op and (y is None or z is None):
            vector.append(Polynomial.from_scalars(index, 'm', 'm', 'm'))

        elif op == '*' and y == z:
            vector.append(Polynomial.from_scalars(index, 'w', 'w', 'w'))

        elif op == '*' and y != z:
            vector.append(Polynomial.from_scalars(index, 'w', 'w', 'w'))
            vector.append(Polynomial.from_scalars(index, 'w', 'w', 'w'))

        elif op in {'+', '-'} and y == z:
            vector.append(Polynomial.from_scalars(index, 'p', 'p', 'w'))

        elif op in {'+', '-'} and y != z:
            vector.append(Polynomial.from_scalars(index, 'm', 'p', 'w'))
            vector.append(Polynomial.from_scalars(index, 'p', 'm', 'w'))

        return index + 1, vector

    @staticmethod
    def unsupported(command: any):
        """Handle unsupported command."""
        warning, endc = '\033[93m', '\033[0m'
        fmt_str = str(command or "").strip()
        logger.warning(f'{warning}Unsupported syntax{endc} '
                       f'not evaluated: {fmt_str}')
