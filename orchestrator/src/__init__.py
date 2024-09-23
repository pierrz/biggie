"""
Logging module based on common logger
TODO: ensure that ALL messages go through the Loguru based logger:
 - in worker.log    -> from INFO/ForkPoolWorker-4 for 'received' and 'succeeded' messages
 - in beat.log      -> from INFO/MainProcess
"""

from src.commons.logging import LoggerManager

logger = LoggerManager(log_filepath="/opt/orchestrator/logs/worker.log").get_logger()
# beat_logger = LoggerManager(log_filepath="/opt/orchestrator/logs/beat.log").get_logger()
