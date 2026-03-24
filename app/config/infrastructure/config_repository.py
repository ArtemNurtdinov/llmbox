from app.config.domain.config_repository import ConfigRepository
from app.config.domain.config_source import ConfigSource
from app.config.domain.model.application import ApplicationConfig
from app.config.domain.model.configuration import Config
from app.config.domain.model.logging import LoggingConfig
from app.config.domain.model.open_ai import OpenAIConfig
from app.config.domain.model.yandex import YandexConfig
from app.config.validation.domain.config_validator import ConfigValidator


class ConfigRepositoryImpl(ConfigRepository):
    def __init__(self, source: ConfigSource, validator: ConfigValidator):
        self._source = source
        self._validator = validator

    def get_config(self) -> Config:
        config = self._load_config_from_env()
        self._validator.validate(config)
        return config

    def _load_config_from_env(self) -> Config:
        return Config(
            application=ApplicationConfig(
                host=self._source.get("HOST", "0.0.0.0"),
                port=int(self._source.get("PORT", "8001")),
            ),
            open_ai=OpenAIConfig(
                model=self._source.get("OPENAI_MODEL"),
                api_key=self._source.get("OPENAI_API_KEY"),
            ),
            yandex=YandexConfig(
                key_id=self._source.get("YANDEX_KEY_ID"),
                service_account_id=self._source.get("YANDEX_SERVICE_ACCOUNT_ID"),
                private_key=self._source.get("YANDEX_PRIVATE_KEY"),
                yandex_gpt_model_path=self._source.get("YANDEX_GPT_MODEL_PATH"),
                yandex_gpt_api_url=self._source.get("YANDEX_GPT_API_URL"),
                yandex_gpt_model_name=self._source.get("YANDEX_GPT_MODEL_NAME"),
                gpt_oss_120b_model_name=self._source.get("YANDEX_GPT_OSS_120B_MODEL_NAME"),
                gpt_oss_20b_model_name=self._source.get("YANDEX_GPT_OSS_20B_MODEL_NAME"),
                qwen_235b_model_name=self._source.get("YANDEX_QWEN_235B_MODEL_NAME"),
                open_ai_api_key=self._source.get("YANDEX_OPEN_AI_API_KEY"),
                open_ai_base_url=self._source.get("YANDEX_OPEN_AI_BASE_URL"),
            ),
            logging=LoggingConfig(
                level=self._source.get("LOG_LEVEL", "INFO"),
                file=self._source.get("LOG_FILE", "llmbox.log"),
                format=self._source.get("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            ),
        )
