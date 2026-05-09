"""
Mustache prompt template loader.

Loads .md templates from the arlo/prompts/ directory and renders
them with chevron (Mustache for Python).
"""
from pathlib import Path

import chevron

_PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_template(name: str) -> str:
    """Load a raw Mustache template by name (without extension)."""
    path = _PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text(encoding="utf-8")


def render_template(name: str, context: dict) -> str:
    """Load and render a Mustache template with the given context."""
    template = load_template(name)
    return chevron.render(template, context)
