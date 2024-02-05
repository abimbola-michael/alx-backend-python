#!/usr/bin/env python3
"""
 Parameterize a unit test
"""


import unittest
from unittest.mock import patch, Mock
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

    @parameterized.expand([
        {{}, ("a",), KeyError},
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        test the access_nested_map exception
        """
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    a class that implement the TestGetJson.test_get_json method to test that
    the method returns the expected result.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        test the get_json method
        """
        with patch('requests.get') as mock_request:
            mock_request.return_value.json.return_value = test_payload
            self.assertEqual(get_json(test_url), test_payload)
            mock_request.assert_called_once()


class TestMemoize(unittest.TestCase):
    """
    a class that implement the TestMemoize.test_memoize method to test that
    the method returns the expected result.
    """

    def test_memoize(self):

        class TestClass:
            """
            a class to test the memoize method
            """

            def a_method(self):
                """
                a method to test the memoize method
                """
                return 42

            @memoize
            def a_property(self):
                """
                a property to test the memoize method
                """
                return self.a_method()

        test_class = TestClass()
        with (patch.object(test_class, "a_method")) as mock_method:
            first_result = test_class.a_property
            second_result = test_class.a_property
            self.assertEqual(first_result, 42)
            self.assertEqual(second_result, 42)
            mock_method.assert_called_once()
