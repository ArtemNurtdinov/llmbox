from app.llm.domain.client.text import TextClient
from app.llm.domain.exception.unknown_assistant import UnknownAssistantException
from app.llm.domain.llm_repository import LLMRepository
from app.llm.domain.model.ai_message import AIMessage
from app.llm.domain.model.assistant import AIAssistant
from app.llm.domain.model.message import Message


class LLMRepositoryImpl(LLMRepository):
    def __init__(
        self,
        chat_gpt_client: TextClient,
        yandex_gpt_client: TextClient,
        qwen_client: TextClient,
        yandex_gpt_oss_20b_client: TextClient,
        yandex_gpt_oss_120b_client: TextClient,
    ):
        self._chat_gpt_client = chat_gpt_client
        self._yandex_gpt_client = yandex_gpt_client
        self._qwen_client = qwen_client
        self._yandex_gpt_oss_120b_client = yandex_gpt_oss_120b_client
        self._yandex_gpt_oss_20b_client = yandex_gpt_oss_20b_client

    async def generate(self, assistant: AIAssistant, messages: list[Message]) -> AIMessage:
        match assistant:
            case AIAssistant.CHAT_GPT:
                return await self._chat_gpt_client.generate(messages)
            case AIAssistant.YANDEX_GPT:
                return await self._yandex_gpt_client.generate(messages)
            case AIAssistant.QWEN3_235B:
                return await self._qwen_client.generate(messages)
            case AIAssistant.GPT_OSS_120B:
                return await self._yandex_gpt_oss_120b_client.generate(messages)
            case AIAssistant.GPT_OSS_20B:
                return await self._yandex_gpt_oss_20b_client.generate(messages)

        raise UnknownAssistantException()
