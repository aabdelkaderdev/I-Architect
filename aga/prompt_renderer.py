"""Template variable builder and Mustache renderer for AGA prompts.

Serialises DiagramSpec into flat Mustache variable dicts and renders
prompt templates with skill-injection pre-processing.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import chevron

from aga.config import AGAConfig
from aga.schemas import DiagramSpec

# Regex for skill injection directives: {{! skill: <tag> as <var> }}
_SKILL_RE = re.compile(r"\{\{!\s*skill:\s*(\S+)\s+as\s+(\S+)\s*\}\}")

# Path to the skills reference file, resolved relative to this module.
_SKILLS_DIR = Path(__file__).resolve().parent / "Skills" / "references"
_C4_REF = _SKILLS_DIR / "c4.md"


def load_skill_content(tag: str) -> str:
    """Load tagged content from Skills/references/c4.md.

    Parameters
    ----------
    tag : str
        Skill tag in the form ``"c4:rules"``.  The part after the colon
        maps to a section heading in ``c4.md`` (e.g. ``"rules"`` → ``# Rules``).

    Returns
    -------
    str
        The content of the referenced section, or an empty string if the
        tag or section is not found.
    """
    if ":" not in tag:
        return ""
    _prefix, section_key = tag.split(":", 1)
    try:
        text = _C4_REF.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

    heading = f"# {section_key.replace('_', ' ').title()}"
    # Match from the heading to the next same-level heading or EOF
    pattern = re.compile(
        rf"^{re.escape(heading)}\s*$(.+?)(?=^#\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def render_template(template_path: str, variables: dict) -> str:
    """Render a Mustache template file with skill injection and variables.

    1. Scans the template for ``{{! skill: <tag> as <var> }}`` directives.
    2. Loads the referenced content and adds it to *variables*.
    3. Strips the YAML frontmatter and skill-injection directives.
    4. Renders the cleaned template with chevron.

    Parameters
    ----------
    template_path : str
        Path to the ``.md`` Mustache template file.
    variables : dict
        Flat key→value dict of Mustache variables.

    Returns
    -------
    str
        Rendered prompt string.
    """
    raw = Path(template_path).read_text(encoding="utf-8")

    # --- skill injection pre-processing ---
    enriched = dict(variables)
    for match in _SKILL_RE.finditer(raw):
        tag = match.group(1)
        var_name = match.group(2)
        content = load_skill_content(tag)
        enriched[var_name] = content

    # --- strip YAML frontmatter and skill directives ---
    body = raw
    if body.startswith("---"):
        parts = body.split("---", 2)
        body = parts[2] if len(parts) >= 3 else body

    body = _SKILL_RE.sub("", body)

    return chevron.render(body, enriched)


# ── Variable builder (from Phase 5) ─────────────────────────────────────────


def build_template_vars(
    spec: DiagramSpec,
    config: AGAConfig,
    retry_count: int = 0,
    error_text: str = "",
    current_puml_code: str = "",
) -> dict:
    """Build the flat variable dict for Mustache template rendering.

    Parameters
    ----------
    spec : DiagramSpec
        The diagram being processed.
    config : AGAConfig
        Runtime config (supplies plantuml_base_url, max_retries, output_dir).
    retry_count : int
        Current render attempt count for error_correction template.
    error_text : str
        Error message for error_correction template.
    current_puml_code : str
        Current PUML code for error_correction template.

    Returns
    -------
    dict
        Flat key→value dict ready to pass to the Mustache renderer.
    """
    is_context = spec.diagram_type == "context"
    is_container = spec.diagram_type == "container"
    is_component = spec.diagram_type == "component"

    output_path = str(Path(config.output_dir) / spec.output_filename)

    source_l1 = spec.source_l1
    source_l2 = spec.source_l2
    source_l3 = spec.source_l3

    return {
        # —— Always-set fields ——
        "diagram_id": spec.diagram_id,
        "diagram_type": spec.diagram_type,
        "diagram_label": spec.label,
        "plantuml_base_url": config.plantuml_base_url,
        "output_path": output_path,
        "max_retries": config.max_retries,
        "is_context": is_context,
        "is_container": is_container,
        "is_component": is_component,
        # —— Context fields (L1) ——
        "system_name": source_l1.system_name if source_l1 else "",
        "system_description": source_l1.system_description if source_l1 else "",
        "actors_json": _serialise_list(source_l1.actors) if source_l1 else "[]",
        "external_systems_json": (
            _serialise_list(source_l1.external_systems) if source_l1 else "[]"
        ),
        # —— Container fields (L2) ——
        "concern_id": source_l2.concern_id if source_l2 else "",
        "condition": source_l2.condition if source_l2 else "",
        "containers_json": (
            _serialise_list(source_l2.containers) if source_l2 else "[]"
        ),
        # —— Component fields (L3) ——
        "parent_container_id": source_l3.parent_container_id if source_l3 else "",
        "components_json": (
            _serialise_list(source_l3.components) if source_l3 else "[]"
        ),
        # —— Relationships (from the active source level) ——
        "relationships_json": _serialise_relationships(spec),
        # —— Error correction fields ——
        "retry_count": retry_count,
        "error_text": error_text,
        "current_puml_code": current_puml_code,
    }


def _serialise_list(items: list) -> str:
    dumped = [item.model_dump() for item in items]
    return json.dumps(dumped, indent=2, ensure_ascii=False)


def _serialise_relationships(spec: DiagramSpec) -> str:
    source = spec.source_l1 or spec.source_l2 or spec.source_l3
    if source is None:
        return "[]"
    return _serialise_list(source.relationships)
