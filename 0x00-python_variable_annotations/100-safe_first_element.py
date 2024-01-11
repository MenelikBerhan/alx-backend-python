#!/usr/bin/env python3
"""Contains a type-annotated function """
from typing import Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """takes a sequence and if its length is greater than
    zero returns the first element, else returns None."""
    if lst:
        return lst[0]
    else:
        return None
