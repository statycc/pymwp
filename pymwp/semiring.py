# flake8: noqa: W605

ZERO_MWP: str = "o"
"""Constant that represents 0 in the analysis."""

UNIT_MWP: str = "m"
"""Constant that represents m in the analysis."""

KEYS: list = ["o", "m", "w", "p", "i"]
"""Different flow values: `o, m, w, p, i` where `o` = 0 and `i` = $\infty$."""

DICT_PROD: dict = {
    "o": {"o": "o", "m": "o", "w": "o", "p": "o", "i": "o"},

    "m": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "o", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "o", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "o", "m": "i", "w": "i", "p": "i", "i": "i"}
}
"""Define product over `KEYS` : o•o=o; o•m=o; o•w=o; etc…"""

DICT_SUM: dict = {
    "o": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "m": {"o": "m", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "w", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "p", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "i", "m": "i", "w": "i", "p": "i", "i": "i"}
}
"""Define sum over `KEYS` : o+o=o; o+m=m; o+w=w; etc…"""


def prod_mwp(a: str, b: str) -> str:
    """Compute product of two scalars

    Arguments:
        a: scalar value
        b: scalar value

    Raises:
          Exception: if `a` or `b` is not in [`KEYS`](semiring.md#pymwp.semiring.KEYS)

    Returns:
        product of a • b or raises an error if a or b ${\\not\\in}$ Keys
    """
    if a in KEYS and b in KEYS:
        return DICT_PROD[a][b]
    else:
        raise Exception("trying to use", a, "and", b, "as keys for DICT_PROD…")


# Return sum a+b or an error if a or b ∉ Keys
def sum_mwp(a: str, b: str) -> str:
    """Compute sum of two scalars

    Arguments:
        a: scalar value
        b: scalar value

    Raises:
          Exception: if `a` or `b` is not in [`KEYS`](semiring.md#pymwp.semiring.KEYS)

    Returns:
        sum of a + b or raises an error if a or b ${\\not\\in}$ Keys
    """
    if a in KEYS and b in KEYS:
        return DICT_SUM[a][b]
    else:
        raise Exception("trying to use", a, "and", b, "as keys for DICT_SUM…")
