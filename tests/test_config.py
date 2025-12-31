import unittest

from app.application.exceptions import ConfigurationException
from app.application.interfaces.config_source import ConfigSource
from app.application.services.config_validator import AppConfigValidator
from app.infrastructure.config.env_config_provider import EnvConfigProvider


class FakeConfigSource(ConfigSource):
    def __init__(self, values: dict[str, str | None]):
        self._values = values

    def get(self, key: str, default: str | None = None) -> str | None:
        return self._values.get(key, default)


FULL_ENV = {
    "HOST": "127.0.0.1",
    "PORT": "9000",
    "OPENAI_MODEL": "gpt-4",
    "OPENAI_API_KEY": "openai-key",
    "YANDEX_KEY_ID": "kid",
    "YANDEX_SERVICE_ACCOUNT_ID": "sa",
    "YANDEX_PRIVATE_KEY": "private",
    "YANDEX_GPT_MODEL_PATH": "path",
    "YANDEX_GPT_API_URL": "https://api",
    "YANDEX_GPT_MODEL_NAME": "ygpt",
    "YANDEX_GPT_OSS_120B_MODEL_NAME": "oss120b",
    "YANDEX_GPT_OSS_20B_MODEL_NAME": "oss20b",
    "YANDEX_QWEN_235B_MODEL_NAME": "qwen235b",
    "YANDEX_OPEN_AI_API_KEY": "ya-openai",
    "YANDEX_OPEN_AI_BASE_URL": "https://ya-openai",
}


class EnvConfigProviderTests(unittest.TestCase):
    def test_returns_typed_config_and_defaults(self) -> None:
        provider = EnvConfigProvider(FakeConfigSource(FULL_ENV), AppConfigValidator())

        config = provider.get_config()

        self.assertEqual(config.application.host, "127.0.0.1")
        self.assertEqual(config.application.port, 9000)
        self.assertEqual(config.open_ai.model, "gpt-4")
        self.assertEqual(config.logging.level, "INFO")

    def test_validator_raises_on_missing_required_keys(self) -> None:
        env = {**FULL_ENV}
        env.pop("OPENAI_MODEL")
        provider = EnvConfigProvider(FakeConfigSource(env), AppConfigValidator())

        with self.assertRaises(ConfigurationException):
            provider.get_config()


if __name__ == "__main__":
    unittest.main()

