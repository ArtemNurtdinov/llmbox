from functools import lru_cache

from app.application.services import AIService
from app.composition.container import build_ai_service
from app.infrastructure.config.env_config_provider import get_env_config_provider


@lru_cache()
def get_ai_service() -> AIService:
    config = get_env_config_provider().get_config()
    return build_ai_service(config)
