from dataclasses import dataclass

from app.llm.application.model.message import MessageDTO
from app.llm.domain.model.assistant import AIAssistant


@dataclass
class GenerateAIRequestDTO:
    messages: list[MessageDTO]
    assistant: AIAssistant
