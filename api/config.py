"""
Configuration module
"""

from pydantic import BaseSettings


class Config(BaseSettings):
    """
    Config class.
    """

    LOCAL_DEV = True


app_config = Config()
