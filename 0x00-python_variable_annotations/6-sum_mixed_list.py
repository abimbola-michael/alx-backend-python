#!/usr/bin/env python3
"""Type-annotated function sum_mixed_list"""


def sum_mixed_list(mxd_lst: list[int | float]) -> float:
    """a type-annotated function sum_mixed_list
    which takes a list mxd_lst of integers
    and floats and returns their sum as a float"""
    return float(sum(mxd_lst))
