import asyncio
import time
import jwt
import httpx
import logging

from config import config

logger = logging.getLogger(__name__)


class YandexAuth:
    _KEY_ID = config.yandex.key_id
    _SERVICE_ACCOUNT_ID = config.yandex.service_account_id
    _PRIVATE_KEY = config.yandex.private_key

    def __init__(self):
        self._PRIVATE_KEY = self._normalize_private_key(self._PRIVATE_KEY)
        logger.info("Initializing Yandex Auth...")
        
        if not all([self._KEY_ID, self._SERVICE_ACCOUNT_ID, self._PRIVATE_KEY]):
            missing = []
            if not self._KEY_ID: missing.append("technokratos_yandex_key_id")
            if not self._SERVICE_ACCOUNT_ID: missing.append("technokratos_yandex_service_account_id")
            if not self._PRIVATE_KEY: missing.append("technokratos_yandex_private_key")
            logger.error(f"Missing environment variables: {missing}")
            raise ValueError(f"Missing required environment variables: {missing}")
        
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
            
        except Exception as e:
            logger.error(f"Error getting IAM key: {str(e)}", exc_info=True)
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
                'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                'iss': self._SERVICE_ACCOUNT_ID,
                'iat': now,
                'exp': expires_at
            }
            encoded_token = jwt.encode(
                payload,
                self._PRIVATE_KEY,
                algorithm='PS256',
                headers={'kid': self._KEY_ID}
            )

            self.jwt_expires_at = expires_at
            
            logger.debug(f"JWT token created, expires at {expires_at}")
            return encoded_token
            
        except Exception as e:
            logger.error(f"Error creating JWT token: {str(e)}", exc_info=True)
            raise

    async def create_iam_token(self, jwt_token: str) -> str:
        try:
            iam_token_url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"

            headers = {
                'Content-Type': 'application/json'
            }

            data = {
                "jwt": jwt_token
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(iam_token_url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()["iamToken"]
                return result
            else:
                error_text = response.text
                logger.error(f"IAM token creation failed: status={response.status_code}, response={error_text}")
                raise Exception(f"Ошибка при получении IAM-токена: {response.status_code} - {error_text}")
                
        except Exception as e:
            logger.error(f"Error creating IAM token: {str(e)}", exc_info=True)
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
                except Exception as e:
                    logger.error(f"Error refreshing tokens: {str(e)}", exc_info=True)
                    self.jwt_token = None
                    self.jwt_expires_at = 0
                    self.iam_key = None
                    self.iam_expires_at = 0
                await asyncio.sleep(3000)
                
        except Exception as e:
            logger.error(f"Token refresh task crashed: {str(e)}", exc_info=True)
            self._iam_token_task = None
