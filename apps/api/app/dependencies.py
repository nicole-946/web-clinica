"""FastAPI dependency injection."""

from functools import lru_cache

from app.config import Settings, get_settings
from app.services.session_service import SessionService


@lru_cache
def get_session_service() -> SessionService:
    return SessionService(get_settings())


def settings_dep() -> Settings:
    return get_settings()
