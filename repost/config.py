"""Singleton configuration based on environment variables."""

import os
import secrets
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

from dotenv import load_dotenv

env_path = Path.cwd() / 'config.env'
env_prefix = 'REPOST_'


def _format_key(key: str) -> str:
    """Format the key as an environment variable, and remove prefixed
    underscores from the key to allow properties in Config.
    """
    return env_prefix + key.upper().lstrip('_')


@dataclass
class Config:
    """Definition and defaults for package configuration."""
    client_id: str = 'repost'
    jwt_secret: str = secrets.token_hex(32)
    jwt_algorithm: str = 'HS256'
    database_url: str = 'sqlite:///./repost.db'
    _origins: str = 'http://localhost;http://localhost:8080'

    @property
    def origins(self) -> List[str]:
        return self._origins.split(';')

    def __init__(self):
        """Initialize and load the config instance."""
        # Initialize config file with defaults if it does not exist
        if not env_path.exists():
            with env_path.open(mode='w') as f:
                f.write('\n'.join(f'{_format_key(key)}={value}' for key, value in asdict(self).items()) + '\n')

        load_dotenv(dotenv_path=env_path, verbose=True)

        # Add environment variables to configurations
        for key, default in asdict(self).items():
            setattr(self, key, os.getenv(_format_key(key), default))


config = Config()
