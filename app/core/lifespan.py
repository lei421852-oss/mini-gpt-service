from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.model.loader import load_runtime
from app.services.generation_service import GenerationService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)

    runtime = load_runtime(settings.model_artifact_path)
    app.state.generation_service = GenerationService(runtime=runtime)

    yield
