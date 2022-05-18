#FROM debian:latest
FROM ubuntu:20.04

# install java & python
RUN apt-get clean \
    && apt-get update \
    && apt-get install -qy wget default-jdk

RUN apt-get install -qy libssl-dev openssl make gcc tar unzip

RUN apt update \
    && apt install zlib1g-dev

RUN cd /opt \
    && wget https://www.python.org/ftp/python/3.9.11/Python-3.9.11.tgz \
    && tar -xzvf Python-3.9.11.tgz

RUN cd /opt/Python-3.9.11 \
    && ./configure \
    && make \
    && make install \
    && ln -fs /opt/Python-3.9.11/Python /usr/bin/python3 \
    && python3 --version

RUN cd /tmp \
    && wget https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz \
    && tar -xvzf spark-3.1.2-bin-hadoop3.2.tgz \
    && mv spark-3.1.2-bin-hadoop3.2/ /opt/spark

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt install -qy python3-pip
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /opt/app
COPY ./app/pyproject.toml ./app/poetry.lock* ./

# Project initialization:
RUN poetry config virtualenvs.create false\
    && poetry install --no-interaction --no-ansi --no-dev

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
    PATH=$PATH:$JAVA_HOME/bin \
    PYSPARK_HADOOP_VERSION=3.2 \
    SPARK_HOME=/opt/spark \
    PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin \
    PYSPARK_DRIVER_PYTHON=/usr/bin/python3 \
    PYSPARK_PYTHON=/usr/bin/python3

# Creating folders and files for the project:
COPY ./app ./
