import logging

from fastapi import APIRouter, Depends, HTTPException

from app.presentation.dependencies import get_ai_service
from app.application.services import AIService
from app.presentation.api.schemas import AIResponseSchema, GenerateAIRequestSchema, GenerateVisionAIRequestSchema
from app.presentation.mappers.mappers import to_response_schema, to_generate_ai_request_dto, to_generate_vision_ai_request_dto

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate-ai-response", response_model=AIResponseSchema)
async def generate_ai_response(
    body: GenerateAIRequestSchema,
    ai_service: AIService = Depends(get_ai_service),
):
    try:
        request_dto = to_generate_ai_request_dto(body)
        response_dto = await ai_service.generate_ai_response(request_dto)
        return to_response_schema(response_dto)
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
        request_dto = to_generate_vision_ai_request_dto(body)
        response_dto = await ai_service.generate_ai_response_vision(request_dto)
        return to_response_schema(response_dto)
    except ValueError as exc:
        logger.error("VISION AI REQUEST VALIDATION ERROR: error=%s", exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.error("VISION AI REQUEST CRITICAL ERROR: error=%s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate Vision AI response")
