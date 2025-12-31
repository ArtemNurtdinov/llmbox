import logging

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.domain.interfaces import TextModelClient
from app.domain.models import AIResponse, Message, Role, Usage

logger = logging.getLogger(__name__)


class YandexGPTOssClient(TextModelClient):
    def __init__(self, model_name: str, model_path: str, api_key: str, base_url: str):
        if not model_name or not model_path or not api_key or not base_url:
            raise ValueError("Yandex GPT OSS model_name, model_path, api_key and base_url are required")
        self.model_name = model_name
        self._model_path = model_path
        self.open_ai = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def generate(self, user_messages: list[Message]) -> AIResponse:
        messages = []

        for message in user_messages:
            if message.role == Role.SYSTEM:
                messages.append(ChatCompletionSystemMessageParam(role=message.role.value, content=message.content))
            elif message.role == Role.USER:
                messages.append(ChatCompletionUserMessageParam(role=message.role.value, content=message.content))
            elif message.role == Role.ASSISTANT:
                messages.append(ChatCompletionAssistantMessageParam(role=message.role.value, content=message.content))

        logger.info("Sending request to OpenAI-compatible API")
        model = f"{self._model_path}{self.model_name}"
        completion = await self.open_ai.chat.completions.create(model=model, messages=messages, temperature=0.2, max_tokens=2000,)

        assistant_message = completion.choices[0].message.content
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens

        logger.info("OpenAI-compatible response received")

        usage_model = Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
        return AIResponse(assistant_message=assistant_message, usage=usage_model)


