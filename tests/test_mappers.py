import unittest

from app.application.dto import (
    AIMessageDTO,
    GenerateAIRequestDTO,
    GenerateVisionAIRequestDTO,
    ImageContentItemDTO,
    MessageDTO,
    TextContentItemDTO,
)
from app.application.exceptions import ValidationException
from app.application.mappers.dto_to_domain import (
    to_domain_ai_message,
    to_domain_ai_messages_from_dto,
    to_domain_message,
    to_domain_messages_from_dto,
)
from app.domain.models import AIAssistant, ContentType, Role


class DummyContentItem:

    def __init__(self) -> None:
        self.type = "unknown"


class MapperTests(unittest.TestCase):
    def test_to_domain_message(self) -> None:
        dto = MessageDTO(role=Role.USER, content="hello")

        domain = to_domain_message(dto)

        self.assertEqual(domain.role, Role.USER)
        self.assertEqual(domain.content, "hello")

    def test_to_domain_ai_message_with_text_and_image(self) -> None:
        dto = AIMessageDTO(
            role=Role.ASSISTANT,
            content=[
                TextContentItemDTO(text="hello"),
                ImageContentItemDTO(image_base64="img", type=ContentType.IMAGE_URL),
            ],
        )

        domain = to_domain_ai_message(dto)

        self.assertEqual(domain.role, Role.ASSISTANT)
        self.assertEqual(len(domain.content), 2)
        self.assertEqual(domain.content[0].text, "hello")
        self.assertEqual(domain.content[1].image_base64, "img")

    def test_to_domain_ai_message_raises_on_unknown_type(self) -> None:
        dto = AIMessageDTO(role=Role.ASSISTANT, content=[DummyContentItem()])

        with self.assertRaises(ValidationException):
            to_domain_ai_message(dto)

    def test_to_domain_messages_from_dto(self) -> None:
        request = GenerateAIRequestDTO(
            messages=[MessageDTO(role=Role.USER, content="hi")],
            assistant=AIAssistant.CHAT_GPT,
        )

        messages, assistant = to_domain_messages_from_dto(request)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, "hi")
        self.assertEqual(assistant, AIAssistant.CHAT_GPT)

    def test_to_domain_ai_messages_from_dto(self) -> None:
        request = GenerateVisionAIRequestDTO(
            messages=[
                AIMessageDTO(
                    role=Role.USER,
                    content=[ImageContentItemDTO(image_base64="img", type=ContentType.IMAGE_URL)],
                )
            ]
        )

        messages = to_domain_ai_messages_from_dto(request)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content[0].image_base64, "img")


if __name__ == "__main__":
    unittest.main()

