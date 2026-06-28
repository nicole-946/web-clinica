"""Patient response service — isolated LLM layer per architect rules."""

import logging
from typing import Any

from app.ai.guardrails.output_guard import check_output
from app.ai.llm.mock_patient import generate_mock_response
from app.config import Settings

logger = logging.getLogger(__name__)


class PatientLLMService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def respond(
        self,
        persona: dict[str, Any],
        state: dict[str, Any],
        student_message: str,
    ) -> tuple[str, dict[str, Any]]:
        try:
            raw = await self._generate(persona, state, student_message)
            safe, content = check_output(raw)
            meta = {"guardrail_triggered": not safe}
            return content, meta
        except Exception:
            logger.exception("Patient LLM failed")
            fallback = "Perdón... no sé qué decir ahora mismo."
            return fallback, {"error": True}

    async def _generate(
        self,
        persona: dict[str, Any],
        state: dict[str, Any],
        student_message: str,
    ) -> str:
        if self._settings.llm_provider == "mock":
            return generate_mock_response(state, student_message)
        return generate_mock_response(state, student_message)
