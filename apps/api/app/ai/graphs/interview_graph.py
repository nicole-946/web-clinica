"""Interview graph — orchestrates one chat turn (guard → respond → guard → state)."""

from typing import Any

from app.ai.guardrails.input_guard import check_input
from app.ai.llm.patient_service import PatientLLMService
from app.ai.memory.state_helpers import update_trust
from app.config import Settings


class InterviewGraph:
    def __init__(self, settings: Settings, patient_service: PatientLLMService) -> None:
        self._settings = settings
        self._patient = patient_service

    async def run_turn(
        self,
        persona: dict[str, Any],
        state: dict[str, Any],
        student_message: str,
    ) -> dict[str, Any]:
        ok, blocked = check_input(student_message)
        if not ok:
            return self._blocked_turn(state, blocked or "")
        content, meta = await self._patient.respond(persona, state, student_message)
        new_state = update_trust(state, student_message)
        return {
            "patient_content": content,
            "patient_metadata": meta,
            "session_state": new_state,
            "blocked": False,
        }

    def _blocked_turn(self, state: dict[str, Any], message: str) -> dict[str, Any]:
        return {
            "patient_content": message,
            "patient_metadata": {"input_guard": True},
            "session_state": state,
            "blocked": True,
        }
