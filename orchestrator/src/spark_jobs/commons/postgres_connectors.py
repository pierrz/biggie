"""
Gathering all Spark/Postgres connector classes.
NB: since Postgres > v15.x, tables are not created automatically anymore
=> see test_postgres.py and the postgres_model fixture for further details
"""

import os
from abc import ABC
from typing import Iterable, Tuple

from pyspark.sql import DataFrame
from pyspark.sql import functions as psf
from src import logger
from src.db.postgres.postgres_db import HOST_DB, Base, pg_engine

from .connectors import ReaderBase
from .session import spark_session

pg_params = {
    "driver": "org.postgresql.Driver",
    "url": f"jdbc:postgresql://{HOST_DB}",
    "user": os.getenv("POSTGRES_APP_USER"),
    "password": os.getenv("POSTGRES_APP_PASSWORD"),
}


class PostgresBase(ABC):
    """
    Base class dedicated to defining the Mongo collection 'character' related to the Github Event API data
    """

    table: str
    check_columns: Iterable[psf.col]


class PostgresLoader(ABC):
    """
    Base class dedicated to load a specific Postgres table
    """

    def __init__(self, spark_df: DataFrame, table: str):
        logger.info("=> Loading Postgres ...")
        pg_params["dbtable"] = table
        # TODO: fix/implement with Postgres 16.4
        # pg_params["dbtable"] = f"{main_config.DB_USER}_schema.{table}"

        Base.metadata.create_all(pg_engine)  # /!\ IMPORTANT
        spark_df.write.format("jdbc").options(**pg_params).mode("append").save()


class PostgresReader(PostgresBase, ReaderBase):
    """
    Base class dedicated to read from a specific Postgres table
    """

    table: str

    def __init__(self, table: str = None, check_columns=None):

        if table is not None:
            self.table = table
        pg_params["dbtable"] = self.table
        db_data = spark_session.read.format("jdbc").options(**pg_params).load()
        logger.success(" ... data fetched from Postgres")

        if check_columns is None:
            self.preps_and_checks(db_data)
        self.preps_and_checks(db_data, check_columns)

    def _name(self) -> Tuple[str, str, str]:
        return self.table, "table", "PostgresReader"
