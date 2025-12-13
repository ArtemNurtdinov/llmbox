import logging
from fastapi import APIRouter, Depends, HTTPException
from features.openai.open_ai import OpenAIClient
from features.ai_schemas import GenerateVisionAIRequestBody, GenerateAIRequestBody, AIResponse
from features.yandex.yandex_gpt import YandexGPTClient
from features.yandex.yandex_gpt_oss import YandexGPTOssClient
from features.ai_service import AIService

logger = logging.getLogger(__name__)
router = APIRouter()

_openai_client = OpenAIClient()
_yandex_gpt_client = YandexGPTClient()
_yandex_gpt_oss_client = YandexGPTOssClient()


def get_openai_client() -> OpenAIClient:
    return _openai_client


def get_yandex_gpt_client() -> YandexGPTClient:
    return _yandex_gpt_client


def get_yandex_gpt_oss_client() -> YandexGPTOssClient:
    return _yandex_gpt_oss_client


def get_ai_repository(
    open_ai=Depends(get_openai_client, use_cache=True),
    yandex_gpt=Depends(get_yandex_gpt_client, use_cache=True),
    yandex_gpt_oss_client=Depends(get_yandex_gpt_oss_client, use_cache=True)
) -> AIService:
    return AIService(open_ai, yandex_gpt, yandex_gpt_oss_client)


@router.post("/generate-ai-response", response_model=AIResponse)
async def generate_ai_response(
    body: GenerateAIRequestBody,
    ai_repo: AIService = Depends(get_ai_repository)
):
    try:
        return await ai_repo.generate_ai_response(body.messages, body.assistant)
    except ValueError as e:
        logger.error(f"AI REQUEST VALIDATION ERROR: assistant={body.assistant.value}, error={str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"AI REQUEST CRITICAL ERROR: assistant={body.assistant.value}, error={str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate AI response")


@router.post("/generate-ai-response-vision", response_model=AIResponse)
async def generate_vision_ai_response(
    body: GenerateVisionAIRequestBody,
    ai_repo: AIService = Depends(get_ai_repository)
):
    try:
        return await ai_repo.generate_ai_response_vision(body.messages)
    except ValueError as e:
        logger.error(f"VISION AI REQUEST VALIDATION ERROR: error={str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"VISION AI REQUEST CRITICAL ERROR: error={str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate Vision AI response")
