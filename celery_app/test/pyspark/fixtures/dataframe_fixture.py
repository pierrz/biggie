"""
Test fixtures
"""

from datetime import datetime

# pylint: disable=E0611
from pyspark.sql.types import (ArrayType, DoubleType, LongType, StringType,
                               StructField, StructType, TimestampType)


class DataframeFixture:
    """
    Base class embeded with data to generate dataframes, eventually for specific collection
    """

    table_or_collection: str
    test_data = [
        {
            "event_id": "12364",
            "a": 1,
            "b": 2.9,
            "c": "string1",
            "d": {"date": datetime(2000, 1, 1), "values": list(range(5))},
            "created_at": "2022-04-03T13:40:21Z"
        },
        {
            "event_id": "6438748",
            "a": 2,
            "b": 3.9,
            "c": "string2",
            "d": {"date": datetime(2000, 2, 1), "values": list(range(7))},
            "created_at": "2023-02-01T10:00:11Z"
        },
        {
            "event_id": "420383",
            "a": 4,
            "b": 5.9,
            "c": "string3",
            "d": {"date": datetime(2000, 3, 1), "values": list(range(3))},
            "created_at": "2024-09-06T01:30:41Z"
        },
    ]

    # event_id and created_at are related to the Github specific cleaning
    test_schema = StructType([
        StructField("event_id", LongType(), True),
        StructField("a", LongType(), True),  # `a` is an (long AKA 64 bytes) integer
        StructField("b", DoubleType(), True),  # `b` is a float (double in PySpark)
        StructField("c", StringType(), True),  # `c` is a string
        StructField("d_date", TimestampType(), True),  # `d.date` is a datetime (flattened as `d_date`)
        StructField("d_values", ArrayType(LongType()), True),  # `d.values` is a list of integers
        StructField("created_at", TimestampType(), True)
    ])

    def __init__(self, table_or_collection):
        self.table_or_collection = table_or_collection
