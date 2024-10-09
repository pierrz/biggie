"""
Test related Celery tasks
"""

from typing import Dict, List

from src import logger
from src.spark_jobs.commons.session import session_check
from worker import celery


@celery.task(name="dummy_spark_task")
def dummy_spark_task() -> List[Dict]:
    """
    Dummy numpy task
    :param input_int: input number
    :return: computed result
    """
    logger.info("Initiating dummy Spark task...")
    try:
        df = session_check()
    except Exception as e:
        logger.error(f"Issue with task: {e}")

    pandas_df = df.toPandas()
    logger.success("Spark dummy task successful.")
    return pandas_df.to_dict("records")
