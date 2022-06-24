"""
Configuration module
"""

import os
from pathlib import Path

from pydantic import BaseSettings

data_dir = Path(os.sep, "opt", "data")


class Config(BaseSettings):
    """
    Config class.
    """

    MONGODB_URI: str = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("DB_NAME")
    HARVESTER_OUTPUT_DIR = Path(data_dir, "marvel")
    PROCESSED_DIR = Path(data_dir, "processed")


pyspark_config = Config()
