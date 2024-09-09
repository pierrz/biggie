"""
Module dedicated to constructing Spark dataframes

TODO:
- typing
- fully align Mongo and Postgres DataframeMaker (investigate)
"""

from abc import ABC, abstractmethod
from typing import Callable, Dict, Iterable, Optional, Type, Union

import pandas as pd

# pylint: disable=E0611
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from src import logger
from src.commons import names as ns

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
    custom_preps: Optional[Union[Callable, Type]]

    def __init__(
        self,
        table_or_collection: str,
        custom_preps,
        check_columns=check_columns,
    ):

        self.check_columns = check_columns
        self.table_or_collection = table_or_collection
        self.custom_preps = custom_preps

    def store_spark_df(self, df):
        """
        Stores the spark df elements into this instance
        :param df: the dataframe to handle
        """
        self.spark_df = df
        self.schema = self.spark_df.schema
        # # extended logs (extra info for celery)
        # logger.info("... PySpark dataframe prepared with inferred schema:\n")
        # self.spark_df.printSchema()
        # self.spark_df.select(*self.check_columns).show()

    def normalize_input_data(self, input_array: Iterable[Dict]):
        """
        Takes the input data and clean/normalise it
        :return: does its thing
        """
        logger.info("=> Normalising data ...")
        flat_df: pd.DataFrame = pd.json_normalize(input_array, sep="_")

        if self.custom_preps is not None:
            self.custom_preps(flat_df)

        self.flat_df = flat_df

    @abstractmethod
    def prepare_spark_dataframes(self, **kwargs):
        """
        Gets the right spark engine and then prepare the dataframe with it
        """


class MongoDataframeMaker(DataframeMaker):
    def __init__(
        self,
        input_array,
        table_or_collection,
        check_columns,
        custom_preps=None,
        schema: StructType = None,
    ):
        try:
            super().__init__(table_or_collection, custom_preps, check_columns)
            self.normalize_input_data(input_array)
            self.prepare_spark_dataframes(schema)

        except Exception as exception:
            logger.error("Error while preparing the data for Spark ...")
            logger.error(exception)

    def prepare_spark_dataframes(self, schema: StructType = None):
        """
        Generates the PySpark dataframes from the cleaned/normalised data
        :return: does its thing
        """
        logger.info("=> Preparing PySpark dataframe for Mongo ...")

        parameters = {ns.data: self.flat_df}
        if schema is not None:
            parameters[ns.schema] = schema

        spark_df = spark_mongo.createDataFrame(**parameters)
        self.store_spark_df(spark_df)

    def load_mongo(self):
        """
        Load mongo with the produced PySpark dataframes
        :return: does its thing
        """
        return MongoLoader(self.spark_df, self.table_or_collection)


class PostgresDataframeMaker(DataframeMaker):
    """
    TODO: align with MongoDataframeMaker (property names, flow)
    """

    def __init__(
        self,
        array_or_dataframe,
        table_or_collection,
        check_columns,
        custom_preps=None,
        schema: StructType = None,
    ):
        try:
            super().__init__(table_or_collection, custom_preps, check_columns)
            if isinstance(array_or_dataframe, pd.DataFrame):
                self.prepare_spark_dataframes(array_or_dataframe)
            else:
                self.normalize_input_data(array_or_dataframe)
                self.prepare_spark_dataframes(schema)

        except Exception as exception:
            logger.error("Error while preparing the data for Spark ...")
            logger.error(exception)

    def prepare_spark_dataframes(
        self, df: pd.DataFrame = None, schema: StructType = None
    ):
        """
        Generates the PySpark dataframes from the cleaned/normalised data
        :return: does its thing
        """
        logger.info("=> Preparing PySpark dataframe for Postgres ...")

        if df is None:
            parameters = {ns.data: self.flat_df}
        else:
            parameters = {ns.data: df}

        if schema is not None:
            parameters[ns.schema] = schema

        spark_df = spark_postgres.createDataFrame(**parameters)
        self.store_spark_df(spark_df)

    def load_postgres(self):
        """
        Load mongo with the produced PySpark dataframes
        :return: does its thing
        """
        return PostgresLoader(self.spark_df, self.table_or_collection)
