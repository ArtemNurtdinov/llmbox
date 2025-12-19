import logging
from typing import List

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.domain.interfaces import TextModelClient, VisionModelClient
from app.core.config import config
from app.domain.models import (
    AIMessage,
    AIResponse,
    ImageContentItem,
    Message,
    Role,
    TextContentItem,
    Usage,
)

logger = logging.getLogger(__name__)


class OpenAIClient(TextModelClient, VisionModelClient):
    _OPEN_AI_MODEL = config.open_ai.model
    _OPEN_AI_TOKEN = config.open_ai.api_key

    def __init__(self):
        self._client = AsyncOpenAI(api_key=self._OPEN_AI_TOKEN)

    async def generate(self, user_messages: List[Message]) -> AIResponse:
        return await self._generate_text(user_messages)

    @staticmethod
    def _serialize_message(msg: AIMessage) -> dict:
        content_items = []
        for item in msg.content:
            if isinstance(item, TextContentItem):
                content_items.append({"type": "text", "text": item.text})
            elif isinstance(item, ImageContentItem):
                content_items.append({"type": "image_url", "image_url": item.image_url})
        return {"role": msg.role.value, "content": content_items}

    async def _generate_text(self, user_messages: List[Message]) -> AIResponse:
        try:
            messages = []

            for message in user_messages:
                if message.role == Role.SYSTEM:
                    messages.append(ChatCompletionSystemMessageParam(role=message.role.value, content=message.content))
                elif message.role == Role.USER:
                    messages.append(ChatCompletionUserMessageParam(role=message.role.value, content=message.content))
                elif message.role == Role.ASSISTANT:
                    messages.append(ChatCompletionAssistantMessageParam(role=message.role.value, content=message.content))

            completion = await self._client.chat.completions.create(model=self._OPEN_AI_MODEL, messages=messages)

            assistant_message = completion.choices[0].message.content
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens

            usage_model = Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
            return AIResponse(assistant_message=assistant_message, usage=usage_model)
        except Exception as exc:
            logger.error("OpenAI API error: %s", exc, exc_info=True)
            raise

    async def generate_vision(self, user_messages: List[AIMessage]) -> AIResponse:
        try:
            logger.info("OpenAI Vision API request starting: messages_count=%s", len(user_messages))

            messages = [self._serialize_message(msg) for msg in user_messages]

            logger.info("Sending Vision API request to OpenAI with %s messages using model %s", len(messages), self._OPEN_AI_MODEL)
            response = await self._client.chat.completions.create(model=self._OPEN_AI_MODEL, messages=messages)

            usage = None
            if hasattr(response, "usage") and response.usage:
                usage = Usage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                )

            content = response.choices[0].message.content

            logger.info(
                "OpenAI Vision API response received: response_length=%s, tokens_used=%s",
                len(content) if content else 0,
                usage.total_tokens if usage else 0,
            )

            return AIResponse(assistant_message=content, usage=usage)

        except Exception as exc:
            logger.error("OpenAI Vision API error: %s", exc, exc_info=True)
            raise


