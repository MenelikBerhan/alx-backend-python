#!/usr/bin/env python3
"""Tests for `GithubOrgClient` class in `client` module.
"""
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from typing import Dict
from unittest.mock import patch, Mock, PropertyMock
import unittest

org_payload, repos_payload, expected_repos, apache2_repos = TEST_PAYLOAD[0]


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict[str, Dict],
                         license_key: str, res: bool):
        """Tests the `has_license` method."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), res)


@parameterized_class([
    {'org_payload': org_payload,
     'repos_payload': repos_payload,
     'expected_repos': expected_repos,
     'apache2_repos': apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls):
        """Setups test by mocking `requests.get` using a patcher."""
        cls.get_patcher = patch('requests.get')
        # start mocking `requests.get`
        mocked_req_get = cls.get_patcher.start()

        def side_effect(url):
            """A function to be used as a side_effect for mock object.
            Returns a mock object that has a `json` method."""
            # to be used as a return value for `requests.get` mocker
            result = Mock()     # a mock object that has a `json` method

            # based on url set return value for `result`'s `json` method
            if url == "https://api.github.com/orgs/google":
                result.json.return_value = cls.org_payload
                # return result
            elif url == "https://api.github.com/orgs/google/repos":
                result.json.return_value = cls.repos_payload
                # return result
            else:
                result.json.return_value = {}
            return result

        # set side_effect function to `requests.get` mocker
        mocked_req_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stops the patcher used to mock `requests.get`."""
        # stop mocking `requests.get`
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Tests the `public_repos` method with out using license argument."""
        client_obj = GithubOrgClient('google')
        self.assertEqual(client_obj.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Tests the `public_repos` method using a license argument."""
        client_obj = GithubOrgClient('google')
        self.assertEqual(client_obj.public_repos('apache-2.0'),
                         self.apache2_repos)
