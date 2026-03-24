from abc import ABC, abstractmethod

from app.config.domain.model.configuration import Config


class ConfigValidator(ABC):
    @abstractmethod
    def validate(self, config: Config) -> None: ...
