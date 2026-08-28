import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.model.loader import load_runtime
from app.services.generation_service import GenerationService

DEFAULT_ARTIFACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "model-artifacts"
    / "char-gpt-v1"
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    artifact_path = Path(
        os.getenv("MODEL_ARTIFACT_PATH", DEFAULT_ARTIFACT_PATH)
    )
    runtime = load_runtime(artifact_path)
    app.state.generation_service = GenerationService(runtime=runtime)

    yield
