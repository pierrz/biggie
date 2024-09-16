FROM bitnami/spark:3.5.2

USER root
RUN install_packages curl python3.11 \
    && ln -s /usr/bin/python3.11 /usr/local/bin/python3.11

USER 1001
RUN curl https://jdbc.postgresql.org/download/postgresql-42.7.4.jar --output /opt/bitnami/spark/jars/postgresql-42.7.4.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar --output /opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar

# Set environment variables for Python 3.11
ENV PYSPARK_PYTHON=/usr/local/bin/python3.11 \
    PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.11
