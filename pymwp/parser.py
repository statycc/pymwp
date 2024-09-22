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

from __future__ import annotations
import os
import re
import tempfile
from abc import ABC, abstractmethod
from logging import getLogger
# noinspection PyPackageRequirements,PyProtectedMember
from typing import Any, List, Type, Union

# noinspection PyProtectedMember
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
class Nodes(ABC):  # pragma: no cover
    @property
    @abstractmethod
    def ArrayDecl(self):
        pass

    @property
    @abstractmethod
    def ArrayRef(self):
        pass

    @property
    @abstractmethod
    def Assignment(self):
        pass

    @property
    @abstractmethod
    def BinaryOp(self):
        pass

    @property
    @abstractmethod
    def Break(self):
        pass

    @property
    @abstractmethod
    def Case(self):
        pass

    @property
    @abstractmethod
    def Cast(self):
        pass

    @property
    @abstractmethod
    def Compound(self):
        pass

    @property
    @abstractmethod
    def Constant(self):
        pass

    @property
    @abstractmethod
    def Continue(self):
        pass

    @property
    @abstractmethod
    def Decl(self):
        pass

    @property
    @abstractmethod
    def DeclList(self):
        pass

    @property
    @abstractmethod
    def Default(self):
        pass

    @property
    @abstractmethod
    def DoWhile(self):
        pass

    @property
    @abstractmethod
    def EmptyStatement(self):
        pass

    @property
    @abstractmethod
    def ExprList(self):
        pass

    @property
    @abstractmethod
    def For(self):
        pass

    @property
    @abstractmethod
    def FuncCall(self):
        pass

    @property
    @abstractmethod
    def FuncDef(self):
        pass

    @property
    @abstractmethod
    def ID(self):
        pass

    @property
    @abstractmethod
    def If(self):
        pass

    @property
    @abstractmethod
    def ParamList(self):
        pass

    @property
    @abstractmethod
    def Return(self):
        pass

    @property
    @abstractmethod
    def Switch(self):
        pass

    @property
    @abstractmethod
    def TernaryOp(self):
        pass

    @property
    @abstractmethod
    def TypeDecl(self):
        pass

    @property
    @abstractmethod
    def UnaryOp(self):
        pass

    @property
    @abstractmethod
    def While(self):
        pass


# noinspection PyPep8Naming
class NodeHandler(ABC):  # pragma: no cover

    def ArrayDecl(self, node: Nodes.ArrayDecl, *args, **kwargs):
        pass

    def ArrayRef(self, node: Nodes.ArrayRef, *args, **kwargs):
        pass

    def Assignment(self, node: Nodes.Assignment, *args, **kwargs):
        pass

    def BinaryOp(self, node: Nodes.BinaryOp, *args, **kwargs):
        pass

    def Break(self, node: Nodes.Break, *args, **kwargs):
        pass

    def Case(self, node: Nodes.Case, *args, **kwargs):
        pass

    def Cast(self, node: Nodes.Cast, *args, **kwargs):
        pass

    def Compound(self, node: Nodes.Compound, *args, **kwargs):
        pass

    def Constant(self, node: Nodes.Constant, *args, **kwargs):
        pass

    def Continue(self, node: Nodes.Continue, *args, **kwargs):
        pass

    def Decl(self, node: Nodes.Decl, *args, **kwargs):
        pass

    def DeclList(self, node: Nodes.DeclList, *args, **kwargs):
        pass

    def Default(self, node: Nodes.Default, *args, **kwargs):
        pass

    def DoWhile(self, node: Nodes.DoWhile, *args, **kwargs):
        pass

    def EmptyStatement(self, node: Nodes.EmptyStatement, *args, **kwargs):
        pass

    def ExprList(self, node: Nodes.ExprList, *args, **kwargs):
        pass

    def For(self, node: Nodes.For, *args, **kwargs):
        pass

    def FuncCall(self, node: Nodes.FuncCall, *args, **kwargs):
        pass

    def FuncDef(self, node: Nodes.FuncDef, *args, **kwargs):
        pass

    def ID(self, node: Nodes.ID, *args, **kwargs):
        pass

    def If(self, node: Nodes.If, *args, **kwargs):
        pass

    def ParamList(self, node: Nodes.ParamList, *args, **kwargs):
        pass

    def Return(self, node: Nodes.Return, *args, **kwargs):
        pass

    def Switch(self, node: Nodes.Switch, *args, **kwargs):
        pass

    def TernaryOp(self, node: Nodes.TernaryOp, *args, **kwargs):
        pass

    def TypeDecl(self, node: Nodes.TypeDecl, *args, **kwargs):
        pass

    def UnaryOp(self, node: Nodes.UnaryOp, *args, **kwargs):
        pass

    def While(self, node: Nodes.While, *args, **kwargs):
        pass


# noinspection PyPep8Naming
class ParserInterface(Nodes):  # pragma: no cover
    """Interface for C code parser."""

    @staticmethod
    @abstractmethod
    def parse(full_file_name: str, **kwargs) -> dict:
        """Extract text from the currently loaded file."""
        pass

    @abstractmethod
    def is_func(self, node: Any) -> bool:
        """True if node is a function implementation."""
        pass

    @abstractmethod
    def is_loop(self, node: Any) -> bool:
        """True is node is a loop statement."""
        pass

    @abstractmethod
    def to_c(self, node: Any) -> str:
        """Translate node back to C code."""
        pass

    @property
    @abstractmethod
    def Node(self) -> Type:
        """Base type for all AST nodes."""
        pass

    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def LoopT(self) -> Type:
        """Loop type."""
        pass


class PyCParser(ParserInterface):
    """Implementation of the parser interface using pycparser."""

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

    def is_func(self, node: ParserInterface.Node) -> bool:
        """True if node is a (non-empty) function implementation."""
        return (isinstance(node, self.FuncDef) and
                hasattr(node, 'body') and
                hasattr(node.body, 'block_items'))

    def is_loop(self, node: ParserInterface.Node) -> bool:
        """True is node is a (non-empty) loop statement."""
        return (isinstance(node, (self.While, self.For, self.DoWhile))
                and hasattr(node, 'stmt') and node.stmt
                and not isinstance(node.stmt, self.EmptyStatement))

    def to_c(self, node: Any, compact: bool = False) -> str:
        """Translate node back to C code."""
        generator = c_generator.CGenerator()
        comm = generator.visit(node)
        if compact:
            comm = re.sub(r"[\n\t\s]+", " ", comm).strip()
        return comm.strip()

    @property
    def Node(self) -> Type:
        """Base type for all AST nodes."""
        return Type[c_ast.Node]

    # noinspection PyPep8Naming
    @property
    def LoopT(self) -> Type:
        """Loop type."""
        return Type[Union[Parser.While, Parser.DoWhile, Parser.For]]

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
