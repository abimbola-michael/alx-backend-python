#!/usr/bin/env python3
"""
 Parameterize a unit test
"""


import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """
    a class that implement the TestAccessNestedMap.test_access_nested_map
    method to test that the method returns what it is supposed to.
    Decorate the method with @parameterized.expand to test the
    function for following inputs:
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        test the access_nested_map method
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
