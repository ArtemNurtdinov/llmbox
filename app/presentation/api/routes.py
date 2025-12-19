import logging

from fastapi import APIRouter, Depends, HTTPException

from app.presentation.dependencies import create_ai_service
from app.application.services import AIService
from app.domain.models import AIAssistant
from app.presentation.api.schemas import AIResponseSchema, GenerateAIRequestSchema, GenerateVisionAIRequestSchema
from app.presentation.mappers.mappers import to_response_schema, _to_domain_ai_message, _to_domain_message

logger = logging.getLogger(__name__)
router = APIRouter()

_ai_service = create_ai_service()


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
