from functools import lru_cache

from app.application.use_cases import GenerateTextAIUseCase, GenerateVisionAIUseCase
from app.config.domain.config_repository import ConfigRepository
from app.config.domain.config_source import ConfigSource
from app.config.domain.model.configuration import Config
from app.config.infrastructure.config_repository import ConfigRepositoryImpl
from app.config.infrastructure.config_source import EnvConfigSource
from app.config.validation.application.config_validator import AppConfigValidator
from app.config.validation.domain.config_validator import ConfigValidator
from app.domain.interfaces import TextModelClient, VisionModelClient
from app.domain.models import AIAssistant
from app.infrastructure.clients.openai_client import OpenAIClient
from app.infrastructure.clients.yandex_auth import YandexAuth
from app.infrastructure.clients.yandex_gpt_client import YandexGPTClient
from app.infrastructure.clients.yandex_gpt_oss_client import YandexGPTOssClient


@lru_cache
def load_config() -> Config:
    config_source: ConfigSource = EnvConfigSource()
    config_validator: ConfigValidator = AppConfigValidator()
    provider: ConfigRepository = ConfigRepositoryImpl(config_source, config_validator)
    return provider.get_config()


def build_generate_text_ai_use_case(config: Config) -> GenerateTextAIUseCase:
    openai_client = OpenAIClient(model=config.open_ai.model, api_key=config.open_ai.api_key)
    yandex_auth = YandexAuth(
        key_id=config.yandex.key_id, service_account_id=config.yandex.service_account_id, private_key=config.yandex.private_key
    )
    yandex_gpt_client = YandexGPTClient(
        api_url=config.yandex.yandex_gpt_api_url,
        model_path=config.yandex.yandex_gpt_model_path,
        model_name=config.yandex.yandex_gpt_model_name,
        auth=yandex_auth,
    )

    yandex_gpt_oss_20b = YandexGPTOssClient(
        model_name=config.yandex.gpt_oss_20b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url,
    )

    yandex_gpt_oss_120b = YandexGPTOssClient(
        model_name=config.yandex.gpt_oss_120b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url,
    )

    yandex_qwen_235b = YandexGPTOssClient(
        model_name=config.yandex.qwen_235b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url,
    )

    text_clients: dict[AIAssistant, TextModelClient] = {
        AIAssistant.CHAT_GPT: openai_client,
        AIAssistant.YANDEX_GPT: yandex_gpt_client,
        AIAssistant.GPT_OSS_20B: yandex_gpt_oss_20b,
        AIAssistant.GPT_OSS_120B: yandex_gpt_oss_120b,
        AIAssistant.QWEN3_235B: yandex_qwen_235b,
    }

    return GenerateTextAIUseCase(text_clients=text_clients)


@lru_cache
def get_generate_text_ai_use_case() -> GenerateTextAIUseCase:
    config = load_config()
    return build_generate_text_ai_use_case(config)


def build_generate_vision_ai_use_case(config: Config) -> GenerateVisionAIUseCase:
    openai_client = OpenAIClient(model=config.open_ai.model, api_key=config.open_ai.api_key)
    vision_client: VisionModelClient = openai_client
    return GenerateVisionAIUseCase(vision_client=vision_client)


@lru_cache
def get_generate_vision_ai_use_case() -> GenerateVisionAIUseCase:
    config = load_config()
    return build_generate_vision_ai_use_case(config)
