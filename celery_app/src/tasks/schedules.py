"""
Schedule for Celery chained tasks.

TODO: investigate/fix the erratic cleaning waiting time interval
 (jumps between remaining minutes, not working consistently anymore since last package update)
"""

from celery import signature
from celery.schedules import crontab

data_pipeline_queue = {"queue": "data_pipeline"}

# Github events fetched and loaded every minute, and only cleaned every 30 minutes
github_events_stream = {
    "task": "github-events-data-acquisition",
    "schedule": crontab(minute="*"),
    "options": {
        **data_pipeline_queue,
        "link": signature(
            "load-github-events",
            options={
                **data_pipeline_queue,
                "link": signature(
                    "github-events-cleaning",
                    kwargs={"wait_minutes": 30},
                    options=data_pipeline_queue,
                ),
            },
        ),
    },
}
