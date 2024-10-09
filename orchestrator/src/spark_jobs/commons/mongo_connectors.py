"""
Mongo connectors
"""

# TODO: refactoring to discard all E0611 errors from pylint (currently ignored)

from abc import ABC
from typing import Iterable, Tuple

from config import main_config

# pylint: disable=E0611
from pyspark.sql import DataFrame
from pyspark.sql import functions as psf
from src import logger

from .connectors import ReaderBase
from .session import spark_session

mongo_params = {"database": main_config.DB_NAME}


class MongoCollection(ABC):
    """
    Base class defining a Mongo table name
    """

    collection: str


class MongoConnector(MongoCollection, ABC):
    """
    Base class extending MongoCollection with columns to check during data processes
    """

    check_columns: Iterable[psf.col]


class MongoLoader(ABC):
    """
    Base class dedicated  to load a specific Mongo collection
    """

    def __init__(self, spark_df: DataFrame, collection: str):
        logger.info("=> Loading Mongo ...")
        mongo_write_params = {
            "collection": collection,
            "uri": main_config.MONGODB_URI,
            **mongo_params,
        }
        spark_df.write.format("mongodb").options(**mongo_write_params).mode(
            "append"
        ).save()
        logger.success(" ... Mongo loaded")


class MongoReader(ReaderBase):
    """
    Base class dedicated to read data from a specific Mongo collection
    """

    collection: str

    def __init__(self):

        logger.info("=> Reading Mongo ...")
        mongo_read_params = {
            "collection": self.collection,
            **mongo_params,
        }
        db_data = (
            spark_session.read.format("mongodb").options(**mongo_read_params).load()
        )
        self.preps_and_checks(db_data)

    def _name(self) -> Tuple[str]:
        return self.collection, "collection", "MongoReader"
