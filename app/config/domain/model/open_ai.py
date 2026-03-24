from dataclasses import dataclass


@dataclass(frozen=True)
class OpenAIConfig:
    model: str | None
    api_key: str | None
