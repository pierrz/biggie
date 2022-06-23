"""
Module entry point
"""

import os

from config import pyspark_config
from src.jobs import SparkJobFromJson

if __name__ == "__main__":

    if not pyspark_config.PROCESSED_DIR.exists():
        os.mkdir(pyspark_config.PROCESSED_DIR)

    SparkJobFromJson()
