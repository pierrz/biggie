import os

from pydantic import BaseSettings
from pyspark.sql import SparkSession  # pylint: disable=E0611


class SparklusterConfig(BaseSettings):
    """
    PySpark module config
    """

    MONGODB_URI: str = os.getenv("MONGODB_URI")
    DB_NAME: str = os.getenv("DB_NAME")


sparkluster_config = SparklusterConfig()


spark_mongo = (
    SparkSession.builder.appName("Spark/Mongo IO")
    .master("local[2]")
    .config("spark.executor.memory", "2g")
    .config("spark.mongodb.input.uri", sparkluster_config.MONGODB_URI)
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0")
    .getOrCreate()
)

spark_postgres = (
    SparkSession.builder.appName("Spark/Postgres IO")
    .master("local[2]")
    .config("spark.executor.memory", "2g")
    .config("spark.executor.extraClassPath", "/opt/spark/jars/postgresql-42.4.1.jar")
    .config("spark.driver.extraClassPath", "/opt/spark/jars/postgresql-42.4.1.jar")
    .getOrCreate()
)
