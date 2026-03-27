from dataclasses import dataclass

from app.llm.application.model.ai_message import AIMessageDTO


@dataclass
class GenerateVisionAIRequestDTO:
    messages: list[AIMessageDTO]
