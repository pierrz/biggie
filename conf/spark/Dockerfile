FROM bitnami/spark:3.5.2
# FROM spark:3.5.2-java17

# Install Python 3.11 to align with the version used in the Celery container
# NB: this Bitnami image comes with Python 3.12 installed, but it is not stable enough for our use case
USER root
RUN install_packages curl python3.11 \
    && ln -s /usr/bin/python3.11 /usr/local/bin/python3.11
RUN mkdir -p /opt/bitnami/logs
# RUN apt-get update && apt-get install -y curl python3.11

# # Install drivers and connectors for Spark
USER 1001
# RUN rm -r /opt/bitnami/spark/jars && \
#     curl --location https://dlcdn.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz | \
#     tar --extract --gzip --strip=1 --directory /opt/bitnami/spark/ spark-3.5.2-bin-hadoop3/jars/

# RUN cd /tmp \
#     && wget https://dlcdn.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz \
#     && tar -xvzf spark-3.5.2-bin-hadoop3.tgz \
#     && mv spark-3.5.2-bin-hadoop3/ /opt/spark

RUN curl https://jdbc.postgresql.org/download/postgresql-42.7.4.jar \
    --output /opt/bitnami/spark/jars/postgresql-42.7.4.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar \
#     --output /opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.14/mongo-java-driver-3.12.14.jar \
#     --output /opt/bitnami/spark/jars/mongo-java-driver-3.12.14.jar
# RUN curl https://jdbc.postgresql.org/download/postgresql-42.7.4.jar \
#     --output /opt/spark/jars/postgresql-42.7.4.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar \
#     --output /opt/spark/jars/mongo-spark-connector_2.12-10.4.0.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.14/mongo-java-driver-3.12.14.jar \
#     --output /opt/spark/jars/mongo-java-driver-3.12.14.jar

# Set environment variables for PySpark (aligned with the Celery container)
ENV PYSPARK_PYTHON=/usr/local/bin/python3.11 \
    PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.11
