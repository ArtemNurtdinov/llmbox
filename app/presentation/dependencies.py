from functools import lru_cache

from core.config import load_config
from app.application.services import AIService
from app.infrastructure.di import create_ai_service


@lru_cache()
def get_ai_service() -> AIService:
    config = load_config()
    return create_ai_service(config)
