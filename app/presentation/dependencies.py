from core.config import config
from app.application.services import AIService
from app.domain.interfaces import TextModelClient, VisionModelClient
from app.domain.models import AIAssistant
from app.infrastructure.clients.openai_client import OpenAIClient
from app.infrastructure.clients.yandex_gpt_client import YandexGPTClient
from app.infrastructure.clients.yandex_gpt_oss_client import YandexGPTOssClient


def create_ai_service() -> AIService:
    openai_client = OpenAIClient()
    yandex_gpt_client = YandexGPTClient()
    yandex_gpt_oss_20b = YandexGPTOssClient(model_name=config.yandex.gpt_oss_20b_model_name)
    yandex_gpt_oss_120b = YandexGPTOssClient(model_name=config.yandex.gpt_oss_120b_model_name)
    yandex_qwen_235b = YandexGPTOssClient(model_name=config.yandex.qwen_235b_model_name)

    text_clients: dict[AIAssistant, TextModelClient] = {
        AIAssistant.CHAT_GPT: openai_client,
        AIAssistant.YANDEX_GPT: yandex_gpt_client,
        AIAssistant.GPT_OSS_20B: yandex_gpt_oss_20b,
        AIAssistant.GPT_OSS_120B: yandex_gpt_oss_120b,
        AIAssistant.QWEN3_235B: yandex_qwen_235b,
    }

    vision_client: VisionModelClient = openai_client

    return AIService(text_clients=text_clients, vision_client=vision_client)

