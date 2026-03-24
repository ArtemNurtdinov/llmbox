from dataclasses import dataclass


@dataclass(frozen=True)
class YandexConfig:
    key_id: str | None
    service_account_id: str | None
    private_key: str | None
    yandex_gpt_model_path: str | None
    yandex_gpt_api_url: str | None
    yandex_gpt_model_name: str | None
    gpt_oss_120b_model_name: str | None
    gpt_oss_20b_model_name: str | None
    qwen_235b_model_name: str | None
    open_ai_api_key: str | None
    open_ai_base_url: str | None
