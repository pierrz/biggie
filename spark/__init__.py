"""
Module entry point
"""

import os

from .config import spark_config
from .src.jobs import SparkJobFromJson

if __name__ == "__main__":

    if not spark_config.PROCESSED_DIR.exists():
        os.mkdir(spark_config.PROCESSED_DIR)

    SparkJobFromJson()
