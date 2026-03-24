from dataclasses import dataclass

from app.llm.domain.model.role import Role


@dataclass(frozen=True)
class Message:
    role: Role
    content: str
