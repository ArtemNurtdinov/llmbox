from dataclasses import dataclass


@dataclass
class UsageDTO:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class AIResponseDTO:
    assistant_message: str
    usage: UsageDTO
