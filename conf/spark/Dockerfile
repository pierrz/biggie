FROM bitnami/spark:3.5.2

# Install specific Java and Python versions
USER root

RUN install_packages curl
RUN ln -s /opt/bitnami/python/bin/python /usr/local/bin/python3
# build-essential

# RUN apt-get update && apt-get install -y openjdk-17-jdk && \
#     update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java

# RUN curl -O https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz && \
#     tar -xzf Python-3.11.9.tgz && \
#     cd Python-3.11.9 && \
#     ./configure --enable-optimizations && \
#     make altinstall && \
#     ln -s /usr/local/bin/python3.11 /usr/local/bin/python3.11.9 && \
#     cd .. && \
#     rm -rf Python-3.11.9 Python-3.11.9.tgz

# Get connectors and drivers packages
USER 1001
RUN curl https://jdbc.postgresql.org/download/postgresql-42.7.4.jar --output /opt/bitnami/spark/jars/postgresql-42.7.4.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar --output /opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar


# Set PySpark environment variables
# ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
ENV PYSPARK_PYTHON=/usr/local/bin/python3 \
    PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3
# ENV PYSPARK_PYTHON=/opt/bitnami/python/bin/python \
#     PYSPARK_DRIVER_PYTHON=/opt/bitnami/python/bin/python
