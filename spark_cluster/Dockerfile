# TODO: fix/investigate the error message at startup:
# "Unable to load native-hadoop library for your platform... using builtin-java classes where applicable"

FROM bitnami/spark:3.5.2

# Install Python 3.11 to align with the version used in the Celery container
# NB: this Bitnami image comes with Python 3.12 installed, but it is not stable enough for our use case
USER root

RUN install_packages python3.11 python3.11-dev python3.11-distutils

# Remove the symlink to Python 3.12 and create new ones for 3.11
RUN rm -f /opt/bitnami/python/bin/python3 \
    && ln -sf /usr/bin/python3.11 /opt/bitnami/python/bin/python3 \
    && ln -sf /usr/bin/python3.11 /usr/local/bin/python3.11

# Set environment variables
ENV PYSPARK_PYTHON=/opt/bitnami/python/bin/python3 \
    PYSPARK_DRIVER_PYTHON=/opt/bitnami/python/bin/python3

# RUN install_packages python3.11 \
#     && ln -s /usr/bin/python3.11 /usr/local/bin/python3.11

# # Set environment variables
# ENV PYSPARK_PYTHON=/usr/local/bin/python3.11 \
#     PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.11

# Comprehensive Python management
# RUN install_packages python3.11 \
#     && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
#     && update-alternatives --set python3 /usr/bin/python3.11

# Explicit, absolute path configurations
# ENV PYSPARK_PYTHON=/usr/bin/python3.11 \
#     PYSPARK_DRIVER_PYTHON=/usr/bin/python3.11 \
#     PYTHON_EXECUTABLE=/usr/bin/python3.11

# RUN install_packages curl python3.11 \
#     && ln -s /usr/bin/python3.11 /usr/local/bin/python3.11

# # Set environment variables for PySpark (aligned with the Celery container)
# ENV PYSPARK_PYTHON=/usr/local/bin/python3.11 \
# PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.11

# DISABLED (not working): Install drivers and connectors for Spark
# Cf. https://github.com/bitnami/containers/tree/main/bitnami/spark#installing-additional-jars
# USER 1001
# RUN curl https://jdbc.postgresql.org/download/postgresql-42.7.4.jar \
#     --output /opt/bitnami/spark/jars/postgresql-42.7.4.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar \
#     --output /opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar
