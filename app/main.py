from fastapi import FastAPI

from app.api.exception_handlers import unknown_character_error_handler
from app.api.routes.generation import router as generation_router
from app.api.routes.health import router as health_router
from app.core.exceptions import UnknownCharacterError
from app.core.lifespan import lifespan

app = FastAPI(
    title="mini-gpt-service",
    lifespan=lifespan,
)
app.add_exception_handler(
    UnknownCharacterError,
    unknown_character_error_handler,
)
app.include_router(health_router)
app.include_router(generation_router)
