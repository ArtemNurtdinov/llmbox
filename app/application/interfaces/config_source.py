from typing import Protocol


class ConfigSource(Protocol):
    """Abstraction over configuration value retrieval."""

    def get(self, key: str, default: str | None = None) -> str | None:
        ...

