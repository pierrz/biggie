"""
Mongo connectors
"""

from abc import ABC
from typing import Dict, Iterable, List

import pandas as pd
from config import app_config
from pyspark.sql import DataFrame
from pyspark.sql import functions as psf
from pyspark.sql.types import StructType

from .runner import spark


class MongoCollection(ABC):
    collection: str


class MongoConnector(MongoCollection, ABC):
    check_columns: Iterable[psf.col]


class DataframeMaker(MongoCollection, ABC):
    input_array: Iterable[Dict]
    flat_df: pd.DataFrame
    spark_df: DataFrame
    schema: StructType
    check_columns: Iterable[str] = None

    def __init__(
        self, input_array: List[Dict], collection: str, check_columns=check_columns
    ):
        self.check_columns = check_columns
        self.collection = collection
        self.input_array = input_array
        self.normalize_input_data()
        self.prepare_spark_dataframes()

    def normalize_input_data(self):
        print("=> Normalising pandas dataframe ...")
        flat_df: pd.DataFrame = pd.json_normalize(self.input_array)
        mapper = {}
        for col in flat_df.columns.to_list():
            if "." in col:
                mapper[col] = col.replace(".", "_")
        flat_df.rename(columns=mapper, inplace=True)

        print(" ... dataframe normalised")
        columns = flat_df.columns.to_list()
        print(f"with {flat_df.shape[0]} rows and {len(columns)} columns")
        print(columns)
        if self.check_columns is not None:
            print(flat_df[self.check_columns])
        self.flat_df = flat_df

    def prepare_spark_dataframes(self):
        print("=> Preparing PySpark dataframe")
        df = spark.createDataFrame(data=self.flat_df)
        self.spark_df = df
        print("... PySpark dataframe prepared with inferred schema:\n")
        df.printSchema()
        self.schema = df.schema
        self.spark_df.select(*self.check_columns)

    def load_mongo(self):
        return MongoLoader(self.spark_df, self.collection)


class MongoLoader(ABC):
    def __init__(self, spark_df: DataFrame, collection: str):
        print("=> Loading Mongo ...")
        spark_df.write.format("mongo").options(
            uri=app_config.MONGODB_URI,
            database=app_config.DB_NAME,
            collection=collection,
        ).mode("append").save()
        print(" ... Mongo loaded")


class MongoReader(ABC):
    db_data: DataFrame
    schema: StructType
    initial_id_col: List
    columns: Iterable[str]
    n_rows: int

    def __init__(self):

        print("=> Reading Mongo ...")
        db_data = (
            spark.read.format("mongo")
            .option("database", app_config.DB_NAME)
            .option("collection", self.collection)
            .load()
        )

        # preps
        self.n_rows = db_data.count()
        self.columns = list(db_data.columns)
        print(self.columns)
        self.initial_id_col = self.columns[
            1
        ]  # hack to enforce ascending order (test purpose)
        self.db_data = db_data.sort(self.initial_id_col)
        self.schema = self.db_data.schema

        # checks
        print(self.__repr__())
        self.db_data.select(*self.check_columns)

    def __str__(self):
        trimmed_cols_str = str([*self.columns[:3]])[1:-1]
        columns_trimmed = f"[{trimmed_cols_str}, ...]"
        return (
            f"Spark dataframe from Mongo collection '{self.collection}' "
            f"with {self.db_data.count()} rows and {len(self.columns)} columns {columns_trimmed}"
        )

    def __repr__(self):
        return f"MongoReader('{self.collection}' collection, {len(self.columns)} columns, {self.db_data.count()} rows)"


class CharacterBase(MongoConnector, ABC):
    collection = "character"
    check_columns = [
        psf.col("id"),
        psf.col("name"),
        psf.col("description"),
        psf.col("comics_available"),
    ]


class CharacterLoader(CharacterBase, MongoLoader):
    pass


class CharacterReader(CharacterBase, MongoReader):
    pass
