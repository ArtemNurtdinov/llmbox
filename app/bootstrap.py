import logging
from functools import lru_cache
from logging.handlers import TimedRotatingFileHandler

from app.config.application.load_configuration_use_case import LoadConfigurationUseCase
from app.config.domain.config_repository import ConfigRepository
from app.config.domain.config_source import ConfigSource
from app.config.domain.model.configuration import Config
from app.config.domain.model.logging import LoggingConfig
from app.config.infrastructure.config_repository import ConfigRepositoryImpl
from app.config.infrastructure.config_source import EnvConfigSource
from app.config.validation.application.usecase.validate_config_use_case import ValidateConfigUseCase
from app.llm.application.mapper.ai_message_mapper import AIMessageMapper
from app.llm.application.usecase.generate_text_ai_use_case import GenerateTextAIUseCase
from app.llm.application.usecase.generate_vision_ai_use_case import GenerateVisionAIUseCase
from app.llm.domain.llm_repository import LLMRepository
from app.llm.domain.llm_vision_repository import LLMVisionRepository
from app.llm.infrastructure.client.auth.yandex_auth import YandexAuth
from app.llm.infrastructure.client.openai_client import OpenAIClient
from app.llm.infrastructure.client.yandex_gpt_client import YandexGPTClient
from app.llm.infrastructure.client.yandex_gpt_oss_client import YandexGPTOssClient
from app.llm.infrastructure.llm_repository import LLMRepositoryImpl
from app.llm.infrastructure.llm_vision_repository import LLMVisionRepositoryImpl


def get_config_source() -> ConfigSource:
    return EnvConfigSource()


def get_config_repository() -> ConfigRepository:
    source: ConfigSource = get_config_source()
    return ConfigRepositoryImpl(source)


def get_validate_config_use_case() -> ValidateConfigUseCase:
    return ValidateConfigUseCase()


def get_load_configuration_use_case() -> LoadConfigurationUseCase:
    config_repository: ConfigRepository = get_config_repository()
    validate_config_use_case: ValidateConfigUseCase = get_validate_config_use_case()
    return LoadConfigurationUseCase(config_repository, validate_config_use_case)


@lru_cache
def load_config() -> Config:
    load_configuration_use_case: LoadConfigurationUseCase = get_load_configuration_use_case()
    return load_configuration_use_case.execute()


@lru_cache
def get_yandex_auth() -> YandexAuth:
    config = load_config()
    return YandexAuth(
        key_id=config.yandex.key_id, service_account_id=config.yandex.service_account_id, private_key=config.yandex.private_key
    )


def get_open_ai_client() -> OpenAIClient:
    config = load_config()
    return OpenAIClient(model=config.open_ai.model, api_key=config.open_ai.api_key)


def get_yandex_gpt_client() -> YandexGPTClient:
    config = load_config()
    auth = get_yandex_auth()
    return YandexGPTClient(
        api_url=config.yandex.yandex_gpt_api_url,
        model_path=config.yandex.yandex_gpt_model_path,
        model_name=config.yandex.yandex_gpt_model_name,
        auth=auth,
    )


def get_gpt_oss_20_client() -> YandexGPTOssClient:
    config = load_config()
    return YandexGPTOssClient(
        model_name=config.yandex.gpt_oss_20b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url,
    )


def get_gpt_oss_120_client() -> YandexGPTOssClient:
    config = load_config()
    return YandexGPTOssClient(
        model_name=config.yandex.gpt_oss_120b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url,
    )


def get_qwen_client() -> YandexGPTOssClient:
    config = load_config()
    return YandexGPTOssClient(
        model_name=config.yandex.qwen_235b_model_name,
        model_path=config.yandex.yandex_gpt_model_path,
        api_key=config.yandex.open_ai_api_key,
        base_url=config.yandex.open_ai_base_url,
    )


def get_llm_repository() -> LLMRepository:
    openai_client = get_open_ai_client()
    yandex_gpt_client = get_yandex_gpt_client()
    yandex_gpt_oss_20b = get_gpt_oss_20_client()
    yandex_gpt_oss_120b = get_gpt_oss_120_client()
    yandex_qwen_235b = get_qwen_client()

    llm_repository: LLMRepository = LLMRepositoryImpl(
        chat_gpt_client=openai_client,
        yandex_gpt_client=yandex_gpt_client,
        qwen_client=yandex_qwen_235b,
        yandex_gpt_oss_120b_client=yandex_gpt_oss_120b,
        yandex_gpt_oss_20b_client=yandex_gpt_oss_20b,
    )
    return llm_repository


def get_generate_text_ai_use_case() -> GenerateTextAIUseCase:
    llm_repository: LLMRepository = get_llm_repository()

    return GenerateTextAIUseCase(llm_repository=llm_repository, ai_message_mapper=AIMessageMapper())


def get_llm_vision_repository() -> LLMVisionRepository:
    openai_client = get_open_ai_client()
    llm_vision_repository: LLMVisionRepository = LLMVisionRepositoryImpl(openai_client)
    return llm_vision_repository


def get_generate_vision_ai_use_case() -> GenerateVisionAIUseCase:
    llm_vision_repository: LLMVisionRepository = get_llm_vision_repository()
    return GenerateVisionAIUseCase(llm_vision_repository=llm_vision_repository, ai_message_mapper=AIMessageMapper())


def setup_logging(config: LoggingConfig) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(config.level)
    root_logger.handlers.clear()

    file_handler = TimedRotatingFileHandler(
        filename=config.file,
        when="H",
        interval=8,
        backupCount=2,
        utc=False,
        encoding="utf-8",
    )
    file_handler.setLevel(config.level)
    file_formatter = logging.Formatter(config.format)
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.level)
    console_formatter = logging.Formatter(config.format)
    console_handler.setFormatter(console_formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
