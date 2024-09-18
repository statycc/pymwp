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
__version__ = "0.4.2"

# flake8: noqa: F401
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
from pymwp.result import Result
from pymwp.analysis import Analysis, LoopAnalysis
