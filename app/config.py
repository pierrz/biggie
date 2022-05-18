"""
Configuration module
"""

import os
from datetime import datetime
from hashlib import md5
from pathlib import Path
from typing import Tuple

from pydantic import BaseSettings


class Config(BaseSettings):
    """
    Config class.
    """

    APP_MODE: str = os.getenv("APP_MODE")
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("DB_NAME")
    LOCAL_DEV = True
    API_PUBLIC_KEY: str = os.getenv("API_PUBLIC_KEY")
    API_PRIVATE_KEY: str = os.getenv("API_PRIVATE_KEY")
    OUTPUT_DIR = Path(os.sep, "opt", "data", "marvel")
    PROCESSED_DIR = Path(os.sep, "opt", "data", "processed")

    def generate_auth_parts(self) -> Tuple[str, str]:
        """
        chunks a string such as md5(ts+privateKey+publicKey)
        :return: the hashed key
        """
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{timestamp}{self.API_PRIVATE_KEY}{self.API_PUBLIC_KEY}"
        return timestamp, md5(hash_input.encode("utf-8")).hexdigest()


class CeleryConfig(BaseSettings):
    """
    Celery config class.
    """

    broker_url = os.getenv("CELERY_BROKER_URL")
    result_backend = os.getenv("CELERY_RESULT_BACKEND")
    imports = [
        "test.fixtures.tasks",
        "src.tasks.harvester_task",
        "src.tasks.spark_task",
    ]
    enable_utc = True
    timezone = "Europe/Amsterdam"
    task_track_started = True
    result_persistent = True
    task_publish_retry = True
    # The acks_late setting would be used when you need the task to be executed again
    # if the worker (for some reason) crashes mid-execution
    task_acks_late = "Enabled"


app_config = Config()
celery_config = CeleryConfig()
