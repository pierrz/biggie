"""
Spark core runner
"""

from config import pyspark_config
from pyspark.sql import SparkSession  # pylint: disable=E0611

spark = (
    SparkSession.builder.appName("Spark/Mongo IO")
    .master("local[2]")
    .config("spark.executor.memory", "2g")
    .config("spark.mongodb.input.uri", pyspark_config.MONGODB_URI)
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.0")
    .getOrCreate()
)

# cheatsheet for further settings
# .config("spark.mongodb.input.uri", "mongodb://mongo1:27017,mongo2:27018,mongo3:27019/Stocks.Source?replicaSet=rs0")\
# .master("spark://spark-master:7077")\     Spark standalone cluster
# .master("local[2]")\      local run with 2 cores
