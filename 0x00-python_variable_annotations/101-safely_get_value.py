#!/usr/bin/env python3
"""Contains a type-annotated function """
from typing import Any, Mapping, TypeVar, Union

K = TypeVar('K')    # type of dct keys
V = TypeVar('V')    # type of dct values
T = TypeVar('T')    # type of default


def safely_get_value(
        dct: Mapping, key: Any, default: Union[T, None] = None
        ) -> Union[Any, T]:
    """If key is in dct returns its corresponding value,
    else returns default."""
    if key in dct:
        return dct[key]
    else:
        return default


# def safely_get_value(
#         dct: Mapping[K, V], key: K, default: Any = None
#         ) -> Union[V, Any]:
#     """If key is in dct returns its corresponding value,
#     else returns default."""
#     if key in dct:
#         return dct[key]
#     else:
#         return default
