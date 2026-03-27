from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.vision import TextVisionMessage


class LLMVisionRepository:
    async def generate_vision(self, messages: list[TextVisionMessage]) -> AIMessage: ...
