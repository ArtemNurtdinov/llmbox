from dataclasses import dataclass, field

from app.llm.application.model.message import MessageDTO
from app.llm.domain.model.role import Role
from app.llm.domain.model.vision import ContentType


@dataclass(frozen=True)
class TextContentItemDTO:
    text: str
    type: ContentType = ContentType.TEXT


@dataclass(frozen=True)
class ImageContentItemDTO:
    image_base64: str
    type: ContentType = ContentType.IMAGE_URL


@dataclass(frozen=True)
class AIMessageDTO(MessageDTO):
    role: Role = field(default=Role.ASSISTANT, init=False)
    content: list[TextContentItemDTO | ImageContentItemDTO]
