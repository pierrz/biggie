"""
Spark core runner
"""

from config import pyspark_config
from pyspark.sql import SparkSession  # pylint: disable=E0611

# .config("spark.mongodb.connection.uri", pyspark_config.MONGODB_URI)
spark_mongo = (
    SparkSession.builder.appName("Spark/Mongo IO")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "2g")
    .config(
        "spark.mongodb.read.connection.uri",
        f"{pyspark_config.MONGODB_URI}{pyspark_config.DB_NAME}",
    )
    .config(
        "spark.mongodb.write.connection.uri",
        f"{pyspark_config.MONGODB_URI}{pyspark_config.DB_NAME}",
    )
    .config(
        "spark.jars.packages",
        "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
    )
    .getOrCreate()
)

spark_postgres = (
    SparkSession.builder.appName("Spark/Postgres IO")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "2g")
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.7.4.jar")
    .config(
        "spark.driver.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.7.4.jar"
    )
    .getOrCreate()
)

# .config(
#     "spark.executor.extraClassPath",
#     "/opt/bitnami/spark/jars/postgresql-42.7.4.jar",
# )
# .config(
#     "spark.driver.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.7.4.jar"
# )

# cheatsheet for further settings
# .config("spark.mongodb.input.uri", "mongodb://mongo1:27017,mongo2:27018,mongo3:27019/Stocks.Source?replicaSet=rs0")\
# .master("spark://spark-master:7077")\     Spark standalone cluster
# .master("local[2]")\      local run with 2 cores

# draft
# .config("spark.jars.packages", "org.postgresql:postgresql:42.4.1")
# .config("spark.jars", "/opt/spark/jars/postgresql-42.4.1.jar")
