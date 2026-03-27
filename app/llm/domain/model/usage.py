from dataclasses import dataclass


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
