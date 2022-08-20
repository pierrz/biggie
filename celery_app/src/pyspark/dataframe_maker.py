"""
Module dedicated to constructing Spark dataframes
"""

from abc import ABC, abstractmethod
from typing import Dict, Iterable

import pandas as pd
# pylint: disable=E0611
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

from .mongo_connectors import MongoLoader
from .postgres_connectors import PostgresLoader
from .runner import spark_mongo, spark_postgres


class DataframeMaker(ABC):
    """
    Class used to read data and transform it into PySpark dataframe.
    Can also load the produced data into Mongo.
    """

    flat_df: pd.DataFrame
    spark_df: DataFrame
    schema: StructType
    check_columns: Iterable[str] = None

    def __init__(
        self,
        table_or_collection: str,
        check_columns=check_columns,
    ):

        self.check_columns = check_columns
        self.table_or_collection = table_or_collection

    def store_spark_df(self, df):
        """
        Stores the spark df elements into this instance
        :param df: the dataframe to handle
        """
        self.spark_df = df
        self.schema = self.spark_df.schema
        # # extended logs (extra info for celery)
        # print("... PySpark dataframe prepared with inferred schema:\n")
        # self.spark_df.printSchema()
        # self.spark_df.select(*self.check_columns).show()

    def normalize_input_data(self, input_array: Iterable[Dict]):
        """
        Takes the input data and clean/normalise it
        :return: does its thing
        """
        print("=> Normalising data ...")
        flat_df: pd.DataFrame = pd.json_normalize(input_array, sep="_")

        # hack to load Mongo seamlessly
        print("=> Preparing dataframe ...")
        columns_to_drop = []
        mapper = {}
        for col in flat_df.columns.to_list():

            # specific to github api data (minimize)
            if col.startswith("payload_") or col.startswith("org_"):
                columns_to_drop.append(col)

        if len(columns_to_drop) > 0:
            flat_df.drop(
                columns=columns_to_drop, inplace=True
            )  # reducing the loaded data (prod)

        flat_df.rename(columns=mapper, inplace=True)
        print(" ... dataframe finalised")

        columns = flat_df.columns.to_list()
        print(f"=> {flat_df.shape[0]} rows and {len(columns)} columns")

        # # extended logs (extra info for celery)
        # print(columns)
        # if self.check_columns is not None:
        #     print(flat_df[self.check_columns])
        self.flat_df = flat_df

    @abstractmethod
    def prepare_spark_dataframes(self, **kwargs):
        """
        Gets the right spark engine and then prepare the dataframe with it
        """


class MongoDataframeMaker(DataframeMaker):

    def __init__(self, input_array, table_or_collection, check_columns):
        super().__init__(table_or_collection, check_columns)
        self.normalize_input_data(input_array)
        self.prepare_spark_dataframes()

    def prepare_spark_dataframes(self):
        """
        Generates the PySpark dataframes from the cleaned/normalised data
        :return: does its thing
        """
        print("=> Preparing PySpark dataframe for Mongo ...")
        spark_df = spark_mongo.createDataFrame(data=self.flat_df)
        self.store_spark_df(spark_df)

    def load_mongo(self):
        """
        Load mongo with the produced PySpark dataframes
        :return: does its thing
        """
        return MongoLoader(self.spark_df, self.table_or_collection)


class PostgresDataframeMaker(DataframeMaker):

    def __init__(self, array_or_dataframe, table_or_collection, check_columns):
        super().__init__(table_or_collection, check_columns)
        if isinstance(array_or_dataframe, pd.DataFrame):
            self.prepare_spark_dataframes(array_or_dataframe)
        else:
            self.normalize_input_data(array_or_dataframe)
            self.prepare_spark_dataframes()

    def prepare_spark_dataframes(self, df: pd.DataFrame = None):
        """
        Generates the PySpark dataframes from the cleaned/normalised data
        :return: does its thing
        """
        print("=> Preparing PySpark dataframe for Postgres ...")

        if df is None:
            spark_df = spark_postgres.createDataFrame(data=self.flat_df)
        else:
            spark_df = spark_postgres.createDataFrame(data=df)

        self.store_spark_df(spark_df)

    def load_postgres(self):
        """
        Load mongo with the produced PySpark dataframes
        :return: does its thing
        """
        return PostgresLoader(self.spark_df, self.table_or_collection)
