"""
Module spinning up the Celery worker
"""

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
from config import celery_config
from src import logger

celery = Celery(__name__)
celery.config_from_object(celery_config)
celery.autodiscover_tasks(force=True)


class InterceptHandler:
    """
    Custom InterceptHandler to redirect Celery logs to Loguru
    """

    def emit(self, record):
        """
        Convert Celery LogRecord to something Loguru can understand
        """
        loguru_level = record.levelname.lower()
        logger.opt(depth=2, exception=record.exc_info).log(
            loguru_level, record.getMessage()
        )


@after_setup_logger.connect
def setup_celery_logger(celery_logger, *args, **kwargs):
    """
    Setup Celery root logger
    """

    # Remove existing handlers to avoid duplicate logging
    for handler in list(celery_logger.handlers):
        celery_logger.removeHandler(handler)

    # Append Loguru intercept handler to Celery logger
    celery_logger.addHandler(InterceptHandler())


@after_setup_task_logger.connect
def setup_task_logger(task_logger, *args, **kwargs):
    """
    Setup task-specific logger
    """

    # Remove existing handlers to avoid duplicate logging
    for handler in list(task_logger.handlers):
        task_logger.removeHandler(handler)

    # Append Loguru intercept handler to task logger
    task_logger.addHandler(InterceptHandler())
