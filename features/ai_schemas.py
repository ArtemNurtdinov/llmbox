from enum import unique, Enum
from typing import List, Union
from pydantic import BaseModel


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    role: Role
    content: str


class AIAssistant(Enum):
    CHAT_GPT = "chat_gpt"
    YANDEX_GPT = "yandex_gpt"
    GPT_OSS_120B = "gpt_oss_120b"
    GPT_OSS_20B = "gpt_oss_20b"
    QWEN3_235B = "qwen3_235b"


@unique
class ContentType(str, Enum):
    TEXT = "text"
    IMAGE_URL = "image_url"


class TextContentItem(BaseModel):
    text: str
    type: ContentType = ContentType.TEXT


class ImageContentItem(BaseModel):
    image_base64: str
    type: ContentType = ContentType.IMAGE_URL

    @property
    def image_url(self) -> dict:
        return {"url": self.image_base64}


class AIMessage(BaseModel):
    role: Role
    content: List[Union[TextContentItem, ImageContentItem]]


class GenerateAIRequestBody(BaseModel):
    messages: List[Message]
    assistant: AIAssistant


class GenerateVisionAIRequestBody(BaseModel):
    messages: List[AIMessage]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class AIResponse(BaseModel):
    assistant_message: str
    usage: Usage
