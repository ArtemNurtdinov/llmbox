import os

from app.application.interfaces.config_source import ConfigSource


class EnvConfigSource(ConfigSource):

    def get(self, key: str, default: str | None = None) -> str | None:
        return os.getenv(key, default)

