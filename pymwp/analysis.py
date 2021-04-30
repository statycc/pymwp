import os
import sys
import logging
import json
from subprocess import CalledProcessError
from typing import Optional, List, Tuple
from pycparser import parse_file, c_ast
from pycparser.c_ast import Node, Assignment, If, While, For

from .relation_list import RelationList
from .relation import Relation
from .polynomial import Polynomial
from .monomial import Monomial
from .matrix import decode

logger = logging.getLogger(__name__)


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
        indice = self.parent[1]
        opt = self.is_opt
        print(indent + "while - " + str(indice) + " est opt:" + str(opt))
        self.node_while.show()
        for sub_while in self.sub_whiles:
            sub_while.show("\t")


class VarVisitor(c_ast.NodeVisitor):
    """
    pycparser provides visitors of nodes. This simplify action we want
    to perform on specific node in a traversal way.
    Here for visiting variables nodes.

    TODO: this is not being used, why?
    """

    def __init__(self):
        self.values = []

    @staticmethod
    def list_var(node):
        vv = VarVisitor()
        vv.visit(node)
        return vv.values


class WhileVisitor(c_ast.NodeVisitor):
    """For visiting and performing actions for every encountered while node."""

    def __init__(self):
        self.values = []

    def visit(self, node, parent=None, i=-1):
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


class Analysis:
    """MWP analysis implementation."""

    def __init__(self, file_in: str, file_out: Optional[str] = None):
        """Run MWP analysis on specified input file.

        Arguments:
            file_in: C source code file path
            file_out: where to store result
        """

        # TODO: parametrize
        output_file = file_out or Analysis.default_file_out(file_in)
        use_cpp, cpp_path, cpp_args = None, None, None
        choices = [0, 1, 2]

        logger.info("Starting analysis of %s", file_in)
        ast = Analysis.parse_c_file(file_in, use_cpp, cpp_path, cpp_args)

        if not ast.ext or \
                ast.ext[0].body is None or \
                ast.ext[0].body.block_items is None:
            logger.error('Input is invalid or empty. Terminating.')
            sys.exit(1)

        function_body = ast.ext[0].body
        index, relations = 0, RelationList()
        total = len(function_body.block_items)

        for i, node in enumerate(function_body.block_items):
            logger.debug(f'computing relation...{i} of {total} {type(node)}')
            index, rel_list = Analysis.compute_relation(index, node)
            logger.debug(f'computing composition...{i} of {total}')
            relations.composition(rel_list)

        relation = relations.relations[0]
        combinations = relation.non_infinity(choices, index)
        Analysis.save_relation(output_file, relation, combinations)
        logger.info("saved result in %s", output_file)

        logger.debug(relations)
        if combinations:
            logger.info(f"\n{combinations}")
        else:
            logger.info("infinite")

    @staticmethod
    def default_file_out(input_file: str) -> str:
        """Generates default output file.

        Arguments:
            input_file: input filename (with or without path)

        Returns:
            Generated output filename with path.

        """
        file_only = os.path.splitext(input_file)[0]
        file_name = os.path.basename(file_only)
        return os.path.join("output", f"{file_name}.txt")

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
            node: binary node to analyze

        Returns:
            Updated index value and relation list
        """
        x = node.lvalue.name
        dblist = [[x], []]
        nb_cst = 2
        if not isinstance(node.rvalue.left, c_ast.Constant):
            y = node.rvalue.left.name
            dblist[1].append(y)
            nb_cst -= 1
        if not isinstance(node.rvalue.right, c_ast.Constant):
            z = node.rvalue.right.name
            dblist[1].append(z)
            nb_cst -= 1
        listvar = dblist[0]
        for var in dblist[1]:
            if var not in listvar:
                listvar.append(var)
        # listvar=list(set(dblist[0])|set(dblist[1]))
        rest = RelationList.identity(listvar)
        # Define dependence type
        if node.rvalue.op in ["+", "-"]:
            logger.debug("operator +…")
            if nb_cst == 0:
                index, list_vect = Analysis \
                    .create_vector(index, dblist, "+")
            else:
                index, list_vect = Analysis \
                    .create_vector(index, dblist, "u")
        elif node.rvalue.op in ["*"]:
            logger.debug("operator *…")
            if nb_cst == 0:
                index, list_vect = Analysis \
                    .create_vector(index, dblist, "*")
            else:
                index, list_vect = Analysis \
                    .create_vector(index, dblist, "u")
        else:
            index, list_vect = Analysis \
                .create_vector(index, dblist, "undef")
        # logger.debug(f"list_vect={list_vect}")
        rest.replace_column(list_vect[0], dblist[0][0])
        logger.debug('Computing Relation (first case)')
        return index, rest

    @staticmethod
    def constant(index: int, node: Assignment) -> Tuple[int, RelationList]:
        """Analyze a constant.

        Arguments:
            index: delta index
            node: node representing a constant

        Returns:
            Updated index value and relation list
        """
        # TODO: implement
        logger.debug('Computing Relation (second case)')
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
        # TODO : implement
        logger.debug('Computing Relation (third case)')
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
        for child in node.iftrue.block_items:
            index, rel_list = Analysis.compute_relation(index, child)
            true_relation.composition(rel_list)

        false_relation = RelationList()
        if node.iffalse is not None:
            for child in node.iffalse.block_items:
                index, rel_list = Analysis.compute_relation(index, child)
                false_relation.composition(rel_list)

        relations = false_relation + true_relation
        return index, relations

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
            index: int, db_list: List[list], operator_type: str
    ) -> Tuple[int, List[List[Polynomial]]]:
        """Assign value flow regarding to operator operator_type.

        Arguments
            index: delta index
            db_list: TODO
            operator_type: one of `"u"`,`"+"`,`"*"`,`"undef"`

        Returns:
              updated index, nested list of polynomials
        """

        vector = []

        # helper for creating polynomials
        def append_poly(scalar1: str, scalar2: str, scalar3: str):
            vector.append(Polynomial([
                Monomial(scalar1, [(0, index)]),
                Monomial(scalar2, [(1, index)]),
                Monomial(scalar3, [(2, index)]),
            ]))

        if operator_type == "u":
            append_poly('m', 'm', 'm')

        elif db_list[1][0] == db_list[1][1]:
            if operator_type == "*":
                append_poly('w', 'w', 'w')
            if operator_type == "+":
                append_poly('w', 'p', 'w')

        else:
            if operator_type == "*":
                append_poly('w', 'w', 'w')
                append_poly('w', 'w', 'w')

            if operator_type == "+":
                append_poly('w', 'm', 'p')
                append_poly('w', 'p', 'm')

        if db_list[0][0] not in db_list[1]:
            vector.insert(0, Polynomial([Monomial("o")]))

        return index + 1, [vector]

    @staticmethod
    def parse_c_file(
            file: str, use_cpp: Optional[bool] = True,
            cpp_path: Optional[str] = "gcc", cpp_args: Optional[str] = "-E"
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
            logger.debug("C file parsed using args: %s %s", cpp_path, cpp_args)
            return ast
        except CalledProcessError:
            logger.error('Failed to parse C file. Terminating.')
            sys.exit(1)

    @staticmethod
    def save_relation(
            file_name: str, relation: Relation, combinations: List[List[int]]
    ) -> None:
        """Save analysis result to file.

        Arguments:
            file_name: file to write
            relation: result relation
            combinations: non-infinity choices
        """
        info = {
            "relation": relation.to_dict(),
            "combinations": combinations
        }

        # ensure directory path exists
        dir_path, _ = os.path.split(file_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # write to file
        with open(file_name, "w") as outfile:
            json.dump(info, outfile, indent=4)

    @staticmethod
    def load_relation(file_name: str) -> Tuple[RelationList, List[List[int]]]:
        """Load previous analysis result from file.

        Arguments:
            file_name: file to read

        Returns:
            parsed relation list and combinations

        """
        # read the file
        with open(file_name) as file_object:
            data = json.load(file_object)

        # parse its data
        matrix = data["relation"]["matrix"]
        variables = data["relation"]["variables"]
        combinations = data["combinations"]

        # generate objects
        relation = Relation(variables, decode(matrix))
        relation_list = RelationList(relation_list=[relation])
        return relation_list, combinations
