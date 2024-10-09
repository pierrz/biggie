"""
Test related Celery tasks
"""

import numpy as np
from src import logger
from worker import celery


@celery.task(name="dummy_task")
def dummy_task(input_int: int) -> int:
    """
    Dummy numpy task
    :param input_int: input number
    :return: computed result
    """
    logger.info("Initiating dummy test task.")
    result = int(np.multiply(input_int, input_int))
    logger.success(f"=> Calculated: {result}")

    return result
