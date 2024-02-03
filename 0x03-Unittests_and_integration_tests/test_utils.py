#!/usr/bin/env python3
"""Parameterized unittests.
"""
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import patch, Mock
import unittest


class TestAccessNestedMap(unittest.TestCase):
    """Unit test class for utils module.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Tests `access_nested_map` method's expected return."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, err_msg):
        """Tests if `access_nested_map` raises exception for invalid input."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], err_msg)


class TestGetJson(unittest.TestCase):
    """Unit test class for utils module with mocked `request.get` method.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, url: str, payload: dict, mock_req_get: Mock):
        """Tests the method for correct return."""
        mock_req_get.return_value.json.return_value = payload
        # assert correct return
        self.assertEqual(get_json(url), payload)
        # assert get is called once with the right argument
        mock_req_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Unit test class for utils module.
    """
    def test_memoize(self):
        """Tests the `memoize` decorator."""
        class TestClass:
            """An example class to test the decorator."""
            def a_method(self):
                """A method called only once by a memoized method."""
                return 42

            @memoize
            def a_property(self):
                """A memoized method that calls `a_method` once for first
                run and returns from memory for subsequent calls."""
                return self.a_method()

        mocked_a_method = patch.object(TestClass, 'a_method').start()
        mocked_a_method.return_value = 42
        obj = TestClass()
        self.assertEqual(obj.a_property, 42)
        self.assertEqual(obj.a_property, 42)
        mocked_a_method.assert_called_once()
