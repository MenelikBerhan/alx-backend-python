#!/usr/bin/env python3
"""Contains a type-annotated function """
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """takes a list mxd_lst of integers and
    floats and returns their sum as a float."""
    return 0.0 + sum(mxd_lst)
