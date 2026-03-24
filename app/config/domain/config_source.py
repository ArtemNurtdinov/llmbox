from abc import ABC, abstractmethod


class ConfigSource(ABC):
    @abstractmethod
    def get(self, key: str, default: str | None = None) -> str | None: ...
