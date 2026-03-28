import logging
from functools import lru_cache
from logging.handlers import TimedRotatingFileHandler

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


@lru_cache
def load_config() -> Config:
    config_source: ConfigSource = EnvConfigSource()
    repository: ConfigRepository = ConfigRepositoryImpl(config_source)
    config = repository.get_config()
    validate_config_use_case = ValidateConfigUseCase()
    validate_config_use_case.validate(config)
    return config


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

    llm_repository: LLMRepository = LLMRepositoryImpl(
        chat_gpt_client=openai_client,
        yandex_gpt_client=yandex_gpt_client,
        qwen_client=yandex_qwen_235b,
        yandex_gpt_oss_120b_client=yandex_gpt_oss_120b,
        yandex_gpt_oss_20b_client=yandex_gpt_oss_20b,
    )

    return GenerateTextAIUseCase(llm_repository=llm_repository, ai_message_mapper=AIMessageMapper())


@lru_cache
def get_generate_text_ai_use_case() -> GenerateTextAIUseCase:
    config = load_config()
    return build_generate_text_ai_use_case(config)


def build_generate_vision_ai_use_case(config: Config) -> GenerateVisionAIUseCase:
    openai_client = OpenAIClient(model=config.open_ai.model, api_key=config.open_ai.api_key)
    llm_vision_repository: LLMVisionRepository = LLMVisionRepositoryImpl(openai_client)
    return GenerateVisionAIUseCase(llm_vision_repository=llm_vision_repository, ai_message_mapper=AIMessageMapper())


@lru_cache
def get_generate_vision_ai_use_case() -> GenerateVisionAIUseCase:
    config = load_config()
    return build_generate_vision_ai_use_case(config)


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
