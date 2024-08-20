FROM python:3.10.8

# java
RUN apt-get clean \
    && apt-get update \
    && apt-get install -qy wget default-jdk tar

# spark
# TODO: eventually implement Spark with Scala 2.13
# (currently not the default version in many related PaaS offers though)
# https://dlcdn.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3-scala2.13.tgz
RUN cd /tmp \
    && wget https://dlcdn.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz \
    && tar -xvzf spark-3.5.2-bin-hadoop3.tgz \
    && mv spark-3.5.2-bin-hadoop3/ /opt/spark

# postgres lib
RUN wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar -O /opt/spark/jars/postgresql-42.7.3.jar

# environment
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
    PATH=$PATH:$JAVA_HOME/bin \
    PYSPARK_HADOOP_VERSION=3 \
    SPARK_HOME=/opt/spark \
    PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin \
    PYSPARK_DRIVER_PYTHON=/usr/bin/python3 \
    PYSPARK_PYTHON=/usr/bin/python3 \
    # python environment
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=off \
    PIP_DEFAULT_TIMEOUT=100

# poetry
# RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
# RUN /etc/poetry --version
#RUN wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
#RUN python3.10 /tmp/get-pip.py
#RUN python3.10 -m pip install --upgrade pip \
#    && python3.10 -m pip install poetry
#RUN python3.10 -m pip install --upgrade pip \
RUN python3 -m pip install --upgrade pip
#    && pip install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH="${PATH}:/etc/poetry/bin"

# Copy only requirements to cache them in docker layer
WORKDIR /opt/celery_app
COPY ./celery_app/pyproject.toml ./
COPY ./celery_app/poetry.lock* ./
#RUN poetry config virtualenvs.create true \
#    && poetry install --no-interaction --no-ansi
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV PATH="${PATH}:/etc/poetry/bin" \
    PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.10 \
    PYSPARK_PYTHON=/usr/local/bin/python3.10

COPY ./celery_app ./
COPY ./db ./src/db
COPY ./utils ./src/utils
