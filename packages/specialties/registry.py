"""Specialty plugin registry — extend without modifying core."""

SPECIALTIES: dict[str, dict[str, str]] = {
    "clinical": {
        "prompts_dir": "system_prompts/clinical",
        "rubrics_dir": "evaluation/rubrics/clinical",
    },
    "organizational": {
        "prompts_dir": "system_prompts/organizational",
        "rubrics_dir": "evaluation/rubrics/organizational",
    },
    "educational": {
        "prompts_dir": "system_prompts/educational",
        "rubrics_dir": "evaluation/rubrics/educational",
    },
}
