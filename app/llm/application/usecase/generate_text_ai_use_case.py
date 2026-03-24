from app.application.dto import AIResponseDTO, GenerateAIRequestDTO
from app.application.exceptions import ServiceUnavailableException, ValidationException
from app.application.mappers.domain_to_dto import to_ai_response_dto
from app.application.mappers.dto_to_domain import to_domain_messages_from_dto
from app.domain.interfaces import TextModelClient
from app.domain.models import AIResponse
from app.llm.domain.model.assistant import AIAssistant


class GenerateTextAIUseCase:
    def __init__(self, text_clients: dict[AIAssistant, TextModelClient]):
        self._text_clients = text_clients

    async def execute(self, request: GenerateAIRequestDTO) -> AIResponseDTO:
        messages, assistant = to_domain_messages_from_dto(request)

        client = self._text_clients.get(assistant)
        if client is None:
            raise ValidationException(f"Unknown AI assistant: {assistant.value}")
        try:
            domain_response: AIResponse = await client.generate(messages)
            return to_ai_response_dto(domain_response)
        except Exception as exc:
            raise ServiceUnavailableException(f"Failed to generate AI response {assistant.value}", original_error=exc)
