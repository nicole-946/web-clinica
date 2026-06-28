"""Application settings loaded from environment."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[3] / ".env"),
        extra="ignore",
    )

    database_url: str = "sqlite+aiosqlite:///./clinical_sim.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:3000"
    llm_provider: str = "mock"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    system_prompts_dir: str = "system_prompts"
    evaluation_dir: str = "evaluation"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def repo_root(self) -> Path:
        # apps/api/app/config.py → repo root is three levels up
        return Path(__file__).resolve().parents[3]

    @property
    def prompts_path(self) -> Path:
        p = Path(self.system_prompts_dir)
        return p if p.is_absolute() else self.repo_root / p

    @property
    def evaluation_path(self) -> Path:
        p = Path(self.evaluation_dir)
        return p if p.is_absolute() else self.repo_root / p


@lru_cache
def get_settings() -> Settings:
    return Settings()
