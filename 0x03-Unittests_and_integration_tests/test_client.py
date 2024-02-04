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

    @patch('client.get_json')
    def test_public_repos(self, mocked_get_json: Mock):
        """Tests the `public_repos` method."""
        # `public_repos` calls `repos_paylod()` which in turn
        # returns `get_json(_public_repos_url)`
        test_payload = [
            {'name': 'a', 'license': {'key': '1'}},
            {'name': 'b', 'license': {'key': '2'}},
            {'name': 'c', 'license': {'key': '1'}},
        ]
        target = 'test_client.GithubOrgClient._public_repos_url'
        # `PropertyMock` to mock a property (`_public_repos_url`)
        with patch(target, new_callable=PropertyMock) as mock_public_repos_url:
            # set return value for mocked methods
            mocked_get_json.return_value = test_payload
            mock_public_repos_url.return_value = "https://test.com"

            # check returns from `public_repos`
            client_obj = GithubOrgClient('test')
            self.assertEqual(client_obj.public_repos(), ['a', 'b', 'c'])
            self.assertEqual(client_obj.public_repos('1'), ['a', 'c'])
            self.assertEqual(client_obj.public_repos('2'), ['b'])
            self.assertEqual(client_obj.public_repos('3'), [])

            # since `repos_paylod` is memoized, get_json(_public_repos_url) is
            # called only once. For the rest, returned from memory.
            mock_public_repos_url.assert_called_once_with()
            mocked_get_json.assert_called_once_with("https://test.com")
