from app.application.dto import AIResponseDTO
from app.application.exceptions import ServiceUnavailableException
from app.application.mappers.dto_to_domain import to_domain_messages_from_dto
from app.llm.application.mapper.ai_message_mapper import AIMessageMapper
from app.llm.application.model.request.generate_text import GenerateAIRequestDTO
from app.llm.domain.llm_repository import LLMRepository
from app.llm.domain.model.ai_message import AIMessage


class GenerateTextAIUseCase:
    def __init__(self, llm_repository: LLMRepository, ai_message_mapper: AIMessageMapper):
        self._llm_repository = llm_repository
        self._ai_message_mapper = ai_message_mapper

    async def execute(self, request: GenerateAIRequestDTO) -> AIResponseDTO:
        messages, assistant = to_domain_messages_from_dto(request)

        try:
            ai_message: AIMessage = await self._llm_repository.generate(assistant, messages)
            return self._ai_message_mapper.map_ai_message_to_dto(ai_message)
        except Exception as exc:
            raise ServiceUnavailableException(f"Failed to generate AI response {assistant.value}", original_error=exc)
