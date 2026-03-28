from app.application.exceptions import ServiceUnavailableException
from app.application.mappers.dto_to_domain import to_domain_ai_messages_from_dto
from app.llm.application.mapper.ai_message_mapper import AIMessageMapper
from app.llm.application.model.request.vision import GenerateVisionAIRequestDTO
from app.llm.application.model.response.generate import AIResponseDTO
from app.llm.domain.llm_vision_repository import LLMVisionRepository
from app.llm.domain.model.ai_message import AIMessage


class GenerateVisionAIUseCase:
    def __init__(self, llm_vision_repository: LLMVisionRepository, ai_message_mapper: AIMessageMapper):
        self._llm_vision_repository = llm_vision_repository
        self._ai_message_mapper = ai_message_mapper

    async def execute(self, request: GenerateVisionAIRequestDTO) -> AIResponseDTO:
        messages = to_domain_ai_messages_from_dto(request)

        try:
            ai_message: AIMessage = await self._llm_vision_repository.generate_vision(messages)
            return self._ai_message_mapper.map_ai_message_to_dto(ai_message)
        except Exception as exc:
            raise ServiceUnavailableException("Failed to generate vision AI response", original_error=exc)
