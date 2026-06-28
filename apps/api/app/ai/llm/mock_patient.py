"""Mock patient LLM — deterministic responses for MVP without API key."""

from typing import Any


MOCK_RESPONSES = [
    "Hola... gracias por recibirme. No sé muy bien por dónde empezar.",
    "Últimamente duermo mal. Me cuesta mucho conciliar el sueño y me despierto cansada.",
    "Sí, eso es... siento que nada me ilusiona como antes. Todo me da igual.",
    "A veces pienso que es culpa mía, que debería poder salir de esto sola.",
    "En el trabajo me cuesta concentrarme. Mis compañeros no lo saben, pero me cuesta mucho.",
    "No quiero preocupar a mi familia... por eso no les he contado cómo me siento.",
]


def generate_mock_response(state: dict[str, Any], student_message: str) -> str:
    turn = state.get("turn_count", 0)
    trust = state.get("trust_level", 0.0)
    if "cómo te sientes" in student_message.lower() or "cómo estás" in student_message.lower():
        return MOCK_RESPONSES[1]
    if trust >= 0.5 and any(w in student_message.lower() for w in ["entiendo", "debe ser", "difícil"]):
        return MOCK_RESPONSES[5]
    idx = min(turn, len(MOCK_RESPONSES) - 1)
    return MOCK_RESPONSES[idx]
