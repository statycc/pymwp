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

import logging
from typing import List, Tuple, Dict

from . import Coverage, Variables, FindLoops, COM_RES
from . import DeltaGraph, Polynomial, RelationList, Relation, Bound, Choices
from . import Result, FuncResult, FuncLoops, LoopResult, VResult
# noinspection PyPep8Naming
from .parser import Parser as pr
from .semiring import ZERO_MWP, UNIT_MWP, POLY_MWP, WEAK_MWP

logger = logging.getLogger(__name__)


class Analysis:
    """MWP analysis implementation."""

    DOMAIN = [0, 1, 2]

    @staticmethod
    def run(ast: pr.Node, res: Result = None, fin: bool = False,
            strict: bool = False, **kwargs) -> Result:
        """Run MWP analysis on AST.

        Arguments:
            ast (pr.Node): Parsed C source code AST Node.
            res (Result): Pre-initialized result object.
            fin (bool): Always run to completion.
            strict (bool): Require supported syntax.

        Returns:
            Analysis Result object.
        """
        result: Result = res or Result()
        logger.debug("started analysis")
        result.on_start()
        for f_node in [f for f in ast if pr.is_func(f)]:
            if Analysis.syntax_check(f_node, strict):
                func_res = Analysis.func(f_node, not fin)
                func_res.func_code = pr.to_c(f_node, True)
                result.add_relation(func_res)
        result.on_end().log_result()
        return result

    @staticmethod
    def func(node: pr.FuncDef, stop: bool) -> FuncResult:
        """Analyze a function.

        Arguments:
            node: parsed C source code function node
            stop: terminate if no bound exists

        Returns:
              Analysis result for provided function.
        """
        assert pr.is_func(node)
        name = node.decl.name
        logger.info(f"Analyzing {name}")
        result = FuncResult(name).on_start()

        # setup for function analysis
        variables, body = Variables(node).vars, (node.body.block_items or [])
        relations = RelationList.identity(variables=variables)
        total, num_v = len(body), len(variables)
        show_vars = ', '.join(variables) if num_v <= 5 else num_v
        logger.debug(f"{name} variables: {show_vars}")
        logger.debug(f"{total} top-level commands to analyze")

        # analyze body commands
        delta_infty, index = Analysis.cmds(relations, 0, body, stop)

        # evaluate choices + calculate a bound
        evaluated, choices, bound = False, None, None
        if not delta_infty:
            choices = relations.first.eval(Analysis.DOMAIN, index)
            if not choices.infinite:
                bound = Bound().calculate(
                    relations.first.apply_choice(*choices.first))
            evaluated = True
        # infinite by delta graph or by choice
        infinite = delta_infty or (evaluated and choices.infinite)

        # record results
        result.index = index
        result.infinite = infinite
        result.variables = relations.first.variables
        if not (infinite and stop):
            result.relation = relations.first
        if infinite and not stop:
            var_choices = relations.first.var_eval(Analysis.DOMAIN, index)
            result.inf_flows = relations.first.infty_pairs(
                [v for v, c in var_choices.items() if c.infinite])
        if not infinite:
            result.bound = bound
            result.choices = choices
        result.on_end()
        return result

    @staticmethod
    def cmds(relations: RelationList, index: int, nodes: List[pr.Node],
             stop: bool = True) -> Tuple[bool, int]:
        """Analyze some list of commands, typically body block statements.

        Arguments:
            relations (RelationList): Initialized relation list.
            index (int): Derivation index.
            nodes (List[pr.Node]): List of AST nodes to analyze.
            stop (bool): Set True to terminate early.

        Returns:
            True if nodes lead to infinity by delta graph.
        """
        if not nodes:
            return False, index
        delta_infty, total, dg = False, len(nodes), DeltaGraph()
        for i, node in enumerate(nodes):
            logger.debug(f'computing relation...{i} of {total}')
            index, rel_list, delta_infty_ = Analysis \
                .compute_relation(index, node, dg)
            delta_infty = delta_infty or delta_infty_  # cannot erase
            if stop and delta_infty:
                logger.debug('delta_graphs: infinite -> Exit now')
                break
            logger.debug(f'computing composition...{i} of {total}')
            relations.composition(rel_list)
        return delta_infty, index

    @staticmethod
    def syntax_check(node: pr.Node, strict: bool) -> bool:
        """Analyze function syntax and conditionally modify the AST.

        Arguments:
            node (pr.Node): An AST node.
            strict (bool): When true, AST will not be modified.

        Returns:
            True if analysis can be performed and False otherwise.
        """
        name = node.decl.name if pr.is_func(node) else 'node'
        cover = Coverage(node).report()
        if not cover.full and strict:
            logger.warning(f"{name} syntax is not fully analyzable")
            return False
        if not cover.full:
            cover.ast_mod()  # removes unsupported commands
            logger.warning(f"{name} syntax was modified")
        return True

    @staticmethod
    def compute_relation(index: int, node: pr.Node, dg: DeltaGraph) -> COM_RES:
        """Create a relation list corresponding for all possible matrices
        of an AST node.

        Arguments:
            index (int): Delta index.
            node (pr.Node): AST node to analyze.
            dg (DeltaGraph): DeltaGraph instance.

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug("in compute_relation")
        if isinstance(node, (
                pr.Return, pr.Break, pr.Continue,
                pr.EmptyStatement, pr.Decl)):  # => skip
            return index, RelationList(), False
        if isinstance(node, pr.Assignment) and \
                isinstance(node.lvalue, pr.ID):
            rvalue = node.rvalue.expr if isinstance(
                node.rvalue, pr.Cast) else node.rvalue
            if isinstance(rvalue, pr.BinaryOp):
                return Analysis.binary_op(index, node)
            if isinstance(rvalue, pr.Constant):
                return Analysis.constant(index, node.lvalue.name)
            if isinstance(rvalue, pr.UnaryOp):
                return Analysis.unary_asgn(index, node, dg)
            if isinstance(rvalue, pr.ID):
                return Analysis.id(index, node)
        if isinstance(node, pr.UnaryOp):
            return Analysis.unary_op(index, node)
        if isinstance(node, pr.If):
            return Analysis.if_stmt(index, node, dg)
        if isinstance(node, (pr.While, pr.DoWhile)):
            return Analysis.while_loop(index, node, dg)
        if isinstance(node, pr.For):
            return Analysis.for_loop(index, node, dg)
        if isinstance(node, pr.Compound):
            return Analysis.compound(index, node, dg)
        if (isinstance(node, pr.FuncCall)
                and isinstance(node.name, pr.ID)
                and (node.name.name in ('assert', 'assume'))):
            return index, RelationList(), False

        Analysis._unsupported(pr.to_c(node))
        return index, RelationList(), False

    @staticmethod
    def id(index: int, node: pr.Assignment) -> COM_RES:
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

        x, y = node.lvalue.name, node.rvalue.name
        vars_list = [[x], [y]]
        logger.debug(f'Computing relation {x} = {y}')

        # create a vector of polynomials based on operator type
        #     x   y
        # x | o   o
        # y | m   m    because x != y
        vector = [Polynomial('o'), Polynomial('m')]

        variables = vars_list[0] + vars_list[1]
        rel_list = RelationList.identity(variables)
        rel_list.replace_column(vector, x)
        return index, rel_list, False

    @staticmethod
    def binary_op(index: int, node: pr.Assignment) -> COM_RES:
        """Analyze binary operation, e.g. `x = y + z`.

        Arguments:
            index: delta index
            node: AST node representing a binary operation

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('Computing Relation: binary op')
        x = node.lvalue
        y = Analysis.rm_cast(node.rvalue.left)
        z = Analysis.rm_cast(node.rvalue.right)

        # operands cannot be unary, nested cast etc.
        assert isinstance(y, (pr.Constant, pr.ID))
        assert isinstance(z, (pr.Constant, pr.ID))

        non_constants = tuple([
            v.name if hasattr(v, 'name') else None
            for v in [x, y, z]])

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
    def constant(index: int, variable_name: str) -> COM_RES:
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
    def unary_asgn(index: int, node: pr.Assignment, dg: DeltaGraph) -> COM_RES:
        """Assignment where right-hand-size is a unary op e.g. `x = y++;`.

        Arguments:
            index (int): delta index
            node (pr.Assignment): Node with right-side unary operation.
            dg (DeltaGraph): DeltaGraph instance.

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('Computing Relation: unary')
        tgt, right, op = node.lvalue, node.rvalue.expr, node.rvalue.op
        init = f'{pr.to_c(node, True)} ==> '
        new_node = None

        if isinstance(right, pr.Constant):
            new_node = pr.Assignment('=', tgt, right)

        if isinstance(right, pr.ID):
            r_name = right.name
            if op in Coverage.INC_DEC:
                fst = Analysis.rewrite_id_inc_dec(node.rvalue)
                snd = pr.Assignment('=', tgt, pr.ID(r_name))
                cmds = [fst, snd] if op in Coverage.PREFIX else [snd, fst]
                new_node = pr.Compound(cmds)
            if op == Coverage.MINUS:  # flips sign
                neg_1 = pr.Constant('int', -1)
                r_node = pr.BinaryOp(Coverage.MULT, pr.ID(r_name), neg_1)
                new_node = pr.Assignment('=', tgt, r_node)
            if op == Coverage.PLUS:  # does nothing
                new_node = pr.Assignment('=', tgt, pr.ID(r_name))

        if op == Coverage.NEG:  # negation=> 0 or 1
            new_node = pr.Assignment('=', tgt, pr.Constant('int', 1))

        if op == Coverage.SIZEOF:  # var size in bytes ≤ 64
            new_node = pr.Assignment('=', tgt, pr.Constant('int', 64))

        if new_node:
            logger.debug(f'{init}{pr.to_c(new_node, True)}')
            return Analysis.compute_relation(index, new_node, dg)

        Analysis._unsupported(pr.to_c(node))
        return index, RelationList(), False

    @staticmethod
    def unary_op(index: int, node: pr.UnaryOp) -> COM_RES:
        """Analyze a standalone unary operation.

        Arguments:
            index (int): Delta index.
            node (pr.UnaryOp): AST node to analyze.

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        expr = Analysis.rm_cast(node.expr)
        if node.op in Coverage.INC_DEC and isinstance(expr, pr.ID):
            node_ = Analysis.rewrite_id_inc_dec(node)
            return Analysis.binary_op(index, node_)
        # could be recursive unary...
        # others operators do nothing without assignment.
        return index, RelationList(), False

    @staticmethod
    def rewrite_id_inc_dec(node: pr.UnaryOp):
        """Converts unary ++/-- operators to binary: x = x (op) 1."""
        expr = Analysis.rm_cast(node.expr)
        new_op, name = node.op[-1], expr.name
        const_1 = pr.Constant('int', 1)
        rvalue = pr.BinaryOp(new_op, pr.ID(name), const_1)
        node_ = pr.Assignment('=', pr.ID(name), rvalue)
        logger.debug(f'{pr.to_c(node)} rewrite to {pr.to_c(node_)}')
        return node_

    @staticmethod
    def rm_cast(node: pr.Node) -> pr.Node:
        """If Cast node, returns the expression of cast."""
        while isinstance(node, pr.Cast) and node.expr:
            node = node.expr
        return node

    @staticmethod
    def if_stmt(index: int, node: pr.If, dg: DeltaGraph) -> COM_RES:
        """Analyze an if statement.

        Arguments:
            index (int): Delta index.
            node (pr.If): if-statement AST node.
            dg (DeltaGraph): DeltaGraph instance.

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
            index (int): Current delta index value.
            node (pr.If): AST if statement branch node.
            relation_list (RelationList): Current relation list state.
            dg (DeltaGraph): DeltaGraph instance.

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
    def while_loop(index: int, node: pr.While, dg: DeltaGraph) -> COM_RES:
        """Analyze a while loop.

        Arguments:
            index (int): Delta index.
            node (pr.while): While loop node.
            dg (DeltaGraph): DeltaGraph instance.

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
    def for_loop(index: int, node: pr.For, dg: DeltaGraph) -> COM_RES:
        """Analyze for loop node.

        Arguments:
            index (int): Delta index.
            node (pr.For): for loop node.
            dg (DeltaGraph): DeltaGraph instance.

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
    def compound(index: int, node: pr.Compound, dg: DeltaGraph) -> COM_RES:
        """Compound AST node contains zero or more children and is
        created by braces in source code.

        We analyze such compound node by recursively analysing its children.

        Arguments:
            index (int): Delta index.
            node (pr.Compound): Compound AST node.
            dg (DeltaGraph): DeltaGraph instance.

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
        assert op in Coverage.BIN_OPS
        x, y, z = variables
        vector = []

        # when left variable does not occur on right side of assignment
        # x = … (if x not in …), i.e. when left side variable does not
        # occur on the right side of assignment, we prepend 0 to vector
        if x != y and x != z:
            vector.append(Polynomial(ZERO_MWP))

        if y is None or z is None:
            vector.append(Polynomial.from_scalars(
                index, UNIT_MWP, UNIT_MWP, UNIT_MWP))

        elif op == '*' and y == z:
            vector.append(Polynomial.from_scalars(
                index, WEAK_MWP, WEAK_MWP, WEAK_MWP))

        elif op == '*' and y != z:
            vector.append(Polynomial.from_scalars(
                index, WEAK_MWP, WEAK_MWP, WEAK_MWP))
            vector.append(Polynomial.from_scalars(
                index, WEAK_MWP, WEAK_MWP, WEAK_MWP))

        elif op in {'+', '-'} and y == z:
            vector.append(Polynomial.from_scalars(
                index, POLY_MWP, POLY_MWP, WEAK_MWP))

        elif op in {'+', '-'} and y != z:
            vector.append(Polynomial.from_scalars(
                index, UNIT_MWP, POLY_MWP, WEAK_MWP))
            vector.append(Polynomial.from_scalars(
                index, POLY_MWP, UNIT_MWP, WEAK_MWP))

        return index + 1, vector

    @staticmethod
    def _unsupported(command: any):
        """Keep for debugging extending parser+syntax support."""
        warning, endc = '\033[93m', '\033[0m'
        fmt_str = str(command or "").strip()
        logger.warning(f'{warning}Unsupported syntax {fmt_str}{endc}')


class LoopAnalysis(Analysis):
    """MWP analysis for loops."""

    @staticmethod
    def run(ast: pr.Node, res: Result = None, strict: bool = False, **kwargs) \
            -> Result:
        """Run loop analysis.

        Arguments:
            ast (pr.Node): Parsed C source code as an AST.
            res (Result): Pre-initialized result object.
            strict (bool): Require supported syntax.

        Returns:
            Analysis Result object.
        """
        result = res or Result()
        result.on_start()
        logger.debug("Starting loop analysis")
        functions = [f for f in ast if pr.is_func(f)]
        for func in functions:
            f_name = func.decl.name
            f_result = FuncLoops(f_name)
            f_result.on_start()
            logger.info(f"Analyzing {f_name}")
            # find loops and check/fix loop body syntax
            # nested loops are duplicated+lifted
            loops = [loop for loop in FindLoops(func).loops if
                     LoopAnalysis.syntax_check(loop, strict)]
            logger.debug(f"Total analyzable loops: {len(loops)}")
            # analyze each loop
            for loop in loops:
                f_result.loops.append(LoopAnalysis.inspect(loop))
            f_result.on_end()
            result.add_loop(f_result)
        result.on_end()
        result.log_result()
        return result

    @staticmethod
    def inspect(node: pr.LoopT) -> LoopResult:
        """Analyze a loop.

        Arguments:
            node (LOOP_T): A loop node.

        Returns:
            Loop analysis result.
        """
        assert pr.is_loop(node)
        result = LoopResult(pr.to_c(node)).on_start()

        # setup for loop analysis
        relations = RelationList.identity(variables=Variables(node).vars)

        # analyze body commands, always run to completion
        infty, index = LoopAnalysis.cmds(relations, 0, [node], stop=False)

        # lame fix because of #148
        infty = infty or relations.first.eval(Analysis.DOMAIN, index).infinite

        # evaluate at variables
        variables = relations.first.variables
        result.variables = dict(zip(variables, map(
            lambda v: LoopAnalysis.get_result(
                relations.first, index, v), variables))) \
            if not infty else \
            LoopAnalysis.maybe_result(relations.first, index)

        result.on_end()
        return result

    @staticmethod
    def syntax_check(node: pr.LoopT, strict: bool) -> bool:
        """Analyze function syntax and conditionally modify the AST.

        Arguments:
            node (LOOP_T): An AST loop node.
            strict (bool): When true, AST will not be modified.

        Returns:
            True if analysis can be performed and False otherwise.
        """
        base = Analysis.syntax_check(node, strict)
        return base and pr.is_loop(node)

    @staticmethod
    def get_result(relation: Relation, index: int, v_name: str) -> VResult:
        """Find variable bounds when they are known to exist.

        Arguments:
            relation (Relation): Relation object.
            index (int): Degree of analysis choice.
            v_name (str): Name of variable to evaluate.

        Returns:
            Evaluation result for identified variable.
        """
        result = VResult(v_name)
        options = (('is_m', (WEAK_MWP, POLY_MWP)),
                   ('is_w', (POLY_MWP,)),
                   ('is_p', ()))
        # find the "least bound-choice": 0/m < has w < has p
        for attr, scalars in options:
            choices = relation.var_eval(
                Analysis.DOMAIN, index, v_name, *scalars)
            if not choices.infinite:
                setattr(result, attr, True)
                result.choices = choices
                break
        assert result.choices
        simple_mat = relation.apply_choice(*result.choices.first)
        result.bound = Bound().calculate(simple_mat).bound_dict[v_name]
        return result

    @staticmethod
    def maybe_result(relation: Relation, index: int) -> Dict[str, VResult]:
        """Evaluate variables when some variables are known to fail.

        Arguments:
            relation (Relation): Relation object.
            index (int): Degree of analysis choice.

        Returns:
            Dictionary of results, for each variable in relation.
        """
        variables = relation.variables
        p_bounds = dict(zip(variables, map(lambda v: relation.var_eval(
            Analysis.DOMAIN, index, v), variables)))
        fail = [v for v, c in p_bounds.items() if c.infinite]
        rest = dict([(v, p_bounds[v]) for v in (set(variables) - set(fail))])
        result = dict([(v, VResult(v)) for v in fail])
        fail_idx = [relation.variables.index(v) for v in fail]
        if rest:  # maybe some well-behaving variables?
            red = Choices.choice_reduce(*rest.values())
            assert not red.infinite  # should always give a choice?
            simple_mat = relation.apply_choice(*red.first)
            for v in rest.keys():
                idx = relation.variables.index(v)
                # assumption: if dep is 0, it is 0 in all derivations?
                deps = set([simple_mat.matrix[fi][idx] for fi in fail_idx])
                # only when variable has no dependency on failing ones
                result[v] = (LoopAnalysis.get_result(relation, index, v)
                             if deps == {ZERO_MWP} else VResult(v))
        return result
