import logging

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionAssistantMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from app.llm.domain.client.vision import TextWithVisionClient
from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.message import Message
from app.llm.domain.model.role import Role
from app.llm.domain.model.usage import Usage
from app.llm.domain.model.vision import ImageContentItem, TextContentItem, TextVisionMessage

logger = logging.getLogger(__name__)


class OpenAIClient(TextWithVisionClient):
    def __init__(self, model: str, api_key: str):
        if not model or not api_key:
            raise ValueError("OpenAI model and api_key are required")
        self._model = model
        self._client = AsyncOpenAI(api_key=api_key)

    async def generate(self, user_messages: list[Message]) -> AIMessage:
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
        return AIMessage(content=assistant_message, usage=usage_model)

    @staticmethod
    def _serialize_message(msg: TextVisionMessage) -> dict:
        content_items = []
        for item in msg.content:
            if isinstance(item, TextContentItem):
                content_items.append({"type": "text", "text": item.text})
            elif isinstance(item, ImageContentItem):
                content_items.append({"type": "image_url", "image_url": {"url": item.image_base64}})
        return {"role": msg.role.value, "content": content_items}


    async def generate_vision(self, user_messages: list[TextVisionMessage]) -> AIMessage:
        messages = [self._serialize_message(msg) for msg in user_messages]

        response = await self._client.chat.completions.create(model=self._model, messages=messages)

        usage = Usage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

        content = response.choices[0].message.content

        logger.info("OpenAI Vision API response received")

        return AIMessage(content=content, usage=usage)
