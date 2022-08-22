"""
Mongo connectors
"""
# TODO: refactoring to discard all E1101 errors from pylint (currently ignored)

from abc import ABC
from typing import Iterable, Tuple

from config import pyspark_config
# pylint: disable=E0611
from pyspark.sql import DataFrame
from pyspark.sql import functions as psf

from .connectors import ReaderBase
from .runner import spark_mongo

mongo_params = {"database": pyspark_config.DB_NAME}


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
        print("=> Loading Mongo ...")
        mongo_params_with_uri = {
            "collection": collection,
            "uri": pyspark_config.MONGODB_URI,
            **mongo_params,
        }
        spark_df.write.format("mongo").options(**mongo_params_with_uri).mode(
            "append"
        ).save()
        print(" ... Mongo loaded")


class MongoReader(ReaderBase):
    """
    Base class dedicated to read data from a specific Mongo collection
    """

    def __init__(self):

        print("=> Reading Mongo ...")
        mongo_params["collection"] = self.collection
        db_data = spark_mongo.read.format("mongo").options(**mongo_params).load()
        self.preps_and_checks(db_data)

    def _name(self) -> Tuple[str]:
        return self.collection, "collection", "MongoReader"


class EventBase(MongoConnector, ABC):
    """
    Base class dedicated to defining the Mongo collection 'character' related to the Marvel Characters API data
    """

    collection = "event"
    check_columns = [
        psf.col("id"),
        psf.col("type"),
        psf.col("actor_id"),
        psf.col("repo_name"),
    ]


class EventLoader(EventBase, MongoLoader):
    """
    Class dedicated to load the Mongo collection 'event' with new data
    """


class EventReader(EventBase, MongoReader):
    """
    Class dedicated to read data from the Mongo collection 'event'
    """
