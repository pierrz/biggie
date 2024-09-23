"""
Logging module based on common logger
"""

# import logging

from src.commons.logging import LoggerManager  # , InterceptHandler

logger = LoggerManager(log_filepath="/opt/orchestrator/logs/worker.log").get_logger()

# class CeleryInterceptHandler(InterceptHandlerBase):
#     logger_object = logger

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


# def tune_logger(logger_to_intercept: str):
#     # # Redirect all logging (including Celery) to Loguru
#     # logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

#     # Intercept Celery-specific logs
#     intercepted_logger = logging.getLogger(logger_to_intercept)
#     # intercepted_logger.setLevel(logging.INFO)
#     intercepted_logger.addHandler(InterceptHandler())

#     return intercepted_logger
