"""
Logging module, re-usable between components.
"""

import logging
import sys

# alias to be sure to import the correct 'logger' object in the modules using logging
from loguru import logger as loguru_logger


class InterceptHandler(logging.Handler):
    """
    Custom InterceptHandler to redirect Celery logs to Loguru
    """

    def emit(self, record):
        """
        Convert Celery LogRecord to something Loguru can understand
        """
        loguru_level = record.levelname.lower()
        level_map = {
            "debug": "DEBUG",
            "info": "INFO",
            "warning": "WARNING",
            "error": "ERROR",
            "critical": "CRITICAL",
            "success": "SUCCESS",
        }
        loguru_level = level_map.get(loguru_level, "INFO")  # default to INFO if unknown
        loguru_logger.opt(depth=6, exception=record.exc_info).log(
            loguru_level, record.getMessage()
        )


# def logger_settings(logger_instance):

#     # remove all default sinks
#     # logger_instance.remove()
#     # format with (close to) fixed prefix length
#     # tuned on the longest level label i.e. CRITICAL + icon
#     logger_format = (
#         "<light-blue>{time:%Y-%m-%d %H:%M:%S}</light-blue>"
#         " | {level: <10}"
#         " | <level>{message}</level>"
#     )
#     # use the following to show either the source file/line or function
#     # " | {name}.{file}:{line}" \
#     # " | {function}" \

#     # some parameters disabled as not used anymore, though kept for tests/debugging
#     logging_parameters = {
#         "format": logger_format,
#         # "filter": self.log_tuning,
#         "backtrace": False,
#         "diagnose": False,
#     }

#     logger_instance.add(log_filepath, rotation="20MB", **logging_parameters)
#     logger_instance.add(sys.stderr, colorize=True, **logging_parameters)


class LoggerManager:

    def __init__(self, log_filepath: str):

        # Remove all handlers associated with the root logger object.
        # for handler in logging.root.handlers[:]:
        #     logging.root.removeHandler(handler)

        # remove all default sinks
        loguru_logger.remove()
        # format with (close to) fixed prefix length
        # tuned on the longest level label i.e. CRITICAL + icon
        logger_format = (
            "<light-blue>{time:%Y-%m-%d %H:%M:%S}</light-blue>"
            " | {level: <10}"
            " | <level>{message}</level>"
        )
        # use the following to show either the source file/line or function
        # " | {name}.{file}:{line}" \
        # " | {function}" \

        # some parameters disabled as not used anymore, though kept for tests/debugging
        logging_parameters = {
            "format": logger_format,
            # "filter": self.log_tuning,
            "backtrace": False,
            "diagnose": False,
        }

        loguru_logger.add(log_filepath, rotation="20MB", **logging_parameters)
        loguru_logger.add(sys.stderr, colorize=True, **logging_parameters)

        logging.basicConfig(
            handlers=[InterceptHandler()], level=logging.INFO, force=True
        )

    # previous approach, discarded to avoid some erratic issues with tests
    # + unconsitent messages length due to icon width not identical
    # @staticmethod
    # def log_tuning(record):

    #     # exclude filepath from log message (was useful)
    #     # record["extra"].clear()

    #     # include icon
    #     if not TEST_MODE:
    #         level = record["level"].name
    #         icon = record["level"].icon
    #         record["level"] = f"{level} {icon}"

    #     return record

    @staticmethod
    def get_logger():
        return loguru_logger
