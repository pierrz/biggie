FROM python:3.11.9

# Java (required for PySpark)
RUN apt-get clean \
    && apt-get update \
    && apt-get install -qy openjdk-17-jdk curl

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
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="/root/.local/bin:$PATH"

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy only requirements to cache them in docker layer
WORKDIR /opt/orchestrator
COPY ./orchestrator/pyproject.toml ./orchestrator/uv.lock* ./

# Project initialization (only main and security groups installed here)
RUN uv sync --group security

# Install test dependencies only in TEST_MODE
ARG TEST_MODE="False"
RUN if [ $(echo $TEST_MODE | tr -d '\"') = "True" ]; then \
        echo "Running in TEST mode"; \
        uv sync --only-group test ; \
    else \
        echo "Running in normal mode"; \
        chmod +x run.sh; \
    fi

# Include project files
COPY ./orchestrator ./
COPY ./db ./src/db
COPY ./commons ./src/commons
