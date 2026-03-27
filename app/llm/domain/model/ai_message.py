from dataclasses import dataclass, field

from app.llm.domain.model.message import Message
from app.llm.domain.model.role import Role
from app.llm.domain.model.usage import Usage


@dataclass(frozen=True)
class AIMessage(Message):
    role: Role = field(default=Role.ASSISTANT, init=False)
    usage: Usage
