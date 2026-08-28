import pytest
from pydantic import ValidationError

from app.api.schemas.generation import GenerateRequest


def test_generate_request_accepts_valid_values() -> None:
    request = GenerateRequest(
        prompt="Once",
        max_tokens=20,
        temperature=0.8,
    )

    assert request.top_k is None


@pytest.mark.parametrize(
    "data",
    [
        {"prompt": "", "max_tokens": 20, "temperature": 0.8},
        {"prompt": "Once", "max_tokens": 0, "temperature": 0.8},
        {"prompt": "Once", "max_tokens": 20, "temperature": -0.1},
        {
            "prompt": "Once",
            "max_tokens": 20,
            "temperature": 0.8,
            "top_k": 0,
        },
    ],
)
def test_generate_request_rejects_invalid_values(data) -> None:
    with pytest.raises(ValidationError):
        GenerateRequest(**data)
