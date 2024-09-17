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

import os
import re
import tempfile
from abc import ABC, abstractmethod
from logging import getLogger
# noinspection PyPackageRequirements,PyProtectedMember
from typing import Any, List

from pycparser import c_ast, parse_file, c_generator
from pycparser_fake_libc import directory as fake_libc_dir

logger = getLogger(__name__)

"""Interface the pycparser dependency.

Make all explicit references to pycparser within this module.
If some functionality is missing, extend this interface as necessary,
then test the used functionality in tests/test_parser.py.
Do not import pycparser directly elsewhere outside this module+test.

The motivation for using this interface is to make it easier to
test and replace this dependency with newer versions and ensuring it
such upgrades do not break pymwp.
"""


# noinspection PyPep8Naming
class ParserInterface(ABC):  # pragma: no cover
    """Interface for C code parser."""

    @staticmethod
    @abstractmethod
    def parse(full_file_name: str, **kwargs) -> dict:
        """Extract text from the currently loaded file."""
        pass

    def is_func(self, node: Any) -> bool:
        """True if node is a function implementation."""
        return False

    def is_loop(self, node: Any) -> bool:
        """True is node is a loop/repetition statement."""
        return False

    def to_c(self, node: Any) -> str:
        """Translate node back to C code."""
        return ""

    @property
    def ArrayDecl(self):
        return None

    @property
    def ArrayRef(self):
        return None

    @property
    def AST(self):
        return None

    @property
    def Assignment(self):
        return None

    @property
    def BinaryOp(self):
        return None

    @property
    def Break(self):
        return None

    @property
    def Case(self):
        return None

    @property
    def Cast(self):
        return None

    @property
    def Compound(self):
        return None

    @property
    def Constant(self):
        return None

    @property
    def Continue(self):
        return None

    @property
    def Decl(self):
        return None

    @property
    def DeclList(self):
        return None

    @property
    def Default(self):
        return None

    @property
    def DoWhile(self):
        return None

    @property
    def EmptyStatement(self):
        return None

    @property
    def ExprList(self):
        return None

    @property
    def For(self):
        return None

    @property
    def FuncCall(self):
        return None

    @property
    def FuncDef(self):
        return None

    @property
    def ID(self):
        return None

    @property
    def If(self):
        return None

    @property
    def Node(self):
        return None

    @property
    def NodeVisitor(self):
        return None

    @property
    def ParamList(self):
        return None

    @property
    def Return(self):
        return None

    @property
    def Switch(self):
        return None

    @property
    def TernaryOp(self):
        return None

    @property
    def TypeDecl(self):
        return None

    @property
    def UnaryOp(self):
        return None

    @property
    def While(self):
        return None


class PyCParser(ParserInterface):
    """Implementation of the parser interface, using pycparser."""

    @staticmethod
    def parse(file_name: str, headers: List[str] = None, **kwargs):

        # build parser cpp arguments
        # always append -E and fake_libc args when C preprocessor
        # is enabled
        if kwargs.get('use_cpp', False):
            args = kwargs.get('cpp_args', None)
            args = args.split(' ') if args else []
            if '-E' not in args:
                args.append(r'-E')
            args.append(r'-I' + fake_libc_dir)
            if headers:
                for h in headers:
                    args.append(r'-I' + h)
            kwargs['cpp_args'] = args
        logger.debug(f'parser arguments: {kwargs}')

        # if running windows there is no automated fix for you, boo hoo
        # add headers manually

        if os.name == 'nt':
            warning = 'automatic pre-parser processing was not ' \
                      'applied on Windows: manual fix may be needed'
            logger.warning(warning)
            # on Windows parse the original file as-is
            return parse_file(file_name, **kwargs)

        # read the original C program source
        with open(file_name, "r+") as cfile:
            c_prog = cfile.read()

        # apply preprocessing steps
        preprocessed = PyCParser.add_attr_x(c_prog)
        # convert to byte string
        prog_bytes = str.encode(preprocessed)

        # create temporary file copy where we apply custom preprocessing
        fp = tempfile.NamedTemporaryFile(suffix=".c")
        fp.write(prog_bytes)
        fp.seek(0)
        # pass the temporary file pointer to pycparser
        ast = parse_file(fp.name, **kwargs)
        fp.close()
        return ast

    def is_func(self, node: Any) -> bool:
        return isinstance(node, self.FuncDef) and \
               hasattr(node, 'body') and node.body.block_items

    def is_loop(self, node: Any) -> bool:
        return (isinstance(node, self.While) or
                isinstance(node, self.For) or
                isinstance(node, self.DoWhile))

    def to_c(self, node: Any, compact: bool = False) -> str:
        """Translate node back to C code."""
        generator = c_generator.CGenerator()
        comm = generator.visit(node)
        if compact:
            comm = re.sub(r"[\n\t\s]+", " ", comm).strip()
        return comm

    @staticmethod
    def add_attr_x(text: str) -> str:
        """Conditionally add `#define __attribute__(x)` to C file
        for pycparser.

        See: <https://github.com/eliben/pycparser/wiki/FAQ#what-do-i-do
        -about-__attribute__/>

        Arguments:
            text: C program file content as a string

        Returns:
            contents of C file, with `#define __attribute__(x)` included.
        """
        attr_x = '#define __attribute__(x)'
        lines = text.split('\n')
        not_found = not any([line.startswith(attr_x) for line in lines])
        if not_found:
            lines.insert(0, attr_x)
            text = '\n'.join(lines)
            logger.debug(f'inserted {attr_x}')
        return text

    @property
    def ArrayDecl(self):
        return c_ast.ArrayDecl

    @property
    def ArrayRef(self):
        return c_ast.ArrayRef

    @property
    def AST(self):
        return c_ast

    @property
    def Assignment(self):
        return c_ast.Assignment

    @property
    def BinaryOp(self):
        return c_ast.BinaryOp

    @property
    def Break(self):
        return c_ast.Break

    @property
    def Case(self):
        return c_ast.Case

    @property
    def Cast(self):
        return c_ast.Cast

    @property
    def Compound(self):
        return c_ast.Compound

    @property
    def Constant(self):
        return c_ast.Constant

    @property
    def Continue(self):
        return c_ast.Continue

    @property
    def Decl(self):
        return c_ast.Decl

    @property
    def DeclList(self):
        return c_ast.DeclList

    @property
    def Default(self):
        return c_ast.Default

    @property
    def DoWhile(self):
        return c_ast.DoWhile

    @property
    def ExprList(self):
        return c_ast.ExprList

    @property
    def EmptyStatement(self):
        return c_ast.EmptyStatement

    @property
    def For(self):
        return c_ast.For

    @property
    def FuncCall(self):
        return c_ast.FuncCall

    @property
    def FuncDef(self):
        return c_ast.FuncDef

    @property
    def ID(self):
        return c_ast.ID

    @property
    def If(self):
        return c_ast.If

    @property
    def Node(self):
        return c_ast.Node

    @property
    def NodeVisitor(self):
        return c_ast.NodeVisitor

    @property
    def ParamList(self):
        return c_ast.ParamList

    @property
    def Return(self):
        return c_ast.Return

    @property
    def Switch(self):
        return c_ast.Switch

    @property
    def TernaryOp(self):
        return c_ast.TernaryOp

    @property
    def TypeDecl(self):
        return c_ast.TypeDecl

    @property
    def UnaryOp(self):
        return c_ast.UnaryOp

    @property
    def While(self):
        return c_ast.While


# Parser is an instance of the preferred parser implementation
Parser = PyCParser()
