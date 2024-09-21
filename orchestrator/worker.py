"""
Module spinning up the Celery worker
"""

# from src import logger
import logging

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
from config import celery_config
from src.commons.logging import InterceptHandler, LoggerManager

logger = LoggerManager(log_filepath="/opt/orchestrator/logs/worker.log").get_logger()


# Intercept Celery-specific logs
celery_logger = logging.getLogger("celery")
celery_logger.setLevel(logging.INFO)
celery_logger.addHandler(InterceptHandler())

celery = Celery(__name__)
celery.config_from_object(celery_config)
celery.autodiscover_tasks(force=True)


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    """
    No need to modify the logger since we're intercepting all logs via Loguru.
    """
    pass


@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    """
    Same here, Loguru takes care of the task-specific logging.
    """
    pass
