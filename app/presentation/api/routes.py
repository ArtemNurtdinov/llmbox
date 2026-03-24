from fastapi import APIRouter, Depends

from app.bootstrap import get_generate_text_ai_use_case, get_generate_vision_ai_use_case
from app.llm.application.usecase.generate_text_ai_use_case import GenerateTextAIUseCase
from app.llm.application.usecase.generate_vision_ai_use_case import GenerateVisionAIUseCase
from app.presentation.api.schemas import AIResponseSchema, GenerateAIRequestSchema, GenerateVisionAIRequestSchema
from app.presentation.decorators import handle_service_errors
from app.presentation.mappers.mappers import to_generate_ai_request_dto, to_generate_vision_ai_request_dto, to_response_schema

router = APIRouter()


@handle_service_errors(endpoint_name="AI REQUEST")
@router.post("/generate-ai-response", response_model=AIResponseSchema)
async def generate_ai_response(
    body: GenerateAIRequestSchema, generate_text_ai_use_case: GenerateTextAIUseCase = Depends(get_generate_text_ai_use_case)
):
    request_dto = to_generate_ai_request_dto(body)
    response_dto = await generate_text_ai_use_case.execute(request_dto)
    return to_response_schema(response_dto)


@handle_service_errors(endpoint_name="VISION AI REQUEST")
@router.post("/generate-ai-response-vision", response_model=AIResponseSchema)
async def generate_vision_ai_response(
    body: GenerateVisionAIRequestSchema,
    generate_vision_ai_use_case: GenerateVisionAIUseCase = Depends(get_generate_vision_ai_use_case),
):
    request_dto = to_generate_vision_ai_request_dto(body)
    response_dto = await generate_vision_ai_use_case.execute(request_dto)
    return to_response_schema(response_dto)
