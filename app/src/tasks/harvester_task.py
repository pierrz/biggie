"""
Harvester task
"""

from src.harvester import run
from worker import celery, logger


@celery.task(name="harvester_task")
def harvester_task():
    result_flag = run()
    logger.info(f"-- RESULT --> {result_flag}")
    return result_flag
