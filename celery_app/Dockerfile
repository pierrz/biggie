FROM python:3.11.9

ARG TEST_MODE="False"

# Java (required for PySpark)
RUN apt-get clean \
    && apt-get update \
    && apt-get install -qy wget openjdk-17-jdk

# environment
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
    PATH="${PATH}:/etc/poetry/bin"

# poetry
RUN python3 -m pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

# Copy only requirements to cache them in docker layer
WORKDIR /opt/celery_app
COPY ./celery_app/pyproject.toml ./celery_app/poetry.lock* ./

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

# RUN mkdir -p /opt/bitnami/spark/jars
# RUN curl https://jdbc.postgresql.org/download/postgresql-42.7.4.jar \
#     --output /opt/bitnami/spark/jars/postgresql-42.7.4.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar \
#     --output /opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.14/mongo-java-driver-3.12.14.jar \
#     --output /opt/bitnami/spark/jars/mongo-java-driver-3.12.14.jar

COPY ./celery_app ./
COPY ./db ./src/db
COPY ./commons ./src/commons
