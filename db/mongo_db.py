"""
Mongo objects module
"""

import os

from pymongo import MongoClient


def init_pymongo_client():
    mongo = MongoClient(os.getenv("MONGODB_URI"))
    return mongo[os.getenv("DB_NAME")]
