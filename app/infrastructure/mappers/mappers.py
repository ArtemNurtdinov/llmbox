from app.domain.models import AIMessage, AIResponse, ImageContentItem, Message, TextContentItem, ContentType
from app.infrastructure.api.schemas import AIMessageSchema, AIResponseSchema, MessageSchema, UsageSchema

def _to_domain_message(message: MessageSchema) -> Message:
    return Message(role=message.role, content=message.content)


def _to_domain_ai_message(message: AIMessageSchema) -> AIMessage:
    content_items = []
    for item in message.content:
        if item.type == ContentType.TEXT:
            content_items.append(TextContentItem(text=item.text))
        else:
            content_items.append(ImageContentItem(image_base64=item.image_base64))

    return AIMessage(role=message.role, content=content_items)


def to_response_schema(response: AIResponse) -> AIResponseSchema:
    usage_schema = None
    if response.usage:
        usage_schema = UsageSchema(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

    return AIResponseSchema(assistant_message=response.assistant_message, usage=usage_schema)


