"""
Configuration module
"""

import os

from pydantic import BaseSettings


class CeleryConfig(BaseSettings):
    """
    Celery config class.
    """

    broker_url = os.getenv("CELERY_BROKER_URL")
    result_backend = os.getenv("CELERY_RESULT_BACKEND")
    imports = ["tasks"]
    enable_utc = True
    timezone = "Europe/Amsterdam"
    task_track_started = True
    result_persistent = True
    task_publish_retry = True
    # The acks_late setting would be used when you need the task to be executed again
    # if the worker (for some reason) crashes mid-execution
    task_acks_late = "Enabled"


celery_config = CeleryConfig()
