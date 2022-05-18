from base_test import DataframeTestBase, TestReader
from pandas.testing import assert_frame_equal
from src.db.mongo import db

test_mongo_collection = "test_mongo_loader"


class MongoTestReader(TestReader):
    collection = test_mongo_collection


class MongoLoaderTest(DataframeTestBase):
    def start_test(self):
        db.drop_collection(self.fixture.collection)
        test_df = self.data.spark_df
        self.data.load_mongo()

        mongo_data = MongoTestReader().db_data
        mongo_df = mongo_data.drop("_id")  # discard mong id

        assert_frame_equal(mongo_df.toPandas(), test_df.toPandas())
        assert mongo_df.schema == test_df.schema


def test_mongo_loader():
    mongo_test = MongoLoaderTest(test_mongo_collection)
    db.drop_collection(mongo_test.fixture.collection)
