"""
Configuration module
"""

import os
from pathlib import Path

from pydantic import BaseSettings
from src.tasks.schedules import github_events_stream

data_dir_root = Path(os.sep, "opt", "data")
TEST_MODE = bool(os.getenv("TEST"))


class CeleryConfig(BaseSettings):
    """
    Config class.
    """

    broker_url: str = os.getenv("CELERY_BROKER_URL")
    result_backend: str = os.getenv("CELERY_RESULT_BACKEND")
    enable_utc = True
    timezone = "Europe/Amsterdam"
    task_track_started = True
    result_persistent = True
    task_publish_retry = True
    # The acks_late setting would be used when you need the task to be executed again
    # if the worker (for some reason) crashes mid-execution
    task_acks_late = "Enabled"

    if TEST_MODE:
        imports = ["src.tasks.dummy_task.py"]
        # todo: implement beat test
        # beat_schedule = {"task": "test_task", "schedule": crontab(minute="*"), "options": {**data_pipeline_queue}}
    else:
        imports = [
            "src.tasks.github_events_data_acquisition",
            "src.tasks.github_events_load",
            "src.tasks.github_events_cleaning"
        ]
        beat_schedule = {
            "github-events-stream": github_events_stream
        }


class DataDirectories(BaseSettings):
    github_in = Path(data_dir_root, "events", "received")
    github_out = Path(data_dir_root, "events", "processed")
    github_diagrams = Path(data_dir_root, "events", "diagrams")
    ukr_dp = Path(data_dir_root, "lake")
    batch = Path(data_dir_root, "batch-io")


class HarvesterConfig(BaseSettings):
    """
    Harvester module config
    """

    TOKEN_GITHUB_API: str = os.getenv("TOKEN_GITHUB_API")
    EVENTS = ["IssuesEvent", "PullRequestEvent", "WatchEvent"]
    PER_PAGE = 20


class PySparkConfig(BaseSettings):
    """
    PySpark module config
    """

    MONGODB_URI: str = os.getenv("MONGODB_URI")
    DB_NAME: str = os.getenv("DB_NAME")


celery_config = CeleryConfig()
harvester_config = HarvesterConfig()
pyspark_config = PySparkConfig()
data_directories = DataDirectories()
