"""
Configuration module
"""

from pathlib import Path

from pydantic_settings import BaseSettings

github_events = "github_events"
diagrams_dir = Path("templates", github_events, "diagrams")  # github endpoints specific


class Config(BaseSettings):
    """
    Config class.
    """

    LOCAL_DEV: bool = True


app_config = Config()
