from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MINI_GPT_",
        extra="ignore",
    )

    model_artifact_path: Path = Path("model-artifacts/char-gpt-v1")
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
