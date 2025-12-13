import httpx
import logging
from config import config
from features.ai_schemas import Message, AIResponse, Usage
from features.yandex.auth import YandexAuth

logger = logging.getLogger(__name__)


class YandexGPTClient:
    _YANDEX_GPT_API_URL = config.yandex.yandex_gpt_api_url
    MODEL_PATH = config.yandex.yandex_gpt_model_path
    YANDEX_GPT_MODEL_NAME = config.yandex.yandex_gpt_model_name

    def __init__(self):
        self.auth = YandexAuth()

    async def generate_ai_response(self, user_messages: list[Message], model_name: str) -> AIResponse:
        try:
            model_uri = f"{self.MODEL_PATH}{model_name}"
            data = {
                "modelUri": model_uri,
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.2,
                    "maxTokens": 2000
                },
                "messages": [
                    {"role": message.role.value, "text": message.content} for message in user_messages
                ]
            }

            iam_key = await self.auth.get_iam_key()

            headers = {
                "Authorization": f"Bearer {iam_key}",
                "Content-Type": "application/json"
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{self._YANDEX_GPT_API_URL}/completion", json=data, headers=headers)

                if response.status_code != 200:
                    error_text = response.text
                    logger.error(f"Yandex GPT API error: status={response.status_code}, response={error_text}")
                    raise Exception(f"Yandex GPT API error: {response.status_code} - {error_text}")

                response_json = response.json()
                logger.debug(f"Yandex GPT response JSON: {response_json}")

            assistant_message = response_json["result"]["alternatives"][0]["message"]["text"]
            usage = response_json["result"]["usage"]

            prompt_tokens = int(usage["inputTextTokens"])
            completion_tokens = int(usage["completionTokens"])
            total_tokens = int(usage["totalTokens"])

            usage = Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens)
            return AIResponse(assistant_message=assistant_message, usage=usage)
        except Exception as e:
            logger.error(f"Yandex GPT error: model={model_name}, error={str(e)}", exc_info=True)
            raise