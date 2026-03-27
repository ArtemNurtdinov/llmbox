from dataclasses import dataclass
from enum import Enum, unique

from app.llm.domain.model.role import Role


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
class TextVisionMessage:
    role: Role
    content: list[TextContentItem | ImageContentItem]
