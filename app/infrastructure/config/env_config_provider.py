from functools import lru_cache
from dotenv import load_dotenv
from app.application.interfaces.config_provider import ConfigProvider
from core.config import Config, load_config

class EnvConfigProvider(ConfigProvider):

    def __init__(self) -> None:
        load_dotenv()

    @lru_cache()
    def get_config(self) -> Config:
        return load_config()


@lru_cache()
def get_env_config_provider() -> EnvConfigProvider:
    return EnvConfigProvider()
