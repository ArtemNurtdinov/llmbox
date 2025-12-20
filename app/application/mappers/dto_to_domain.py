from app.domain.models import (
    AIMessage,
    ImageContentItem,
    Message,
    TextContentItem,
    AIAssistant as DomainAIAssistant,
    Role as DomainRole,
    ContentType as DomainContentType,
)
from app.application.dto import (
    MessageDTO,
    AIMessageDTO,
    TextContentItemDTO,
    ImageContentItemDTO,
    GenerateAIRequestDTO,
    GenerateVisionAIRequestDTO,
)
from app.application.dto import (
    Role as ApplicationRole,
    ContentType as ApplicationContentType,
    AIAssistant as ApplicationAIAssistant,
)


def _to_domain_role(role: ApplicationRole) -> DomainRole:
    return DomainRole(role.value)


def _to_domain_content_type(content_type: ApplicationContentType) -> DomainContentType:
    return DomainContentType(content_type.value)


def _to_domain_ai_assistant(assistant: ApplicationAIAssistant) -> DomainAIAssistant:
    return DomainAIAssistant(assistant.value)


def to_domain_message(dto: MessageDTO) -> Message:
    domain_role = _to_domain_role(dto.role)
    return Message(role=domain_role, content=dto.content)


def to_domain_ai_message(dto: AIMessageDTO) -> AIMessage:
    domain_role = _to_domain_role(dto.role)
    content_items = []
    for item in dto.content:
        if isinstance(item, TextContentItemDTO):
            domain_content_type = _to_domain_content_type(item.type)
            content_items.append(TextContentItem(text=item.text, type=domain_content_type))
        elif isinstance(item, ImageContentItemDTO):
            domain_content_type = _to_domain_content_type(item.type)
            content_items.append(ImageContentItem(image_base64=item.image_base64, type=domain_content_type))
        else:
            raise ValueError(f"Unknown content item type: {type(item)}")

    return AIMessage(role=domain_role, content=content_items)


def to_domain_messages_from_dto(dto: GenerateAIRequestDTO) -> tuple[list[Message], DomainAIAssistant]:
    messages = [to_domain_message(msg) for msg in dto.messages]
    domain_assistant = _to_domain_ai_assistant(dto.assistant)
    return messages, domain_assistant


def to_domain_ai_messages_from_dto(dto: GenerateVisionAIRequestDTO) -> list[AIMessage]:
    return [to_domain_ai_message(msg) for msg in dto.messages]
