import sys
import logging
from subprocess import CalledProcessError
from typing import List, Tuple
from pycparser import parse_file, c_ast
from pycparser.c_ast import Node, Assignment, If, While, For, Compound

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
        total = len(function_body.block_items)
        relations = RelationList()
        delta_infty = False
        dg = DeltaGraph()
        combinations = []
        index = 0

        # variables = Analysis.find_variables(function_body)
        # relations = RelationList(variables=variables)

        for i, node in enumerate(function_body.block_items):
            logger.debug(f'computing relation...{i} of {total}')
            index, rel_list, exit_ = Analysis.compute_relation(index, node, dg)
            if exit_:
                delta_infty = True
                break
            logger.debug(f'computing composition...{i} of {total}')
            relations.composition(rel_list)

        # skip evaluation when delta graph has detected infinity
        if not delta_infty:
            combinations = relations.first.non_infinity(choices, index, dg)

        if not no_save:
            save_relation(file_out, relations.first, combinations)

        logger.debug(f'\nMATRIX{relations}')
        if not combinations:
            logger.info('infinite')
            # Should not raise here since delta_graph takes care of it
        else:
            logger.info(f'CHOICES:\n{combinations}')

        return relations.first, combinations

    @staticmethod
    def find_variables(root: Node):
        variables = []

        def recurse_nodes(node_):
            if isinstance(node_, c_ast.Decl):
                variables.append(node_.name)
            if hasattr(node_, 'block_items'):
                for sub_node in node_.block_items:
                    recurse_nodes(sub_node)

        if hasattr(root, 'block_items'):
            for node in root.block_items:
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
            dg: DeltaGraph instance

        Returns:
            Updated index value and relation list and a boolean telling
            us if we should stop here
        """

        logger.debug("in compute_relation")

        if isinstance(node, c_ast.Decl):
            return index, RelationList(), False
        if isinstance(node, c_ast.Assignment):
            if isinstance(node.rvalue, c_ast.BinaryOp):
                index, rel_list = Analysis.binary_op(index, node)
                return index, rel_list, False
            if isinstance(node.rvalue, c_ast.Constant):
                index, rel_list = Analysis.constant(index, node)
                return index, rel_list, False
            if isinstance(node.rvalue, c_ast.UnaryOp):
                index, rel_list = Analysis.unary_op(index, node)
                return index, rel_list, False
            if isinstance(node.rvalue, c_ast.ID):
                x = node.lvalue.name
                y = node.rvalue.name
                if x != y:
                    index, rel_list = Analysis.id(index, node)
                    return index, rel_list, False
        if isinstance(node, c_ast.If):
            return Analysis.if_(index, node, dg)
        if isinstance(node, c_ast.While):
            return Analysis.while_(index, node, dg)
        if isinstance(node, c_ast.For):
            return Analysis.for_(index, node, dg)
        if isinstance(node, c_ast.Compound):
            return Analysis.compound_(index, node, dg)

        # TODO: handle uncovered cases
        logger.debug(f"uncovered case! type: {type(node)}")

        return index, RelationList(), False

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
            Updated index value and relation list and False
        """
        # TODO : implement unary op
        logger.debug('Computing Relation (third case / unary)')
        var_name = node.lvalue.name
        # list_var = None  # list_var(exp)
        # variables = [var_name] + list_var
        variables = [var_name]
        return index, RelationList.identity(variables)

    @staticmethod
    def if_(index: int, node: If, dg: DeltaGraph) \
            -> Tuple[int, RelationList, bool]:
        """Analyze an if statement.

        Arguments:
            index: delta index
            node: if-statement AST node
            dg: DeltaGraph instance

        Returns:
            Updated index value and relation list, and exit flag
        """
        logger.debug('computing relation (conditional case)')
        true_relation, false_relation = RelationList(), RelationList()

        index, exit_ = Analysis.if_branch(
            node.iftrue, index, true_relation, dg)
        if exit_:
            return index, true_relation, exit_
        index, exit_ = Analysis.if_branch(
            node.iffalse, index, false_relation, dg)
        if exit_:
            return index, false_relation, exit_

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
            dg: DeltaGraph instance

        Returns:
            Updated index value and exit flag
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
            dg: DeltaGraph instance

        Returns:
            Updated index value and relation list and a boolean saying
            if we can stop here
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
            dg: DeltaGraph instance

        Returns:
            Updated index value and relation list and exit flag
        """
        logger.debug("analysing for:")

        relations = RelationList()
        for child in node.stmt.block_items:
            index, rel_list, exit = Analysis.compute_relation(index, child, dg)
            if exit:
                return index, rel_list, exit
            relations.composition(rel_list)

        relations.fixpoint()
        # TODO: unknown method conditionRel
        #  ref: https://github.com/seiller/pymwp/issues/5
        # relations = relations.conditionRel(VarVisitor.list_var(node.cond))
        return index, relations, True

    @staticmethod
    def compound_(
            index: int, node: Compound, dg: DeltaGraph
    ) -> Tuple[int, RelationList, bool]:
        """Compound AST node contains zero or more children and is
        created by braces in source code.

        We analyze such compound node by recursively analysing its children.

        Arguments:
            index: delta index
            node: compound AST node
            dg: DeltaGraph instance

        Returns:
            Updated index value and relation list and exit flag
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
            index: int, node: Assignment, variables: List[List[str]]
    ) -> Tuple[int, List[Polynomial]]:
        """Build a polynomial vector based on operator and the operands
        of a binary operation statement.

        For an AST node that represents a binary operation, this method
        generates a vector of polynomials based on the properties of that
        operation. The returned vector depends on the type of operator,
        how many operands are constants, and if the operands are equal.

        Arguments:
            index: delta index
            node: AST node under analysis
            variables: list of unique variables in this operation where:
                - variables[0][0] is the variable on left side of assignment
                - variables[1][0] is left operand of binary operation
                - variables[1][1] is right operand of binary operation
                - note: left/right operand is not present if it is a constant,
                therefore check length of variables[1] before use/unpacking.

        Returns:
             Updated index, list of Polynomial vectors
        """

        dependence_type = None
        p1_scalars, p2_scalars = None, None
        const_count = 2 - len(variables[1])
        unknown = 'u'

        # Do right hand side operators match each other.
        # when they are different we create a vector of
        # 2 polynomials, and 1 polynomial otherwise.
        operand_match = const_count == 0 and variables[1][0] == variables[1][1]

        # x = … (if x not in …), i.e. when left side variable does not
        # occur on the right side of assignment, we prepend 0 to vector
        prepend_zero = variables[0][0] not in variables[1]

        # determine dependence type
        if node.rvalue.op in ["+", "-"]:
            dependence_type = "+" if const_count == 0 else unknown
        elif node.rvalue.op in ["*"]:
            dependence_type = "*" if const_count == 0 else unknown

        # determine what scalars polynomial should have
        if dependence_type == unknown:
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

        # now build vector of 0 or more polynomials
        vector = []

        # when left variable does not occur on right side of assignment
        if prepend_zero:
            vector.append(Polynomial([Monomial("o")]))

        # we _should_ have at least this one, but will be None if the
        # operator is not + or * so check
        if p1_scalars:
            vector.append(Polynomial(
                [Monomial(scalar, [(val, index)])
                 for val, scalar in enumerate(p1_scalars)]))

        # when there are two different, non-constant operands on right
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

        invalid = ast is None or ast.ext is None or len(ast.ext) == 0 or \
                  ast.ext[0].body is None or \
                  ast.ext[0].body.block_items is None

        if invalid:
            logger.error('Input C file is invalid or empty.')
            sys.exit(1)
