"""
Configuration module
"""

from pathlib import Path

from pydantic_settings import BaseSettings
from src.commons import names as ns

diagrams_dir = Path(
    "templates", ns.github_events, ns.diagrams
)  # github endpoints specific


class MainConfig(BaseSettings):
    """
    Config class.
    """

    API_PORT: str
    DOCKER_SUBNET_BASE: str
    DB_NAME: str
    MONGODB_URI: str
    POSTGRESDB_HOST: str
    POSTGRES_APP_USER: str
    POSTGRES_APP_PASSWORD: str


main_config = MainConfig()
