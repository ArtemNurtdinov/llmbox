import logging
from typing import List

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionAssistantMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from app.domain.interfaces import TextModelClient, VisionModelClient
from app.domain.models import AIMessage, AIResponse, ImageContentItem, Message, Role, TextContentItem, Usage

logger = logging.getLogger(__name__)


class OpenAIClient(TextModelClient, VisionModelClient):
    def __init__(self, model: str, api_key: str):
        if not model or not api_key:
            raise ValueError("OpenAI model and api_key are required")
        self._model = model
        self._client = AsyncOpenAI(api_key=api_key)

    async def generate(self, user_messages: List[Message]) -> AIResponse:
        return await self._generate_text(user_messages)

    @staticmethod
    def _serialize_message(msg: AIMessage) -> dict:
        content_items = []
        for item in msg.content:
            if isinstance(item, TextContentItem):
                content_items.append({
                    "type": "text",
                    "text": item.text
                })
            elif isinstance(item, ImageContentItem):
                content_items.append({
                    "type": "image_url",
                    "image_url": {"url": item.image_base64}
                })
        return {
            "role": msg.role.value,
            "content": content_items
        }

    async def _generate_text(self, user_messages: List[Message]) -> AIResponse:
        messages = []

        for message in user_messages:
            if message.role == Role.SYSTEM:
                messages.append(ChatCompletionSystemMessageParam(role=message.role.value, content=message.content))
            elif message.role == Role.USER:
                messages.append(ChatCompletionUserMessageParam(role=message.role.value, content=message.content))
            elif message.role == Role.ASSISTANT:
                messages.append(ChatCompletionAssistantMessageParam(role=message.role.value, content=message.content))

        completion = await self._client.chat.completions.create(model=self._model, messages=messages)

        assistant_message = completion.choices[0].message.content
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens

        usage_model = Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
        return AIResponse(assistant_message=assistant_message, usage=usage_model)

    async def generate_vision(self, user_messages: List[AIMessage]) -> AIResponse:
        messages = [self._serialize_message(msg) for msg in user_messages]

        response = await self._client.chat.completions.create(model=self._model, messages=messages)

        usage = Usage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

        content = response.choices[0].message.content

        logger.info("OpenAI Vision API response received")

        return AIResponse(assistant_message=content, usage=usage)
