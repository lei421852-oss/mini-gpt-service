from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_generation_service
from app.api.schemas.generation import GenerateRequest, GenerateResponse
from app.services.generation_service import GenerationService

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
def generate(
    request: GenerateRequest,
    service: Annotated[
        GenerationService,
        Depends(get_generation_service),
    ],
) -> GenerateResponse:
    result = service.generate(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_k=request.top_k,
    )
    return GenerateResponse(
        text=result.text,
        generated_tokens=result.generated_tokens,
        latency_ms=result.latency_ms,
    )
