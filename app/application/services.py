import logging
from typing import Dict, List

from app.domain.interfaces import TextModelClient, VisionModelClient
from app.domain.models import AIMessage, AIResponse, Message, AIAssistant

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self, text_clients: Dict[AIAssistant, TextModelClient], vision_client: VisionModelClient):
        self._text_clients = text_clients
        self._vision_client = vision_client

    async def generate_ai_response(self, messages: List[Message], assistant: AIAssistant) -> AIResponse:
        logger.info("Generating AI response with assistant=%s", assistant.value)

        client = self._text_clients.get(assistant)
        if client is None:
            error_msg = f"Unknown AI assistant: {assistant}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            return await client.generate(messages)
        except Exception as exc:
            logger.error("Error generating AI response with %s: %s", assistant.value, exc, exc_info=True)
            raise

    async def generate_ai_response_vision(self, messages: List[AIMessage]) -> AIResponse:
        logger.info("Generating Vision AI response")
        try:
            return await self._vision_client.generate_vision(messages)
        except Exception as exc:
            logger.error("Error generating Vision AI response: %s", exc, exc_info=True)
            raise
