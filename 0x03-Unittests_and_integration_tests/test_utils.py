#!/usr/bin/env python3
"""Parameterized unittests.
"""
from utils import access_nested_map, get_json
from parameterized import parameterized, parameterized_class
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
