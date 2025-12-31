from app.application.dto import (
    AIMessageDTO,
    GenerateAIRequestDTO,
    GenerateVisionAIRequestDTO,
    ImageContentItemDTO,
    MessageDTO,
    TextContentItemDTO,
)
from app.application.exceptions import ValidationException
from app.domain.models import (
    AIAssistant as DomainAIAssistant,
)
from app.domain.models import (
    AIMessage,
    ImageContentItem,
    Message,
    TextContentItem,
)


def to_domain_message(dto: MessageDTO) -> Message:
    return Message(role=dto.role, content=dto.content)


def to_domain_ai_message(dto: AIMessageDTO) -> AIMessage:
    content_items = []
    for item in dto.content:
        if isinstance(item, TextContentItemDTO):
            content_items.append(TextContentItem(text=item.text, type=item.type))
        elif isinstance(item, ImageContentItemDTO):
            content_items.append(ImageContentItem(image_base64=item.image_base64, type=item.type))
        else:
            raise ValidationException(f"Unknown content item type: {type(item)}")

    return AIMessage(role=dto.role, content=content_items)


def to_domain_messages_from_dto(dto: GenerateAIRequestDTO) -> tuple[list[Message], DomainAIAssistant]:
    messages = [to_domain_message(msg) for msg in dto.messages]
    return messages, dto.assistant


def to_domain_ai_messages_from_dto(dto: GenerateVisionAIRequestDTO) -> list[AIMessage]:
    return [to_domain_ai_message(msg) for msg in dto.messages]
