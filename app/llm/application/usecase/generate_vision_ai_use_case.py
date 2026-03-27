from app.application.dto import AIResponseDTO, GenerateVisionAIRequestDTO
from app.application.exceptions import ServiceUnavailableException
from app.application.mappers.domain_to_dto import to_ai_response_dto
from app.application.mappers.dto_to_domain import to_domain_ai_messages_from_dto
from app.llm.domain.llm_vision_repository import LLMVisionRepository
from app.llm.domain.model.ai_message import AIMessage


class GenerateVisionAIUseCase:
    def __init__(self, llm_vision_repository: LLMVisionRepository):
        self._llm_vision_repository = llm_vision_repository

    async def execute(self, request: GenerateVisionAIRequestDTO) -> AIResponseDTO:
        messages = to_domain_ai_messages_from_dto(request)

        try:
            ai_message: AIMessage = await self._llm_vision_repository.generate_vision(messages)
            return to_ai_response_dto(ai_message)
        except Exception as exc:
            raise ServiceUnavailableException("Failed to generate vision AI response", original_error=exc)
