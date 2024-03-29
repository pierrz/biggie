"""
Spark core runner
"""

from config import pyspark_config
from pyspark.sql import SparkSession  # pylint: disable=E0611

spark_mongo = (
    SparkSession.builder.appName("Spark/Mongo IO")
    .master("local[2]")
    .config("spark.executor.memory", "2g")
    .config("spark.mongodb.input.uri", pyspark_config.MONGODB_URI)
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
