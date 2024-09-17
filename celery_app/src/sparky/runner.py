"""
Spark core runner
"""

from config import pyspark_config
from pyspark.sql import SparkSession  # pylint: disable=E0611

spark_mongo = (
    SparkSession.builder.appName("Spark/Mongo IO")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "2g")
    .config("spark.mongodb.connection.uri", pyspark_config.MONGODB_URI)
    .config(
        "spark.jars.packages",
        "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
    )
    .config(
        "spark.driver.extraJavaOptions",
        "-Dlog4j.configuration=file:///opt/bitnami/logs/log4j.properties -Dlog4j.debug",
    )
    .config(
        "spark.executor.extraJavaOptions",
        "-Dlog4j.configuration=file:///opt/bitnami/logs/log4j.properties -Dlog4j.debug",
    )
    .getOrCreate()
)
# Should be added when jars is manually downloaded and included in spark files
# .config(
#     "spark.jars",
#     "/opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar",
# )


spark_postgres = (
    SparkSession.builder.appName("Spark/Postgres IO")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "2g")
    .config(
        "spark.driver.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.7.4.jar"
    )
    .config(
        "spark.executor.extraClassPath",
        "/opt/bitnami/spark/jars/postgresql-42.7.4.jar",
    )
    .getOrCreate()
)
# .config(
#     "spark.jars.packages",
#     "org.postgresql:postgresql:jar:42.7.4",
# )


# cheatsheet
# .master("local[2]")\      local run with 2 cores
# .config(
#     "spark.mongodb.read.connection.uri",
#     f"{pyspark_config.MONGODB_URI}{pyspark_config.DB_NAME}",
# )
# .config(
#     "spark.mongodb.write.connection.uri",
#     f"{pyspark_config.MONGODB_URI}{pyspark_config.DB_NAME}",
# )
# .config("spark.mongodb.input.uri", f"{pyspark_config.MONGODB_URI}{pyspark_config.DB_NAME}")
# .config("spark.mongodb.output.uri", f"{pyspark_config.MONGODB_URI}{pyspark_config.DB_NAME}")
