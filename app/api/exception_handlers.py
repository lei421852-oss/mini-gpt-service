from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import UnknownCharacterError


async def unknown_character_error_handler(
    _request: Request,
    exc: UnknownCharacterError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
