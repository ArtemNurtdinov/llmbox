import logging
from typing import Dict

from app.domain.interfaces import TextModelClient, VisionModelClient
from app.domain.models import AIResponse, AIAssistant
from app.application.dto import AIResponseDTO, GenerateAIRequestDTO, GenerateVisionAIRequestDTO
from app.application.mappers.domain_to_dto import to_ai_response_dto
from app.application.mappers.dto_to_domain import to_domain_messages_from_dto, to_domain_ai_messages_from_dto

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self, text_clients: Dict[AIAssistant, TextModelClient], vision_client: VisionModelClient):
        self._text_clients = text_clients
        self._vision_client = vision_client

    async def generate_ai_response(self, dto: GenerateAIRequestDTO) -> AIResponseDTO:
        logger.info("Generating AI response with assistant=%s", dto.assistant)

        messages, assistant = to_domain_messages_from_dto(dto)

        client = self._text_clients.get(assistant)
        if client is None:
            error_msg = f"Unknown AI assistant: {assistant.value}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            domain_response: AIResponse = await client.generate(messages)
            return to_ai_response_dto(domain_response)
        except Exception as exc:
            logger.error("Error generating AI response with %s: %s", assistant.value, exc, exc_info=True)
            raise

    async def generate_ai_response_vision(self, dto: GenerateVisionAIRequestDTO) -> AIResponseDTO:
        logger.info("Generating Vision AI response")

        messages = to_domain_ai_messages_from_dto(dto)
        
        try:
            domain_response: AIResponse = await self._vision_client.generate_vision(messages)
            return to_ai_response_dto(domain_response)
        except Exception as exc:
            logger.error("Error generating Vision AI response: %s", exc, exc_info=True)
            raise
