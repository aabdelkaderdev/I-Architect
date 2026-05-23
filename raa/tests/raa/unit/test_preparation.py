"""
Unit tests for the Phase 1 normalization node (FR-1).

Tests cover:
- Integer ID → "R{id}" string conversion for ASRs
- Non-ASR description resolution from parent requirements dict
- Non-ASR default field population (is_asr, quality_attributes, condition_text)
- Empty input handling
"""
import pytest
from langchain_core.runnables import RunnableConfig

from raa.nodes.preparation import normalize_requirements
from raa.state.schemas import RAAState


def _make_config() -> RunnableConfig:
    """Minimal config for tests — no LLM needed for normalization."""
    return {"configurable": {"thread_id": "test-thread-1"}}


def _make_state(
    requirements: dict | None = None,
    asrs: list[dict] | None = None,
    non_asr: list[str] | None = None,
) -> RAAState:
    """Build a minimal RAAState for normalization tests."""
    return {
        "requirements": requirements or {},
        "asrs": asrs or [],
        "non_asr": non_asr or [],
        "condition_groups": [],
        "quality_weights": {},
        "review_mode": "autonomous",
        # Output / internal channels (unused by normalize but required by TypedDict)
        "normalized_asrs": [],
        "normalized_non_asr": [],
        "embeddings_ready": False,
        "batch_outputs": [],
        "batch_cursor": 0,
        "open_questions": [],
        "incoherent_batches": [],
    }


# ── ID conversion tests (AC: transform integer IDs to string IDs) ──────────


def test_asr_integer_id_converts_to_r_prefix():
    """ARLO-internal int ID 5 → RAA string ID 'R5'."""
    state = _make_state(
        requirements={"5": "The system shall authenticate users via OAuth2."},
        asrs=[{
            "id": 5,
            "quality_attributes": ["security"],
            "condition_text": "under any circumstances",
        }],
    )
    result = normalize_requirements(state, _make_config())

    assert len(result["normalized_asrs"]) == 1
    assert result["normalized_asrs"][0]["id"] == "R5"


def test_asr_id_already_string_still_gets_r_prefix():
    """String IDs without R prefix get normalized."""
    state = _make_state(
        requirements={"7": "Log all access events."},
        asrs=[{
            "id": "7",
            "quality_attributes": ["reliability"],
        }],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["id"] == "R7"


def test_multiple_asrs_all_normalized():
    """Every ASR in the list gets its ID normalized."""
    state = _make_state(
        requirements={
            "1": "Req one",
            "2": "Req two",
            "3": "Req three",
        },
        asrs=[
            {"id": 1, "quality_attributes": ["security"]},
            {"id": 2, "quality_attributes": ["reliability"]},
            {"id": 3, "quality_attributes": ["usability"]},
        ],
    )
    result = normalize_requirements(state, _make_config())
    ids = [r["id"] for r in result["normalized_asrs"]]
    assert ids == ["R1", "R2", "R3"]


# ── ASR description resolution ────────────────────────────────────────────


def test_requirements_dict_wins_over_arlo_description():
    """Requirements dict is authoritative; ARLO description is fallback only."""
    state = _make_state(
        requirements={"5": "Authoritative from requirements."},
        asrs=[{
            "id": 5,
            "description": "ARLO-provided — should not be used.",
        }],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "Authoritative from requirements."


def test_asr_falls_back_to_requirements_dict():
    """ASR dict has no description → resolve from parent requirements dict."""
    state = _make_state(
        requirements={"5": "The system shall encrypt data at rest."},
        asrs=[{"id": 5}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "The system shall encrypt data at rest."


def test_asr_no_description_anywhere_gets_empty_string():
    """Neither ASR dict nor requirements have description → empty string."""
    state = _make_state(
        requirements={},
        asrs=[{"id": 99}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == ""


# ── ASR field preservation ─────────────────────────────────────────────────


def test_asr_preserves_quality_attributes():
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1, "quality_attributes": ["security", "reliability"]}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["quality_attributes"] == ["security", "reliability"]


def test_asr_defaults_quality_attributes_to_empty_list():
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["quality_attributes"] == []


def test_asr_preserves_condition_text():
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1, "condition_text": "when user count > 1000"}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["condition_text"] == "when user count > 1000"


def test_asr_condition_text_defaults_to_none():
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["condition_text"] is None


def test_asr_is_asr_flag_is_true():
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["is_asr"] is True


# ── Non-ASR normalization ──────────────────────────────────────────────────


def test_non_asr_id_normalized_with_r_prefix():
    state = _make_state(
        requirements={"N1": "Performance monitoring requirement."},
        non_asr=["N1"],
    )
    result = normalize_requirements(state, _make_config())
    assert len(result["normalized_non_asr"]) == 1
    assert result["normalized_non_asr"][0]["id"] == "RN1"


def test_non_asr_resolves_description_from_requirements():
    state = _make_state(
        requirements={"N1": "The system shall log all errors."},
        non_asr=["N1"],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_non_asr"][0]["description"] == "The system shall log all errors."


def test_non_asr_missing_description_gets_empty_string():
    state = _make_state(
        requirements={},
        non_asr=["N99"],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_non_asr"][0]["description"] == ""


def test_non_asr_default_fields_are_set():
    """Non-ASR records must have is_asr=False, empty QAs, null condition_text."""
    state = _make_state(
        requirements={"N1": "Some requirement."},
        non_asr=["N1"],
    )
    result = normalize_requirements(state, _make_config())
    rec = result["normalized_non_asr"][0]
    assert rec["is_asr"] is False
    assert rec["quality_attributes"] == []
    assert rec["condition_text"] is None


def test_non_asr_already_r_prefixed_not_double_prefixed():
    """ID already in 'R5' format stays as-is."""
    state = _make_state(
        requirements={"R5": "Already prefixed."},
        non_asr=["R5"],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_non_asr"][0]["id"] == "R5"


def test_multiple_non_asrs_all_normalized():
    state = _make_state(
        requirements={"N1": "First", "N2": "Second", "N3": "Third"},
        non_asr=["N1", "N2", "N3"],
    )
    result = normalize_requirements(state, _make_config())
    ids = [r["id"] for r in result["normalized_non_asr"]]
    assert ids == ["RN1", "RN2", "RN3"]


# ── Empty input handling ───────────────────────────────────────────────────


def test_empty_asrs_and_non_asrs():
    """Empty input lists produce empty output lists, no crash."""
    state = _make_state(requirements={}, asrs=[], non_asr=[])
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"] == []
    assert result["normalized_non_asr"] == []


def test_embeddings_ready_is_false_after_normalization():
    """Normalization node sets embeddings_ready = False to gate downstream."""
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["embeddings_ready"] is False


# ── Review fix: Description lookup tries multiple ID forms ────────────────


def test_asr_description_lookup_tries_normalized_key_form():
    """When requirements dict has 'R5' and asr_id is 5, find it."""
    state = _make_state(
        requirements={"R5": "Found via normalized key."},
        asrs=[{"id": 5}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "Found via normalized key."


def test_non_asr_description_lookup_tries_both_raw_and_normalized_keys():
    """Non-ASR lookup tries raw 'N1' then normalized 'RN1'."""
    state = _make_state(
        requirements={"RN1": "Found via RN1 key."},
        non_asr=["N1"],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_non_asr"][0]["description"] == "Found via RN1 key."


def test_asr_description_falls_back_to_arlo_provided_last():
    """Requirements dict wins over ARLO-provided description."""
    state = _make_state(
        requirements={"5": "Authoritative from requirements."},
        asrs=[{
            "id": 5,
            "description": "ARLO-provided — fallback only.",
        }],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "Authoritative from requirements."


def test_asr_arlo_description_used_when_requirements_empty():
    """ARLO-provided description used as last resort."""
    state = _make_state(
        requirements={},
        asrs=[{
            "id": 5,
            "description": "ARLO fallback description.",
        }],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "ARLO fallback description."


# ── Review fix: QA attributes coercion ───────────────────────────────────


def test_quality_attributes_coerces_non_list_to_empty():
    """Non-list QA values from ARLO are coerced to empty list."""
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1, "quality_attributes": "security"}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["quality_attributes"] == []


def test_quality_attributes_filters_non_string_entries():
    """QA list entries that aren't strings are dropped."""
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1, "quality_attributes": ["security", 123, None, "reliability"]}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["quality_attributes"] == ["security", "reliability"]


def test_quality_attributes_none_becomes_empty_list():
    """Explicit None QA value becomes empty list."""
    state = _make_state(
        requirements={"1": "R1"},
        asrs=[{"id": 1, "quality_attributes": None}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["quality_attributes"] == []


# ── Review fix: ID normalization robustness ─────────────────────────────


def test_id_with_whitespace_is_stripped():
    """IDs with leading/trailing whitespace are cleaned."""
    state = _make_state(
        requirements={" 5 ": "Trimmed."},
        asrs=[{"id": " 5 "}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["id"] == "R5"


def test_id_lowercase_r_prefix_is_normalized():
    """Lowercase 'r5' becomes uppercase 'R5'."""
    state = _make_state(
        requirements={"r5": "Uppercased."},
        non_asr=["r5"],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_non_asr"][0]["id"] == "R5"


def test_id_with_non_numeric_r_prefix_gets_prefixed():
    """Non-numeric raw IDs that only start with R get prefixed, not preserved."""
    assert normalize_requirements(
        _make_state(
            requirements={},
            asrs=[{"id": "REQ-1"}],
        ),
        _make_config(),
    )["normalized_asrs"][0]["id"] == "RREQ-1"


def test_asr_description_lookup_uses_stripped_raw_id():
    """Whitespace in raw IDs is stripped before description lookup."""
    state = _make_state(
        requirements={"5": "The system shall normalize whitespace IDs."},
        asrs=[{"id": " 5 "}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "The system shall normalize whitespace IDs."


def test_asr_description_lookup_uses_unprefixed_alternate_key():
    """Canonical prefixed IDs can still resolve unprefixed requirement keys."""
    state = _make_state(
        requirements={"5": "The system shall support alternate lookup keys."},
        asrs=[{"id": "R5"}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "The system shall support alternate lookup keys."


def test_requirements_empty_string_description_wins_over_arlo_fallback():
    """An explicit empty string in requirements is authoritative."""
    state = _make_state(
        requirements={"5": ""},
        asrs=[{"id": 5, "description": "Fallback should not win."}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == ""


def test_whitespace_only_requirement_description_is_ignored():
    """Whitespace-only requirement text should not be treated as usable content."""
    state = _make_state(
        requirements={"5": "   "},
        asrs=[{"id": 5, "description": "ARLO fallback remains usable."}],
    )
    result = normalize_requirements(state, _make_config())
    assert result["normalized_asrs"][0]["description"] == "ARLO fallback remains usable."


def test_duplicate_canonical_ids_raise_error():
    """Two raw requirement IDs that map to one canonical ID must fail fast."""
    state = _make_state(
        requirements={"5": "Duplicate target."},
        asrs=[{"id": 5}],
        non_asr=["R5"],
    )
    with pytest.raises(ValueError, match="Duplicate canonical requirement ID 'R5'"):
        normalize_requirements(state, _make_config())
