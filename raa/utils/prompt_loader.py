"""Prompt template loader using chevron mustache rendering with skill injection."""
from __future__ import annotations

import re
from pathlib import Path

import chevron

from raa.utils.skill_loader import load_skill_section

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

_SKILL_DECL_PATTERN = re.compile(
    r"\{\{!\s*skill:\s*(\S+)\s+as\s+(\S+)\s*\}\}"
)


class SkillContextKeyCollisionError(Exception):
    """Skill injection would overwrite an explicit caller-provided context key."""


def load_prompt(template_name: str, context: dict) -> str:
    """Load a mustache template from raa/prompts/ and render with context.

    Skill declarations in the template (``{{! skill: <tag> as <key> }}``)
    are resolved via ``skill_loader`` and injected into the render context
    before calling ``chevron.render()``.

    Args:
        template_name: Filename without path (e.g. ``"saam_analysis.md"``).
        context: Dict of template variables.

    Returns:
        Rendered prompt string.

    Raises:
        FileNotFoundError: Template file not found.
        SkillContextKeyCollisionError: A skill key would overwrite a caller key.
    """
    template_path = _PROMPTS_DIR / template_name
    if not template_path.is_file():
        raise FileNotFoundError(f"Prompt template not found: {template_path}")
    with open(template_path) as f:
        template = f.read()

    # Resolve skill declarations
    declarations = _SKILL_DECL_PATTERN.findall(template)
    if declarations:
        render_context = dict(context)
        for tag, key in declarations:
            if key in render_context:
                raise SkillContextKeyCollisionError(
                    f"Skill injection key '{key}' (tag: '{tag}') would overwrite "
                    f"an explicit context key. Rename the 'as' variable in the "
                    f"template or remove the conflicting context key."
                )
            render_context[key] = load_skill_section(tag)
        return chevron.render(template, render_context)

    return chevron.render(template, context)
