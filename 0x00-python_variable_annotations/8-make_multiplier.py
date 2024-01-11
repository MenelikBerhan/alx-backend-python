#!/usr/bin/env python3
"""Contains a type-annotated function """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """takes a float multiplier as argument and returns a
    function that multiplies a float by multiplier."""
    def square(num: float): return 1.0 * num * multiplier
    return square
