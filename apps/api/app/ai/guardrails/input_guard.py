"""Input guard — blocks student requests for real clinical advice."""

import re

BLOCKED_PATTERNS = [
    re.compile(r"\b(tengo|tengo\s+)?(depresi[oó]n|ansiedad|tdah|bipolar)\b", re.I),
    re.compile(r"\b(diagn[oó]stic|recet|medicament|pastilla)\b", re.I),
    re.compile(r"\b(qu[eé]\s+tengo|estoy\s+enferm)\b", re.I),
]

BLOCKED_MESSAGE = (
    "Este sistema es una simulación educativa y no puede ofrecer diagnósticos "
    "ni orientación clínica real. Continúa practicando tu entrevista con el paciente virtual."
)


def check_input(content: str) -> tuple[bool, str | None]:
    for pattern in BLOCKED_PATTERNS:
        if pattern.search(content):
            return False, BLOCKED_MESSAGE
    return True, None
