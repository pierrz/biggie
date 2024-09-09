"""
Configuration module
"""

import os
from pathlib import Path

from pydantic import BaseSettings
from src.commons import names as ns
from src.tasks.schedules import github_events_stream

data_dir_root = Path(os.sep, "opt", ns.data)
TEST_MODE: str = bool(os.getenv("TEST_MODE"))


class CeleryConfig(BaseSettings):
    """
    Config class.
    """

    broker_url: str
    result_backend: str
    enable_utc = True
    timezone = "Europe/Amsterdam"
    task_track_started = True
    result_persistent = True
    task_publish_retry = True
    task_acks_late = "Enabled"  # re-run the task if the worker crashes mid-execution

    if TEST_MODE:
        imports = ["src.tasks.dummy_task.py"]
        # TODO: implement beat test
        # beat_schedule = {"task": "test_task", "schedule": crontab(minute="*"), "options": {**data_pipeline_queue}}
    else:
        imports = [
            "src.tasks.github_events_data_acquisition",
            "src.tasks.github_events_load",
            "src.tasks.github_events_cleaning",
        ]
        beat_schedule = {"github-events-stream": github_events_stream}


class DataDirectories(BaseSettings):
    github_in = Path(data_dir_root, ns.events, ns.received)
    github_out = Path(data_dir_root, ns.events, ns.processed)
    github_diagrams = Path(data_dir_root, ns.events, ns.diagrams)
    batch = Path(data_dir_root, "batch-io")  # test purposes


class HarvesterConfig(BaseSettings):
    """
    Harvester module config
    """

    # if TEST_MODE:     # to implement only once the branch split has been done
    TOKEN_GITHUB_API: str
    EVENTS = list(ns.GithubEventTypes)
    PER_PAGE = 20


class PySparkConfig(BaseSettings):
    """
    PySpark module config
    """

    MONGODB_URI: str
    DB_NAME: str


celery_config = CeleryConfig()
harvester_config = HarvesterConfig()
pyspark_config = PySparkConfig()
data_directories = DataDirectories()
