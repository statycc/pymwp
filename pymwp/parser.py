import os
import tempfile
from logging import getLogger

# noinspection PyPackageRequirements,PyProtectedMember
from typing import Any, List

from pycparser import c_ast, parse_file
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
class ParserInterface:  # pragma: no cover
    """Interface for C code parser."""

    @staticmethod
    def parse(full_file_name: str, **kwargs) -> dict:
        """Extract text from the currently loaded file."""
        pass

    def is_func(self, node: Any) -> bool:
        return False

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
    def DoWhile(self):
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
        preprocessed = PyCParser.__add_attr_x(c_prog)
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

    @staticmethod
    def __add_attr_x(text: str) -> str:
        """Conditionally add #define __attribute__(x) to C file
        for pycparser.

        See: <https://github.com/eliben/pycparser/wiki/FAQ#what-do-i-do
        -about-__attribute__/>

        Arguments:
            text: C program file content as a string

        Returns:
            contents of C file, with attribute(x) included.
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
    def DoWhile(self):
        return c_ast.DoWhile

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
    def UnaryOp(self):
        return c_ast.UnaryOp

    @property
    def While(self):
        return c_ast.While


# Parser is an instance of the preferred parser implementation
Parser = PyCParser()
