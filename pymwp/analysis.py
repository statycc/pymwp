import os
import logging
import json
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
        function_body = ast.ext[0].body

        index, relations = 0, RelationList()
        total = len(function_body.block_items)

        for i, stmt in enumerate(function_body.block_items):
            logger.debug(f'computing relation...{i} of {total}')
            index, rel_list = self.compute_relation(index, stmt)
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
        ast = parse_file(file, use_cpp, cpp_path, cpp_args)
        logger.debug("C file parsed using args: %s %s", cpp_path, cpp_args)
        return ast

    def compute_relation(self, index: int, node) -> Tuple[int, RelationList]:
        """Return a RelationList corresponding for all possible matrices
        of `node`.

        Arguments:
            index: TODO
            node: TODO

        Returns:
            TODO
        """
        # TODO miss unary and constantes operation

        logger.debug("In compute_relation")

        if isinstance(node, c_ast.Assignment):
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
        if isinstance(node, c_ast.If):  # if cond then … else …
            logger.debug("analysing If:")
            relT = RelationList([])
            for child in node.iftrue.block_items:
                index, rel_list = self.compute_relation(index, child)
                relT.composition(rel_list)
            relF = RelationList([])
            if node.iffalse is not None:
                for child in node.iffalse.block_items:
                    index, rel_list = self.compute_relation(index, child)
                    relF.composition(rel_list)
            rels = relF + relT
            # rels=rels.conditionRel(list_var(node.cond))
            # if DEBUG_LEVEL >= 2:
            logger.debug('Computing Relation (conditional case)')
            return index, rels
        if isinstance(node, c_ast.While):
            logger.debug("analysing While:")
            rels = RelationList()
            for child in node.stmt.block_items:
                index, rel_list = self.compute_relation(index, child)
                rels.composition(rel_list)
            logger.debug('Computing Relation (loop case) before fixpoint')
            rels.fixpoint()
            logger.debug('Computing Relation (loop case) after fixpoint)')
            rels.while_correction()
            logger.debug('Computing Relation (loop case)')
            return index, rels
        if isinstance(node, c_ast.For):
            logger.debug("analysing For:")
            rels = RelationList()
            for child in node.stmt.block_items:
                index, rel_list = self.compute_relation(index, child)
                rels = rels.composition(rel_list)
            rels.fixpoint()
            rels = rels.conditionRel(VarVisitor.list_var(node.cond))
            return index, rels
        logger.debug(f"uncovered case! Type: {type(node)}")
        return index, RelationList()  #  FIXME

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
              updated index, list of polynomials
        """

        def create_polynomial(scalar1: str, scalar2: str,
                              scalar3: str) -> Polynomial:
            return Polynomial([
                Monomial(scalar1, [(0, index)]),
                Monomial(scalar2, [(1, index)]),
                Monomial(scalar3, [(2, index)]),
            ])

        vector = []

        if operator_type == "u":
            vector.append(create_polynomial('m', 'm', 'm'))

        if db_list[1][0] == db_list[1][1]:
            if operator_type == "*":
                vector.append(create_polynomial('w', 'w', 'w'))
            if operator_type == "+":
                vector.append(create_polynomial('w', 'p', 'w'))
        else:
            if operator_type == "*":
                poly1 = create_polynomial('w', 'w', 'w')
                poly2 = create_polynomial('w', 'w', 'w')
                vector = [poly1, poly2]
            if operator_type == "+":
                poly1 = create_polynomial('w', 'm', 'p')
                poly2 = create_polynomial('w', 'p', 'm')
                vector = [poly1, poly2]

        if db_list[0][0] not in db_list[1]:
            vector.insert(0, Polynomial([Monomial("o")]))

        return index + 1, [vector]

    @staticmethod
    def save_relation(file_name: str, relation: Relation,
                      combinations: List[List[int]]) -> None:
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

        !!! info
            This method is not currently used.

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
