from dataclasses import dataclass

from app.domain.models import AIAssistant, ContentType, Role


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
    content: list[TextContentItemDTO | ImageContentItemDTO]


@dataclass
class GenerateAIRequestDTO:
    messages: list[MessageDTO]
    assistant: AIAssistant


@dataclass
class GenerateVisionAIRequestDTO:
    messages: list[AIMessageDTO]


@dataclass
class UsageDTO:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class AIResponseDTO:
    assistant_message: str
    usage: UsageDTO
