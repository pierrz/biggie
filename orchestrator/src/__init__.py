"""
Logging module based on common logger
"""

from src.commons.logging import LoggerManager

logger = LoggerManager(log_filepath="/opt/orchestrator/logs/worker.log").get_logger()
