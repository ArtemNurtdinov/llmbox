from app.application.dto import AIResponseDTO, GenerateAIRequestDTO
from app.application.exceptions import ServiceUnavailableException
from app.application.mappers.domain_to_dto import to_ai_response_dto
from app.application.mappers.dto_to_domain import to_domain_messages_from_dto
from app.llm.domain.llm_repository import LLMRepository
from app.llm.domain.model.ai_message import AIMessage


class GenerateTextAIUseCase:
    def __init__(self, llm_repository: LLMRepository):
        self._llm_repository = llm_repository

    async def execute(self, request: GenerateAIRequestDTO) -> AIResponseDTO:
        messages, assistant = to_domain_messages_from_dto(request)

        try:
            ai_message: AIMessage = await self._llm_repository.generate(assistant, messages)
            return to_ai_response_dto(ai_message)
        except Exception as exc:
            raise ServiceUnavailableException(f"Failed to generate AI response {assistant.value}", original_error=exc)
