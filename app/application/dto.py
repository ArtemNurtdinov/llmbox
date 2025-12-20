from dataclasses import dataclass
from typing import List, Union


@dataclass
class MessageDTO:
    role: str
    content: str


@dataclass
class TextContentItemDTO:
    text: str
    type: str = "text"


@dataclass
class ImageContentItemDTO:
    image_base64: str
    type: str = "image_url"


@dataclass
class AIMessageDTO:
    role: str
    content: List[Union[TextContentItemDTO, ImageContentItemDTO]]


@dataclass
class GenerateAIRequestDTO:
    messages: List[MessageDTO]
    assistant: str


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