from app.application.exceptions import ConfigurationException
from app.application.interfaces.config_validator import ConfigValidator
from core.config import Config


class AppConfigValidator(ConfigValidator):

    def validate(self, config: Config) -> None:
        missing: list[str] = []

        # OpenAI
        if not config.open_ai.model:
            missing.append("OPENAI_MODEL")
        if not config.open_ai.api_key:
            missing.append("OPENAI_API_KEY")

        # Yandex auth
        if not config.yandex.key_id:
            missing.append("YANDEX_KEY_ID")
        if not config.yandex.service_account_id:
            missing.append("YANDEX_SERVICE_ACCOUNT_ID")
        if not config.yandex.private_key:
            missing.append("YANDEX_PRIVATE_KEY")

        # Yandex GPT
        if not config.yandex.yandex_gpt_model_path:
            missing.append("YANDEX_GPT_MODEL_PATH")
        if not config.yandex.yandex_gpt_api_url:
            missing.append("YANDEX_GPT_API_URL")
        if not config.yandex.yandex_gpt_model_name:
            missing.append("YANDEX_GPT_MODEL_NAME")

        # Yandex GPT OSS / OpenAI-compatible endpoint
        if not config.yandex.open_ai_api_key:
            missing.append("YANDEX_OPEN_AI_API_KEY")
        if not config.yandex.open_ai_base_url:
            missing.append("YANDEX_OPEN_AI_BASE_URL")
        if not config.yandex.gpt_oss_20b_model_name:
            missing.append("YANDEX_GPT_OSS_20B_MODEL_NAME")
        if not config.yandex.gpt_oss_120b_model_name:
            missing.append("YANDEX_GPT_OSS_120B_MODEL_NAME")
        if not config.yandex.qwen_235b_model_name:
            missing.append("YANDEX_QWEN_235B_MODEL_NAME")

        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ConfigurationException(f"Missing required configuration keys: {missing_list}")

