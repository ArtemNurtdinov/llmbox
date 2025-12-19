import logging

from fastapi import APIRouter, Depends, HTTPException

from app.application.services import AIService
from core.config import config
from app.domain.interfaces import TextModelClient, VisionModelClient
from app.domain.models import AIAssistant
from app.presentation.api.schemas import AIResponseSchema, GenerateAIRequestSchema, GenerateVisionAIRequestSchema
from app.infrastructure.clients.openai_client import OpenAIClient
from app.infrastructure.clients.yandex_gpt_client import YandexGPTClient
from app.infrastructure.clients.yandex_gpt_oss_client import YandexGPTOssClient
from app.presentation.mappers.mappers import to_response_schema, _to_domain_ai_message, _to_domain_message

logger = logging.getLogger(__name__)
router = APIRouter()


def _create_ai_service() -> AIService:
    openai_client = OpenAIClient()
    yandex_gpt_client = YandexGPTClient()
    yandex_gpt_oss_20b = YandexGPTOssClient(model_name=config.yandex.gpt_oss_20b_model_name)
    yandex_gpt_oss_120b = YandexGPTOssClient(model_name=config.yandex.gpt_oss_120b_model_name)
    yandex_qwen_235b = YandexGPTOssClient(model_name=config.yandex.qwen_235b_model_name)

    text_clients: dict[AIAssistant, TextModelClient] = {
        AIAssistant.CHAT_GPT: openai_client,
        AIAssistant.YANDEX_GPT: yandex_gpt_client,
        AIAssistant.GPT_OSS_20B: yandex_gpt_oss_20b,
        AIAssistant.GPT_OSS_120B: yandex_gpt_oss_120b,
        AIAssistant.QWEN3_235B: yandex_qwen_235b,
    }

    vision_client: VisionModelClient = openai_client

    return AIService(text_clients=text_clients, vision_client=vision_client)


_ai_service = _create_ai_service()


def get_ai_service() -> AIService:
    return _ai_service


@router.post("/generate-ai-response", response_model=AIResponseSchema)
async def generate_ai_response(
    body: GenerateAIRequestSchema,
    ai_service: AIService = Depends(get_ai_service),
):
    try:
        messages = [_to_domain_message(msg) for msg in body.messages]
        assistant = AIAssistant(body.assistant)
        result = await ai_service.generate_ai_response(messages, assistant)
        return to_response_schema(result)
    except ValueError as exc:
        logger.error("AI REQUEST VALIDATION ERROR: assistant=%s, error=%s", body.assistant.value, exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.error("AI REQUEST CRITICAL ERROR: assistant=%s, error=%s", body.assistant.value, exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate AI response")


@router.post("/generate-ai-response-vision", response_model=AIResponseSchema)
async def generate_vision_ai_response(
    body: GenerateVisionAIRequestSchema,
    ai_service: AIService = Depends(get_ai_service),
):
    try:
        messages = [_to_domain_ai_message(msg) for msg in body.messages]
        result = await ai_service.generate_ai_response_vision(messages)
        return to_response_schema(result)
    except ValueError as exc:
        logger.error("VISION AI REQUEST VALIDATION ERROR: error=%s", exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.error("VISION AI REQUEST CRITICAL ERROR: error=%s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate Vision AI response")

