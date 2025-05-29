#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('utils.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Test GithubOrgClient.org returns correct value and calls get_json once."""
        test_payload = {"name": org_name, "id": 123}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")