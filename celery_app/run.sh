#!/bin/sh

celery --app=worker.celery beat --loglevel=info --logfile=logs/beat.log --detach

# celery worker not detached / showing in docker-compose terminal
celery --app=worker.celery worker --loglevel=info --logfile=logs/worker.log -Q data_pipeline
