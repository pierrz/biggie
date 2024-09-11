"""
Configuration module
"""

from pathlib import Path

from pydantic_settings import BaseSettings

diagrams_dir = Path("templates", "diagrams")  # github endpoints specific


class Config(BaseSettings):
    """
    Config class.
    """

    LOCAL_DEV: bool = True


app_config = Config()
