from dataclasses import dataclass
from enum import Enum, unique


class AIAssistant(Enum):
    CHAT_GPT = "chat_gpt"
    YANDEX_GPT = "yandex_gpt"
    GPT_OSS_120B = "gpt_oss_120b"
    GPT_OSS_20B = "gpt_oss_20b"
    QWEN3_235B = "qwen3_235b"


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    role: Role
    content: str


@unique
class ContentType(str, Enum):
    TEXT = "text"
    IMAGE_URL = "image_url"


@dataclass
class TextContentItem:
    text: str
    type: ContentType = ContentType.TEXT


@dataclass
class ImageContentItem:
    image_base64: str
    type: ContentType = ContentType.IMAGE_URL


@dataclass
class AIMessage:
    role: Role
    content: list[TextContentItem | ImageContentItem]


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class AIResponse:
    assistant_message: str
    usage: Usage
