"""
Module gathering the base classes used for testing purpose
"""

from abc import ABC, abstractmethod
from test.sparky.fixtures.dataframe_fixture import DataframeFixture

from pyspark.sql import functions as psf  # pylint: disable=E0611
from src.sparky.dataframe_maker import MongoDataframeMaker, PostgresDataframeMaker
from src.sparky.mongo_connectors import MongoReader
from src.sparky.postgres_connectors import PostgresReader


class DataframeTestBase(ABC):
    """
    Class used to prepare fixtures for dataframe related tests
    """

    fixture: DataframeFixture
    check_columns = ["a", "d_date"]

    def __init__(self, table_or_collection):
        """
        Initialises the fixture based on a specific MongoDB collection name
        :param collection: MongoDB collection name
        """
        self.fixture = DataframeFixture(table_or_collection)

    @abstractmethod
    def run(self, **kwargs):
        """
        Will run the test
        :return: does its thing
        """


class PostgresDFTest(DataframeTestBase):
    """
    Class used for Postgres test dfs
    """

    def __init__(self, table):
        super().__init__(table)
        self.data = PostgresDataframeMaker(
            self.fixture.test_data,
            self.fixture.table_or_collection,
            check_columns=self.check_columns,
        )
        self.run()


class MongoDFTest(DataframeTestBase):
    """
    Class used for Postgres test dfs
    """

    def __init__(self, collection, schema):
        super().__init__(collection)
        self.data = MongoDataframeMaker(
            self.fixture.test_data,
            self.fixture.table_or_collection,
            check_columns=self.check_columns,
            schema=schema,
        )
        self.run()


# TODO: fix for MongoTestReader and TestBase
#  PytestCollectionWarning: cannot collect test class 'MongoTestReader' because it has a __init__ constructor
#  (from: test/base_test.py test/test_celery.py test/test_mongo.py)
class TestReader:

    check_columns = [
        psf.col("a"),
        psf.col("d_date"),
    ]


class MongoTestReader(MongoReader, TestReader):
    """
    Class used to prepare Spark/Mongo connectors for a given collection,
    along with specific columns to check the data with.
    """

    collection = "test_mongo_loader_reader"


class PostgresTestReader(PostgresReader, TestReader):

    table = "test_postgres_loader_reader"
