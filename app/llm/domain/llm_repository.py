from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.assistant import AIAssistant
from app.llm.domain.model.message import Message


class LLMRepository:
    async def generate(self, assistant: AIAssistant, messages: list[Message]) -> AIMessage: ...
