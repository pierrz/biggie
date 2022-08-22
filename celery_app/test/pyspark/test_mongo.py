"""
Tests focused on Mongo based features
"""
from test.pyspark.base_test import MongoDFTest, MongoTestReader

from pandas.testing import assert_frame_equal
from src.db.mongo import init_mongo_connection


class MongoLoaderReaderTest(MongoDFTest):
    """
    Test focused on the features of the MongoLoader class
    """

    def run(self):
        test_df = self.data.spark_df
        self.data.load_mongo()

        mongo_data = MongoTestReader().db_data
        mongo_df = mongo_data.drop("_id")  # discard mongo id

        assert_frame_equal(mongo_df.toPandas(), test_df.toPandas())
        assert mongo_df.schema == test_df.schema


def test_mongo_loader_reader():
    """
    Starts the test
    :return: does its thing
    """

    MongoLoaderReaderTest(MongoTestReader.collection)
    mongodb = init_mongo_connection()
    mongodb.drop_collection(MongoTestReader.collection)
