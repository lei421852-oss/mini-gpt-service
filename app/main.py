from fastapi import FastAPI

from app.api.routes.generation import router as generation_router
from app.api.routes.health import router as health_router
from app.core.lifespan import lifespan

app = FastAPI(
    title="mini-gpt-service",
    lifespan=lifespan,
)
app.include_router(health_router)
app.include_router(generation_router)
