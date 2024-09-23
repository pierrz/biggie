"""
Module spinning up the Celery worker
"""

# import logging

import celery

# from celery import Celery
# from celery.signals import setup_logging  # after_setup_logger, after_setup_task_logger,
from config import celery_config

# from src import logger  # as logger_instance, tune_logger
# from src.commons.logging import InterceptHandler  # LoggerManager

# import sys


# logger.addHandler(InterceptHandler())
# logger = LoggerManager(log_filepath="/opt/orchestrator/logs/worker.log").get_logger()
# from loguru import logger


# # Intercept Celery-specific logs
# logger = logging.getLogger("celery")
# logger.setLevel(logging.INFO)
# logger.addHandler(InterceptHandler())


celery = celery.Celery(__name__)
celery.config_from_object(celery_config)
celery.autodiscover_tasks(force=True)


# @setup_logging.connect
# # def setup_celery_logger(level, logfile, format, colorize, **kwargs):
# def setup_celery_logger(**kwargs):
#     """
#     Setup Celery logging to integrate with Loguru.
#     This will intercept Celery's logging and direct it to Loguru.
#     """

#     celery_logger = logging.getLogger("celery")
#     if celery_logger.handlers:
#         celery_logger.handlers.clear()
#         celery_logger.addHandler(InterceptHandler())

#     task_logger = logging.getLogger("celery.task")
#     if task_logger.handlers:
#         task_logger.handlers.clear()
#         task_logger.addHandler(InterceptHandler())

#     logger.info("--> Loguru logging setup ...?")
#     # Use our configured logger
#     return True

# This ensures Celery uses Loguru for logging
# pass  # No need for additional configuration since Loguru is already setup


# @celery.signals.setup_logging.connect
# def on_setup_logging(**kwargs):
#     pass


# @after_setup_logger.connect
# def setup_celery_logger(logger, *args, **kwargs):
#     """
#     No need to modify the logger since we're intercepting all logs via Loguru.
#     """
#     pass


# @after_setup_task_logger.connect
# def setup_task_logger(logger, *args, **kwargs):
#     """
#     Same here, Loguru takes care of the task-specific logging.
#     """
#     pass


# class InterceptHandler(logging.Handler):
#     """
#     Custom InterceptHandler to redirect Celery logs to Loguru
#     """

#     def emit(self, record):
#         """
#         Convert Celery LogRecord to something Loguru can understand
#         """
#         loguru_level = record.levelname.lower()
#         level_map = {
#             "debug": "DEBUG",
#             "info": "INFO",
#             "warning": "WARNING",
#             "error": "ERROR",
#             "critical": "CRITICAL",
#             "success": "SUCCESS"
#         }
#         loguru_level = level_map.get(loguru_level, "INFO")  # default to INFO if unknown
#         logger.opt(depth=2, exception=record.exc_info).log(
#             loguru_level, record.getMessage()
#         )


# @after_setup_logger.connect
# def setup_celery_logger(logger, *args, **kwargs):
#     """
#     Setup Celery root logger
#     """

#     # Remove existing handlers to avoid duplicate logging
#     for handler in list(logger.handlers):
#         logger.removeHandler(handler)

#     # Append Loguru intercept handler to Celery logger
#     logger.addHandler(InterceptHandler())


# @after_setup_task_logger.connect
# def setup_task_logger(logger, *args, **kwargs):
#     """
#     Setup task-specific logger
#     """

#     # Remove existing handlers to avoid duplicate logging
#     for handler in list(logger.handlers):
#         logger.removeHandler(handler)

#     # Append Loguru intercept handler to task logger
#     logger.addHandler(InterceptHandler())
