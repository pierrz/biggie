from config import app_config
from pymongo import MongoClient

mongo = MongoClient(app_config.MONGODB_URI)
db = mongo[app_config.DB_NAME]
