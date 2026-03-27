from app.application.dto import AIResponseDTO, UsageDTO
from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.usage import Usage


def to_usage_dto(usage: Usage) -> UsageDTO:
    return UsageDTO(
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )


def to_ai_response_dto(message: AIMessage) -> AIResponseDTO:
    return AIResponseDTO(
        assistant_message=message.content,
        usage=to_usage_dto(message.usage),
    )
