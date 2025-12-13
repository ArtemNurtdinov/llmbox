import logging
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam
from config import config
from features.ai_schemas import Message, Role, AIResponse, Usage
from features.yandex.yandex_gpt import YandexGPTClient

logger = logging.getLogger(__name__)


class YandexGPTOssClient:
    GPT_OSS_120B = config.yandex.gpt_oss_120b_model_name
    GPT_OSS_20B = config.yandex.gpt_oss_20b_model_name
    QWEN3_235B_A22B_instruct = config.yandex.qwen_235b_model_name

    def __init__(self):
        self.open_ai = AsyncOpenAI(api_key=config.yandex.open_ai_api_key, base_url=config.yandex.open_ai_base_url)

    async def generate_ai_response(self, user_messages: list[Message], model_name: str) -> AIResponse:
        try:
            messages = []

            for message in user_messages:
                if message.role == Role.SYSTEM:
                    messages.append(ChatCompletionSystemMessageParam(role=message.role.value, content=message.content))
                elif message.role == Role.USER:
                    messages.append(ChatCompletionUserMessageParam(role=message.role.value, content=message.content))
                elif message.role == Role.ASSISTANT:
                    messages.append(ChatCompletionAssistantMessageParam(role=message.role.value, content=message.content))

            logger.info(f"Sending request to OpenAI API with {len(messages)} messages")
            completion = await self.open_ai.chat.completions.create(
                model=f"{YandexGPTClient.MODEL_PATH}{model_name}",
                messages=messages,
                temperature=0.2,
                max_tokens=2000
            )

            assistant_message = completion.choices[0].message.content
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            total_tokens = completion.usage.total_tokens

            logger.info(f"OpenAI response received: "
                        f"response_length={len(assistant_message) if assistant_message else 0}, "
                        f"prompt_tokens={prompt_tokens}, "
                        f"completion_tokens={completion_tokens}, "
                        f"total_tokens={total_tokens}")

            usage_model = Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
            return AIResponse(assistant_message=assistant_message, usage=usage_model)
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            raise
