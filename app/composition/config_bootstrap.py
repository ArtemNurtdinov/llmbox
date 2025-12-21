from functools import lru_cache

from core.config import Config

from app.application.services.config_validator import AppConfigValidator
from app.infrastructure.config.env_config_provider import EnvConfigProvider
from app.infrastructure.config.env_config_source import EnvConfigSource


@lru_cache()
def load_config() -> Config:
    provider = EnvConfigProvider(EnvConfigSource(), AppConfigValidator())
    return provider.get_config()

