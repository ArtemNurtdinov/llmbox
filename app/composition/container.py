from core.config import Config
from app.application.services import AIService
from app.application.use_cases.generate_text_ai_use_case import GenerateTextAIUseCase
from app.application.use_cases.generate_vision_ai_use_case import GenerateVisionAIUseCase
from app.domain.interfaces import TextModelClient, VisionModelClient
from app.domain.models import AIAssistant
from app.infrastructure.clients.openai_client import OpenAIClient
from app.infrastructure.clients.yandex_gpt_client import YandexGPTClient
from app.infrastructure.clients.yandex_gpt_oss_client import YandexGPTOssClient
from app.infrastructure.clients.yandex_auth import YandexAuth


def build_ai_service(config: Config) -> AIService:
    if not config.open_ai.model or not config.open_ai.api_key:
        raise ValueError("OpenAI model and api_key must be configured")
    openai_client = OpenAIClient(
        model=config.open_ai.model,
        api_key=config.open_ai.api_key
    )

    if not config.yandex.key_id or not config.yandex.service_account_id or not config.yandex.private_key:
        raise ValueError("Yandex authentication credentials must be configured")
    yandex_auth = YandexAuth(
        key_id=config.yandex.key_id,
        service_account_id=config.yandex.service_account_id,
        private_key=config.yandex.private_key
    )

    if not config.yandex.yandex_gpt_api_url or not config.yandex.yandex_gpt_model_path or not config.yandex.yandex_gpt_model_name:
        raise ValueError("Yandex GPT configuration must be complete")
    yandex_gpt_client = YandexGPTClient(
        api_url=config.yandex.yandex_gpt_api_url,
        model_path=config.yandex.yandex_gpt_model_path,
        model_name=config.yandex.yandex_gpt_model_name,
        auth=yandex_auth
    )

    if not config.yandex.yandex_gpt_model_path or not config.yandex.open_ai_api_key or not config.yandex.open_ai_base_url:
        raise ValueError("Yandex GPT OSS configuration must be complete")

    if not config.yandex.gpt_oss_20b_model_name:
        raise ValueError("Yandex GPT OSS 20B model name must be configured")
    yandex_gpt_oss_20b = YandexGPTOssClient(
        model_name=config.yandex.gpt_oss_20b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url
    )

    if not config.yandex.gpt_oss_120b_model_name:
        raise ValueError("Yandex GPT OSS 120B model name must be configured")
    yandex_gpt_oss_120b = YandexGPTOssClient(
        model_name=config.yandex.gpt_oss_120b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url
    )

    if not config.yandex.qwen_235b_model_name:
        raise ValueError("Yandex Qwen 235B model name must be configured")
    yandex_qwen_235b = YandexGPTOssClient(
        model_name=config.yandex.qwen_235b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url
    )

    text_clients: dict[AIAssistant, TextModelClient] = {
        AIAssistant.CHAT_GPT: openai_client,
        AIAssistant.YANDEX_GPT: yandex_gpt_client,
        AIAssistant.GPT_OSS_20B: yandex_gpt_oss_20b,
        AIAssistant.GPT_OSS_120B: yandex_gpt_oss_120b,
        AIAssistant.QWEN3_235B: yandex_qwen_235b,
    }

    vision_client: VisionModelClient = openai_client

    generate_text_use_case = GenerateTextAIUseCase(text_clients=text_clients)
    generate_vision_use_case = GenerateVisionAIUseCase(vision_client=vision_client)

    return AIService(
        generate_text_use_case=generate_text_use_case,
        generate_vision_use_case=generate_vision_use_case,
    )

