FROM python:3.9.12-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /opt/api
COPY ./api/pyproject.toml ./api/poetry.lock* ./

# Project initialization:
RUN poetry config virtualenvs.create false\
    && poetry install --no-interaction --no-ansi

# Creating folders and files for the project:
COPY ./api ./
COPY ./db ./src/db
COPY ./utils/json_utils.py ./src/
