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
