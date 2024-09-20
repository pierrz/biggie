# pylint: disable=E0611
from pyspark.sql.types import (
    ArrayType,
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

test_mongo_schema = StructType(
    [
        StructField("a", LongType(), True),  # `a` is an (long AKA 64 bytes) integer
        StructField("b", DoubleType(), True),  # `b` is a float (double in PySpark)
        StructField("c", StringType(), True),  # `c` is a string
        StructField(
            "d_date", TimestampType(), True
        ),  # `d.date` is a datetime (flattened as `d_date`)
        StructField(
            "d_values", ArrayType(LongType()), True
        ),  # `d.values` is a list of integers
    ]
)
