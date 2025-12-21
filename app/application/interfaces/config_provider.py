from typing import Protocol

from core.config import Config


class ConfigProvider(Protocol):

    def get_config(self) -> Config:
        ...