"""Prompt excerpt loader — tag-based retrieval of constraint snippets.

Section 7 and Section 21C of RAA_Plan.md.  Maps colon-delimited tags to
excerpt ``.txt`` files under ``raa/prompts/excerpts/`` and defines the
per-node tag registry that enforces retrieval isolation.
"""

from __future__ import annotations

import functools
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_PROMPTS_DIR = _PROJECT_ROOT / "raa" / "prompts"
_EXCERPTS_DIR = _PROMPTS_DIR / "excerpts"

# ---------------------------------------------------------------------------
# Node → tag registry  (RAA_Plan.md §21C)
# ---------------------------------------------------------------------------
NODE_TAG_REGISTRY: dict[str, tuple[str, ...]] = {
    "entity_extraction": ("c4:levels", "c4:notation"),
    "relationship_extraction": ("c4:notation", "c4:technology"),
    "pattern_selection": ("c4:levels",),
    "saam_tradeoff": ("saam:steps", "saam:scenarios"),
    "final_merge": ("c4:levels", "c4:notation", "c4:technology"),
}

# ---------------------------------------------------------------------------
# Tag ↔ filename translation
# ---------------------------------------------------------------------------
def tag_to_filename(tag: str) -> str:
    """Map ``c4:levels`` → ``c4_levels.txt``."""
    return tag.replace(":", "_") + ".txt"


def excerpt_path(tag: str, excerpts_dir: Path | None = None) -> Path:
    """Resolve *tag* to an absolute path under the excerpts directory.

    When *excerpts_dir* is ``None`` the default ``raa/prompts/excerpts/`` is
    used.  Tests inject a temporary directory via this parameter.
    """
    base = excerpts_dir if excerpts_dir is not None else _EXCERPTS_DIR
    return base / tag_to_filename(tag)


# ---------------------------------------------------------------------------
# Single-tag loading  (US1)
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=16)
def _load_excerpt_cached(path_str: str) -> str:
    """Read and strip an excerpt file.  Cached by absolute-path string."""
    p = Path(path_str)
    if not p.exists():
        raise FileNotFoundError(f"Excerpt file not found: {p}")
    return p.read_text(encoding="utf-8").strip()


def load_excerpt(tag: str, excerpts_dir: Path | None = None) -> str:
    """Return the stripped text content of the excerpt file for *tag*.

    Raises ``FileNotFoundError`` when the translated file path does not exist.
    When *excerpts_dir* is supplied (test injection) the ``lru_cache`` is
    bypassed so test-created files are always read fresh.
    """
    path = excerpt_path(tag, excerpts_dir=excerpts_dir)
    if excerpts_dir is not None:
        if not path.exists():
            raise FileNotFoundError(f"Excerpt file not found: {path}")
        return path.read_text(encoding="utf-8").strip()
    return _load_excerpt_cached(str(path))


# ---------------------------------------------------------------------------
# Node-scoped retrieval  (US2)
# ---------------------------------------------------------------------------
def get_node_tags(node_name: str) -> tuple[str, ...]:
    """Return the immutable tag tuple for *node_name*.

    Raises ``KeyError`` when *node_name* is not in ``NODE_TAG_REGISTRY``.
    """
    if node_name not in NODE_TAG_REGISTRY:
        raise KeyError(
            f"Unknown node: {node_name!r}. "
            f"Known: {list(NODE_TAG_REGISTRY)}"
        )
    return NODE_TAG_REGISTRY[node_name]


def get_node_constraints(
    node_name: str, excerpts_dir: Path | None = None
) -> dict[str, str]:
    """Return ``{tag: content, …}`` for every tag assigned to *node_name*."""
    tags = get_node_tags(node_name)
    return {tag: load_excerpt(tag, excerpts_dir=excerpts_dir) for tag in tags}


def format_constraints_block(constraints: dict[str, str]) -> str:
    """Format a constraint dict into a prompt-injection text block."""
    if not constraints:
        return ""
    parts = ["--- CONSTRAINTS ---"]
    for tag, content in constraints.items():
        parts.append(f"[{tag}]")
        parts.append(content)
    parts.append("--- END CONSTRAINTS ---")
    return "\n".join(parts)
