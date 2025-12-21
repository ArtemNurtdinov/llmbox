import logging
from typing import Dict

from app.domain.interfaces import TextModelClient
from app.domain.models import AIAssistant, AIResponse
from app.domain.exceptions import (
    UnknownAIAssistantException,
    AIServiceException,
    DomainException,
)
from app.application.dto import AIResponseDTO, GenerateAIRequestDTO
from app.application.mappers.domain_to_dto import to_ai_response_dto
from app.application.mappers.dto_to_domain import to_domain_messages_from_dto
from app.application.exceptions import ValidationException, ServiceUnavailableException

logger = logging.getLogger(__name__)


class GenerateTextAIUseCase:

    def __init__(self, text_clients: Dict[AIAssistant, TextModelClient]):
        self._text_clients = text_clients

    async def execute(self, request: GenerateAIRequestDTO) -> AIResponseDTO:
        logger.info("Executing GenerateTextAIUseCase with assistant=%s", request.assistant)

        messages, assistant = to_domain_messages_from_dto(request)

        client = self._text_clients.get(assistant)
        if client is None:
            raise ValidationException(f"Unknown AI assistant: {assistant.value}")
        try:
            domain_response: AIResponse = await client.generate(messages)
            return to_ai_response_dto(domain_response)
        except UnknownAIAssistantException as exc:
            raise ValidationException(str(exc))
        except AIServiceException as exc:
            raise ServiceUnavailableException(str(exc), original_error=exc)
        except DomainException as exc:
            raise ValidationException(str(exc))
        except Exception as exc:
            logger.error("Error in GenerateTextAIUseCase with assistant=%s: %s",assistant.value, exc, exc_info=True)
            raise ServiceUnavailableException(
                f"Failed to generate AI response with assistant {assistant.value}",
                original_error=exc,
            )

