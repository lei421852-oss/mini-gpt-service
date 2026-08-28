from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)
    max_tokens: int = Field(gt=0)
    temperature: float = Field(ge=0)
    top_k: int | None = Field(default=None, gt=0)


class GenerateResponse(BaseModel):
    text: str
