from app.application.dto import AIResponseDTO, UsageDTO
from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.usage import Usage


class AIMessageMapper:
    def map_ai_message_to_dto(self, message: AIMessage) -> AIResponseDTO:
        return AIResponseDTO(
            assistant_message=message.content,
            usage=self._map_usage(message.usage),
        )

    def _map_usage(self, usage: Usage) -> UsageDTO:
        return UsageDTO(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )
