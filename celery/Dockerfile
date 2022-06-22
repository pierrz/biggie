FROM python:3.9.12

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PYTHONPATH=/opt/celery

#RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /opt/celery/
COPY ./celery/pyproject.toml ./celery/poetry.lock* /

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY ./celery .

CMD celery --app=worker.celery worker --loglevel=info --logfile=logs/celery.log
