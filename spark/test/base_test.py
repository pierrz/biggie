"""
Module gathering the base classes used for testing purpose
"""
from abc import ABC, abstractmethod

from fixtures.dataframe_fixture import DataframeFixture
from pyspark.sql import functions as psf
from src.mongo_connectors import DataframeMaker, MongoReader


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
        # self.data.close()
        self.start_test()

    @abstractmethod
    def start_test(self):
        """
        Will run the test
        :return: does its thing
        """


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
