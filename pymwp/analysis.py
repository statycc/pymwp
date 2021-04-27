import os
import sys
import logging
import json
from subprocess import CalledProcessError
from typing import Optional, List, Tuple
from pycparser import parse_file, c_ast

from .relation_list import RelationList
from .relation import Relation
from .polynomial import Polynomial
from .monomial import Monomial
from .matrix import decode

logger = logging.getLogger(__name__)


class MyWhile:
    """Loop object."""

    def __init__(self, node_while, parent, isOpt, subWhiles):
        # Corresponding node in the ast
        self.node_while = node_while
        # its parent node
        self.parent = parent
        # a boolean to know if it's optimzed yet
        self.isOpt = isOpt
        # Sub loops it may contains
        self.subWhiles = subWhiles

    # Pretty printing
    def show(self, indent=""):
        indice = self.parent[1]
        opt = self.isOpt
        print(indent + "while - " + str(indice) + " est opt:" + str(opt))
        self.node_while.show()
        for sub_while in self.subWhiles:
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
        # Will contain list of `myWhile` object
        self.values = []

    def visit(self, node, parent=None, i=-1):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, parent, i)

    # When visit create `myWhile` object to the list of while
    def visit_While(self, node, parent=None, i=-1):
        wv = WhileVisitor()
        wv.visit(node.stmt)
        myWhile = MyWhile(node, (parent, i), False, wv.values)
        # mywhile = c_ast.While(node.cond,node.stmt)
        self.values.append(myWhile)

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

    def __init__(self, in_file: str, out_path: Optional[str] = None):
        """Run MWP analysis on specified file.

        Arguments:
            in_file: path to C file
            out_path: where to store result
        """
        out_file = out_path or Analysis.default_out_file(in_file)
        choices = [0, 1, 2]

        logger.info("Starting analysis of %s", in_file)
        ast = Analysis.parse_c_file(in_file)

        if not ast.ext or \
                ast.ext[0].body is None or \
                ast.ext[0].body.block_items is None:
            logger.error('Input is invalid or empty. Terminating.')
            sys.exit(1)

        function_body = ast.ext[0].body

        index, relations = 0, RelationList()
        total = len(function_body.block_items)

        for i, stmt in enumerate(function_body.block_items):
            logger.debug(f'computing relation...{i} of {total}')
            index, rel_list = Analysis.compute_relation(index, stmt)
            logger.debug(f'computing composition...{i} of {total}')
            relations.composition(rel_list)

        relation = relations.relations[0]
        combinations = relation.non_infinity(choices, index)
        logger.debug('saving result')
        Analysis.save_relation(out_file, relation, combinations)
        logger.info("saved result in %s", out_file)

        if combinations:
            logger.info(combinations)
        else:
            logger.info("infinite")

    @staticmethod
    def default_out_file(in_file: str):
        file_only = os.path.splitext(in_file)[0]
        file_name = os.path.basename(file_only)
        return os.path.join("output", f"{file_name}.txt")

    @staticmethod
    def parse_c_file(
            file, use_cpp: bool = True, cpp_path: str = "gcc",
            cpp_args: str = "-E"
    ):
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
    def compute_relation(index: int, node) -> Tuple[int, RelationList]:
        """Create a relation list corresponding for all possible matrices
        of node.

        Arguments:
            index: delta index
            node: AST node to analyze

        Returns:
            Updated index value and relation list
        """

        # TODO: miss unary and constants operation
        logger.debug("in compute_relation")

        if isinstance(node, c_ast.Assignment):
            return Analysis.analyze_assignment(node, index)
        if isinstance(node, c_ast.If):
            return Analysis.analyse_if(node, index)
        if isinstance(node, c_ast.While):
            return Analysis.analyze_while(node, index)
        if isinstance(node, c_ast.For):
            return Analysis.analyze_for(node, index)

        # TODO: handle uncovered cases
        logger.debug(f"uncovered case! type: {type(node)}")
        return index, RelationList()

    @staticmethod
    def analyze_assignment(node, index):
        """Analyze assignment."""
        x = node.lvalue.name
        dblist = [[x], []]
        if isinstance(node.rvalue, c_ast.BinaryOp):  # x=y+z
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
        if isinstance(node.rvalue, c_ast.Constant):  # x=Cte TODO
            rest = RelationList([x])
            logger.debug('Computing Relation (second case)')
            return index, rest
        if isinstance(node.rvalue, c_ast.UnaryOp):  # x=exp(…) TODO
            listVar = None  # list_var(exp)
            rels = RelationList.identity([x] + listVar)
            # TODO
            logger.debug('Computing Relation (third case)')
            return index, rels

    @staticmethod
    def analyse_if(node, index):
        """Analyze if statement."""
        logger.debug("analysing If:")
        true_relation = RelationList([])
        for child in node.iftrue.block_items:
            index, rel_list = Analysis.compute_relation(index, child)
            true_relation.composition(rel_list)
        false_relation = RelationList([])
        if node.iffalse is not None:
            for child in node.iffalse.block_items:
                index, rel_list = Analysis.compute_relation(index, child)
                false_relation.composition(rel_list)
        relations = false_relation + true_relation
        logger.debug('computing relation (conditional case)')
        return index, relations

    @staticmethod
    def analyze_while(node, index):
        """Analyze while loop."""
        logger.debug("analysing While:")
        relations = RelationList()
        for child in node.stmt.block_items:
            index, rel_list = Analysis.compute_relation(index, child)
            relations.composition(rel_list)
        logger.debug('while loop fixpoint')
        relations.fixpoint()
        relations.while_correction()
        return index, relations

    @staticmethod
    def analyze_for(node, index):
        """Analyze for loop node."""
        logger.debug("analysing For:")
        relations = RelationList()
        for child in node.stmt.block_items:
            index, rel_list = Analysis.compute_relation(index, child)
            relations.composition(rel_list)
        relations.fixpoint()
        # TODO: what is conditionRel?
        relations = relations.conditionRel(VarVisitor.list_var(node.cond))
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
        with open(file_name, "r") as file_object:
            data = json.load(file_object)

        # parse its data
        matrix = data["relation"]["matrix"]
        variables = data["relation"]["variables"]
        combinations = data["combinations"]

        # generate objects
        relation = Relation(variables, decode(matrix))
        relation_list = RelationList(relation_list=[relation])
        return relation_list, combinations
