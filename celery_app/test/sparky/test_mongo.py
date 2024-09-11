"""
Tests focused on Mongo based features

TODO: investigate why we need to use .simpleString() to get identical schemas
 though the field.metadata property are not present anymore
 as we are reading data based on a provided schema
"""

from test.sparky.base_test import MongoDFTest, MongoTestReader
from test.sparky.fixtures.mongo_schema import test_mongo_schema

from pandas.testing import assert_frame_equal
from src.db.mongo_db import init_pymongo_client

# DEPRECATED ...? (used when reading data without providing a schema)
# from pyspark.sql.types import StructField, StructType
# def strip_metadata(schema):
#     """Used to remove the "metada: {"inferred": true}" field
#     from the Mongo retrieved data, as it is missing
#     from the straight Spark Dataframe compared to the one loaded from Mongo)"""
#     return StructType(
#         [
#             StructField(field.name, field.dataType, field.nullable)
#             for field in schema.fields
#         ]
#     )


class MongoLoaderReaderTest(MongoDFTest):
    """
    Test focused on the features of the MongoLoader class
    """

    def run(self):
        """Test igniter, triggered by the base class"""
        test_df = self.data.spark_df
        self.data.load_mongo()

        mongo_data = MongoTestReader().db_data
        mongo_df = mongo_data.drop("_id")  # discard mongo id

        assert_frame_equal(mongo_df.toPandas(), test_df.toPandas())
        # assert strip_metadata(mongo_df.schema) == strip_metadata(test_df.schema)
        assert mongo_df.schema.simpleString() == test_df.schema.simpleString()


def test_mongo_loader_reader():
    """
    Starts the test
    :return: does its thing
    """

    MongoLoaderReaderTest(
        collection=MongoTestReader.collection, schema=test_mongo_schema
    )
    mongodb = init_pymongo_client()
    mongodb.drop_collection(MongoTestReader.collection)
