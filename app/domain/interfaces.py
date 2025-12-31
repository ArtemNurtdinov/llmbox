from typing import Protocol

from app.domain.models import AIMessage, AIResponse, Message


class TextModelClient(Protocol):
    async def generate(self, messages: list[Message]) -> AIResponse:
        ...


class VisionModelClient(Protocol):
    async def generate_vision(self, messages: list[AIMessage]) -> AIResponse:
        ...
