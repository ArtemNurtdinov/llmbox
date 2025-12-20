import asyncio
import logging
import time

import httpx
import jwt

logger = logging.getLogger(__name__)


class YandexAuth:
    def __init__(self, key_id: str, service_account_id: str, private_key: str):
        if not key_id or not service_account_id or not private_key:
            missing = []
            if not key_id:
                missing.append("key_id")
            if not service_account_id:
                missing.append("service_account_id")
            if not private_key:
                missing.append("private_key")
            logger.error("Missing required parameters: %s", missing)
            raise ValueError(f"Missing required parameters: {missing}")
        
        self._KEY_ID = key_id
        self._SERVICE_ACCOUNT_ID = service_account_id
        self._PRIVATE_KEY = self._normalize_private_key(private_key)
        logger.info("Initializing Yandex Auth...")

        self.jwt_token = None
        self.jwt_expires_at = 0
        self.iam_key = None
        self.iam_expires_at = 0
        self._iam_token_task = None
        logger.info("Yandex Auth initialized")

    @staticmethod
    def _normalize_private_key(key: str | None) -> str | None:
        if not key:
            return key
        key = key.strip().strip('"').strip("'")
        return key.replace("\\n", "\n")

    def _is_jwt_valid(self) -> bool:
        return self.jwt_token is not None and time.time() < self.jwt_expires_at - 60  # 60 seconds buffer

    def _is_iam_valid(self) -> bool:
        return self.iam_key is not None and time.time() < self.iam_expires_at - 60  # 60 seconds buffer

    async def get_iam_key(self) -> str:
        try:
            if not self._is_jwt_valid():
                logger.info("JWT token expired or missing, creating new one...")
                self.jwt_token = self.create_jwt_token()
                self.iam_key = None
                self.iam_expires_at = 0

            if not self._is_iam_valid():
                logger.info("IAM token expired or missing, creating new one...")
                self.iam_key = await self.create_iam_token(self.jwt_token)
                self.iam_expires_at = time.time() + 3600

                if self._iam_token_task is None:
                    logger.info("Starting IAM token refresh task...")
                    self._iam_token_task = asyncio.create_task(self.update_iam_token())

            logger.debug("IAM key provided")
            return self.iam_key

        except Exception as exc:
            logger.error("Error getting IAM key: %s", exc, exc_info=True)
            self.jwt_token = None
            self.jwt_expires_at = 0
            self.iam_key = None
            self.iam_expires_at = 0
            raise

    def create_jwt_token(self) -> str:
        try:
            logger.debug("Creating JWT token...")
            now = int(time.time())
            expires_at = now + 3600
            payload = {
                "aud": "https://iam.api.cloud.yandex.net/iam/v1/tokens",
                "iss": self._SERVICE_ACCOUNT_ID,
                "iat": now,
                "exp": expires_at,
            }
            encoded_token = jwt.encode(
                payload,
                self._PRIVATE_KEY,
                algorithm="PS256",
                headers={"kid": self._KEY_ID},
            )

            self.jwt_expires_at = expires_at

            logger.debug("JWT token created, expires at %s", expires_at)
            return encoded_token

        except Exception as exc:
            logger.error("Error creating JWT token: %s", exc, exc_info=True)
            raise

    async def create_iam_token(self, jwt_token: str) -> str:
        try:
            iam_token_url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"

            headers = {
                "Content-Type": "application/json"
            }

            data = {
                "jwt": jwt_token
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(iam_token_url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()["iamToken"]
                return result
            error_text = response.text
            logger.error("IAM token creation failed: status=%s, response=%s", response.status_code, error_text)
            raise Exception(f"Ошибка при получении IAM-токена: {response.status_code} - {error_text}")

        except Exception as exc:
            logger.error("Error creating IAM token: %s", exc, exc_info=True)
            raise

    async def update_iam_token(self):
        try:
            await asyncio.sleep(3000)
            while True:
                try:
                    self.jwt_token = self.create_jwt_token()
                    self.iam_key = await self.create_iam_token(self.jwt_token)
                    self.iam_expires_at = time.time() + 3600
                    logger.info("Tokens refreshed successfully")
                except Exception as exc:
                    logger.error("Error refreshing tokens: %s", exc, exc_info=True)
                    self.jwt_token = None
                    self.jwt_expires_at = 0
                    self.iam_key = None
                    self.iam_expires_at = 0
                await asyncio.sleep(3000)

        except Exception as exc:
            logger.error("Token refresh task crashed: %s", exc, exc_info=True)
            self._iam_token_task = None



