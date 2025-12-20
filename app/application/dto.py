from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Union


class Role(str, Enum):
    """Role enum для application слоя"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@unique
class ContentType(str, Enum):
    """ContentType enum для application слоя"""
    TEXT = "text"
    IMAGE_URL = "image_url"


class AIAssistant(str, Enum):
    """AIAssistant enum для application слоя"""
    CHAT_GPT = "chat_gpt"
    YANDEX_GPT = "yandex_gpt"
    GPT_OSS_120B = "gpt_oss_120b"
    GPT_OSS_20B = "gpt_oss_20b"
    QWEN3_235B = "qwen3_235b"


@dataclass
class MessageDTO:
    role: Role
    content: str


@dataclass
class TextContentItemDTO:
    text: str
    type: ContentType = ContentType.TEXT


@dataclass
class ImageContentItemDTO:
    image_base64: str
    type: ContentType = ContentType.IMAGE_URL


@dataclass
class AIMessageDTO:
    role: Role
    content: List[Union[TextContentItemDTO, ImageContentItemDTO]]


@dataclass
class GenerateAIRequestDTO:
    messages: List[MessageDTO]
    assistant: AIAssistant


@dataclass
class GenerateVisionAIRequestDTO:
    messages: List[AIMessageDTO]


@dataclass
class UsageDTO:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class AIResponseDTO:
    assistant_message: str
    usage: UsageDTO