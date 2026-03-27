from fastapi import APIRouter, Depends

from app.application.dto import AIResponseDTO
from app.bootstrap import get_generate_text_ai_use_case, get_generate_vision_ai_use_case
from app.llm.application.model.request.generate_text import GenerateAIRequestDTO
from app.llm.application.model.request.vision import GenerateVisionAIRequestDTO
from app.llm.application.usecase.generate_text_ai_use_case import GenerateTextAIUseCase
from app.llm.application.usecase.generate_vision_ai_use_case import GenerateVisionAIUseCase
from app.llm.infrastructure.decorators import handle_service_errors

router = APIRouter()


@handle_service_errors(endpoint_name="AI REQUEST")
@router.post("/generate-ai-response", response_model=AIResponseDTO)
async def generate_ai_response(
    body: GenerateAIRequestDTO, generate_text_ai_use_case: GenerateTextAIUseCase = Depends(get_generate_text_ai_use_case)
):
    return await generate_text_ai_use_case.execute(body)


@handle_service_errors(endpoint_name="VISION AI REQUEST")
@router.post("/generate-ai-response-vision", response_model=AIResponseDTO)
async def generate_vision_ai_response(
    body: GenerateVisionAIRequestDTO,
    generate_vision_ai_use_case: GenerateVisionAIUseCase = Depends(get_generate_vision_ai_use_case),
):
    return await generate_vision_ai_use_case.execute(body)
