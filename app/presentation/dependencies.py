from functools import lru_cache

from app.application.services import AIService
from app.composition.container import build_ai_service
from app.infrastructure.config.env_config_provider import EnvConfigProvider


@lru_cache()
def get_ai_service() -> AIService:
    provider = EnvConfigProvider()
    config = provider.get_config()
    return build_ai_service(config)
