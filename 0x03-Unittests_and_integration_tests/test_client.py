#!/usr/bin/env python3
"""Tests for `GithubOrgClient` class in `client` module.
"""
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch, Mock, PropertyMock
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

        # `org` method returns `get_json(org_url)`
        self.assertEqual(client_obj.org, payload)

        org_url = "https://api.github.com/orgs/{}".format(org_name)
        mocked_get_json.assert_called_once_with(org_url)

    def test_public_repos_url(self):
        """Tests the property method `_public_repos_url`."""
        target = 'test_client.GithubOrgClient.org'
        # `PropertyMock` to mock a property (`org`)
        with patch(target, new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://test.com"}
            client_obj = GithubOrgClient('test')

            # `_public_repos_url` returns `org["repos_url"]`
            self.assertEqual(client_obj._public_repos_url, "https://test.com")
            mock_org.assert_called_once_with()
