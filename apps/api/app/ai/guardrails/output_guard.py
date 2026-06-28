"""Output guard — ensures virtual patient stays in character and safe."""

import re

UNSAFE_PATTERNS = [
    re.compile(r"\b(debes tomar|te receto|te recomiendo tomar)\b", re.I),
    re.compile(r"\b(tienes (depresi[oó]n|ansiedad|trastorno))\b", re.I),
    re.compile(r"\b(diagn[oó]stico:|dsm[- ]?5)\b", re.I),
    re.compile(r"\b(soy un asistente|como ia|inteligencia artificial)\b", re.I),
]

SAFE_FALLBACK = (
    "No sé... es difícil ponerle nombre. Solo sé que me siento muy mal últimamente "
    "y no tengo ganas de hacer nada."
)


def check_output(content: str) -> tuple[bool, str]:
    for pattern in UNSAFE_PATTERNS:
        if pattern.search(content):
            return False, SAFE_FALLBACK
    return True, content
