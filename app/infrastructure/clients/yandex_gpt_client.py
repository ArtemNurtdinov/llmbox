import logging
from typing import List

import httpx

from app.domain.interfaces import TextModelClient
from app.domain.models import AIResponse, Message, Usage
from app.infrastructure.clients.yandex_auth import YandexAuth

logger = logging.getLogger(__name__)


class YandexGPTClient(TextModelClient):
    def __init__(
        self,
        api_url: str,
        model_path: str,
        model_name: str,
        auth: YandexAuth,
    ):
        if not api_url or not model_path or not model_name:
            raise ValueError("Yandex GPT api_url, model_path and model_name are required")
        self._api_url = api_url
        self._model_path = model_path
        self.model_name = model_name
        self.auth = auth

    async def generate(self, user_messages: List[Message]) -> AIResponse:
        model_uri = f"{self._model_path}{self.model_name}"
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
                response = await client.post(f"{self._api_url}/completion", json=data, headers=headers)

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


