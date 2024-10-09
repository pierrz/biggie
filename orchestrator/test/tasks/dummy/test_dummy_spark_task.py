"""
Test that Celery can handle task which rely on Spark jobs.
"""

from src import logger
from src.tasks.dummy.dummy_spark_task import dummy_spark_task


def test_spark_job():
    """
    Just to check that Celery is up and running.
    """

    logger.info("Initiating dummy Spark task test ...")
    task = dummy_spark_task.s()
    result = task()
    assert len(result) == 3
    logger.success("Dummy Spark task test successful.")
    assert True
