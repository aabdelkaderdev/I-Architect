"""
Quality-architecture pattern matrix loader.

The matrix is a nested dict mapping architecture patterns (rows) to
quality attributes (columns) with integer scores. This row-oriented
shape is required by the ILP / Greedy optimizers in Phase 2.

Row-oriented (target format):
    {"Caching": {"Performance": 3, "Reliability": 1}, ...}

If the JSON file is quality-oriented (qualities as top-level keys),
the loader auto-transposes it to row-oriented before returning.
"""
from __future__ import annotations

import json
from pathlib import Path


def load_matrix_from_json(path: str | Path) -> dict[str, dict[str, int]]:
    """Load the quality-architecture matrix from a JSON file.

    Auto-detects orientation and returns row-oriented shape.
    """
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    if not raw:
        return {}

    return _ensure_row_oriented(raw)


def _is_row_oriented(matrix: dict) -> bool:
    """Heuristic: row-oriented matrices have architecture patterns as keys
    whose inner dict values are quality-attribute scores."""
    first_inner = next(iter(matrix.values()))
    if not isinstance(first_inner, dict):
        return False

    # For row-oriented: inner keys are quality attributes (e.g. "Performance", "Reliability").
    # For quality-oriented: inner keys are patterns (e.g. "Caching", "Load Balancing").
    # We use a heuristic: check if the inner keys match known quality attribute names.
    known_qualities = {
        "performance efficiency", "compatibility", "usability", "reliability",
        "security", "maintainability", "portability", "cost efficiency",
        "performance", "scalability", "availability", "modifiability",
        "testability", "interoperability", "reusability", "efficiency",
        "functionality", "flexibility", "safety",
    }

    inner_keys_lower = {str(k).strip().lower() for k in first_inner}
    quality_match_count = len(inner_keys_lower & known_qualities)

    # Also check outer keys for quality-like names
    outer_keys_lower = {str(k).strip().lower() for k in matrix}
    outer_quality_count = len(outer_keys_lower & known_qualities)

    # If outer keys look like qualities (more quality matches), it's quality-oriented
    # If inner keys look like qualities, it's row-oriented
    return quality_match_count >= outer_quality_count


def _ensure_row_oriented(matrix: dict) -> dict[str, dict[str, int]]:
    """Transpose quality-oriented matrix to row-oriented if needed."""
    if _is_row_oriented(matrix):
        return matrix

    # Transpose: quality-keyed → pattern-keyed
    result: dict[str, dict[str, int]] = {}
    for quality, patterns in matrix.items():
        if not isinstance(patterns, dict):
            continue
        for pattern, score in patterns.items():
            if pattern not in result:
                result[pattern] = {}
            result[pattern][quality] = score

    return result
