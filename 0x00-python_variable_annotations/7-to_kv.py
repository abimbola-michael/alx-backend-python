#!/usr/bin/env python3
"""Type-annotated function to_kv"""


def to_kv(k: str, v: [int | float]) -> tuple[str, float]:
    """a type-annotated function to_kv that takes
    a string k and an int OR float v as arguments
    and returns a tuple"""
    return (k, float(v ** 2))