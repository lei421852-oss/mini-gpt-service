from fastapi import Request

from app.services.generation_service import GenerationService


def get_generation_service(request: Request) -> GenerationService:
    return request.app.state.generation_service
