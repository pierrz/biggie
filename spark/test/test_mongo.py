"""
Tests focused on Mongo based features
"""
from base_test import DataframeTestBase, TestReader
from pandas.testing import assert_frame_equal
from src.db.mongo import db  # pylint: disable=E0611

mongo_collection_name = "test_mongo_loader_reader"


class MongoTestReader(TestReader):
    """
    Test class specific to the given collection
    """

    collection = mongo_collection_name


class MongoLoaderReaderTest(DataframeTestBase):
    """
    Test focused on the features of the MongoLoader class
    """

    def run(self):
        db.drop_collection(self.fixture.collection)
        test_df = self.data.spark_df
        self.data.load_mongo()

        mongo_data = MongoTestReader().db_data
        mongo_df = mongo_data.drop("_id")  # discard mong id

        assert_frame_equal(mongo_df.toPandas(), test_df.toPandas())
        assert mongo_df.schema == test_df.schema


def test_mongo_loader_reader():
    """
    Starts the test
    :return: does its thing
    """
    mongo_test = MongoLoaderReaderTest(mongo_collection_name)
    db.drop_collection(mongo_test.fixture.collection)
