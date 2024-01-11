#!/usr/bin/env python3
"""Contains a type-annotated function """
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Takes a sequence lst and returns a list of
    tuples with each element and its length"""
    return [(i, len(i)) for i in lst]
