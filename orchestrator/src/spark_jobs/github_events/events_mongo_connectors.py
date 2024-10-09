from abc import ABC

from pyspark.sql import functions as psf
from src.commons import names as ns
from src.spark_jobs.commons.mongo_connectors import (
    MongoConnector,
    MongoLoader,
    MongoReader,
)


class EventBase(MongoConnector, ABC):
    """
    Base class dedicated to defining the Mongo collection 'event' related to the Github Event API data
    """

    collection = ns.events
    check_columns = [
        psf.col("event_id"),
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
