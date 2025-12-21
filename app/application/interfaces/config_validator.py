from typing import Protocol

from core.config import Config


class ConfigValidator(Protocol):
    """Validates configuration objects according to application rules."""

    def validate(self, config: Config) -> None:
        ...

