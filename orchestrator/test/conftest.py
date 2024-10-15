"""
conftest file for the Harvester package
"""

from pathlib import Path
from typing import Dict

import pytest
from config import data_directories


@pytest.fixture(scope="module")
def dog_sample_urls():
    return {
        "test": "https://dog.ceo/api/breeds/image/random",
        "result-url-prefix": "https://images.dog.ceo/breeds",
    }


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

    test_data = {
        "id": None,
        "name": "test-",
        "data": ["some", "sample", "values"],
    }

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
    data = JsonSample(id_sample)
    return data.dict()


@pytest.fixture(scope="module")
def test_dir():
    return Path(data_directories.data_dir_root, "test")


@pytest.fixture(scope="module")
def json_array_dict(ids_array):
    return [JsonSample(sample_id).dict() for sample_id in ids_array]
