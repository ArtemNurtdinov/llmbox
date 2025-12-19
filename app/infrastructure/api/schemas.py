from typing import List, Union, Optional

from pydantic import BaseModel

from app.domain.models import ContentType, Role, AIAssistant


class MessageSchema(BaseModel):
    role: Role
    content: str


class TextContentItemSchema(BaseModel):
    text: str
    type: ContentType = ContentType.TEXT


class ImageContentItemSchema(BaseModel):
    image_base64: str
    type: ContentType = ContentType.IMAGE_URL


class AIMessageSchema(BaseModel):
    role: Role
    content: List[Union[TextContentItemSchema, ImageContentItemSchema]]


class UsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class AIResponseSchema(BaseModel):
    assistant_message: str
    usage: Optional[UsageSchema] = None


class GenerateAIRequestSchema(BaseModel):
    messages: List[MessageSchema]
    assistant: AIAssistant


class GenerateVisionAIRequestSchema(BaseModel):
    messages: List[AIMessageSchema]


