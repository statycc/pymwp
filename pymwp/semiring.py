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

# flake8: noqa: W605

from typing import List

ZERO_MWP: str = "o"
"""Scalar that represents 0 in the analysis (`'o'`)."""

UNIT_MWP: str = "m"
"""Scalar that represents m in the analysis (`'m'`)."""

KEYS: List[str] = ["o", "m", "w", "p", "i"]
"""Different scalar values: `"o", "m", "w", "p", "i"` where `o` = 0 and `i` 
= $\\infty$."""

__DICT_PROD: dict = {
    "o": {"o": "o", "m": "o", "w": "o", "p": "o", "i": "i"},

    "m": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "o", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "o", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "i", "m": "i", "w": "i", "p": "i", "i": "i"}
}


def mwp_sort(scalars: List[str]):
    """Ascending sort of scalars (o < m < w < p < i)"""
    return sorted(scalars, key=lambda x: KEYS.index(x))


def prod_mwp(scalar1: str, scalar2: str) -> str:
    """Compute product of two scalars.

    | $\\times$  | $0$ | $m$       | $w$        | $p$       | $\\infty$ |
    | ---        | --- | ---       | ---        | ---       | --- |
    | $0$        | $0$ | $0$       | $0$        | $0$       | $\\infty$ |
    | $m$        | $0$ | $m$       | $w$        | $p$       | $\\infty$ |
    | $w$        | $0$ | $w$       | $w$        | $p$       | $\\infty$ |
    | $p$        | $0$ | $p$       | $p$        | $p$       | $\\infty$ |
    | $\\infty$  | $\\infty$ | $\\infty$ | $\\infty$  | $\\infty$ | $\\infty$ |

    Arguments:
        scalar1: scalar value
        scalar2: scalar value

    Raises:
          Exception: if `scalar1` or `scalar2` is not in KEYS

    Returns:
        product of scalar1 * scalar2
    """
    if scalar1 in KEYS and scalar2 in KEYS:
        return __DICT_PROD[scalar1][scalar2]
    else:
        raise Exception(
            f"trying to use {scalar1} and {scalar2} as keys for prod…")


__DICT_SUM: dict = {
    "o": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "m": {"o": "m", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "w", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "p", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "i", "m": "i", "w": "i", "p": "i", "i": "i"}
}


def sum_mwp(scalar1: str, scalar2: str) -> str:
    """Compute sum of two scalars.

    | $+$        | $0$       | $m$       | $w$        | $p$       | $\\infty$ |
    | ---        | ---       | ---       | ---        | ---       | --- |
    | $0$        | $0$       | $m$       | $w$        | $p$       | $\\infty$ |
    | $m$        | $m$       | $m$       | $w$        | $p$       | $\\infty$ |
    | $w$        | $w$       | $w$       | $w$        | $p$       | $\\infty$ |
    | $p$        | $p$       | $p$       | $p$        | $p$       | $\\infty$ |
    | $\\infty$  | $\\infty$ | $\\infty$ | $\\infty$  | $\\infty$ | $\\infty$ |

    Arguments:
        scalar1: scalar value
        scalar2: scalar value

    Raises:
          Exception: if `scalar1` or `scalar2` is not in KEYS

    Returns:
        sum of scalar1 + scalar2
    """
    if scalar1 in KEYS and scalar2 in KEYS:
        return __DICT_SUM[scalar1][scalar2]
    else:
        raise Exception(
            f"trying to use {scalar1} and {scalar2} as keys for sum…")
