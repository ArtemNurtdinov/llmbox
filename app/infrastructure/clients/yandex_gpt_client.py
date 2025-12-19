import logging
from typing import List

import httpx

from app.domain.interfaces import TextModelClient
from core.config import config
from app.domain.models import AIResponse, Message, Usage
from app.infrastructure.clients.yandex_auth import YandexAuth

logger = logging.getLogger(__name__)


class YandexGPTClient(TextModelClient):
    _YANDEX_GPT_API_URL = config.yandex.yandex_gpt_api_url
    MODEL_PATH = config.yandex.yandex_gpt_model_path

    def __init__(self, model_name: str | None = None, auth: YandexAuth | None = None):
        self.model_name = model_name or config.yandex.yandex_gpt_model_name
        self.auth = auth or YandexAuth()

    async def generate(self, user_messages: List[Message]) -> AIResponse:
        model_uri = f"{self.MODEL_PATH}{self.model_name}"
        data = {
            "modelUri": model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": 2000,
            },
            "messages": [
                {"role": message.role.value, "text": message.content} for message in user_messages
            ],
        }

        iam_key = await self.auth.get_iam_key()

        headers = {
            "Authorization": f"Bearer {iam_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{self._YANDEX_GPT_API_URL}/completion", json=data, headers=headers)

            if response.status_code != 200:
                error_text = response.text
                logger.error("Yandex GPT API error: status=%s, response=%s", response.status_code, error_text)
                raise Exception(f"Yandex GPT API error: {response.status_code} - {error_text}")

            response_json = response.json()
            logger.debug("Yandex GPT response JSON: %s", response_json)

            assistant_message = response_json["result"]["alternatives"][0]["message"]["text"]
            usage_raw = response_json["result"]["usage"]

            usage = Usage(
                prompt_tokens=int(usage_raw["inputTextTokens"]),
                completion_tokens=int(usage_raw["completionTokens"]),
                total_tokens=int(usage_raw["totalTokens"]),
            )
            return AIResponse(assistant_message=assistant_message, usage=usage)

        except Exception as exc:
            logger.error("Yandex GPT error: model=%s, error=%s", self.model_name, exc, exc_info=True)
            raise


