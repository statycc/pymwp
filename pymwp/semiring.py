# -*- coding: UTF-8 -*-

ZERO_MWP = "o"

UNIT_MWP = "m"

# Different flow values
KEYS = ["o", "m", "w", "p", "i"]

#  Define product over Keys : o•o=o; o•m=o; o•w=o; etc…
DICT_PROD = {
    "o": {"o": "o", "m": "o", "w": "o", "p": "o", "i": "o"},

    "m": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "o", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "o", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "o", "m": "i", "w": "i", "p": "i", "i": "i"}
}

#  Define sum over Keys : o+o=o; o+m=m; o+w=w; etc…
DICT_SUM = {
    "o": {"o": "o", "m": "m", "w": "w", "p": "p", "i": "i"},

    "m": {"o": "m", "m": "m", "w": "w", "p": "p", "i": "i"},

    "w": {"o": "w", "m": "w", "w": "w", "p": "p", "i": "i"},

    "p": {"o": "p", "m": "p", "w": "p", "p": "p", "i": "i"},

    "i": {"o": "i", "m": "i", "w": "i", "p": "i", "i": "i"}
}


def prod_mwp(a, b):
    """Compute product of two scalars

    Arguments:
        a: scalar
        b: scalar

    Returns:
        product of a•b or raises an error if a or b ∉ Keys
    """
    if a in KEYS and b in KEYS:
        return DICT_PROD[a][b]
    else:
        raise Exception("trying to use", a, "and", b, "as keys for DICT_PROD…")


# Return sum a+b or an error if a or b ∉ Keys
def sum_mwp(a, b):
    """Compute sum of two scalars

    Arguments:
        a: scalar
        b: scalar

    Returns:
        sum of a+b or raises an error if a or b ∉ Keys
    """
    if a in KEYS and b in KEYS:
        return DICT_SUM[a][b]
    else:
        raise Exception("trying to use", a, "and", b, "as keys for DICT_SUM…")
