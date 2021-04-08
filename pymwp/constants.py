from enum import IntEnum


def is_debug():
    # TODO: make this return env variable
    return 0


class Comparison(IntEnum):
    """represent result of delta comparison"""
    SMALLER = 0
    EQUAL = 1
    LARGER = 2


DEBUG = is_debug()
