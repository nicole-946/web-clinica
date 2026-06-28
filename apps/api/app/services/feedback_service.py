"""Post-session feedback evaluator (separate from patient agent)."""

import json
from pathlib import Path
from typing import Any

from app.config import Settings


def _count_open_questions(messages: list[dict[str, str]]) -> int:
    student = [m["content"] for m in messages if m["role"] == "student"]
    return sum(1 for m in student if "?" in m and not m.lower().startswith("¿por qué"))


def _count_validation(messages: list[dict[str, str]]) -> int:
    keywords = ["entiendo", "debe ser difícil", "tiene sentido", "gracias por compartir"]
    student = [m["content"].lower() for m in messages if m["role"] == "student"]
    return sum(1 for m in student if any(k in m for k in keywords))


def _score_dimension(count: int, thresholds: tuple[int, int, int]) -> int:
    if count >= thresholds[2]:
        return 5
    if count >= thresholds[1]:
        return 4
    if count >= thresholds[0]:
        return 3
    return 2 if count >= 1 else 1


APA_REFERENCES: dict[str, str] = {
    "maria-depression": (
        "Asociación Americana de Psiquiatría. (2014). *Manual diagnóstico y estadístico de los trastornos "
        "mentales* (5ª ed.; DSM-5). Editorial Médica Panamericana.\n\n"
        "Beck, A. T., Rush, A. J., Shaw, B. F., & Emery, G. (1979). *Cognitive therapy of depression*. Guilford Press."
    ),
    "pedro-anxiety": (
        "Asociación Americana de Psiquiatría. (2014). *Manual diagnóstico y estadístico de los trastornos "
        "mentales* (5ª ed.; DSM-5). Editorial Médica Panamericana.\n\n"
        "Beck, A. T., Emery, G., & Greenberg, R. L. (2005). *Anxiety disorders and phobias: A cognitive perspective*. "
        "Basic Books."
    ),
    "lucia-borderline": (
        "Asociación Americana de Psiquiatría. (2014). *Manual diagnóstico y estadístico de los trastornos "
        "mentales* (5ª ed.; DSM-5). Editorial Médica Panamericana.\n\n"
        "Linehan, M. M. (1993). *Cognitive-behavioral treatment of borderline personality disorder*. Guilford Press."
    ),
}


class FeedbackEvaluator:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def evaluate(self, messages: list[dict[str, str]], case_id: str | None = None) -> dict[str, Any]:
        rubric = self._load_rubric()
        open_q = _count_open_questions(messages)
        validation = _count_validation(messages)
        scores = {
            "active_listening": _score_dimension(validation, (1, 2, 3)),
            "validation": _score_dimension(validation, (1, 2, 3)),
            "question_quality": _score_dimension(open_q, (2, 4, 6)),
        }
        narrative = self._build_narrative(scores, open_q, validation, case_id)
        return {
            "rubric_version": rubric.get("version", "1.0"),
            "scores": scores,
            "narrative": narrative,
            "highlights": self._highlights(messages),
        }

    def _load_rubric(self) -> dict[str, Any]:
        path = self._settings.evaluation_path / "rubrics" / "clinical" / "intake_interview_v1.json"
        if not path.exists():
            return {"version": "1.0"}
        return json.loads(path.read_text(encoding="utf-8"))

    def _build_narrative(
        self, scores: dict[str, int], open_q: int, validation: int, case_id: str | None = None
    ) -> str:
        lines = [
            "## Retroalimentación pedagógica\n",
            "Esta evaluación es formativa y se basa en técnicas de entrevista clínica simulada.\n",
            f"- **Escucha activa / validación:** {scores['validation']}/5",
            f"- **Calidad de preguntas:** {scores['question_quality']}/5",
            f"- Preguntas abiertas detectadas: {open_q}",
            f"- Expresiones de validación detectadas: {validation}\n",
            "**Sugerencia:** Practica parafrasear lo emocional antes de formular la siguiente pregunta.\n",
        ]
        
        # Append strictly formatted APA 7 references based on case_id
        lines.append("### Lecturas recomendadas (Referencias APA 7ma edición):\n")
        ref = APA_REFERENCES.get(case_id or "maria-depression")
        lines.append(ref)
        
        return "\n".join(lines)

    def _highlights(self, messages: list[dict[str, str]]) -> list[dict[str, str]]:
        student = [m for m in messages if m["role"] == "student"][:3]
        return [{"role": "student", "quote": m["content"][:200]} for m in student]
