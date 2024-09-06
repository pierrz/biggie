from pyspark.sql.types import (LongType, StringType, StructField, StructType,
                               TimestampType)

# Based on api.src.db.mongo.models -> Event
event_schema = StructType([
    # StructField("id", StringType(), True),  # `PyObjectId` -> StringType
    StructField("event_id", LongType(), True),  # `int` -> IntegerType
    StructField("type", StringType(), True),  # `EventType` -> StringType (since it's an Enum)
    StructField("public", StringType(), True),  # `str` -> StringType
    StructField("created_at", TimestampType(), True),  # `datetime` -> TimestampType
    StructField("org", StringType(), True),  # `str` -> StringType
    StructField("actor_id", LongType(), True),  # `int` -> IntegerType
    StructField("actor_login", StringType(), True),  # `str` -> StringType
    StructField("actor_display_login", StringType(), True),  # `str` -> StringType
    StructField("actor_gravatar_id", StringType(), True),  # `str` -> StringType
    StructField("actor_url", StringType(), True),  # `HttpUrl` -> StringType
    StructField("actor_avatar_url", StringType(), True),  # `HttpUrl` -> StringType
    StructField("repo_id", LongType(), True),  # `int` -> IntegerType
    StructField("repo_name", StringType(), True),  # `str` -> StringType
    StructField("repo_url", StringType(), True),  # `HttpUrl` -> StringType
])
