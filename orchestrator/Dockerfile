FROM python:3.11.9

ARG TEST_MODE="False"

# Java (required for PySpark)
RUN apt-get clean \
    && apt-get update \
    && apt-get install -qy wget openjdk-17-jdk

# Environment
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    PYSPARK_HADOOP_VERSION=3 \
    PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.11 \
    PYSPARK_PYTHON=/usr/local/bin/python3.11 \
    # python environment
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=off \
    PIP_DEFAULT_TIMEOUT=100

# Poetry
RUN python3 -m pip install --upgrade pip \
    && pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /opt/orchestrator
COPY ./orchestrator/pyproject.toml ./orchestrator/poetry.lock* ./

# Project initialization (only main and security groups installed here)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main,security

# Install test dependencies only in TEST_MODE
RUN if [ $(echo $TEST_MODE | tr -d '\"') = "True" ]; then \
        echo "Running in TEST mode"; \
        poetry install --only dev; \
    else \
        echo "Running in normal mode"; \
    fi

# Include project files
COPY ./orchestrator ./
COPY ./db ./src/db
COPY ./commons ./src/commons
