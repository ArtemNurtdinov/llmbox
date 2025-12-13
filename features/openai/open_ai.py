import logging
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam
from config import config
from features.ai_schemas import AIMessage, ImageContentItem, TextContentItem, Message, Role, AIResponse, Usage

logger = logging.getLogger(__name__)


class OpenAIClient:
    _OPEN_AI_MODEL = config.open_ai.model
    _OPEN_AI_TOKEN = config.open_ai.api_key

    def __init__(self):
        self.open_ai = AsyncOpenAI(api_key=self._OPEN_AI_TOKEN)
        self.async_client = self.open_ai

    async def generate_ai_response(self, user_messages: list[Message]) -> AIResponse:
        try:
            messages = []

            for message in user_messages:
                if message.role == Role.SYSTEM:
                    messages.append(ChatCompletionSystemMessageParam(role=message.role.value, content=message.content))
                elif message.role == Role.USER:
                    messages.append(ChatCompletionUserMessageParam(role=message.role.value, content=message.content))
                elif message.role == Role.ASSISTANT:
                    messages.append(ChatCompletionAssistantMessageParam(role=message.role.value, content=message.content))

            completion = await self.open_ai.chat.completions.create(model=self._OPEN_AI_MODEL, messages=messages)

            assistant_message = completion.choices[0].message.content
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens

            usage_model = Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
            return AIResponse(assistant_message=assistant_message, usage=usage_model)
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def serialize_message(msg: AIMessage):
        content_items = []
        for item in msg.content:
            if isinstance(item, TextContentItem):
                content_items.append({"type": "text", "text": item.text})
            elif isinstance(item, ImageContentItem):
                content_items.append({"type": "image_url", "image_url": item.image_url})
        return {"role": msg.role.value, "content": content_items}

    async def generate_ai_response_new(self, user_messages: list[AIMessage]) -> AIResponse:
        try:
            logger.info(f"OpenAI Vision API request starting: messages_count={len(user_messages)}")

            messages = [self.serialize_message(msg) for msg in user_messages]

            logger.info(f"Sending Vision API request to OpenAI with {len(messages)} messages using model {self._OPEN_AI_MODEL}")
            response = await self.async_client.chat.completions.create(model=self._OPEN_AI_MODEL, messages=messages)

            usage = None
            if hasattr(response, 'usage') and response.usage:
                usage = Usage(prompt_tokens=response.usage.prompt_tokens, completion_tokens=response.usage.completion_tokens, total_tokens=response.usage.total_tokens)

            content = response.choices[0].message.content

            logger.info(f"OpenAI Vision API response received: "
                        f"response_length={len(content) if content else 0}, "
                        f"tokens_used={usage.total_tokens if usage else 0}")

            return AIResponse(assistant_message=content, usage=usage)

        except Exception as e:
            logger.error(f"OpenAI Vision API error: {str(e)}", exc_info=True)
            raise
