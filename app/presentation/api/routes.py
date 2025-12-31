from fastapi import APIRouter, Depends

from app.application.services import AIService
from app.presentation.api.schemas import AIResponseSchema, GenerateAIRequestSchema, GenerateVisionAIRequestSchema
from app.presentation.decorators import handle_service_errors
from app.presentation.dependencies import get_ai_service
from app.presentation.mappers.mappers import to_generate_ai_request_dto, to_generate_vision_ai_request_dto, to_response_schema

router = APIRouter()


@handle_service_errors(endpoint_name="AI REQUEST")
@router.post("/generate-ai-response", response_model=AIResponseSchema)
async def generate_ai_response(
    body: GenerateAIRequestSchema,
    ai_service: AIService = Depends(get_ai_service),
):
    request_dto = to_generate_ai_request_dto(body)
    response_dto = await ai_service.generate_ai_response(request_dto)
    return to_response_schema(response_dto)


@handle_service_errors(endpoint_name="VISION AI REQUEST")
@router.post("/generate-ai-response-vision", response_model=AIResponseSchema)
async def generate_vision_ai_response(
    body: GenerateVisionAIRequestSchema,
    ai_service: AIService = Depends(get_ai_service),
):
    request_dto = to_generate_vision_ai_request_dto(body)
    response_dto = await ai_service.generate_ai_response_vision(request_dto)
    return to_response_schema(response_dto)
