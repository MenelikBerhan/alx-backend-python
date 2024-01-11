#!/usr/bin/env python3
"""Contains a type-annotated function """
from typing import Any, Mapping, TypeVar, Union


K = TypeVar('K')    # type of keys
V = TypeVar('V')    # type of values
def safely_get_value(
        dct: Mapping[K, V], key: K, default: Any = None
        ) -> Union[V, Any]:
    """If key is in dct returns its corresponding value,
    else returns default."""
    if key in dct:
        return dct[key]
    else:
        return default
