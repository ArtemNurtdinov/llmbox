from app.llm.application.exception.validation import ValidationException
from app.llm.application.model.ai_message import AIMessageDTO, ImageContentItemDTO, TextContentItemDTO
from app.llm.application.model.message import MessageDTO
from app.llm.application.model.request.generate_text import GenerateAIRequestDTO
from app.llm.application.model.request.vision import GenerateVisionAIRequestDTO
from app.llm.application.model.response.generate import AIResponseDTO, UsageDTO
from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.assistant import AIAssistant
from app.llm.domain.model.message import Message
from app.llm.domain.model.usage import Usage
from app.llm.domain.model.vision import ImageContentItem, TextContentItem, TextVisionMessage


class AIMessageMapper:
    def map_ai_message_to_dto(self, message: AIMessage) -> AIResponseDTO:
        return AIResponseDTO(
            assistant_message=message.content,
            usage=self._map_usage(message.usage),
        )

    def _map_usage(self, usage: Usage) -> UsageDTO:
        return UsageDTO(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )

    def to_domain_message(self, dto: MessageDTO) -> Message:
        return Message(role=dto.role, content=dto.content)

    def to_domain_ai_message(self, dto: AIMessageDTO) -> TextVisionMessage:
        content_items = []
        for item in dto.content:
            if isinstance(item, TextContentItemDTO):
                content_items.append(TextContentItem(text=item.text, type=item.type))
            elif isinstance(item, ImageContentItemDTO):
                content_items.append(ImageContentItem(image_base64=item.image_base64, type=item.type))
            else:
                raise ValidationException(f"Unknown content item type: {type(item)}")

        return TextVisionMessage(role=dto.role, content=content_items)

    def to_domain_messages_from_dto(self, dto: GenerateAIRequestDTO) -> tuple[list[Message], AIAssistant]:
        messages = [self.to_domain_message(msg) for msg in dto.messages]
        return messages, dto.assistant

    def to_domain_ai_messages_from_dto(self, dto: GenerateVisionAIRequestDTO) -> list[TextVisionMessage]:
        return [self.to_domain_ai_message(msg) for msg in dto.messages]
