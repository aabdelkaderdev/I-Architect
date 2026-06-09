"""Mustache template loading, caching, and rendering for prompt files.

Templates are stored as Markdown files with Mustache {{variable}} syntax under raa/prompts/.
Rendered at runtime via langchain_core.utils.mustache. The in-memory cache avoids repeated
disk I/O when the same template is rendered for every batch in a sequential run.

Partials are resolved from the same directory. A template referencing
{{> naming_convention}} loads prompts/naming_convention.md.
"""

from pathlib import Path

from langchain_core.utils.mustache import render

_PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
_cache: dict[str, str] = {}


def load_template(name: str) -> str:
    """Load a Mustache template file from raa/prompts/.

    Pre: `name` is a filename relative to the prompts directory (e.g. "asr_subgraph_system.md").
    Post: Returns the raw template string with partials resolved.
    Side effects: Caches loaded templates in memory to avoid repeated disk reads across batches.

    Partials are resolved from the same directory. A template referencing
    {{> naming_convention}} loads prompts/naming_convention.md.
    """
    if name in _cache:
        return _cache[name]

    path = _PROMPT_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Template not found: {path}")

    raw = path.read_text(encoding="utf-8")
    _cache[name] = raw
    return raw


def render_prompt(template_name: str, variables: dict) -> str:
    """Load and render a Mustache template with the given variables.

    Pre: `template_name` is a valid filename under raa/prompts/.
         `variables` contains all keys referenced by the template's Mustache tags.
    Post: Returns the rendered prompt string with all {{variables}} substituted.
    Side effects: Uses the template cache from load_template().

    Example:
        rendered = render_prompt("asr_subgraph_system.md", {
            "quality_weights": {"Security": 20, "Performance Efficiency": 40},
            "asrs": [{"id": "REQ-001", "text": "The system shall..."}],
        })
    """
    template_str = load_template(template_name)
    return render(template_str, variables)


def render_system_user(
    system_name: str,
    user_name: str,
    variables: dict,
) -> tuple[str, str]:
    """Load and render a system/user prompt pair.

    Pre: `system_name` and `user_name` are template filenames.
         `variables` is the shared variable dict rendered into both templates.
    Post: Returns (system_prompt, user_prompt) as a tuple.
    Side effects: Uses the template cache.

    Convenience wrapper — both templates typically share the same variable context
    (e.g., the batch's ASRs, registry snapshot, and QA weights).
    """
    return (
        render_prompt(system_name, variables),
        render_prompt(user_name, variables),
    )
