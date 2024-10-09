#!/bin/sh

celery --app=worker.celery beat --loglevel=info --logfile=logs/beat.log --detach

# celery worker is not detached i.e. logs are visible in docker-compose terminal
celery --app=worker.celery worker --loglevel=debug --logfile=logs/worker.log -Q data_pipeline
