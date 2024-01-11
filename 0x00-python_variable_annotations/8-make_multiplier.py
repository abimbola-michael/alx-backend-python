#!/usr/bin/env python3
"""Type-annotated function make_multiplier"""


def make_multiplier(multiplier: float) -> callable[[float], float]:
    """a type-annotated function make_multiplier
    that takes a float multiplier as argument and
    returns a function that multiplies a float
    by multiplier"""

    def multiply(m: float) -> float:
        """a type-annotated function multiply that
        multiplies a float m by multiplier"""
        return m * multiplier
    return multiply