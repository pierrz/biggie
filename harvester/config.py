"""
Configuration module
"""

import os
from datetime import datetime
from hashlib import md5
from pathlib import Path
from typing import Tuple

from pydantic import BaseSettings


class Config(BaseSettings):
    """
    Config class.
    """

    API_PUBLIC_KEY: str = os.getenv("API_PUBLIC_KEY")
    API_PRIVATE_KEY: str = os.getenv("API_PRIVATE_KEY")
    OUTPUT_DIR = Path(os.sep, "opt", "data", "marvel")

    def generate_auth_parts(self) -> Tuple[str, str]:
        """
        chunks a string such as md5(ts+privateKey+publicKey)
        :return: the hashed key
        """
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{timestamp}{self.API_PRIVATE_KEY}{self.API_PUBLIC_KEY}"
        return timestamp, md5(hash_input.encode("utf-8")).hexdigest()


harvester_config = Config()
