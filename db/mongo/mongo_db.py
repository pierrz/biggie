"""
Mongo objects module
"""

from config import main_config
from pymongo import MongoClient


def init_pymongo_client():
    mongo_client = MongoClient(main_config.MONGODB_URI)
    return mongo_client
