# -*- coding: utf-8 -*-

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

"""
pymwp: implementation of MWP analysis on C code in Python.
"""

__title__ = "pymwp"
__author__ = "Clément Aubert, Thomas Rubiano, Neea Rusch, Thomas Seiller"
__license__ = "GPL-3.0-or-later"

__notice__ = (
    f"{__title__} Copyright (c) 2020-2024 {__author__}. This program comes "
    f"with ABSOLUTELY NO WARRANTY; for details type `{__title__} --license W`."
    f"This is free software, and you are welcome to redistribute it under "
    f"certain conditions; type `{__title__} --license C` for details.")

__warranty__ = (
    f"{__title__} is distributed in the hope that it will be useful, but "
    f"WITHOUT ANY WARRANTY; without even the implied warranty of "
    f"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU "
    f"General Public License for more details "
    f"https://www.gnu.org/licenses/gpl-3.0.html.")

__conditions__ = (
    "Permissions of this strong copyleft license are conditioned on making "
    "available complete source code of licensed works and modifications, "
    "which include larger works using a licensed work, under the same "
    "license. Copyright and license notices must be preserved. Contributors "
    f"provide an express grant of patent rights. See the GNU General Public "
    f"License for more details https://www.gnu.org/licenses/gpl-3.0.html.")

# flake8: noqa: F401,E402
from pymwp.version import __version__
from pymwp.constants import *  # import all types
from pymwp.parser import Parser
from pymwp.choice import Choices
from pymwp.syntax import Coverage, Variables, FindLoops
from pymwp.monomial import Monomial
from pymwp.delta_graphs import DeltaGraph
from pymwp.polynomial import Polynomial
from pymwp.relation import Relation
from pymwp.relation_list import RelationList
from pymwp.bound import Bound, MwpBound
from pymwp.result import Result, FuncResult, FuncLoops, LoopResult, VResult
from pymwp.analysis import Analysis, LoopAnalysis
