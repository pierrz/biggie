FROM python:3.11.9-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="/root/.local/bin:$PATH"

# Install UV
RUN apt-get update && apt-get install -y curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy only requirements to cache them in docker layer
WORKDIR /opt/api
COPY ./api/pyproject.toml ./api/uv.lock* ./

# Project initialization (only main and security groups installed here)
RUN uv sync --group security

# Install test dependencies only in TEST_MODE
ARG TEST_MODE="False"
RUN if [ $(echo $TEST_MODE | tr -d '\"') = "True" ]; then \
        echo "Running in TEST mode"; \
        uv sync --only-group test; \
    else \
        echo "Running in normal mode"; \
    fi

# Include project files
# NB: Can be disabled if the "Dev speed up" lines are enabled
# in the docker-compose volume for api contianers
COPY ./api ./
COPY ./db ./src/db/
COPY ./commons ./src/commons
