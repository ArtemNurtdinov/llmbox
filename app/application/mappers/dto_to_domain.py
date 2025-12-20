from app.domain.models import AIMessage, ImageContentItem, Message, TextContentItem, ContentType, Role, AIAssistant
from app.application.dto import MessageDTO, AIMessageDTO, TextContentItemDTO, ImageContentItemDTO, GenerateAIRequestDTO, \
    GenerateVisionAIRequestDTO


def map_role_str_to_domain(role: str) -> Role:
    match role:
        case "system":
            return Role.SYSTEM
        case "user":
            return Role.USER
        case "assistant":
            return Role.ASSISTANT
        case _:
            raise ValueError(f"Unknown role: {role}")


def map_content_type_str_to_domain(content_type: str) -> ContentType:
    match content_type:
        case "text":
            return ContentType.TEXT
        case "image_url":
            return ContentType.IMAGE_URL
        case _:
            raise ValueError(f"Unknown content type: {content_type}")


def map_assistant_str_to_domain(assistant: str) -> AIAssistant:
    match assistant:
        case "chat_gpt":
            return AIAssistant.CHAT_GPT
        case "yandex_gpt":
            return AIAssistant.YANDEX_GPT
        case "gpt_oss_120b":
            return AIAssistant.GPT_OSS_120B
        case "gpt_oss_20b":
            return AIAssistant.GPT_OSS_20B
        case "qwen3_235b":
            return AIAssistant.QWEN3_235B
        case _:
            raise ValueError(f"Unknown assistant: {assistant}")


def to_domain_message(dto: MessageDTO) -> Message:
    role = map_role_str_to_domain(dto.role)
    return Message(role=role, content=dto.content)


def to_domain_ai_message(dto: AIMessageDTO) -> AIMessage:
    role = map_role_str_to_domain(dto.role)
    content_items = []
    for item in dto.content:
        if isinstance(item, TextContentItemDTO):
            content_items.append(TextContentItem(text=item.text))
        elif isinstance(item, ImageContentItemDTO):
            content_items.append(ImageContentItem(image_base64=item.image_base64))
        else:
            raise ValueError(f"Unknown content item type: {type(item)}")

    return AIMessage(role=role, content=content_items)


def to_domain_messages_from_dto(dto: GenerateAIRequestDTO) -> tuple[list[Message], AIAssistant]:
    messages = [to_domain_message(msg) for msg in dto.messages]
    assistant = map_assistant_str_to_domain(dto.assistant)
    return messages, assistant


def to_domain_ai_messages_from_dto(dto: GenerateVisionAIRequestDTO) -> list[AIMessage]:
    return [to_domain_ai_message(msg) for msg in dto.messages]
