from typing import Protocol

from core.config import Config


class ConfigProvider(Protocol):
    """Provides application configuration."""

    def get_config(self) -> Config:
        ...

