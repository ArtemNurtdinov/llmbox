from dataclasses import dataclass

from app.config.domain.model.application import ApplicationConfig
from app.config.domain.model.logging import LoggingConfig
from app.config.domain.model.open_ai import OpenAIConfig
from app.config.domain.model.yandex import YandexConfig


@dataclass(frozen=True)
class Config:
    application: ApplicationConfig
    open_ai: OpenAIConfig
    yandex: YandexConfig
    logging: LoggingConfig
