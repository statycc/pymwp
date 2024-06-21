# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

from enum import IntEnum


class Comparison(IntEnum):
    """Represent result of delta comparison."""
    SMALLER = 0
    EQUAL = 1
    LARGER = 2


class SetInclusion(IntEnum):
    """Represent result of monomial inclusion."""
    EMPTY = 0
    CONTAINS = 1
    INCLUDED = -1
