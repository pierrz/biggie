"""
Module spinning up the Celery worker
"""

from config import celery_config
from tasks import run_harvester_container

# pylint: disable=E0611
from celery import Celery
from celery.utils.log import get_task_logger

celery = Celery(__name__)
celery.config_from_object(celery_config)
celery.autodiscover_tasks(force=True)

logger = get_task_logger(__name__)


if __name__ == '__main__':
    run_harvester_container()
