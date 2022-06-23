"""
Mongo objects module
"""

import os

from pymongo import MongoClient

mongo = MongoClient(os.getenv("MONGODB_URI"))
print(os.getenv("DB_NAME"))
db = mongo[os.getenv("DB_NAME")]
