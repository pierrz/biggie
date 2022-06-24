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

    collection: str
    test_data = [
        {
            "a": 1,
            "b": 2.9,
            "c": "string1",
            "d": {"date": datetime(2000, 1, 1), "values": [list(range(5))]},
        },
        {
            "a": 2,
            "b": 3.9,
            "c": "string2",
            "d": {"date": datetime(2000, 2, 1), "values": [list(range(7))]},
        },
        {
            "a": 4,
            "b": 5.9,
            "c": "string3",
            "d": {"date": datetime(2000, 3, 1), "values": [list(range(3))]},
        },
    ]

    test_schema = StructType(
        [
            StructField("a", LongType(), True),
            StructField("b", DoubleType(), True),
            StructField("c", StringType(), True),
            StructField("d_date", TimestampType(), True),
            StructField(
                "d_values",
                ArrayType(ArrayType(LongType(), True), True),
                True,
            ),
        ]
    )

    def __init__(self, collection):
        self.collection = collection
