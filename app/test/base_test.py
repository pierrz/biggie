"""
Module gathering the base classes used for testing purpose
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pyspark.sql import functions as psf
from src.libs.test_lib import \
    get_expected_results_dict  # , get_expected_results_dict_for_specific_file
from src.spark.mongo_connectors import DataframeMaker, MongoReader

from .fixtures.dataframe_fixture import DataframeFixture


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
        url = f"http://api_test/api/{self.test_name}"
        print(f"TEST: {self.test_name}")
        print(f"=> url: {url}")
        expected_response = get_expected_results_dict(f"{self.test_name}")
        response = client.get(url)
        return response, expected_response

    def _check_endpoint(self, client):
        response, expected_response = self._get_test_parts(client)
        assert response.status_code == 200
        assert response.json() == expected_response


class DataframeTestBase(ABC):
    """
    Class used to prepare fixtures for dataframe related tests
    """

    fixture: DataframeFixture
    data: DataframeMaker

    def __init__(self, collection):
        """
        Initialises the fixture based on a specific MongoDB collection name
        :param collection: MongoDB collection name
        """
        self.fixture = DataframeFixture(collection)
        self.data = DataframeMaker(
            self.fixture.test_data,
            self.fixture.collection,
            check_columns=["a", "d_date"],
        )
        self.run()

    @abstractmethod
    def run(self):
        """
        Will run the test
        :return: does its thing
        """
        # pass


# TODO: fix for TestReader and TestBase
#  PytestCollectionWarning: cannot collect test class 'TestReader' because it has a __init__ constructor
#  (from: test/base_test.py test/test_celery.py test/test_mongo.py)
class TestReader(MongoReader):
    """
    Class used to prepare Spark/Mongo connectors for a given collection,
    along with specific columns to check the data with.
    """
    check_columns = [
        psf.col("a"),
        psf.col("d_date"),
    ]
