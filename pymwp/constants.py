from enum import IntEnum


class Comparison(IntEnum):
    """Represent result of delta comparison."""
    SMALLER = 0
    EQUAL = 1
    LARGER = 2
