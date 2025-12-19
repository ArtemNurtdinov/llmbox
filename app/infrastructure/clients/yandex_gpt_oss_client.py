import logging
from typing import List

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.domain.interfaces import TextModelClient
from app.core.config import config
from app.domain.models import AIResponse, Message, Role, Usage
from app.infrastructure.clients.yandex_gpt_client import YandexGPTClient

logger = logging.getLogger(__name__)


class YandexGPTOssClient(TextModelClient):

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.open_ai = AsyncOpenAI(api_key=config.yandex.open_ai_api_key, base_url=config.yandex.open_ai_base_url)

    async def generate(self, user_messages: List[Message]) -> AIResponse:
        messages = []

        for message in user_messages:
            if message.role == Role.SYSTEM:
                messages.append(ChatCompletionSystemMessageParam(role=message.role.value, content=message.content))
            elif message.role == Role.USER:
                messages.append(ChatCompletionUserMessageParam(role=message.role.value, content=message.content))
            elif message.role == Role.ASSISTANT:
                messages.append(ChatCompletionAssistantMessageParam(role=message.role.value, content=message.content))

        try:
            logger.info("Sending request to OpenAI-compatible API with %s messages", len(messages))
            completion = await self.open_ai.chat.completions.create(
                model=f"{YandexGPTClient.MODEL_PATH}{self.model_name}",
                messages=messages,
                temperature=0.2,
                max_tokens=2000,
            )
        except Exception as exc:
            logger.error("OpenAI-compatible API error: %s", exc, exc_info=True)
            raise

        assistant_message = completion.choices[0].message.content
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens

        logger.info(
            "OpenAI-compatible response received: response_length=%s, prompt_tokens=%s, completion_tokens=%s, total_tokens=%s",
            len(assistant_message) if assistant_message else 0,
            prompt_tokens,
            completion_tokens,
            total_tokens,
        )

        usage_model = Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
        return AIResponse(assistant_message=assistant_message, usage=usage_model)


