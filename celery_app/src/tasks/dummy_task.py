"""
Test related Celery tasks
"""

import numpy as np
from worker import celery, logger


@celery.task(name="dummy_task")
def dummy_task(input_int: int) -> int:
    """
    Dummy numpy task
    :param input_int: input number
    :return: computed result
    """
    result = int(np.multiply(input_int, input_int))
    logger.info("=> Calculated: %s", result)

    return result
