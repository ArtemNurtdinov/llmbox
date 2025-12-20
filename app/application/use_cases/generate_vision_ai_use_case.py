import logging

from app.domain.interfaces import VisionModelClient
from app.domain.models import AIResponse
from app.application.dto import AIResponseDTO, GenerateVisionAIRequestDTO
from app.application.mappers.domain_to_dto import to_ai_response_dto
from app.application.mappers.dto_to_domain import to_domain_ai_messages_from_dto

logger = logging.getLogger(__name__)


class GenerateVisionAIUseCase:

    def __init__(self, vision_client: VisionModelClient):
        self._vision_client = vision_client

    async def execute(self, request: GenerateVisionAIRequestDTO) -> AIResponseDTO:
        logger.info("Executing GenerateVisionAIUseCase")

        messages = to_domain_ai_messages_from_dto(request)

        try:
            domain_response: AIResponse = await self._vision_client.generate_vision(messages)
            return to_ai_response_dto(domain_response)
        except Exception as exc:
            logger.error(
                "Error in GenerateVisionAIUseCase: %s",
                exc,
                exc_info=True
            )
            raise

