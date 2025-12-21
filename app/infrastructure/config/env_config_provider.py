from app.application.interfaces.config_provider import ConfigProvider
from app.application.interfaces.config_source import ConfigSource
from app.application.interfaces.config_validator import ConfigValidator
from app.application.services.config_validator import AppConfigValidator
from app.infrastructure.config.env_config_source import EnvConfigSource
from core.config import (
    ApplicationConfig,
    Config,
    LoggingConfig,
    OpenAIConfig,
    YandexConfig,
)


class EnvConfigProvider(ConfigProvider):

    def __init__(self, source: ConfigSource | None = None, validator: ConfigValidator | None = None):
        self._source = source or EnvConfigSource()
        self._validator = validator or AppConfigValidator()

    def get_config(self) -> Config:
        config = self._load_config_from_env()
        self._validator.validate(config)
        return config

    def _load_config_from_env(self) -> Config:
        env = self._source
        return Config(
            application=ApplicationConfig(
                host=env.get("HOST", "0.0.0.0"),
                port=int(env.get("PORT", "8001")),
            ),
            open_ai=OpenAIConfig(
                model=env.get("OPENAI_MODEL"),
                api_key=env.get("OPENAI_API_KEY"),
            ),
            yandex=YandexConfig(
                key_id=env.get("YANDEX_KEY_ID"),
                service_account_id=env.get("YANDEX_SERVICE_ACCOUNT_ID"),
                private_key=env.get("YANDEX_PRIVATE_KEY"),
                yandex_gpt_model_path=env.get("YANDEX_GPT_MODEL_PATH"),
                yandex_gpt_api_url=env.get("YANDEX_GPT_API_URL"),
                yandex_gpt_model_name=env.get("YANDEX_GPT_MODEL_NAME"),
                gpt_oss_120b_model_name=env.get("YANDEX_GPT_OSS_120B_MODEL_NAME"),
                gpt_oss_20b_model_name=env.get("YANDEX_GPT_OSS_20B_MODEL_NAME"),
                qwen_235b_model_name=env.get("YANDEX_QWEN_235B_MODEL_NAME"),
                open_ai_api_key=env.get("YANDEX_OPEN_AI_API_KEY"),
                open_ai_base_url=env.get("YANDEX_OPEN_AI_BASE_URL"),
            ),
            logging=LoggingConfig(
                level=env.get("LOG_LEVEL", "INFO"),
                file=env.get("LOG_FILE", "llmbox.log"),
                format=env.get("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            ),
        )
