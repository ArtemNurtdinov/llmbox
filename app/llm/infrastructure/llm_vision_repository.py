from app.llm.domain.client.vision import TextWithVisionClient
from app.llm.domain.llm_vision_repository import LLMVisionRepository
from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.vision import TextVisionMessage


class LLMVisionRepositoryImpl(LLMVisionRepository):
    def __init__(self, chat_gpt_client: TextWithVisionClient):
        self._chat_gpt_client = chat_gpt_client

    async def generate_vision(self, messages: list[TextVisionMessage]) -> AIMessage:
        return await self._chat_gpt_client.generate_vision(messages)
