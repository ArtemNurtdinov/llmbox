from app.application.dto import AIResponseDTO, GenerateAIRequestDTO, GenerateVisionAIRequestDTO
from app.application.use_cases.generate_text_ai_use_case import GenerateTextAIUseCase
from app.application.use_cases.generate_vision_ai_use_case import GenerateVisionAIUseCase


class AIService:

    def __init__(self, generate_text_use_case: GenerateTextAIUseCase, generate_vision_use_case: GenerateVisionAIUseCase):
        self._generate_text_use_case = generate_text_use_case
        self._generate_vision_use_case = generate_vision_use_case

    async def generate_ai_response(self, dto: GenerateAIRequestDTO) -> AIResponseDTO:
        return await self._generate_text_use_case.execute(dto)

    async def generate_ai_response_vision(self, dto: GenerateVisionAIRequestDTO) -> AIResponseDTO:
        return await self._generate_vision_use_case.execute(dto)
