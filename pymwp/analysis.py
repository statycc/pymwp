import logging
from typing import List, Tuple, Optional, Union, Dict
from pycparser import c_ast
from pycparser.c_ast import Node, Assignment, If, While, For, Compound, \
    ParamList, FuncCall

from .relation_list import RelationList, Relation
from .polynomial import Polynomial
from .monomial import Monomial
from .delta_graphs import DeltaGraph
from .file_io import save_relation

logger = logging.getLogger(__name__)


class Analysis:
    """MWP analysis implementation."""

    @staticmethod
    def run(
            ast: c_ast, file_out: str = None,
            no_save: bool = False, no_eval: bool = False
    ) -> Union[Dict, Tuple[Relation, List[List[int]], bool]]:
        """Run MWP analysis on specified input file.

        Arguments:
            ast: parsed C source code AST
            file_out: where to store result
            no_save: Set true when analysis result should not be saved to file
            no_eval: Skip evaluation phase

        Returns:
              - Computed relation,
              - list of non-infinity choices
              - infinite/not infinite (boolean flag)
        """

        logger.debug("starting analysis")
        single_function = len(ast.ext) == 1
        result, function_name = {}, ''

        for ast_ext in ast:
            choices = [0, 1, 2]
            index, combinations = 0, []
            function_name = ast_ext.decl.name
            function_body = ast_ext.body
            args = ast_ext.decl.type.args
            variables = Analysis.find_variables(function_body, args)
            logger.debug(f"variables of {function_name}: {variables}")
            evaluated = False

            relations = RelationList.identity(variables=variables)
            total = len(function_body.block_items)
            delta_infty = False
            dg = DeltaGraph()

            for i, node in enumerate(function_body.block_items):
                logger.debug(f'computing relation...{i} of {total}')
                index, rel_list, delta_infty = Analysis \
                    .compute_relation(index, node, dg)
                if delta_infty:
                    break
                logger.debug(f'computing composition...{i} of {total}')
                relations.composition(rel_list)

            # skip evaluation when delta graph has detected infinity
            # or caller has manually disabled evaluation
            if not delta_infty and not no_eval:
                combinations = relations.first.non_infinity(choices, index, dg)
                evaluated = True

            # the evaluation is infinite when either of these conditions holds:
            infinite = delta_infty or (
                    relations.first.variables and index > 0 and
                    (evaluated and not combinations))

            # record and display results
            if infinite:
                result[function_name] = None, None, True
                logger.info(f'RESULT: {function_name} is infinite')
            else:
                result[function_name] = relations.first, combinations, False
                logger.info(f'\nMATRIX{relations}')
                if not evaluated:
                    logger.info('Skipped evaluation')
                else:
                    logger.info(f'CHOICES:\n{combinations}')

        # save result to file unless explicitly disabled
        if not no_save:
            save_relation(file_out, result)

        # return results to caller
        return result[function_name] if single_function else result

    @staticmethod
    def find_variables(
            function_body: Compound, param_list: Optional[ParamList]
    ) -> List[str]:
        """Finds all local variable declarations in function body and
        parameter list.

        This method scans recursively AST nodes looking for
        variable declarations. For each declaration, the
        name of the variable will be recorded. Method returns
        a list of all discovered variable names.

        Arguments:
            function_body: AST node with sub-nodes
            param_list: AST function parameter list

        Returns:
            List of all discovered variable names, or
            empty list if no variables were found.
        """
        variables = []

        def recurse_nodes(node_):
            # only look for declarations
            if isinstance(node_, c_ast.Decl):
                variables.append(node_.name)
            if hasattr(node_, 'block_items'):
                for sub_node in node_.block_items:
                    recurse_nodes(sub_node)

        # search function body for local declarations
        if hasattr(function_body, 'block_items'):
            for node in function_body.block_items:
                recurse_nodes(node)

        # process param list which is a list of declarations
        if param_list and hasattr(param_list, 'params'):
            for node in param_list.params:
                recurse_nodes(node)

        return variables

    @staticmethod
    def compute_relation(index: int, node: Node, dg: DeltaGraph) \
            -> Tuple[int, RelationList, bool]:
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

        if isinstance(node, c_ast.Decl):
            return index, RelationList(), False
        if isinstance(node, FuncCall):
            return Analysis.func_call(index)
        if isinstance(node, c_ast.Assignment):
            if isinstance(node.rvalue, c_ast.BinaryOp):
                return Analysis.binary_op(index, node)
            if isinstance(node.rvalue, c_ast.Constant):
                return Analysis.constant(index, node.lvalue.name)
            if isinstance(node.rvalue, c_ast.UnaryOp):
                return Analysis.unary_op(index, node)
            if isinstance(node.rvalue, c_ast.ID):
                return Analysis.id(index, node)
            if isinstance(node.rvalue, FuncCall):
                return Analysis.func_call(index)
        if isinstance(node, c_ast.If):
            return Analysis.if_(index, node, dg)
        if isinstance(node, c_ast.While):
            return Analysis.while_(index, node, dg)
        if isinstance(node, c_ast.For):
            return Analysis.for_(index, node, dg)
        if isinstance(node, c_ast.Compound):
            return Analysis.compound_(index, node, dg)

        logger.debug(f"uncovered case! type: {type(node)}")

        return index, RelationList(), False

    @staticmethod
    def id(index: int, node: Assignment) \
            -> Tuple[int, RelationList, bool]:
        """Analyze x = y (with x != y) and y not a const

        Arguments:
            index: delta index
            node: AST node representing a simple assignment

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        x = node.lvalue.name
        y = node.rvalue.name
        if x == y or isinstance(node.rvalue, c_ast.Constant):
            return index, RelationList(), False

        logger.debug('Computing Relation x = y')
        vars_list = [[x], [y]]

        # create a vector of polynomials based on operator type
        #     x   y
        # x | o   o
        # y | m   m
        vector = [
            # because x != y
            Polynomial([Monomial('o')]),
            Polynomial([Monomial('m')])
        ]

        # build a list of unique variables
        variables = vars_list[0]
        for var in vars_list[1]:
            if var not in variables:
                variables.append(var)

        # create relation list
        rel_list = RelationList.identity(variables)
        rel_list.replace_column(vector, vars_list[0][0])

        return index + 1, rel_list, False

    @staticmethod
    def binary_op(index: int, node: Assignment) \
            -> Tuple[int, RelationList, bool]:
        """Analyze binary operation, e.g. `x = y + z`.

        Arguments:
            index: delta index
            node: AST node representing a binary operation

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('Computing Relation (first case / binary op)')
        x, y, z = node.lvalue, node.rvalue.left, node.rvalue.right
        non_constants = tuple([v.name if hasattr(v, 'name') else None
                               for v in [x, y, z]])

        # create a vector of polynomials based on operator type
        index, vector = Analysis.create_vector(
            index, node.rvalue.op, non_constants)

        # build a list of unique variables but maintain order
        variables = list(dict.fromkeys(non_constants))

        # create relation list
        rel_list = RelationList.identity(variables)
        rel_list.replace_column(vector, x.name)

        return index, rel_list, False

    @staticmethod
    def constant(index: int, variable_name: str) \
            -> Tuple[int, RelationList, bool]:
        """Analyze a constant assignment of form: x = c where x is some
        variable and c is constant.

        From MWP paper:

        > To deal with constants, just replace the program’s constants by
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
    def unary_op(index: int, node: Assignment) \
            -> Tuple[int, RelationList, bool]:
        """Analyze unary operator.

        Arguments:
            index: delta index
            node: unary operator node

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug('Computing Relation (third case / unary)')
        var_name = node.lvalue.name
        # list_var = None  # list_var(exp)
        # variables = [var_name] + list_var
        variables = [var_name]
        return index, RelationList.identity(variables), False

    @staticmethod
    def if_(index: int, node: If, dg: DeltaGraph) \
            -> Tuple[int, RelationList, bool]:
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
            node.iftrue, index, true_relation, dg)
        if exit_:
            return index, true_relation, True
        index, exit_ = Analysis.if_branch(
            node.iffalse, index, false_relation, dg)
        if exit_:
            return index, false_relation, True

        relations = false_relation + true_relation
        return index, relations, False

    @staticmethod
    def if_branch(
            node: If, index: int, relation_list: RelationList, dg: DeltaGraph
    ) -> Tuple[int, bool]:
        """Analyze `if` or `else` branch of a conditional statement.

        This method will analyze the body of the statement and update
        the provided relation. It can handle blocks with or without surrounding
        braces. It will return the updated index value.

        If branch does not exist (when else case is omitted) this
        method does nothing and returns the original index value without
        modification.

        Arguments:
            node: AST if statement branch node
            index: current delta index value
            relation_list: current relation list state
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        if node is not None:
            # when branch has braces
            if hasattr(node, 'block_items'):
                for child in node.block_items:
                    index, rel_list, exit_ = Analysis.compute_relation(
                        index, child, dg)
                    if exit_:
                        return index, exit_
                    relation_list.composition(rel_list)
            else:
                index, rel_list, exit_ = Analysis.compute_relation(
                    index, node, dg)
                if exit_:
                    return index, exit_
                relation_list.composition(rel_list)
        return index, False

    @staticmethod
    def while_(index: int, node: While, dg: DeltaGraph) \
            -> Tuple[int, RelationList, bool]:
        """Analyze while loop.

        Arguments:
            index: delta index
            node: while loop node
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug("analysing While")

        relations = RelationList()
        for child in node.stmt.block_items:
            index, rel_list, exit_ = Analysis.compute_relation(
                index, child, dg)
            if exit_:
                return index, rel_list, exit_
            relations.composition(rel_list)

        logger.debug('while loop fixpoint')
        relations.fixpoint()
        relations.while_correction(dg)

        dg.fusion()

        exit_ = False
        if 0 in dg.graph_dict:
            if dg.graph_dict[0] == {(): {}}:
                logger.info(f'delta graph:\n{dg}')
                logger.info('delta_graphs: infinite')
                logger.info('Exit now !')
                exit_ = True

        return index, relations, exit_

    @staticmethod
    def for_(index: int, node: For, dg: DeltaGraph) \
            -> Tuple[int, RelationList, bool]:
        """Analyze for loop node.

        Arguments:
            index: delta index
            node: for loop node
            dg: [DeltaGraph instance](delta_graphs.md#pymwp.delta_graphs)

        Returns:
            Updated index value, relation list, and an exit flag.
        """
        logger.debug("analysing for:")

        relations = RelationList()
        for child in node.stmt.block_items:
            index, rel_list, exit_ = Analysis.compute_relation(
                index, child, dg)
            if exit_:
                return index, rel_list, True
            relations.composition(rel_list)

        relations.fixpoint()
        # TODO: unknown method conditionRel
        #  ref: https://github.com/statycc/pymwp/issues/5
        # relations = relations.conditionRel(VarVisitor.list_var(node.cond))
        return index, relations, False

    @staticmethod
    def compound_(index: int, node: Compound, dg: DeltaGraph) \
            -> Tuple[int, RelationList, bool]:
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
    def create_vector(
            index: int, operator: str, variables: Tuple[Optional[str], ...]
    ) -> Tuple[int, List[Polynomial]]:
        """Build a polynomial vector based on operator and the operands
        of a binary operation statement that has form `x = y (operator) z`.

        For an AST node that represents a binary operation, this method
        generates a vector of polynomials based on the properties of that
        operation. The returned vector depends on the type of operator,
        how many operands are constants, and if the operands are equal.

        Arguments:
            index: delta index
            operator: operator
            variables: variables in this operation `x = y (op) z` in order,
                where `y` or `z` is `None` if constant

        Returns:
             Updated index, list of Polynomial vectors
        """

        x, y, z = variables
        vector = []

        # when left variable does not occur on right side of assignment
        # x = … (if x not in …), i.e. when left side variable does not
        # occur on the right side of assignment, we prepend 0 to vector
        if x != y and x != z:
            vector.append(Polynomial('o'))

        if operator in {"+", "-", "*"} and (y is None or z is None):
            vector.append(Polynomial.from_scalars(index, 'm', 'm', 'm'))

        elif operator == '*' and y == z:
            vector.append(Polynomial.from_scalars(index, 'w', 'w', 'w'))

        elif operator == '*' and y != z:
            vector.append(Polynomial.from_scalars(index, 'w', 'w', 'w'))
            vector.append(Polynomial.from_scalars(index, 'w', 'w', 'w'))

        elif operator in {'+', '-'} and y == z:
            vector.append(Polynomial.from_scalars(index, 'p', 'p', 'w'))

        elif operator in {'+', '-'} and y != z:
            vector.append(Polynomial.from_scalars(index, 'm', 'p', 'w'))
            vector.append(Polynomial.from_scalars(index, 'p', 'm', 'w'))

        return index + 1, vector

    @staticmethod
    def func_call(index: int) \
            -> Tuple[int, RelationList, bool]:
        """Function call handler stub."""
        logger.debug('Function call detected!\nThis feature is not yet '
                     'supported, but will be added soon')
        return index, RelationList(), False
