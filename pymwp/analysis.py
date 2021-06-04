import sys
import logging
from subprocess import CalledProcessError
from typing import List, Tuple
from pycparser import parse_file, c_ast
from pycparser.c_ast import Node, Assignment, If, While, For

from .relation_list import RelationList, Relation
from .polynomial import Polynomial
from .monomial import Monomial
from .file_io import save_relation

logger = logging.getLogger(__name__)


class Analysis:
    """MWP analysis implementation."""

    @staticmethod
    def run(
            file_in: str, file_out: str = None, no_save: bool = False,
            use_cpp: bool = True, cpp_path: str = None, cpp_args: str = None
    ) -> Tuple[Relation, List[List[int]]]:
        """Run MWP analysis on specified input file.

        Arguments:
            file_in: C source code file path
            file_out: where to store result
            no_save: Set true when analysis result should not be saved to file
            use_cpp: Set to True if you want to execute the C pre-processor
                on the file prior to parsing it.
            cpp_path: If use_cpp is True, this is the path to 'cpp' on your
                system. If no path is provided, it attempts to just execute
                'cpp', so it must be in your PATH.
            cpp_args: If use_cpp is True, set this to the command line
                arguments strings to cpp. Be careful with quotes - it's best
                to pass a raw string (r'') here. If several arguments are
                required, pass a list of strings.

        Returns:
              Computed relation and list of non-infinity choices.

        """

        choices = [0, 1, 2]
        logger.info(f'Starting analysis of {file_in}')
        ast = Analysis.parse_c_file(file_in, use_cpp, cpp_path, cpp_args)
        Analysis.validate_ast(ast)

        function_body = ast.ext[0].body
        index, relations = 0, RelationList()
        total = len(function_body.block_items)

        for i, node in enumerate(function_body.block_items):
            logger.debug(f'computing relation...{i} of {total}')
            index, rel_list = Analysis.compute_relation(index, node)
            logger.debug(f'computing composition...{i} of {total}')
            relations.composition(rel_list)

        relation = relations.relations[0]
        combinations = relation.non_infinity(choices, index)
        if not no_save:
            save_relation(file_out, relation, combinations)

        logger.debug(relations)
        if combinations:
            logger.info(f'\n{combinations}')
        else:
            logger.info('infinite')

        return relation, combinations

    @staticmethod
    def compute_relation(index: int, node: Node) -> Tuple[int, RelationList]:
        """Create a relation list corresponding for all possible matrices
        of an AST node.

        Arguments:
            index: delta index
            node: AST node to analyze

        Returns:
            Updated index value and relation list
        """

        logger.debug("in compute_relation")

        if isinstance(node, c_ast.Assignment):
            if isinstance(node.rvalue, c_ast.BinaryOp):
                return Analysis.binary_op(index, node)
            if isinstance(node.rvalue, c_ast.Constant):
                return Analysis.constant(index, node)
            if isinstance(node.rvalue, c_ast.UnaryOp):
                return Analysis.unary_op(index, node)
            if isinstance(node.rvalue, c_ast.ID):
                x = node.lvalue.name
                y = node.rvalue.name
                if x != y:
                    return Analysis.id(index, node)
        if isinstance(node, c_ast.If):
            return Analysis.if_(index, node)
        if isinstance(node, c_ast.While):
            return Analysis.while_(index, node)
        if isinstance(node, c_ast.For):
            return Analysis.for_(index, node)

        # TODO: handle uncovered cases
        logger.debug(f"uncovered case! type: {type(node)}")

        return index, RelationList()

    @staticmethod
    def id(index: int, node: Assignment) -> Tuple[int, RelationList]:
        """Analyze x = y (with x != y) and y not a const

        Arguments:
            index: delta index
            node: AST node representing a simple assignment

        Returns:
            Updated index value and relation list
        """
        logger.debug('Computing Relation x = y')
        x = node.lvalue.name
        y = node.rvalue.name
        vars_list = [[x], [y]]

        # create a vector of polynomials based on operator type
        #     x   y
        # x | o   o
        # y | m   m
        vector = [
                Polynomial([Monomial("o")]), # because x != y
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

        return index + 1, rel_list

    @staticmethod
    def binary_op(index: int, node: Assignment) -> Tuple[int, RelationList]:
        """Analyze binary operation, e.g. `x = y + z`.

        Arguments:
            index: delta index
            node: AST node representing a binary operation

        Returns:
            Updated index value and relation list
        """
        logger.debug('Computing Relation (first case / binary op)')
        x = node.lvalue.name
        vars_list = [[x], []]

        # get left operand name if not a constant
        if not isinstance(node.rvalue.left, c_ast.Constant):
            y = node.rvalue.left.name
            vars_list[1].append(y)

        # get right operand name if not a constant
        if not isinstance(node.rvalue.right, c_ast.Constant):
            z = node.rvalue.right.name
            vars_list[1].append(z)

        # create a vector of polynomials based on operator type
        index, vector = Analysis.create_vector(index, node, vars_list)

        # build a list of unique variables
        variables = vars_list[0]
        for var in vars_list[1]:
            if var not in variables:
                variables.append(var)

        # create relation list
        rel_list = RelationList.identity(variables)
        rel_list.replace_column(vector, vars_list[0][0])

        return index, rel_list

    @staticmethod
    def constant(index: int, node: Assignment) -> Tuple[int, RelationList]:
        """Analyze a constant.

        From MWP paper:

        > To deal with constants, just replace the program’s constants by
          variables and regard the replaced constants as input to these
          variables.

        Arguments:
            index: delta index
            node: node representing a constant

        Returns:
            Updated index value and relation list
        """

        logger.debug('Computing Relation (second case / constant)')
        var_name = node.lvalue.name
        return index, RelationList([var_name])

    @staticmethod
    def unary_op(index: int, node: Assignment) -> Tuple[int, RelationList]:
        """Analyze unary operator.

        Arguments:
            index: delta index
            node: unary operator node

        Returns:
            Updated index value and relation list
        """
        # TODO : implement unary op
        logger.debug('Computing Relation (third case / unary)')
        var_name = node.lvalue.name
        # list_var = None  # list_var(exp)
        # variables = [var_name] + list_var
        variables = [var_name]
        return index, RelationList.identity(variables)

    @staticmethod
    def if_(index: int, node: If) -> Tuple[int, RelationList]:
        """Analyze an if statement.

        Arguments:
            index: delta index
            node: if-statement AST node

        Returns:
            Updated index value and relation list
        """
        logger.debug('computing relation (conditional case)')
        true_relation, false_relation = RelationList(), RelationList()

        index = Analysis.if_branch(node.iftrue, index, true_relation)
        index = Analysis.if_branch(node.iffalse, index, false_relation)

        relations = false_relation + true_relation
        return index, relations

    @staticmethod
    def if_branch(node, index, relation_list) -> int:
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

        Returns:
            Updated index value
        """
        if node is not None:
            if hasattr(node, 'block_items'):
                for child in node.block_items:
                    index, rel_list = Analysis.compute_relation(index, child)
                    relation_list.composition(rel_list)
            else:
                index, rel_list = Analysis.compute_relation(index, node)
                relation_list.composition(rel_list)
        return index

    @staticmethod
    def while_(index: int, node: While) -> Tuple[int, RelationList]:
        """Analyze while loop.

        Arguments:
            index: delta index
            node: while loop node

        Returns:
            Updated index value and relation list
        """
        logger.debug("analysing While")

        relations = RelationList()
        for child in node.stmt.block_items:
            index, rel_list = Analysis.compute_relation(index, child)
            relations.composition(rel_list)

        logger.debug('while loop fixpoint')
        relations.fixpoint()
        relations.while_correction()

        return index, relations

    @staticmethod
    def for_(index: int, node: For) -> Tuple[int, RelationList]:
        """Analyze for loop node.

        Arguments:
            index: delta index
            node: for loop node

        Returns:
            Updated index value and relation list

        """
        logger.debug("analysing for:")

        relations = RelationList()
        for child in node.stmt.block_items:
            index, rel_list = Analysis.compute_relation(index, child)
            relations.composition(rel_list)

        relations.fixpoint()
        # TODO: unknown method conditionRel
        #  ref: https://github.com/seiller/pymwp/issues/5
        # relations = relations.conditionRel(VarVisitor.list_var(node.cond))
        return index, relations

    @staticmethod
    def create_vector(
            index: int, node: Assignment, variables_list: List[List[str]]
    ) -> Tuple[int, List[Polynomial]]:
        """Create a polynomial vector.

        For an AST node that represents a binary operation, this method
        generates a vector of polynomials based on the properties of that
        node.

        The returned value depends on the type of operator, how many
        operands are constants, and if the operands are equal.

        Arguments:
            index: delta index
            node: AST node under analysis
            variables_list: list of known variables

        Returns:
             Updated index, list of Polynomial vectors
        """

        dependence_type = None
        p1_scalars, p2_scalars = None, None
        const_count = 2 - len(variables_list[1])
        if const_count == 0:
            operand_match = variables_list[1][0] == variables_list[1][1]
        else:
            operand_match = False
        # x = … (if x not in …)
        prepend_zero = variables_list[0][0] not in variables_list[1]

        # determine dependence type
        if node.rvalue.op in ["+", "-"]:
            dependence_type = "+" if const_count == 0 else 'u'
        elif node.rvalue.op in ["*"]:
            dependence_type = "*" if const_count == 0 else 'u'

        # determine scalars
        if dependence_type == 'u':
            p1_scalars = 'm', 'm', 'm'

        if dependence_type == '*':
            p1_scalars = 'w', 'w', 'w'
            if not operand_match:
                p2_scalars = 'w', 'w', 'w'

        if dependence_type == '+':
            if operand_match:
                p1_scalars = 'w', 'p', 'w'
            else:
                p1_scalars = 'w', 'm', 'p'
                p2_scalars = 'w', 'p', 'm'

        # build vector of polynomials
        vector = []
        if prepend_zero:
            vector.append(Polynomial([Monomial("o")]))
        if p1_scalars:
            vector.append(Polynomial(
                [Monomial(scalar, [(val, index)])
                 for val, scalar in enumerate(p1_scalars)]))
        if p2_scalars:
            vector.append(Polynomial(
                [Monomial(scalar, [(val, index)])
                 for val, scalar in enumerate(p2_scalars)]))

        return index + 1, vector

    @staticmethod
    def parse_c_file(
            file: str, use_cpp: bool, cpp_path: str, cpp_args: str
    ) -> c_ast:
        """Parse C file using pycparser.

        Arguments:
            file: path to C file
            use_cpp: Set to True if you want to execute the C pre-processor
                on the file prior to parsing it.
            cpp_path: If use_cpp is True, this is the path to 'cpp' on your
                system. If no path is provided, it attempts to just execute
                'cpp', so it must be in your PATH.
            cpp_args: If use_cpp is True, set this to the command line
                arguments strings to cpp. Be careful with quotes - it's best
                to pass a raw string (r'') here. If several arguments are
                required, pass a list of strings.

        Returns:
            Generated AST
        """
        try:
            ast = parse_file(file, use_cpp, cpp_path, cpp_args)
            if use_cpp:
                info = f'parsed with preprocessor: {cpp_path} {cpp_args}'
            else:
                info = 'parsed without preprocessor'
            logger.debug(info)
            return ast
        except CalledProcessError:
            logger.error('Failed to parse C file. Terminating.')
            sys.exit(1)

    @staticmethod
    def validate_ast(ast: c_ast) -> None:
        """Check if successfully parsed AST can be analyzed.

        Here we check that the C input file contains some source code
        (has body) and that that body is not empty (has block_items).
        These types of inputs do not cause the parser to error, so we
        need to check these separately from parse error.

        If the input is invalid terminate immediately.

        Ref: [issue #4](https://github.com/seiller/pymwp/issues/4)

        Arguments:
            ast: AST object
        """

        invalid = ast is None or ast.ext is None or len(ast.ext) == 0
        invalid = invalid or ast.ext[0].body is None or ast.ext[
            0].body.block_items is None

        if invalid:
            logger.error('Input C file is invalid or empty.')
            sys.exit(1)
