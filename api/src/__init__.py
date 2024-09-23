"""
Logging module based on common logger
"""

from src.commons.logging import LoggerManager

logger = LoggerManager(log_filepath="/var/log/api/run.log").get_logger()
