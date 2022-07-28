FROM ubuntu:20.04

# install java & python & spark
RUN apt-get clean \
    && apt-get update \
    && apt-get install -qy wget default-jdk tar

RUN apt update \
    && apt install -qy software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa\
    && apt install -qy python3.9

RUN cd /tmp \
    && wget https://dlcdn.apache.org/spark/spark-3.2.2/spark-3.2.2-bin-hadoop3.2.tgz \
    && tar -xvzf spark-3.2.2-bin-hadoop3.2.tgz \
    && mv spark-3.2.2-bin-hadoop3.2/ /opt/spark

# spark environment
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
    PATH=$PATH:$JAVA_HOME/bin \
    PYSPARK_HADOOP_VERSION=3.2 \
    SPARK_HOME=/opt/spark \
    PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin \
    PYSPARK_DRIVER_PYTHON=/usr/bin/python3.9 \
    PYSPARK_PYTHON=/usr/bin/python3.9 \
    # python environment
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=off \
    PIP_DEFAULT_TIMEOUT=100

# project installation
RUN apt install -qy python3-pip
RUN python3.9 -m pip install poetry

# NB: the source directory is named 'pyspark_app' to be sure not to conflict
# with the pyspark library and the 'spark' directory
# Copy only requirements to cache them in docker layer
WORKDIR /opt/pyspark_app
COPY ./pyspark_app/pyproject.toml ./pyspark_app/poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./pyspark_app ./
COPY ./db ./src/db
COPY ./utils/json_utils.py ./src/
