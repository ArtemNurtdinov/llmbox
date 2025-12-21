import os
from functools import lru_cache

from dotenv import load_dotenv

from app.application.interfaces.config_provider import ConfigProvider
from core.config import (
    ApplicationConfig,
    Config,
    LoggingConfig,
    OpenAIConfig,
    YandexConfig,
)


class EnvConfigProvider(ConfigProvider):

    def get_config(self) -> Config:
        return self._load_config_from_env()

    def _load_config_from_env(self) -> Config:
        return Config(
            application=ApplicationConfig(
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "8001")),
            ),
            open_ai=OpenAIConfig(
                model=os.getenv("OPENAI_MODEL"),
                api_key=os.getenv("OPENAI_API_KEY"),
            ),
            yandex=YandexConfig(
                key_id=os.getenv("YANDEX_KEY_ID"),
                service_account_id=os.getenv("YANDEX_SERVICE_ACCOUNT_ID"),
                private_key=os.getenv("YANDEX_PRIVATE_KEY"),
                yandex_gpt_model_path=os.getenv("YANDEX_GPT_MODEL_PATH"),
                yandex_gpt_api_url=os.getenv("YANDEX_GPT_API_URL"),
                yandex_gpt_model_name=os.getenv("YANDEX_GPT_MODEL_NAME"),
                gpt_oss_120b_model_name=os.getenv("YANDEX_GPT_OSS_120B_MODEL_NAME"),
                gpt_oss_20b_model_name=os.getenv("YANDEX_GPT_OSS_20B_MODEL_NAME"),
                qwen_235b_model_name=os.getenv("YANDEX_QWEN_235B_MODEL_NAME"),
                open_ai_api_key=os.getenv("YANDEX_OPEN_AI_API_KEY"),
                open_ai_base_url=os.getenv("YANDEX_OPEN_AI_BASE_URL"),
            ),
            logging=LoggingConfig(
                level=os.getenv("LOG_LEVEL", "INFO"),
                file=os.getenv("LOG_FILE", "llmbox.log"),
                format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            ),
        )


@lru_cache()
def get_env_config_provider() -> EnvConfigProvider:
    load_dotenv()
    return EnvConfigProvider()
