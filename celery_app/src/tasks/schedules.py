from celery import signature
from celery.schedules import crontab

data_pipeline_queue = {"queue": "data_pipeline"}

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
                    kwargs={"wait_minutes": 2},
                    options=data_pipeline_queue,
                ),
            },
        ),
    },
}
