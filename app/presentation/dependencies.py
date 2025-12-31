from functools import lru_cache

from app.application.services import AIService
from app.composition.config_bootstrap import load_config
from app.composition.container import build_ai_service


@lru_cache
def get_ai_service() -> AIService:
    config = load_config()
    return build_ai_service(config)
