from dataclasses import dataclass
from typing import List, Union

from app.domain.models import Role, ContentType, AIAssistant


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