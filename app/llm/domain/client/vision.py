from abc import abstractmethod

from app.llm.domain.client.text import TextClient
from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.vision import TextVisionMessage


class TextWithVisionClient(TextClient):
    @abstractmethod
    async def generate_vision(self, messages: list[TextVisionMessage]) -> AIMessage: ...
