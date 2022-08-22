"""
Configuration module
"""

from pathlib import Path

from pydantic import BaseSettings

diagrams_dir = Path("templates", "diagrams")  # github endpoints specific


class Config(BaseSettings):
    """
    Config class.
    """

    LOCAL_DEV = True


app_config = Config()
