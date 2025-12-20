from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class RoleSchema(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ContentTypeSchema(str, Enum):
    TEXT = "text"
    IMAGE_URL = "image_url"


class AIAssistantSchema(str, Enum):
    CHAT_GPT = "chat_gpt"
    YANDEX_GPT = "yandex_gpt"
    GPT_OSS_120B = "gpt_oss_120b"
    GPT_OSS_20B = "gpt_oss_20b"
    QWEN3_235B = "qwen3_235b"


class MessageSchema(BaseModel):
    role: RoleSchema
    content: str


class TextContentItemSchema(BaseModel):
    text: str
    type: ContentTypeSchema = ContentTypeSchema.TEXT


class ImageContentItemSchema(BaseModel):
    image_base64: str
    type: ContentTypeSchema = ContentTypeSchema.IMAGE_URL


class AIMessageSchema(BaseModel):
    role: RoleSchema
    content: List[Union[TextContentItemSchema, ImageContentItemSchema]]


class UsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class AIResponseSchema(BaseModel):
    assistant_message: str
    usage: UsageSchema


class GenerateAIRequestSchema(BaseModel):
    messages: List[MessageSchema]
    assistant: AIAssistantSchema


class GenerateVisionAIRequestSchema(BaseModel):
    messages: List[AIMessageSchema]
