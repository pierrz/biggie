FROM bitnami/spark:3.5.2

# Install OpenJDK 17 if needed
# RUN apt-get update && apt-get install -y openjdk-17-jdk && \
#     update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java

USER root
RUN install_packages curl
USER 1001
RUN curl https://jdbc.postgresql.org/download/postgresql-42.7.4.jar --output /opt/bitnami/spark/jars/postgresql-42.7.4.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar --output /opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar

# Set environment variables for Python 3.11
ENV PYSPARK_PYTHON=/usr/local/bin/python3.11 \
    PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.11
