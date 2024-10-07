"""
Configuration module
"""

import os
from pathlib import Path
from typing import Dict, List

from pydantic_settings import BaseSettings
from src.commons import enums
from src.commons import names as ns
from src.tasks.schedules import github_events_stream

data_dir_root = Path(os.sep, "opt", ns.data)
TEST_MODE: str = bool(os.getenv("TEST_MODE"))


class CeleryConfig(BaseSettings):
    """
    Config class.
    """

    broker_url: str = os.getenv("CELERY_BROKER_URL")
    result_backend: str = os.getenv("CELERY_RESULT_BACKEND")
    enable_utc: bool = True
    # timezone: str = "Europe/Amsterdam"
    timezone: str = "Indian/Antananarivo"
    task_track_started: bool = True
    result_persistent: bool = True
    task_publish_retry: bool = True
    task_acks_late: str = (
        "Enabled"  # re-run the task if the worker crashes mid-execution
    )

    if TEST_MODE:
        imports: List[str] = ["src.tasks.dummy_task.py"]
        # TODO: implement beat test
        # beat_schedule = {"task": "test_task", "schedule": crontab(minute="*"), "options": {**data_pipeline_queue}}
    else:
        imports: List[str] = [
            "src.tasks.github_events_data_acquisition",
            "src.tasks.github_events_load",
            "src.tasks.github_events_cleaning",
        ]
        beat_schedule: Dict[str, Dict] = {"github-events-stream": github_events_stream}


class DataDirectories(BaseSettings):
    github_in: Path = Path(data_dir_root, ns.github_events, ns.received)
    github_out: Path = Path(data_dir_root, ns.github_events, ns.processed)
    github_diagrams: Path = Path(data_dir_root, ns.github_events, ns.diagrams)
    batch: Path = Path(data_dir_root, "batch-io")  # test purposes


class HarvesterConfig(BaseSettings):
    """
    Harvester module config
    """

    TOKEN_GITHUB_API: str
    EVENTS: List[str] = list(enums.GithubEventTypes)
    PER_PAGE: int = 20


class MainConfig(BaseSettings):
    """
    PySpark module config
    """

    MONGODB_URI: str
    POSTGRESDB_HOST: str
    POSTGRES_APP_USER: str
    POSTGRES_APP_PASSWORD: str
    DB_NAME: str
    # POSTGRES_USER: str      # TODO: might be usefult to implement Postgres 16.x


celery_config = CeleryConfig()
harvester_config = HarvesterConfig()
main_config = MainConfig()
data_directories = DataDirectories()
