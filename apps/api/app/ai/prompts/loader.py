"""Load and parse patient persona YAML files."""

from pathlib import Path
from typing import Any

import yaml

from app.config import Settings


def load_persona(settings: Settings, persona_path: str) -> dict[str, Any]:
    full_path = settings.prompts_path / persona_path
    if not full_path.exists():
        raise FileNotFoundError(f"Persona not found: {full_path}")
    with full_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_l0_invariants(settings: Settings) -> str:
    path = settings.prompts_path / "_base" / "L0_platform_invariants.yaml"
    if not path.exists():
        return "This is an educational simulation. Never diagnose or prescribe."
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("invariants_text", "")
