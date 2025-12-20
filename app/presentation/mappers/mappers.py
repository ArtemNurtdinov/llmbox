from app.presentation.api.schemas import (
    AIMessageSchema,
    AIResponseSchema,
    MessageSchema,
    UsageSchema,
    TextContentItemSchema,
    ImageContentItemSchema,
    GenerateAIRequestSchema,
    GenerateVisionAIRequestSchema,
)
from app.application.dto import (
    GenerateAIRequestDTO,
    GenerateVisionAIRequestDTO,
    AIResponseDTO,
    MessageDTO,
    AIMessageDTO,
    TextContentItemDTO,
    ImageContentItemDTO,
)
from app.application.dto import Role, ContentType, AIAssistant


def to_message_dto(schema: MessageSchema) -> MessageDTO:
    return MessageDTO(role=Role(schema.role.value), content=schema.content)


def to_text_content_item_dto(schema: TextContentItemSchema) -> TextContentItemDTO:
    return TextContentItemDTO(text=schema.text, type=ContentType(schema.type.value))


def to_image_content_item_dto(schema: ImageContentItemSchema) -> ImageContentItemDTO:
    return ImageContentItemDTO(image_base64=schema.image_base64, type=ContentType(schema.type.value))


def to_ai_message_dto(schema: AIMessageSchema) -> AIMessageDTO:
    content_items = []
    for item in schema.content:
        if isinstance(item, TextContentItemSchema):
            content_items.append(to_text_content_item_dto(item))
        elif isinstance(item, ImageContentItemSchema):
            content_items.append(to_image_content_item_dto(item))
    
    return AIMessageDTO(role=Role(schema.role.value), content=content_items)


def to_generate_ai_request_dto(schema: GenerateAIRequestSchema) -> GenerateAIRequestDTO:
    messages = [to_message_dto(msg) for msg in schema.messages]
    return GenerateAIRequestDTO(messages=messages, assistant=AIAssistant(schema.assistant.value))


def to_generate_vision_ai_request_dto(schema: GenerateVisionAIRequestSchema) -> GenerateVisionAIRequestDTO:
    messages = [to_ai_message_dto(msg) for msg in schema.messages]
    return GenerateVisionAIRequestDTO(messages=messages)


def to_response_schema(dto: AIResponseDTO) -> AIResponseSchema:
    usage_schema = UsageSchema(
        prompt_tokens=dto.usage.prompt_tokens,
        completion_tokens=dto.usage.completion_tokens,
        total_tokens=dto.usage.total_tokens,
    )

    return AIResponseSchema(assistant_message=dto.assistant_message, usage=usage_schema)
