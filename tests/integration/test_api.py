from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

import app.core.lifespan as lifespan_module
from app.api.dependencies import get_generation_service
from app.main import app


class FakeRuntime:
    def __init__(self) -> None:
        self.call = None

    def generate(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_k: int | None,
    ) -> str:
        self.call = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
        }
        return f"{prompt} generated"


class FakeGenerationService:
    def __init__(self) -> None:
        self.call = None

    def generate(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_k: int | None,
    ) -> str:
        self.call = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
        }
        return "fake response"


@pytest.fixture
def client(monkeypatch) -> Iterator[TestClient]:
    fake_runtime = FakeRuntime()
    monkeypatch.setattr(
        lifespan_module,
        "load_runtime",
        lambda _artifact_path: fake_runtime,
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_with_lifespan_service(client: TestClient) -> None:
    response = client.post(
        "/generate",
        json={
            "prompt": "Once",
            "max_tokens": 20,
            "temperature": 0.8,
            "top_k": 10,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"text": "Once generated"}


def test_generate_with_replaced_service_dependency(
    client: TestClient,
) -> None:
    fake_service = FakeGenerationService()
    app.dependency_overrides[get_generation_service] = lambda: fake_service

    response = client.post(
        "/generate",
        json={
            "prompt": "Once",
            "max_tokens": 20,
            "temperature": 0.8,
            "top_k": 10,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"text": "fake response"}
    assert fake_service.call == {
        "prompt": "Once",
        "max_tokens": 20,
        "temperature": 0.8,
        "top_k": 10,
    }


@pytest.mark.parametrize(
    "payload",
    [
        {
            "prompt": "",
            "max_tokens": 20,
            "temperature": 0.8,
            "top_k": 10,
        },
        {
            "prompt": "Once",
            "max_tokens": 0,
            "temperature": 0.8,
            "top_k": 10,
        },
        {
            "prompt": "Once",
            "max_tokens": 20,
            "temperature": -0.1,
            "top_k": 10,
        },
        {
            "prompt": "Once",
            "max_tokens": 20,
            "temperature": 0.8,
            "top_k": 0,
        },
    ],
)
def test_generate_rejects_invalid_request(
    client: TestClient,
    payload: dict,
) -> None:
    response = client.post("/generate", json=payload)

    assert response.status_code == 422
