from typing import Protocol, List

from app.domain.models import AIMessage, AIResponse, Message


class TextModelClient(Protocol):
    async def generate(self, messages: List[Message]) -> AIResponse:
        ...


class VisionModelClient(Protocol):
    async def generate_vision(self, messages: List[AIMessage]) -> AIResponse:
        ...
