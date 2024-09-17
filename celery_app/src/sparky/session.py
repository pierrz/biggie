"""
Spark session configuration
"""

from config import pyspark_config
from pyspark.sql import SparkSession  # pylint: disable=E0611

# # /!\ jars.packages is required ONLY when fetching directly from maven
spark_session = (
    SparkSession.builder.appName("Biggie/Spark IO")
    .master("spark://spark-master:7077")
    .config("spark.executor.memory", "2g")
    .config("spark.mongodb.connection.uri", pyspark_config.MONGODB_URI)
    .config(
        "spark.jars.packages",
        "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0,org.postgresql:postgresql:42.7.4",
    )
    .config("spark.driver.extraClassPath", "org.postgresql:postgresql:42.7.4")
    .config("spark.executor.extraClassPath", "org.postgresql:postgresql:42.7.4")
    .config(
        "spark.driver.extraJavaOptions",
        "-Dlog4j.configuration=file:///opt/bitnami/spark/logs/log4j.properties -Dlog4j.debug",
    )
    .config(
        "spark.executor.extraJavaOptions",
        "-Dlog4j.configuration=file:///opt/bitnami/spark/logs/log4j.properties -Dlog4j.debug",
    )
    .getOrCreate()
)

# def init_spark_session(session, config):
#     for param, settings in config.items():
#         session = session.config(param, settings)
#     return session.getOrCreate()

# spark_config = {
#     "spark.executor.memory": "2g",
#     "spark.cores.max": "2",
#     "spark.mongodb.connection.uri": pyspark_config.MONGODB_URI,
#     "spark.jars.packages": "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0,org.postgresql:postgresql:42.7.4",
#     "spark.driver.extraClassPath": "org.postgresql:postgresql:42.7.4",
#     "spark.executor.extraClassPath": "org.postgresql:postgresql:42.7.4",
#     "spark.driver.extraJavaOptions": "-Dlog4j.configuration=file:///opt/bitnami/spark/logs/log4j.properties -Dlog4j.debug",
#     "spark.executor.extraJavaOptions": "-Dlog4j.configuration=file:///opt/bitnami/spark/logs/log4j.properties -Dlog4j.debug",
# }
# spark_session_base = (
#     SparkSession.builder.appName("Biggie/Spark IO")
#     .master("spark://spark-master:7077")
# )

# spark_session = init_spark_session(
#     session=spark_session_base,
#     config=spark_config
# )

# DISABLED (not working): absolute path to jars
# "/opt/bitnami/spark/jars/mongo-spark-connector_2.12-10.4.0.jar"
# "/opt/bitnami/spark/jars/postgresql-42.7.4.jar"
