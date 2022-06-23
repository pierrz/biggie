"""
Mongo objects module
"""

import os

from pymongo import MongoClient

mongo = MongoClient(os.getenv("MONGODB_URI"))
db = mongo[os.getenv("DB_NAME")]
