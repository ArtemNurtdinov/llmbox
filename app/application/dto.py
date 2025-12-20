from dataclasses import dataclass
from typing import List, Dict, Any, Union


@dataclass
class MessageDTO:
    """DTO для Message без зависимости от Domain"""
    role: str  # "system", "user", "assistant"
    content: str


@dataclass
class TextContentItemDTO:
    """DTO для TextContentItem без зависимости от Domain"""
    text: str
    type: str = "text"


@dataclass
class ImageContentItemDTO:
    """DTO для ImageContentItem без зависимости от Domain"""
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