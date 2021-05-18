import sys
import logging
from subprocess import CalledProcessError
from typing import Optional, List, Tuple
from pycparser import parse_file, c_ast
from pycparser.c_ast import Node, Assignment, If, While, For

from .relation_list import RelationList
from .polynomial import Polynomial
from .monomial import Monomial
from .file_io import save_relation

logger = logging.getLogger(__name__)


class Analysis:
    """MWP analysis implementation."""

    def __init__(
            self, file_in: str, file_out: str, use_cpp: bool, cpp_path: str,
            cpp_args: str
    ):
        """Run MWP analysis on specified input file.

        Arguments:
            file_in: C source code file path
            file_out: where to store result
            use_cpp: Set to True if you want to execute the C pre-processor
                on the file prior to parsing it.
            cpp_path: If use_cpp is True, this is the path to 'cpp' on your
                system. If no path is provided, it attempts to just execute
                'cpp', so it must be in your PATH.
            cpp_args: If use_cpp is True, set this to the command line
                arguments strings to cpp. Be careful with quotes - it's best
                to pass a raw string (r'') here. If several arguments are
                required, pass a list of strings.
        """

        choices = [0, 1, 2]
        logger.info(f'Starting analysis of {file_in}')
        ast = Analysis.parse_c_file(file_in, use_cpp, cpp_path, cpp_args)

        # handle empty file / empty main
        if not ast.ext or \
                ast.ext[0].body is None or \
                ast.ext[0].body.block_items is None:
            logger.error('Input is invalid or empty. Terminating.')
            sys.exit(1)

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
        save_relation(file_out, relation, combinations)
        logger.info(f'saved result in {file_out}')

        logger.debug(relations)
        if combinations:
            logger.info(f'\n{combinations}')
        else:
            logger.info('infinite')

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

        Arguments:
            index: delta index
            node: node representing a constant

        Returns:
            Updated index value and relation list
        """
        # TODO: implement constants, from MWP paper:
        # To deal with constants, just replace the program’s constants by
        # variables and regard the replaced constants as input to these
        # variables.

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
            node: if-statement node

        Returns:
            Updated index value and relation list
        """
        logger.debug('computing relation (conditional case)')
        true_relation = RelationList()
        false_relation = RelationList()

        index = Analysis.if_branch(node.iftrue, index, true_relation)
        index = Analysis.if_branch(node.iffalse, index, false_relation)

        relations = false_relation + true_relation
        return index, relations

    @staticmethod
    def if_branch(node, index, relation_list) -> int:
        """Analyze true or false branch of an if statement.

        Arguments:
            node: AST branch node
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
        operand_match = variables_list[1][0] == variables_list[1][1]
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
            file: str, use_cpp: Optional[bool], cpp_path: Optional[str],
            cpp_args: Optional[str]
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


class MyWhile:
    """Loop object."""

    def __init__(self, node_while, parent, is_opt, sub_whiles):
        # Corresponding node in the ast
        self.node_while = node_while
        # its parent node
        self.parent = parent
        # a boolean to know if it's optimized yet
        self.is_opt = is_opt
        # Sub loops it may contains
        self.sub_whiles = sub_whiles

    def show(self, indent=""):
        """Pretty printing."""
        index = self.parent[1]
        opt = self.is_opt
        logger.debug(f'{indent} while - {index} est opt: {opt}')
        self.node_while.show()
        for sub_while in self.sub_whiles:
            sub_while.show("\t")


class VarVisitor(c_ast.NodeVisitor):
    """
    pycparser provides visitors of nodes. This simplify action we want
    to perform on specific node in a traversal way.
    Here for visiting variables nodes.

    TODO: this is not being used, do we need it?
    """

    def __init__(self):
        self.values = []

    @staticmethod
    def list_var(node):
        """TODO: what is this?"""
        vv = VarVisitor()
        vv.visit(node)
        return vv.values


class WhileVisitor(c_ast.NodeVisitor):
    """For visiting and performing actions for every encountered while node."""

    def __init__(self):
        self.values = []

    def visit(self, node, parent=None, i=-1):
        """TODO: what is this?"""
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, parent, i)

    def visit_while(self, node, parent=None, i=-1):
        """When visit create `myWhile` object to the list of while."""
        wv = WhileVisitor()
        wv.visit(node.stmt)
        my_while = MyWhile(node, (parent, i), False, wv.values)
        self.values.append(my_while)

    def generic_visit(self, node, parent, i):
        """Called if no explicit visitor function exists for a
        node. Implements preorder visiting of the node.
        """
        i = 0
        for c_name, c in node.children():
            self.visit(c, node, i)
            i += 1
