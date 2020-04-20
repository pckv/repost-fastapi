import os
import secrets
from dataclasses import dataclass, asdict
from pathlib import Path

from dotenv import load_dotenv

env_path = Path.cwd() / 'config.env'
env_prefix = 'REPOST_'


@dataclass
class Config:
    """Definition and defaults for package configuration."""
    client_id: str = 'repost'
    jwt_secret: str = secrets.token_hex(32)
    jwt_algorithm: str = 'HS256'
    database_url: str = 'sqlite:///./repost.db'

    def initialize(self):
        """Initialize and load the config instance."""
        # Initialize config file with defaults if it does not exist
        if not env_path.exists():
            with env_path.open(mode='w') as f:
                f.write('\n'.join(f'{env_prefix}{key.upper()}={value}' for key, value in asdict(self).items()) + '\n')

        load_dotenv(dotenv_path=env_path, verbose=True)

        # Add environment variables to configurations
        for key, default in asdict(self).items():
            setattr(self, key, os.getenv(env_prefix + key.upper(), default))


config = Config()
