"""
Mongo objects module
"""

import os

from pymongo import MongoClient

mongo = MongoClient(os.getenv("MONGODB_URI"))
# db = mongo[os.getenv("DB_NAME")]


def getdb():
    print(os.getenv("DB_NAME"))
    return mongo[os.getenv("DB_NAME")]


db = getdb()
