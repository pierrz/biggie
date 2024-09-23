"""
Module spinning up the Celery worker
"""

from celery import Celery
from config import celery_config

celery = Celery(__name__)
celery.config_from_object(celery_config)
celery.autodiscover_tasks(force=True)


# TODO: include ALL messages into loguru i.e. from INFO/MainProcess and INFO/ForkPoolWorker-4
# -> below is draft/WIP

# import logging
# from src import logger
# from celery.signals import setup_logging

# class InterceptHandler(logging.Handler):
#     """
#     Custom InterceptHandler to redirect Celery logs to Loguru.
#     WIP: not used at the moment, as current attempts to implement result in removing all other messages
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
#             "success": "SUCCESS",
#         }
#         loguru_level = level_map.get(loguru_level, "INFO")  # default to INFO if unknown
#         logger.opt(depth=6, exception=record.exc_info).log(
#             loguru_level, record.getMessage()
#         )

# @setup_logging.connect
# def setup_celery_logging(**kwargs):
#     """
#     Ensure Celery logs are redirected to Loguru.
#     """
#     root_logger = logging.getLogger()
#     task_logger = logging.getLogger('celery.task')

#     if not any(isinstance(h, InterceptHandler) for h in root_logger.handlers):
#         root_logger.addHandler(InterceptHandler())

#     if not any(isinstance(h, InterceptHandler) for h in task_logger.handlers):
#         task_logger.addHandler(InterceptHandler())
