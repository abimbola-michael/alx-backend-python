#!/usr/bin/env python3
"""Type-annotated function sum_list"""


def sum_list(input_list: list[float]) -> float:
    """a type-annotated function sum_list which
    takes a list input_list of floats as
    argument and returns their sum as a float."""
    return float(sum(input_list))
