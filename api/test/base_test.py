"""
Module gathering the base classes used for testing purpose
"""
from abc import ABC
from dataclasses import dataclass
from test.lib_test import \
    get_expected_results_dict  # pylint: disable=E0611     # , get_expected_results_dict_for_specific_file


@dataclass
class EndpointTestBase(ABC):
    """
    Base test class to check whether all the endpoints are up and running
    """

    test_name: str

    def __init__(self, client, test_name: str):
        self.test_name = test_name
        self._check_endpoint(client)

    def _get_test_parts(self, client):
        url = f"http://api_test/{self.test_name}"
        print(f"TEST: {self.test_name}")
        print(f"=> url: {url}")
        expected_response = get_expected_results_dict(
            f"{self.test_name.replace('/', '_')}"
        )
        response = client.get(url)
        return response, expected_response

    def _check_endpoint(self, client):
        response, expected_response = self._get_test_parts(client)
        assert response.status_code == 200
        assert response.json() == expected_response
