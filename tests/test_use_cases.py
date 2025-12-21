import unittest

from app.application.dto import (
    AIMessageDTO,
    GenerateAIRequestDTO,
    GenerateVisionAIRequestDTO,
    ImageContentItemDTO,
    MessageDTO,
    TextContentItemDTO,
)
from app.application.exceptions import (
    ServiceUnavailableException,
    ValidationException,
)
from app.application.use_cases.generate_text_ai_use_case import GenerateTextAIUseCase
from app.application.use_cases.generate_vision_ai_use_case import GenerateVisionAIUseCase
from app.domain.exceptions import AIServiceException, DomainException, UnknownAIAssistantException
from app.domain.models import AIAssistant, AIResponse, Role, Usage


class DummyTextClient:
    def __init__(self, response: AIResponse | Exception):
        self._response = response
        self.received_messages = None

    async def generate(self, messages):
        self.received_messages = messages
        if isinstance(self._response, Exception):
            raise self._response
        return self._response


class DummyVisionClient:
    def __init__(self, response: AIResponse | Exception):
        self._response = response
        self.received_messages = None

    async def generate_vision(self, messages):
        self.received_messages = messages
        if isinstance(self._response, Exception):
            raise self._response
        return self._response


class GenerateTextAIUseCaseTests(unittest.IsolatedAsyncioTestCase):
    async def test_execute_happy_path(self):
        usage = Usage(prompt_tokens=1, completion_tokens=2, total_tokens=3)
        ai_response = AIResponse(assistant_message="ok", usage=usage)
        client = DummyTextClient(ai_response)
        use_case = GenerateTextAIUseCase({AIAssistant.CHAT_GPT: client})
        request = GenerateAIRequestDTO(
            messages=[MessageDTO(role=Role.USER, content="hi")],
            assistant=AIAssistant.CHAT_GPT,
        )

        dto = await use_case.execute(request)

        self.assertEqual(dto.assistant_message, "ok")
        self.assertEqual(dto.usage.total_tokens, 3)
        self.assertIsNotNone(client.received_messages)
        self.assertEqual(client.received_messages[0].content, "hi")

    async def test_execute_raises_on_unknown_assistant(self):
        use_case = GenerateTextAIUseCase({})
        request = GenerateAIRequestDTO(
            messages=[MessageDTO(role=Role.USER, content="hi")],
            assistant=AIAssistant.CHAT_GPT,
        )

        with self.assertRaises(ValidationException):
            await use_case.execute(request)

    async def test_execute_maps_unknown_assistant_exception_to_validation(self):
        client = DummyTextClient(UnknownAIAssistantException("x"))
        use_case = GenerateTextAIUseCase({AIAssistant.CHAT_GPT: client})
        request = GenerateAIRequestDTO(
            messages=[MessageDTO(role=Role.USER, content="hi")],
            assistant=AIAssistant.CHAT_GPT,
        )

        with self.assertRaises(ValidationException):
            await use_case.execute(request)

    async def test_execute_maps_ai_service_exception_to_service_unavailable(self):
        client = DummyTextClient(AIServiceException("boom"))
        use_case = GenerateTextAIUseCase({AIAssistant.CHAT_GPT: client})
        request = GenerateAIRequestDTO(
            messages=[MessageDTO(role=Role.USER, content="hi")],
            assistant=AIAssistant.CHAT_GPT,
        )

        with self.assertRaises(ServiceUnavailableException):
            await use_case.execute(request)

    async def test_execute_maps_domain_exception_to_validation(self):
        client = DummyTextClient(DomainException("bad"))
        use_case = GenerateTextAIUseCase({AIAssistant.CHAT_GPT: client})
        request = GenerateAIRequestDTO(
            messages=[MessageDTO(role=Role.USER, content="hi")],
            assistant=AIAssistant.CHAT_GPT,
        )

        with self.assertRaises(ValidationException):
            await use_case.execute(request)

    async def test_execute_maps_unexpected_exception_to_service_unavailable(self):
        client = DummyTextClient(RuntimeError("oops"))
        use_case = GenerateTextAIUseCase({AIAssistant.CHAT_GPT: client})
        request = GenerateAIRequestDTO(
            messages=[MessageDTO(role=Role.USER, content="hi")],
            assistant=AIAssistant.CHAT_GPT,
        )

        with self.assertRaises(ServiceUnavailableException):
            await use_case.execute(request)


class GenerateVisionAIUseCaseTests(unittest.IsolatedAsyncioTestCase):
    async def test_execute_happy_path(self):
        usage = Usage(prompt_tokens=1, completion_tokens=2, total_tokens=3)
        ai_response = AIResponse(assistant_message="vision", usage=usage)
        client = DummyVisionClient(ai_response)
        use_case = GenerateVisionAIUseCase(client)
        request = GenerateVisionAIRequestDTO(
            messages=[
                AIMessageDTO(
                    role=Role.USER,
                    content=[ImageContentItemDTO(image_base64="img")],
                )
            ]
        )

        dto = await use_case.execute(request)

        self.assertEqual(dto.assistant_message, "vision")
        self.assertEqual(dto.usage.prompt_tokens, 1)
        self.assertIsNotNone(client.received_messages)
        self.assertEqual(client.received_messages[0].content[0].image_base64, "img")

    async def test_execute_maps_ai_service_exception_to_service_unavailable(self):
        client = DummyVisionClient(AIServiceException("fail"))
        use_case = GenerateVisionAIUseCase(client)
        request = GenerateVisionAIRequestDTO(
            messages=[
                AIMessageDTO(
                    role=Role.USER,
                    content=[TextContentItemDTO(text="hello")],
                )
            ]
        )

        with self.assertRaises(ServiceUnavailableException):
            await use_case.execute(request)

    async def test_execute_maps_domain_exception_to_validation(self):
        client = DummyVisionClient(DomainException("bad"))
        use_case = GenerateVisionAIUseCase(client)
        request = GenerateVisionAIRequestDTO(
            messages=[
                AIMessageDTO(
                    role=Role.USER,
                    content=[TextContentItemDTO(text="hello")],
                )
            ]
        )

        with self.assertRaises(ValidationException):
            await use_case.execute(request)

    async def test_execute_maps_unexpected_exception_to_service_unavailable(self):
        client = DummyVisionClient(RuntimeError("oops"))
        use_case = GenerateVisionAIUseCase(client)
        request = GenerateVisionAIRequestDTO(
            messages=[
                AIMessageDTO(
                    role=Role.USER,
                    content=[TextContentItemDTO(text="hello")],
                )
            ]
        )

        with self.assertRaises(ServiceUnavailableException):
            await use_case.execute(request)


if __name__ == "__main__":
    unittest.main()

