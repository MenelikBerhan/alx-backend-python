#!/usr/bin/env python3
"""Tests for `GithubOrgClient` class in `client` module.
"""
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch, Mock
import unittest


class TestGithubOrgClient(unittest.TestCase):
    """Unit test class for testing `GithubOrgClient` class.
    """
    @parameterized.expand([
        ('google', {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ('abc', {"repos_url": "https://api.github.com/orgs/abc/repos"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, payload: str, mocked_get_json: Mock):
        """Tests the `org` method's return."""
        mocked_get_json.return_value = payload
        client_obj = GithubOrgClient(org_name)
        self.assertEqual(client_obj.org, payload)
        org_url = "https://api.github.com/orgs/{}".format(org_name)
        mocked_get_json.assert_called_once_with(org_url)
