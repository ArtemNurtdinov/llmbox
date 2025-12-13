import logging
from typing import List

from features.openai.open_ai import OpenAIClient
from features.ai_schemas import AIMessage, AIAssistant, Message, AIResponse
from features.yandex.yandex_gpt import YandexGPTClient
from features.yandex.yandex_gpt_oss import YandexGPTOssClient

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self, openai_client: OpenAIClient, yandex_gpt_client: YandexGPTClient, yandex_gpt_oss_client: YandexGPTOssClient):
        self.openai_client = openai_client
        self.yandex_gpt_client = yandex_gpt_client
        self.yandex_gpt_oss_client = yandex_gpt_oss_client

    async def generate_ai_response(self, messages: List[Message], assistant: AIAssistant) -> AIResponse:
        logger.info(f"Generating AI response with {assistant.value}")

        try:
            if assistant == AIAssistant.CHAT_GPT:
                ai_response = await self.openai_client.generate_ai_response(messages)

            elif assistant == AIAssistant.YANDEX_GPT:
                ai_response = await self.yandex_gpt_client.generate_ai_response(messages, YandexGPTClient.YANDEX_GPT_MODEL_NAME)

            elif assistant == AIAssistant.GPT_OSS_20B:
                ai_response = await self.yandex_gpt_oss_client.generate_ai_response(messages, YandexGPTOssClient.GPT_OSS_20B)

            elif assistant == AIAssistant.GPT_OSS_120B:
                ai_response = await self.yandex_gpt_oss_client.generate_ai_response(messages, YandexGPTOssClient.GPT_OSS_120B)

            elif assistant == AIAssistant.QWEN3_235B:
                ai_response = await self.yandex_gpt_oss_client.generate_ai_response(messages, YandexGPTOssClient.QWEN3_235B_A22B_instruct)

            else:
                error_msg = f"Unknown AI assistant: {assistant}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            return ai_response

        except Exception as e:
            logger.error(f"Error generating AI response with {assistant.value}: {str(e)}", exc_info=True)
            raise

    async def generate_ai_response_vision(self, messages: List[AIMessage]) -> AIResponse:
        logger.info(f"Generating Vision AI response")

        try:
            logger.info("Calling OpenAI ChatGPT Vision API...")
            ai_response = await self.openai_client.generate_ai_response_new(messages)

            logger.info(f"Vision AI response generated successfully: "
                        f"tokens={ai_response.usage.total_tokens}, "
                        f"response_length={len(ai_response.assistant_message)}")

            return ai_response

        except Exception as e:
            logger.error(f"Error generating Vision AI response: {str(e)}", exc_info=True)
            raise
