"""Validation tests for RAA Prompt Resource Bundle.

Verifies source register structure, C4/SAAM constraint completeness,
retrieval tag mapping, and excerpt word-count limits per RAA_Plan.md Section 2.
"""
from __future__ import annotations

import re
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent.parent / "raa" / "prompts"
EXCERPTS_DIR = PROMPTS_DIR / "excerpts"

EXPECTED_SOURCES = [
    "C4 Model — Diagrams",
    "C4 Model — Notation",
    "SAAM — SEI Technical Report",
]

EXPECTED_TAGS = {
    "c4:levels": "c4_levels.txt",
    "c4:notation": "c4_notation.txt",
    "c4:technology": "c4_technology.txt",
    "saam:steps": "saam_steps.txt",
    "saam:scenarios": "saam_scenarios.txt",
}

C4_REQUIRED_TERMS = [
    "Context",
    "Container",
    "Component",
    "label",
    "description",
    "relationship",
    "technology",
]

SAAM_REQUIRED_TERMS = [
    "partition",
    "map",
    "scenario",
    "evaluate",
    "quality",
]


def _read_file(filename: str, subdir: str = "") -> str:
    """Read a prompt resource file, stripping whitespace."""
    if subdir:
        return (PROMPTS_DIR / subdir / filename).read_text(encoding="utf-8").strip()
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8").strip()


def _word_count(text: str) -> int:
    """Count space-delimited words in text."""
    return len(text.split())


# ---------------------------------------------------------------------------
# T004: Source Register Row Validation
# ---------------------------------------------------------------------------

def test_source_register_exists():
    """source_register.md must exist and be non-empty."""
    content = _read_file("source_register.md")
    assert content, "source_register.md is empty"
    assert len(content) > 50, "source_register.md appears to be a placeholder only"


def test_source_register_has_required_sources():
    """All three authoritative sources from Section 2A must be present."""
    content = _read_file("source_register.md")
    for source in EXPECTED_SOURCES:
        assert source in content, (
            f"Missing source '{source}' in source_register.md"
        )


def test_source_register_has_required_columns():
    """Table must have Source, URL, Retrieval Date, and Governs columns."""
    content = _read_file("source_register.md")
    assert "Source" in content, "Missing 'Source' column in source_register.md"
    assert "URL" in content, "Missing 'URL' column in source_register.md"
    assert "Retrieval" in content, "Missing 'Retrieval Date' column in source_register.md"
    assert "Governs" in content, "Missing 'Governs' column in source_register.md"


# ---------------------------------------------------------------------------
# T005: C4 Constraint Assertions
# ---------------------------------------------------------------------------

def test_c4_constraints_exists():
    """c4_constraints.md must exist and be non-empty."""
    content = _read_file("c4_constraints.md")
    assert content, "c4_constraints.md is empty"
    assert len(content) > 100, "c4_constraints.md appears to be a placeholder only"


def test_c4_constraints_has_levels():
    """Must define Context, Container, and Component levels."""
    content = _read_file("c4_constraints.md")
    for level in ("Context", "Container", "Component"):
        assert level in content, (
            f"Missing C4 level '{level}' in c4_constraints.md"
        )


def test_c4_constraints_has_element_rules():
    """Must require type label, short description, and relationships."""
    content = _read_file("c4_constraints.md")
    for term in C4_REQUIRED_TERMS:
        assert term.lower() in content.lower(), (
            f"Missing required C4 term '{term}' in c4_constraints.md"
        )


def test_c4_constraints_has_technology_rule():
    """Must specify technology stack when determinable from requirements."""
    content = _read_file("c4_constraints.md")
    assert "technology" in content.lower(), (
        "Missing technology annotation rule in c4_constraints.md"
    )


# ---------------------------------------------------------------------------
# T006: SAAM Constraint Assertions
# ---------------------------------------------------------------------------

def test_saam_constraints_exists():
    """saam_constraints.md must exist and be non-empty."""
    content = _read_file("saam_constraints.md")
    assert content, "saam_constraints.md is empty"
    assert len(content) > 100, "saam_constraints.md appears to be a placeholder only"


def test_saam_constraints_has_five_steps():
    """Must define the 5-step SAAM process in order."""
    content = _read_file("saam_constraints.md")
    for term in SAAM_REQUIRED_TERMS:
        assert term.lower() in content.lower(), (
            f"Missing required SAAM term '{term}' in saam_constraints.md"
        )


def test_saam_constraints_has_ordered_list():
    """Must present the SAAM steps as an ordered sequence."""
    content = _read_file("saam_constraints.md")
    # Check for ordered list markers (1. 2. 3. 4. 5.)
    ordered_markers = sum(
        1 for i in range(1, 6) if f"{i}." in content or f" {i} " in content
    )
    assert ordered_markers >= 3, (
        f"Expected at least 3 ordered markers (1. 2. 3. 4. 5.) in saam_constraints.md, found {ordered_markers}"
    )


# ---------------------------------------------------------------------------
# T007: Retrieval Tag Mapping Assertions
# ---------------------------------------------------------------------------

def test_source_register_has_tag_mapping():
    """source_register.md must document the tag-to-file retrieval mapping."""
    content = _read_file("source_register.md")
    for tag, filename in EXPECTED_TAGS.items():
        assert tag in content, (
            f"Missing retrieval tag '{tag}' in source_register.md"
        )
        # At least the filename stem should appear near the tag
        fn_stem = filename.replace(".txt", "")
        assert fn_stem in content, (
            f"Missing file reference '{filename}' for tag '{tag}' in source_register.md"
        )


def test_excerpt_files_exist():
    """All five excerpt .txt files must exist."""
    for filename in EXPECTED_TAGS.values():
        path = EXCERPTS_DIR / filename
        assert path.is_file(), f"Missing excerpt file: raa/prompts/excerpts/{filename}"


# ---------------------------------------------------------------------------
# T008: Excerpt Word-Count Validation
# ---------------------------------------------------------------------------

def test_excerpts_under_word_limit():
    """Every excerpt .txt file must contain 25 words or fewer (Section 2C)."""
    for filename in EXPECTED_TAGS.values():
        path = EXCERPTS_DIR / filename
        assert path.is_file(), f"Missing excerpt file: {filename}"
        text = path.read_text(encoding="utf-8").strip()
        count = _word_count(text)
        assert count <= 25, (
            f"Excerpt '{filename}' has {count} words (limit: 25)"
        )


def test_excerpts_non_empty():
    """Every excerpt .txt file must contain actual content, not just placeholder."""
    for filename in EXPECTED_TAGS.values():
        path = EXCERPTS_DIR / filename
        text = path.read_text(encoding="utf-8").strip()
        assert len(text) > 10, (
            f"Excerpt '{filename}' appears to be a placeholder only"
        )
