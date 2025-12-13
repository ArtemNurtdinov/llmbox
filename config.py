import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ApplicationConfig:
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8001"))


@dataclass
class OpenAIConfig:
    model = os.getenv("OPENAI_MODEL")
    api_key = os.getenv("OPENAI_API_KEY")


@dataclass
class YandexConfig:
    key_id = os.getenv("YANDEX_KEY_ID")
    service_account_id = os.getenv("YANDEX_SERVICE_ACCOUNT_ID")
    private_key = os.getenv("YANDEX_PRIVATE_KEY")
    yandex_gpt_model_path = os.getenv("YANDEX_GPT_MODEL_PATH")
    yandex_gpt_api_url = os.getenv("YANDEX_GPT_API_URL")
    yandex_gpt_model_name = os.getenv("YANDEX_GPT_MODEL_NAME")
    gpt_oss_120b_model_name = os.getenv("YANDEX_GPT_OSS_120B_MODEL_NAME")
    gpt_oss_20b_model_name = os.getenv("YANDEX_GPT_OSS_20B_MODEL_NAME")
    qwen_235b_model_name = os.getenv("YANDEX_QWEN_235B_MODEL_NAME")
    open_ai_api_key = os.getenv("YANDEX_OPEN_AI_API_KEY")
    open_ai_base_url = os.getenv("YANDEX_OPEN_AI_BASE_URL")


@dataclass
class LoggingConfig:
    level: str = os.getenv("LOG_LEVEL", "INFO")
    file: str = os.getenv("LOG_FILE", "llmbox.log")
    format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@dataclass
class Config:
    application: ApplicationConfig
    open_ai: OpenAIConfig
    yandex: YandexConfig
    logging: LoggingConfig


def load_config() -> Config:
    return Config(
        application=ApplicationConfig(),
        open_ai=OpenAIConfig(),
        yandex=YandexConfig(),
        logging=LoggingConfig()
    )


config = load_config()
