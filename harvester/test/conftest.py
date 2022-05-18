"""
conftest file for the Harvester package
"""

from typing import Dict

import pytest


@pytest.fixture(scope="module")
def dog_sample_url():
    return "https://gateway.marvel.com:443/v1/public/creators?firstName=stan&lastName=lee&"


@pytest.fixture(scope="module")
def stan_lee_baseurl():
    return "https://gateway.marvel.com:443/v1/public/creators?firstName=stan&lastName=lee&"


@pytest.fixture(scope="module")
def id_sample():
    return 11


@pytest.fixture(scope="module")
def ids_array():
    return [11, 12, 13]


class JsonSample:
    """
    Data fixture
    """

    test_data = {"id": None, "name": "test-", "data": ["some", "sample", "values"]}

    def __init__(self, row_id: int):
        self.test_data["id"] = row_id
        self.test_data["name"] += f"{row_id}"

    def dict(self) -> Dict:
        """
        Exports the class data as a dictionary
        :return: a dictionary
        """
        return self.test_data


@pytest.fixture(scope="module")
def json_sample_dict(id_sample):
    return JsonSample(id_sample).dict()


@pytest.fixture(scope="module")
def json_array_dict(ids_array):
    return [JsonSample(sample_id).dict() for sample_id in ids_array]
