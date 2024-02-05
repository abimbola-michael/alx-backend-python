#!/usr/bin/env python3
"""
 Parameterize and patch as decorators
"""


import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """
    a class that implements the test_org method.
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org: str, expected: dict, mock_get_json: MagicMock):
        """
        test the org method
        """

        mock_get_json.return_value = MagicMock(return_value=expected)
        test = GithubOrgClient(org)
        self.assertEqual(test.org(), expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self):
        """
        test the _public_repos_url method
        """
        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            payload = {
                "repos_url": "https://api.github.com/users/google/repos"
            }
            mock_org.return_value = payload

            test = GithubOrgClient('google')
            self.assertEqual(
                test._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock):
        """
        test the public_repos method
        """

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_get_json.return_value = [
                {"name": "google"},
                {"name": "abc"},
            ]
            repos_link = "https://api.github.com/orgs/google/repos"
            mock_public_repos_url.return_value = repos_link
            test = GithubOrgClient('google')
            self.assertEqual(
                test.public_repos(),
                ["google", "abc"]
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        test the has_license method
        """
        client = GithubOrgClient('google')
        has = client.has_license(repo, license_key)
        self.assertEqual(has, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    a class and implement the setUpClass and tearDownClass
    which are part of the unittest.TestCase API.
    """

    @classmethod
    def setUpClass(cls):
        """
        a class method that implements the setUpClass method
        """

        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def get_payload(url):
            """
            a method tht returns payload"""
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch('requests.get', side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """
        test the public_repos method
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(), self.expected_repos
        )

    def test_public_repos_with_license(self) -> None:
        """
        test the public_repos method with license
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls):
        """
        a class method that implements the tearDownClass method
        """
        cls.get_patcher.stop()
