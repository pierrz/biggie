from test.base_test import DataframeTestBase, TestReader
from test.fixtures.tasks import dummy_task, spark_test

from pandas.testing import assert_frame_equal
from src.db.mongo import db

test_mongo_collection = "test_spark_celery"


def test_live_celery():
    task = dummy_task.delay(3)  # formula is input * input
    result = task.get()
    assert result == 9


class SparkCeleryTestReader(TestReader):
    collection = test_mongo_collection


class SparkCeleryTest(DataframeTestBase):
    def run(self):
        db.drop_collection(self.fixture.collection)
        task = spark_test.delay(self.fixture.test_data)

        while task.successful():
            test_df = self.data.spark_df
            test_df.show()

            mongo_data = SparkCeleryTestReader().db_data
            result_df = mongo_data.drop("_id")  # discard mongo id
            result_df.show()

            assert_frame_equal(result_df.toPandas(), test_df.toPandas())
            assert result_df.schema == test_df.schema


def test_spark_celery():
    spark_celery_test = SparkCeleryTest(test_mongo_collection)
    db.drop_collection(spark_celery_test.fixture.collection)
