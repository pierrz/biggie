"""
Test that Celery can handle task which rely on Spark jobs.
"""

from src import logger
from src.tasks.dummy_spark_task import dummy_spark_task


def test_spark_job():
    """
    Just to check that Celery is up and running.
    """

    logger.info("Initiating dummy Spark task test ...")
    task = dummy_spark_task.s()
    result = task()
    assert len(result) == 3
    logger.successful("Dummy Spark task test successful.")


# import unittest
# from unittest.mock import patch
# from src.sparky.jobs import ToMongoFromJson

# class TestToMongoFromJson(unittest.TestCase):

#     @patch('src.sparky.jobs.ToMongoFromJson.write_to_mongo')
#     def test_to_mongo_from_json(self, mock_write_to_mongo):
#         # Use the existing Spark session fixture
#         spark = self.spark

#         # Sample JSON data
#         json_data = [
#             {"name": "Alice", "age": 30},
#             {"name": "Bob", "age": 25}
#         ]

#         # Create DataFrame from JSON data
#         df = spark.read.json(spark.sparkContext.parallelize(json_data))

#         # Run the job
#         job = ToMongoFromJson()
#         job.run(df)

#         # Verify that write_to_mongo was called with the correct DataFrame
#         mock_write_to_mongo.assert_called_once()
#         args, kwargs = mock_write_to_mongo.call_args
#         result_df = args[0]

#         # Check if the DataFrame content is as expected
#         self.assertEqual(result_df.collect(), df.collect())

# if __name__ == '__main__':
#     unittest.main()
