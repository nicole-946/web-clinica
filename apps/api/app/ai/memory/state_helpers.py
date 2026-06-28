"""Interview state helpers."""

from typing import Any


def initial_state() -> dict[str, Any]:
    return {"trust_level": 0.0, "turn_count": 0, "topics_disclosed": []}


def update_trust(state: dict[str, Any], student_message: str) -> dict[str, Any]:
    msg = student_message.lower()
    boost = 0.0
    if any(w in msg for w in ["entiendo", "debe ser difícil", "gracias por compartir"]):
        boost = 0.15
    if "?" in student_message and not msg.startswith("por qué"):
        boost = max(boost, 0.05)
    new_trust = min(1.0, state.get("trust_level", 0.0) + boost)
    return {**state, "trust_level": new_trust, "turn_count": state.get("turn_count", 0) + 1}
