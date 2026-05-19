"""Unit tests for raa/utils/prompt_loader.py — tag-based excerpt retrieval."""

import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_EXCERPT_CONTENTS = {
    "c4:levels": "C4 levels: Context (system+actors), Container (deployable units).",
    "c4:notation": "Every element needs a type label and a short description.",
    "c4:technology": "Containers and components must specify technology stack.",
    "saam:steps": "Apply SAAM in order: partition, map, choose, scenarios, evaluate.",
    "saam:scenarios": "Define evaluation scenarios per quality attribute.",
}


def _make_excerpt_dir(parent: Path) -> Path:
    """Create a temporary excerpts/ dir with .txt files for every supported tag.

    Files are created with trailing whitespace to verify stripping behaviour.
    """
    d = parent / "excerpts"
    d.mkdir()
    for tag, content in _EXCERPT_CONTENTS.items():
        fname = tag.replace(":", "_") + ".txt"
        # Add leading/trailing whitespace for strip verification
        (d / fname).write_text(f"  {content}  \n\n", encoding="utf-8")
    return d


def _run_tests():
    import inspect

    tests = sorted(
        (name, obj)
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if name.startswith("test_") and callable(obj)
    )
    passed = 0
    failed = 0
    for name, func in tests:
        try:
            func()
            print(f"  PASS {name}")
            passed += 1
        except Exception as e:
            import traceback
            print(f"  FAIL {name} — {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    return failed == 0


# ---------------------------------------------------------------------------
# Phase 3 — US1: Single-tag excerpt loading  (T009–T015)
# ---------------------------------------------------------------------------
def test_c4_levels_tag_maps_to_file():
    """T009: c4:levels maps to c4_levels.txt."""
    from raa.utils.prompt_loader import load_excerpt, tag_to_filename

    assert tag_to_filename("c4:levels") == "c4_levels.txt"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        text = load_excerpt("c4:levels", excerpts_dir=excerpts_dir)
        assert "C4 levels" in text
        assert not text.startswith(" "), f"leading whitespace not stripped: {text!r}"
        assert not text.endswith(" "), f"trailing whitespace not stripped: {text!r}"


def test_c4_notation_tag_maps_to_file():
    """T010: c4:notation maps to c4_notation.txt."""
    from raa.utils.prompt_loader import load_excerpt, tag_to_filename

    assert tag_to_filename("c4:notation") == "c4_notation.txt"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        text = load_excerpt("c4:notation", excerpts_dir=excerpts_dir)
        assert "type label" in text


def test_c4_technology_tag_maps_to_file():
    """T011: c4:technology maps to c4_technology.txt."""
    from raa.utils.prompt_loader import load_excerpt, tag_to_filename

    assert tag_to_filename("c4:technology") == "c4_technology.txt"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        text = load_excerpt("c4:technology", excerpts_dir=excerpts_dir)
        assert "technology stack" in text


def test_saam_steps_tag_maps_to_file():
    """T012: saam:steps maps to saam_steps.txt."""
    from raa.utils.prompt_loader import load_excerpt, tag_to_filename

    assert tag_to_filename("saam:steps") == "saam_steps.txt"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        text = load_excerpt("saam:steps", excerpts_dir=excerpts_dir)
        assert "SAAM" in text


def test_saam_scenarios_tag_maps_to_file():
    """T013: saam:scenarios maps to saam_scenarios.txt."""
    from raa.utils.prompt_loader import load_excerpt, tag_to_filename

    assert tag_to_filename("saam:scenarios") == "saam_scenarios.txt"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        text = load_excerpt("saam:scenarios", excerpts_dir=excerpts_dir)
        assert "evaluation scenarios" in text


def test_load_excerpt_strips_whitespace():
    """T014: load_excerpt strips leading and trailing whitespace."""
    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        from raa.utils.prompt_loader import load_excerpt

        for tag in _EXCERPT_CONTENTS:
            text = load_excerpt(tag, excerpts_dir=excerpts_dir)
            assert not text.startswith(" "), f"{tag}: leading whitespace not stripped"
            assert not text.endswith("\n"), f"{tag}: trailing newline not stripped"
            assert not text.endswith(" "), f"{tag}: trailing whitespace not stripped"
            assert len(text) > 0, f"{tag}: empty after strip"


def test_load_excerpt_raises_file_not_found():
    """T015: load_excerpt raises FileNotFoundError for missing file."""
    from raa.utils.prompt_loader import load_excerpt

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = Path(tmp) / "excerpts"
        excerpts_dir.mkdir()
        # dir exists but no files — any tag lookup should fail

        try:
            load_excerpt("c4:levels", excerpts_dir=excerpts_dir)
            raise AssertionError("Expected FileNotFoundError")
        except FileNotFoundError:
            pass  # expected


# ---------------------------------------------------------------------------
# Phase 4 — US2: Node-scoped constraint retrieval  (T022–T028)
# ---------------------------------------------------------------------------
def test_entity_extraction_tags():
    """T022: entity_extraction retrieves only c4:levels and c4:notation."""
    from raa.utils.prompt_loader import get_node_tags, get_node_constraints

    tags = get_node_tags("entity_extraction")
    assert tags == ("c4:levels", "c4:notation"), f"got {tags}"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        constraints = get_node_constraints("entity_extraction", excerpts_dir=excerpts_dir)
        assert set(constraints.keys()) == {"c4:levels", "c4:notation"}


def test_relationship_extraction_tags():
    """T023: relationship_extraction retrieves only c4:notation and c4:technology."""
    from raa.utils.prompt_loader import get_node_tags, get_node_constraints

    tags = get_node_tags("relationship_extraction")
    assert tags == ("c4:notation", "c4:technology"), f"got {tags}"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        constraints = get_node_constraints("relationship_extraction", excerpts_dir=excerpts_dir)
        assert set(constraints.keys()) == {"c4:notation", "c4:technology"}


def test_pattern_selection_tags():
    """T024: pattern_selection retrieves only c4:levels."""
    from raa.utils.prompt_loader import get_node_tags, get_node_constraints

    tags = get_node_tags("pattern_selection")
    assert tags == ("c4:levels",), f"got {tags}"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        constraints = get_node_constraints("pattern_selection", excerpts_dir=excerpts_dir)
        assert set(constraints.keys()) == {"c4:levels"}


def test_saam_tradeoff_tags():
    """T025: saam_tradeoff retrieves only saam:steps and saam:scenarios."""
    from raa.utils.prompt_loader import get_node_tags, get_node_constraints

    tags = get_node_tags("saam_tradeoff")
    assert tags == ("saam:steps", "saam:scenarios"), f"got {tags}"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        constraints = get_node_constraints("saam_tradeoff", excerpts_dir=excerpts_dir)
        assert set(constraints.keys()) == {"saam:steps", "saam:scenarios"}


def test_final_merge_tags():
    """T026: final_merge retrieves only c4:levels, c4:notation, and c4:technology."""
    from raa.utils.prompt_loader import get_node_tags, get_node_constraints

    tags = get_node_tags("final_merge")
    assert tags == ("c4:levels", "c4:notation", "c4:technology"), f"got {tags}"

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        constraints = get_node_constraints("final_merge", excerpts_dir=excerpts_dir)
        assert set(constraints.keys()) == {"c4:levels", "c4:notation", "c4:technology"}


def test_unknown_node_raises_key_error():
    """T027: Unknown node name raises KeyError."""
    from raa.utils.prompt_loader import get_node_tags, get_node_constraints

    try:
        get_node_tags("nonexistent_node")
        raise AssertionError("Expected KeyError")
    except KeyError as e:
        assert "nonexistent_node" in str(e)

    with tempfile.TemporaryDirectory() as tmp:
        excerpts_dir = _make_excerpt_dir(Path(tmp))
        try:
            get_node_constraints("unknown_xyz", excerpts_dir=excerpts_dir)
            raise AssertionError("Expected KeyError")
        except KeyError:
            pass


def test_format_constraints_block():
    """T028: format_constraints_block includes tag labels and only provided excerpts."""
    from raa.utils.prompt_loader import format_constraints_block

    constraints = {
        "c4:levels": "C4 levels content.",
        "c4:notation": "C4 notation content.",
    }
    block = format_constraints_block(constraints)

    assert "[c4:levels]" in block
    assert "[c4:notation]" in block
    assert "C4 levels content." in block
    assert "C4 notation content." in block
    assert "--- CONSTRAINTS ---" in block
    assert "--- END CONSTRAINTS ---" in block

    # Verify no unexpected tags leak in
    assert "[c4:technology]" not in block
    assert "[saam:steps]" not in block

    # Empty constraints
    assert format_constraints_block({}) == ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ok = _run_tests()
    sys.exit(0 if ok else 1)
