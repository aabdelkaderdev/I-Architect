"""Validation tests for RAA Skill Resource Bundle references.

Verifies all 8 reference files under Skills/RAA/references/ exist, are non-empty,
follow the correct section template, and contain required hard rules per RAA_Plan.md Section 14.
"""
from __future__ import annotations

import re
from pathlib import Path

REFS_DIR = Path(__file__).parent.parent.parent / "Skills" / "RAA" / "references"

ALL_REFERENCE_FILES = [
    "C4.md",
    "Quality_Attributes.md",
    "Entity_Extraction.md",
    "Relationship_Extraction.md",
    "Pattern_Selection.md",
    "Technology_Inference.md",
    "C4_Level_Mapping.md",
    "SAAM.md",
]

SKILL_FILES_WITH_SEVEN_SECTIONS = [
    "Entity_Extraction.md",
    "Relationship_Extraction.md",
    "Pattern_Selection.md",
    "Technology_Inference.md",
    "C4_Level_Mapping.md",
    "SAAM.md",
]

AUTHORITATIVE_FILES = [
    "C4.md",
    "Quality_Attributes.md",
]

SEVEN_SECTION_HEADERS = [
    (r"## 1\.\s+Purpose", "1. Purpose"),
    (r"## 2\.\s+Input", "2. Input"),
    (r"## 3\.\s+Normative\s+rules", "3. Normative rules"),
    (r"## 4\.\s+Decision\s+guidelines", "4. Decision guidelines"),
    (r"## 5\.\s+Output\s+schema", "5. Output schema"),
    (r"## 6\.\s+Error\s+cases", "6. Error cases"),
    (r"## 7\.\s+Examples", "7. Examples"),
]

# T011: SAAM content that must be preserved
SAAM_REQUIRED_TERMS = [
    "5-step",
    "scenario classification",
    "scoring",
    "merge algorithm",
    "tie-breaking",
    "hotspot",
    "error case",
]


def _read_ref(filename: str) -> str:
    path = REFS_DIR / filename
    return path.read_text(encoding="utf-8").strip()


# ---------------------------------------------------------------------------
# T004–T005: Existence and non-empty content
# ---------------------------------------------------------------------------

def test_all_reference_files_exist():
    """All 8 reference files must exist (Section 14)."""
    for filename in ALL_REFERENCE_FILES:
        path = REFS_DIR / filename
        assert path.is_file(), f"Missing reference: Skills/RAA/references/{filename}"


def test_all_reference_files_non_empty():
    """All 8 reference files must be non-trivial (not just placeholder)."""
    for filename in ALL_REFERENCE_FILES:
        content = _read_ref(filename)
        assert len(content) > 200, (
            f"Skills/RAA/references/{filename} is placeholder only "
            f"(length={len(content)} bytes)"
        )


# ---------------------------------------------------------------------------
# T006: Seven-section header validation for skill reference files
# ---------------------------------------------------------------------------

def test_skill_files_have_seven_section_headers():
    """All 6 skill/SAAM reference files must have all 7 section headers."""
    for filename in SKILL_FILES_WITH_SEVEN_SECTIONS:
        content = _read_ref(filename)
        for pattern, label in SEVEN_SECTION_HEADERS:
            assert re.search(pattern, content, re.MULTILINE | re.IGNORECASE), (
                f"Missing section '{label}' in Skills/RAA/references/{filename}"
            )


def test_skill_files_headers_in_order():
    """The 7 section headers must appear in numbered order."""
    for filename in SKILL_FILES_WITH_SEVEN_SECTIONS:
        content = _read_ref(filename)
        last_pos = -1
        for pattern, label in SEVEN_SECTION_HEADERS:
            match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
            if match:
                assert match.start() > last_pos, (
                    f"Section '{label}' out of order in Skills/RAA/references/{filename}"
                )
                last_pos = match.start()


# ---------------------------------------------------------------------------
# T007: Authoritative references omit Input/Output sections
# ---------------------------------------------------------------------------

def test_authoritative_files_omit_input_output_sections():
    """C4.md and Quality_Attributes.md must NOT have Input/Output sections."""
    for filename in AUTHORITATIVE_FILES:
        content = _read_ref(filename)
        assert not re.search(
            r"## 2\.\s+Input", content, re.MULTILINE | re.IGNORECASE
        ), (
            f"Authoritative reference {filename} must not have 'Input' section"
        )
        assert not re.search(
            r"## 5\.\s+Output\s+schema", content, re.MULTILINE | re.IGNORECASE
        ), (
            f"Authoritative reference {filename} must not have 'Output schema' section"
        )


def test_authoritative_files_define_core_domain_content():
    """Authoritative references must define core domain content."""
    c4 = _read_ref("C4.md")
    assert "Context" in c4, "C4.md missing Context level definition"
    assert "Container" in c4, "C4.md missing Container level definition"
    assert "Component" in c4, "C4.md missing Component level definition"

    qa = _read_ref("Quality_Attributes.md")
    for attr in ["Performance", "Security", "Compatibility", "Usability"]:
        assert attr in qa, f"Quality_Attributes.md missing '{attr}'"


# ---------------------------------------------------------------------------
# T008: Entity_Extraction.md orphan-prevention hard rules
# ---------------------------------------------------------------------------

def test_entity_extraction_has_orphan_prevention():
    """Entity_Extraction.md must contain the orphan-prevention hard rule."""
    content = _read_ref("Entity_Extraction.md")
    assert (
        "component" in content.lower()
        and "container" in content.lower()
        and "system" in content.lower()
    ), "Entity_Extraction.md missing entity-level references"
    # Must assert no component without container, no container without system
    has_parent_rule = (
        ("without" in content.lower() or "must not" in content.lower())
        and "container" in content.lower()
        and "system" in content.lower()
    )
    assert has_parent_rule, (
        "Entity_Extraction.md missing orphan-prevention hard rule: "
        "no component without container, no container without system"
    )


# ---------------------------------------------------------------------------
# T009: Relationship_Extraction.md diagram_scope hard rule
# ---------------------------------------------------------------------------

def test_relationship_extraction_has_diagram_scope():
    """Relationship_Extraction.md must enforce explicit diagram_scope."""
    content = _read_ref("Relationship_Extraction.md")
    assert "diagram_scope" in content, (
        "Relationship_Extraction.md missing explicit diagram_scope rule"
    )
    for scope in ("context", "container", "component"):
        assert scope in content.lower(), (
            f"Relationship_Extraction.md missing diagram_scope value '{scope}'"
        )


# ---------------------------------------------------------------------------
# T010: C4_Level_Mapping.md parent-assignment and scope rules
# ---------------------------------------------------------------------------

def test_c4_level_mapping_has_parent_assignment():
    """C4_Level_Mapping.md must cover parent_system_id and parent_container_id."""
    content = _read_ref("C4_Level_Mapping.md")
    assert "parent_system_id" in content, (
        "C4_Level_Mapping.md missing parent_system_id rules"
    )
    assert "parent_container_id" in content, (
        "C4_Level_Mapping.md missing parent_container_id rules"
    )


def test_c4_level_mapping_has_scope_rules():
    """C4_Level_Mapping.md must cover diagram_scope assignment."""
    content = _read_ref("C4_Level_Mapping.md")
    assert "diagram_scope" in content, (
        "C4_Level_Mapping.md missing diagram_scope rules"
    )
    assert "endpoint" in content.lower(), (
        "C4_Level_Mapping.md missing endpoint-type scope mapping"
    )


# ---------------------------------------------------------------------------
# T011: SAAM.md preservation assertions
# ---------------------------------------------------------------------------

def test_saam_preserves_core_content():
    """SAAM.md must preserve 5-step process, scoring, merge, tie-break, hotspots, errors."""
    content = _read_ref("SAAM.md")
    for term in SAAM_REQUIRED_TERMS:
        assert term.lower() in content.lower(), (
            f"SAAM.md missing required section '{term}'"
        )


def test_saam_preserves_merge_algorithm():
    """SAAM.md must preserve the deterministic merge algorithm steps."""
    content = _read_ref("SAAM.md")
    # Entity dedup, relationship dedup, coverage union, residual scan
    merge_terms = ["entity dedup", "relationship dedup", "coverage union"]
    for term in merge_terms:
        assert term.lower() in content.lower().replace("deduplication", "dedup"), (
            f"SAAM.md missing merge algorithm step '{term}'"
        )


def test_saam_preserves_tie_breaking():
    """SAAM.md must preserve tie-breaking resolution rules."""
    content = _read_ref("SAAM.md")
    assert "tie" in content.lower(), "SAAM.md missing tie-breaking"
    assert "fragment_score" in content or "fragment score" in content.lower() or "score" in content.lower(), (
        "SAAM.md missing scoring references"
    )
