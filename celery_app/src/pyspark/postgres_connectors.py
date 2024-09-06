"""
Gathering all Spark/Postgres connector classes
"""

import os
from abc import ABC
from typing import Iterable, Tuple

from pyspark.sql import DataFrame
from pyspark.sql import functions as psf
from src.db.postgres_db import host_db

from .connectors import ReaderBase
from .runner import spark_postgres

pg_params = {
    "driver": "org.postgresql.Driver",
    "url": f"jdbc:postgresql://{host_db}",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


class PostgresBase(ABC):
    """
    Base class dedicated to defining the Mongo collection 'character' related to the Marvel Characters API data
    """

    table: str
    check_columns: Iterable[psf.col]


class PostgresLoader(ABC):
    """
    Base class dedicated  to load a specific Postgres table
    """

    def __init__(self, spark_df: DataFrame, table: str):
        print("=> Loading Postgres ...")
        pg_params["dbtable"] = table
        spark_df.write.format("jdbc").options(**pg_params).mode("append").save()


class PostgresReader(PostgresBase, ReaderBase):
    """
    Base class dedicated  to load a specific Postgres table
    """

    table: str

    def __init__(self, table: str = None, check_columns=None):

        if table is not None:
            self.table = table
        pg_params["dbtable"] = self.table
        db_data = spark_postgres.read.format("jdbc").options(**pg_params).load()
        print(" ... data fetched from Postgres")

        if check_columns is None:
            self.preps_and_checks(db_data)
        self.preps_and_checks(db_data, check_columns)

    def _name(self) -> Tuple[str, str, str]:
        return self.table, "table", "PostgresReader"
