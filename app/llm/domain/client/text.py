from abc import ABC, abstractmethod

from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.message import Message


class TextClient(ABC):
    @abstractmethod
    async def generate(self, messages: list[Message]) -> AIMessage: ...
