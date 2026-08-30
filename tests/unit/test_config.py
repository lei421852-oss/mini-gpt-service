from pathlib import Path

import pytest

from app.core.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_defaults(monkeypatch) -> None:
    monkeypatch.delenv("MINI_GPT_MODEL_ARTIFACT_PATH", raising=False)
    monkeypatch.delenv("MINI_GPT_LOG_LEVEL", raising=False)

    settings = get_settings()

    assert settings.model_artifact_path == Path(
        "model-artifacts/char-gpt-v1"
    )
    assert settings.log_level == "INFO"


def test_settings_environment_overrides_defaults(monkeypatch) -> None:
    monkeypatch.setenv(
        "MINI_GPT_MODEL_ARTIFACT_PATH",
        "/models/char-gpt-v2",
    )
    monkeypatch.setenv("MINI_GPT_LOG_LEVEL", "DEBUG")

    settings = get_settings()

    assert settings.model_artifact_path == Path("/models/char-gpt-v2")
    assert settings.log_level == "DEBUG"


def test_settings_uses_mini_gpt_prefix(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_ARTIFACT_PATH", "/models/unprefixed")
    monkeypatch.setenv("LOG_LEVEL", "ERROR")
    monkeypatch.delenv("MINI_GPT_MODEL_ARTIFACT_PATH", raising=False)
    monkeypatch.delenv("MINI_GPT_LOG_LEVEL", raising=False)

    settings = get_settings()

    assert settings.model_artifact_path == Path(
        "model-artifacts/char-gpt-v1"
    )
    assert settings.log_level == "INFO"
