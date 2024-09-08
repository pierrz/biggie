"""
Tests focused on Mongo based features
"""

from test.pyspark.base_test import MongoDFTest, MongoTestReader

from pandas.testing import assert_frame_equal
from pyspark.sql.types import StructField, StructType
from src.db.mongo_db import init_mongo_connection


# TODO: implement schema binding when reading data with Spark
def strip_metadata(schema):
    """Used to remove the "metada: {"inferred": true}" field
    from the Mongo retrieved data, as it is missing
    from the straight Spark Dataframe compared to the one loaded from Mongo)"""
    return StructType(
        [
            StructField(field.name, field.dataType, field.nullable)
            for field in schema.fields
        ]
    )


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
        assert strip_metadata(mongo_df.schema) == strip_metadata(test_df.schema)


def test_mongo_loader_reader():
    """
    Starts the test
    :return: does its thing
    """

    MongoLoaderReaderTest(MongoTestReader.collection)
    mongodb = init_mongo_connection()
    mongodb.drop_collection(MongoTestReader.collection)
