"""
Logging module, re-usable between components.
"""

import sys

# alias to be sure to import the correct 'logger' object in the modules using logging
from loguru import logger as loguru_logger


class LoggerManager:

    def __init__(self, log_filepath: str):

        # remove all default sinks
        loguru_logger.remove()
        # format with (close to) fixed prefix length
        # tuned on the longest level label i.e. CRITICAL + icon
        logger_format = (
            "<light-blue>{time:%Y-%m-%d %H:%M:%S}</light-blue>"
            " | {level: <11}"
            " | <level>{message}</level>"
        )
        # use the following to show either the source file/line or function
        # " | {name}.{file}:{line}" \
        # " | {function}" \

        logging_parameters = {
            "format": logger_format,
            "filter": self.log_tuning,
            # "backtrace": False,
            # "diagnose": False
        }

        loguru_logger.add(log_filepath, rotation="20MB", **logging_parameters)
        loguru_logger.add(sys.stderr, colorize=True, **logging_parameters)

    @staticmethod
    def log_tuning(record):

        # exclude filepath from log message (was useful)
        # record["extra"].clear()

        # include icon
        level = record["level"].name
        icon = record["level"].icon
        record["level"] = f"{level} {icon}"

        return record

    @staticmethod
    def get_logger():
        return loguru_logger
