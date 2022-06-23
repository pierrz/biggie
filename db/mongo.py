"""
Mongo objects module
"""

import os

from pymongo import MongoClient

mongo = MongoClient(os.getenv("MONGODB_URI"))
# db = mongo[os.getenv("DB_NAME")]


def getdb():
    print(os.getenv("DB_NAME"))
    print(os.getenv("MONGODB_URI"))
    print(os.getenv("MONGO_INITDB_ROOT_USERNAME"))
    return mongo[os.getenv("DB_NAME")]


db = getdb()
