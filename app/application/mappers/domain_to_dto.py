from app.domain.models import AIResponse, Usage
from app.application.dto import AIResponseDTO, UsageDTO


def to_usage_dto(usage: Usage) -> UsageDTO:
    return UsageDTO(
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )


def to_ai_response_dto(response: AIResponse) -> AIResponseDTO:
    return AIResponseDTO(
        assistant_message=response.assistant_message,
        usage=to_usage_dto(response.usage),
    )

