from __future__ import print_function
import sys
import json
import os
from pycparser import parse_file, c_parser, c_ast
# from Matrix import RelationList
# from Matrix import Relation
from relation import Relation
from relation_list import RelationList
from monomial import Monomial
from polynomial import Polynomial

# -*- coding: UTF-8 -*-
#
sys.path.extend([".", ".."])

DEBUG_LEVEL = 0
NVIND = -1

# Create the parser and ask to parse the text. parse() will throw
# a ParseError if there's an error in the code
#
parser = c_parser.CParser()

# Parse a given file ↓
filename = sys.argv[1]
ast = parse_file(filename, use_cpp=True, cpp_path="gcc",
                 cpp_args=["-E"])  # replace cpp with gcc to remove comments


# Or parse the one given in text above ↑
# ast = parser.parse(text, filename='<None>')

# Can show the ast ↓
# ast.ext[0].show()
# print(ast.ext[0])


# Loop object
class MyWhile:
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


# pycparser provides visitors of nodes
# This simplify action we want to perform on specific node in a traversal way


# Here for visiting variables nodes
class varVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.values = []

    def visit_ID(self, node):
        self.values.append(node.name)


# Her for visiting and performing actions for every encountered while node


class WhileVisitor(c_ast.NodeVisitor):
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


# Rreturn the list of variables in a node


def list_var(node):
    vv = varVisitor()
    vv.visit(node)
    return vv.values


# Assign value flow regarding to operator type


def create_vector(index, dblist, type):  # type in ("u","+","*","undef")
    list_vect = []
    poly = Polynomial([])
    if type == "u":
        poly = Polynomial([
            Monomial("m", [(0, index)]),
            Monomial("m", [(1, index)]),
            Monomial("m", [(2, index)]),
        ])
        list_vect.append([poly])
    if type == "*" and dblist[1][0] == dblist[1][1]:
        poly = Polynomial([
            Monomial("w", [(0, index)]),
            Monomial("w", [(1, index)]),
            Monomial("w", [(2, index)]),
        ])
        list_vect.append([poly])
    if type == "+" and dblist[1][0] == dblist[1][1]:
        poly = Polynomial([
            Monomial("w", [(0, index)]),
            Monomial("p", [(1, index)]),
            Monomial("w", [(2, index)]),
        ])
        list_vect.append([poly])
    if type == "*" and dblist[1][0] != dblist[1][1]:
        poly = Polynomial([
            Monomial("w", [(0, index)]),
            Monomial("w", [(1, index)]),
            Monomial("w", [(2, index)]),
        ])
        poly2 = Polynomial([
            Monomial("w", [(0, index)]),
            Monomial("w", [(1, index)]),
            Monomial("w", [(2, index)]),
        ])
        list_vect.append([poly, poly2])
    if type == "+" and dblist[1][0] != dblist[1][1]:
        poly = Polynomial([
            Monomial("w", [(0, index)]),
            Monomial("m", [(1, index)]),
            Monomial("p", [(2, index)]),
        ])
        poly2 = Polynomial([
            Monomial("w", [(0, index)]),
            Monomial("p", [(1, index)]),
            Monomial("m", [(2, index)]),
        ])
        list_vect.append([poly, poly2])
    if dblist[0][0] not in dblist[1]:
        for v in list_vect:
            v.insert(0, Polynomial([Monomial("o", [])]))
    index = index + 1
    return index, list_vect


# Return a RelationList corresponding for all possible matrices for `node`
def compute_rel(index, node):  # TODO miss unary and constantes operation
    print("In compute_rel")

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
            rest = RelationList(listvar)
            rest.identity()
            # Define dependence type
            node.show()
            if node.rvalue.op in ["+", "-"]:
                print("operator +…")
                if nb_cst == 0:
                    index, list_vect = create_vector(index, dblist, "+")
                else:
                    index, list_vect = create_vector(index, dblist, "u")
            elif node.rvalue.op in ["*"]:
                print("operator *…")
                if nb_cst == 0:
                    index, list_vect = create_vector(index, dblist, "*")
                else:
                    index, list_vect = create_vector(index, dblist, "u")
            else:
                index, list_vect = create_vector(index, dblist, "undef")
            ####
            print("list_vect=", list_vect)
            rest.replace_column(list_vect, dblist[0][0])
            if DEBUG_LEVEL >= 2:
                print("DEBUG: Computing Relation (first case)")
                node.show()
                rest.show()
            return index, rest
        if isinstance(node.rvalue, c_ast.Constant):  # x=Cte TODO
            rest = RelationList([x])
            if DEBUG_LEVEL >= 2:
                print("DEBUG: Computing Relation (second case)")
                node.show()
                rest.show()
            return index, rest
        if isinstance(node.rvalue, c_ast.UnaryOp):  # x=exp(…) TODO
            listVar = None  # list_var(exp)
            rels = RelationList([x] + listVar)
            rels.identity()
            # A FAIRE
            if DEBUG_LEVEL >= 2:
                print("DEBUG: Computing Relation  (third case)")
                node.show()
                rels.show()
            return index, rels
    if isinstance(node, c_ast.If):  # if cond then … else …
        print("analysing If:")
        relT = RelationList([])
        for child in node.iftrue.block_items:
            index, rel_list = compute_rel(index, child)
            relT.composition(rel_list)
        relF = RelationList([])
        if node.iffalse is not None:
            for child in node.iffalse.block_items:
                index, rel_list = compute_rel(index, child)
                relF.composition(rel_list)
        rels = relF.sum_relation(relT)
        # rels=rels.conditionRel(list_var(node.cond))
        if DEBUG_LEVEL >= 2:
            print("DEBUG: Computing Relation (conditional case)")
            node.show()
            rels.show()
        return index, rels
    if isinstance(node, c_ast.While):
        print("analysing While:")
        rels = RelationList([])
        for child in node.stmt.block_items:
            index, rel_list = compute_rel(index, child)
            rels.composition(rel_list)
        if DEBUG_LEVEL >= 2:
            print(
                "DEBUG: Computing Relation (loop case) before fixpoint")
            rels.show()
        rels.fixpoint()
        if DEBUG_LEVEL >= 2:
            print("DEBUG: Computing Relation (loop case) after fixpoint")
            rels.show()
        rels.while_correction()
        # rels = rels.conditionRel(list_var(node.cond))
        if DEBUG_LEVEL >= 2:
            print("DEBUG: Computing Relation (loop case)")
            node.show()
            rels.show()
        return index, rels
    if isinstance(node, c_ast.For):
        print("analysing For:")
        rels = RelationList([])
        for child in node.stmt.block_items:
            index, rel_list = compute_rel(index, child)
            rels = rels.composition(rel_list)
        rels = rels.fixpoint()
        rels = rels.conditionRel(list_var(node.cond))
        if DEBUG_LEVEL >= 2:
            print("DEBUG: Computing Relation (loop case)")
            node.show()
            rels.show()
        return index, rels
    print("uncovered case ! Create empty RelationList (function call) ?")
    node.show()
    return index, RelationList([])  #  FIXME


# ################# Perform on loops ##########

# wv = WhileVisitor()
# wv.visit(ast)
# if len(wv.values) == 0 :
#     print("No loops")
# else :
#     myWhile = wv.values[0]
#     myWhile.show()
#     CompList(myWhile)

# Perform on entire main function


def analysis():
    name = (os.path.join("./output/" +
                         os.path.basename(os.path.splitext(filename)[0])) +
            ".txt")
    return compute_relation(name)
    # TODO uncomment when issues are fixed
    # if not os.path.isfile(
    #         name) or os.path.getmtime(filename) > os.path.getmtime(name):
    #     return compute_relation(name)
    # else:
    #     return retrieve_relation(name)


def compute_relation(name):
    function_body = ast.ext[0].body
    rels = RelationList([])
    index = 0
    for stmt in function_body.block_items:
        index, rel_list = compute_rel(index, stmt)
        rels.composition(rel_list)
    combinations = output_json(name, rels, index)
    return rels, combinations


def retrieve_relation(name):
    with open(name, "r") as file_object:
        data = json.load(file_object)
    matrix = data["relation"]["matrix"]
    variables = data["relation"]["variables"]
    combinations = data["combinations"]
    rel = Relation(variables, matrix)
    # rel.decode_matrix(matrix)
    rels = RelationList([])
    rels.list[0] = rel
    return rels, combinations


def output_json(name, rels, index):
    rel = rels.list[0]
    combinations = rel.is_infinite([0, 1, 2], index)
    info = {"relation": rel.to_dict(), "combinations": combinations}
    dir_path, file_name = os.path.split(name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(name, "w") as outfile:
        json.dump(info, outfile, indent=4)
    return combinations


rels, combinations = analysis()
rels.show()
if combinations:
    print(combinations)
else:
    print("infinite")

# print("*********** FINAL CODE ****************")
# if DEBUG>=3:
#     ast.show()
# generator = c_generator.CGenerator()
# print(generator.visit(ast))
