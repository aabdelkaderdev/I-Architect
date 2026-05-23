"""
Unit tests for deduplication engine (Story 2.4).
"""
from __future__ import annotations

import pytest

from raa.judge.deduplication import (
    normalize_entity_id,
    deduplicate_and_merge_fragment,
    _merge_entities,
    _union_technology,
    _do_ids_overlap,
    _rewrite_relationship_ids,
    _create_boundary_group,
    _to_entity,
    _to_relationship,
)
from raa.state.models import C4Entity, C4Relationship


# ── ID Normalization ────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "input_id, expected",
    [
        ("User_Service", "user_service"),
        ("userService", "user_service"),
        ("user-service", "user_service"),
        ("UserService", "user_service"),
        ("DTOParser", "dto_parser"),
        ("user.service", "user_service"),
        ("user service", "user_service"),
        ("user__service", "user_service"),
        ("_user_service_", "user_service"),
        ("simple", "simple"),
        ("UPPERCASE", "uppercase"),
        ("HTTPClient", "http_client"),
        ("  spaced  ", "spaced"),
    ],
)
def test_normalize_entity_id(input_id, expected):
    assert normalize_entity_id(input_id) == expected


# ── Technology Union ────────────────────────────────────────────────────────


def test_union_technology_basic():
    result = _union_technology("Python, FastAPI", "FastAPI, Redis")
    assert result == "FastAPI, Python, Redis"


def test_union_technology_semicolons():
    result = _union_technology("Python;FastAPI", "Redis; Python")
    assert result == "FastAPI, Python, Redis"


def test_union_technology_empty():
    assert _union_technology("", "") == ""
    assert _union_technology("Python", "") == "Python"


def test_union_technology_whitespace():
    result = _union_technology("  Python  ,  FastAPI  ", "  FastAPI  ")
    assert result == "FastAPI, Python"


# ── Requirement ID Overlap ──────────────────────────────────────────────────


def test_do_ids_overlap_true():
    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
    b = C4Entity(id="b", name="B", requirement_ids=["R2", "R3"])
    assert _do_ids_overlap(a, b) is True


def test_do_ids_overlap_false():
    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
    b = C4Entity(id="b", name="B", requirement_ids=["R3", "R4"])
    assert _do_ids_overlap(a, b) is False


def test_do_ids_overlap_empty():
    a = C4Entity(id="a", name="A")
    b = C4Entity(id="b", name="B")
    assert _do_ids_overlap(a, b) is False


# ── Entity Merging ──────────────────────────────────────────────────────────


def test_merge_entities_longest_description_kept():
    a = C4Entity(id="a", name="A", description="Short", technology="Python",
                 requirement_ids=["R1"])
    b = C4Entity(id="b", name="B", description="Much longer description here",
                 technology="FastAPI", requirement_ids=["R2"])
    merged = _merge_entities(a, b)
    assert merged.description == "Much longer description here"


def test_merge_entities_canonical_id_from_more_reqs():
    a = C4Entity(id="a", name="A", requirement_ids=["R1"])
    b = C4Entity(id="b", name="B", requirement_ids=["R2", "R3"])
    merged = _merge_entities(a, b)
    assert merged.id == "b"


def test_merge_entities_canonical_id_tie_break_a():
    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
    b = C4Entity(id="b", name="B", requirement_ids=["R3", "R4"])
    merged = _merge_entities(a, b)
    assert merged.id == "a"  # tie → entity_a wins


def test_merge_entities_technology_union():
    a = C4Entity(id="a", name="A", technology="Python, FastAPI", requirement_ids=["R1"])
    b = C4Entity(id="b", name="B", technology="FastAPI, Redis", requirement_ids=["R1"])
    merged = _merge_entities(a, b)
    assert "Python" in merged.technology
    assert "FastAPI" in merged.technology
    assert "Redis" in merged.technology


def test_merge_entities_requirement_ids_union():
    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
    b = C4Entity(id="b", name="B", requirement_ids=["R2", "R3"])
    merged = _merge_entities(a, b)
    assert merged.requirement_ids == ["R1", "R2", "R3"]


def test_merge_entities_metadata_merged():
    a = C4Entity(id="a", name="A", metadata={"key_a": 1})
    b = C4Entity(id="b", name="B", metadata={"key_b": 2})
    merged = _merge_entities(a, b)
    assert merged.metadata == {"key_a": 1, "key_b": 2}


def test_merge_entities_retains_c4_type():
    a = C4Entity(id="a", name="A", c4_type="container", requirement_ids=["R1", "R2"])
    b = C4Entity(id="b", name="B", c4_type="component", requirement_ids=["R3"])
    merged = _merge_entities(a, b)
    assert merged.c4_type == "container"  # canonical (more reqs) is a


# ── Relationship Rewriting ──────────────────────────────────────────────────


def test_rewrite_relationship_ids_source():
    rels = [
        C4Relationship(
            id="rel-1", source_id="old_id", target_id="other",
            description="uses", relationship_type="uses",
        ),
    ]
    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
    assert result[0].source_id == "new_id"
    assert result[0].target_id == "other"


def test_rewrite_relationship_ids_target():
    rels = [
        C4Relationship(
            id="rel-1", source_id="other", target_id="old_id",
            description="uses", relationship_type="uses",
        ),
    ]
    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
    assert result[0].source_id == "other"
    assert result[0].target_id == "new_id"


def test_rewrite_relationship_ids_both():
    rels = [
        C4Relationship(
            id="rel-1", source_id="old_id", target_id="old_id",
            description="self-ref", relationship_type="uses",
        ),
    ]
    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
    assert result[0].source_id == "new_id"
    assert result[0].target_id == "new_id"


def test_rewrite_relationship_ids_no_match():
    rels = [
        C4Relationship(
            id="rel-1", source_id="a", target_id="b",
            description="uses", relationship_type="uses",
        ),
    ]
    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
    assert result[0].source_id == "a"
    assert result[0].target_id == "b"


def test_rewrite_relationship_ids_does_not_mutate_original():
    rels = [
        C4Relationship(
            id="rel-1", source_id="old_id", target_id="other",
        ),
    ]
    _rewrite_relationship_ids(rels, "old_id", "new_id")
    assert rels[0].source_id == "old_id"  # unchanged


# ── Boundary Group Creation ─────────────────────────────────────────────────


def test_create_boundary_group():
    bg = _create_boundary_group("entity_a", "entity_b", 0.7234)
    assert bg["group_id"] == "bg_entity_a_entity_b"
    assert bg["entity_ids"] == ["entity_a", "entity_b"]
    assert bg["similarity"] == 0.7234
    assert "rationale" in bg


# ── Type Coercion ───────────────────────────────────────────────────────────


def test_to_entity_from_dict():
    d = {"id": "a", "name": "A", "description": "desc"}
    result = _to_entity(d)
    assert isinstance(result, C4Entity)
    assert result.id == "a"


def test_to_entity_from_c4entity():
    e = C4Entity(id="a", name="A")
    result = _to_entity(e)
    assert result is e


def test_to_entity_bad_type():
    with pytest.raises(TypeError):
        _to_entity("not an entity")


def test_to_relationship_from_dict():
    d = {"id": "r1", "source_id": "a", "target_id": "b"}
    result = _to_relationship(d)
    assert isinstance(result, C4Relationship)
    assert result.id == "r1"


def test_to_relationship_bad_type():
    with pytest.raises(TypeError):
        _to_relationship(42)


# ── Deduplicate and Merge Fragment ──────────────────────────────────────────


def _entity_dict(**overrides):
    defaults = {
        "id": "svc-1",
        "name": "Service 1",
        "description": "A backend service for user management",
        "c4_type": "container",
        "technology": "Python",
        "requirement_ids": ["R1"],
    }
    defaults.update(overrides)
    return defaults


def _rel_dict(**overrides):
    defaults = {
        "id": "rel-1",
        "source_id": "svc-1",
        "target_id": "svc-2",
        "description": "uses",
        "relationship_type": "uses",
    }
    defaults.update(overrides)
    return defaults


class TestDeduplicateAndMergeFragment:
    """Tests for deduplicate_and_merge_fragment function."""

    def test_empty_fragment_empty_model(self):
        """Empty fragment into empty model → empty model."""
        model, questions, _ = deduplicate_and_merge_fragment(
            {"entities": [], "relationships": []},
            {},
            None,
            None,
        )
        assert model["entities"] == []
        assert model["relationships"] == []
        assert model["boundary_groups"] == []
        assert questions == []

    def test_new_entities_added_to_empty_model(self):
        """First batch: all entities added without dedup."""
        pf = {
            "entities": [_entity_dict(id="svc-1"), _entity_dict(id="svc-2")],
            "relationships": [_rel_dict()],
        }
        model, questions, _ = deduplicate_and_merge_fragment(pf, {}, None, None)

        assert len(model["entities"]) == 2
        assert len(model["relationships"]) == 1
        assert questions == []

    def test_exact_id_match_merges(self):
        """Normalized ID match (no model needed)."""
        pf = {
            "entities": [_entity_dict(id="user-service", description="New desc",
                                      technology="FastAPI", requirement_ids=["R1"])],
            "relationships": [],
        }
        running = {
            "entities": [_entity_dict(id="user_service", description="Old",
                                      technology="Python", requirement_ids=["R2"])],
            "relationships": [],
        }

        model, questions, _ = deduplicate_and_merge_fragment(pf, running, None, None)

        assert len(model["entities"]) == 1
        merged = model["entities"][0]
        assert merged["description"] == "New desc"  # longer kept
        assert "FastAPI" in merged["technology"]
        assert "Python" in merged["technology"]
        assert set(merged["requirement_ids"]) == {"R1", "R2"}

    def test_exact_id_match_rewrites_relationships(self):
        """When entity merged by ID, relationships are rewritten."""
        pf = {
            "entities": [_entity_dict(id="user-service")],
            "relationships": [_rel_dict(source_id="user-service", target_id="payment")],
        }
        running = {
            "entities": [_entity_dict(id="user_service")],
            "relationships": [],
        }

        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)

        assert len(model["relationships"]) == 1
        assert model["relationships"][0]["source_id"] == model["entities"][0]["id"]

    def test_no_model_fallback_adds_as_new(self):
        """When cache=None, no similarity check — non-matching entities added as new."""
        pf = {
            "entities": [_entity_dict(id="svc-new")],
            "relationships": [],
        }
        running = {
            "entities": [_entity_dict(id="svc-existing")],
            "relationships": [],
        }

        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)

        assert len(model["entities"]) == 2

    def test_preserves_existing_boundary_groups(self):
        """Existing boundary_groups in running model are preserved."""
        existing_bg = [{"group_id": "bg_old", "entity_ids": ["a", "b"], "similarity": 0.7}]
        pf = {"entities": [_entity_dict()], "relationships": []}
        running = {"entities": [], "relationships": [], "boundary_groups": existing_bg}

        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)

        assert len(model["boundary_groups"]) == 1
        assert model["boundary_groups"][0]["group_id"] == "bg_old"

    def test_returns_serialized_dicts(self):
        """Output should contain plain dicts, not Pydantic models."""
        pf = {"entities": [_entity_dict()], "relationships": [_rel_dict()]}
        model, _, _ = deduplicate_and_merge_fragment(pf, {}, None, None)

        assert isinstance(model["entities"][0], dict)
        assert isinstance(model["relationships"][0], dict)

    def test_no_id_match_no_model(self):
        """Different IDs, no model → entities added separately."""
        pf = {
            "entities": [_entity_dict(id="svc-a")],
            "relationships": [],
        }
        running = {
            "entities": [_entity_dict(id="svc-b")],
            "relationships": [],
        }

        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)

        assert len(model["entities"]) == 2
        ids = {e["id"] for e in model["entities"]}
        assert ids == {"svc-a", "svc-b"}

    def test_union_technology_case_insensitive_dedup(self):
        """Technology union should deduplicate case-insensitively."""
        result = _union_technology("python, fastapi", "Python, FastAPI")
        assert result == "FastAPI, Python"

    def test_merge_hierarchy_mismatch_creates_open_question(self):
        """Hierarchy mismatch during merge should create a change_risk open question."""
        pf = {
            "entities": [_entity_dict(id="user-service", parent_system_id="system-a")],
            "relationships": [],
        }
        running = {
            "entities": [_entity_dict(id="user_service", parent_system_id="system-b")],
            "relationships": [],
        }
        model, questions, _ = deduplicate_and_merge_fragment(pf, running, None, None)
        assert len(questions) == 1
        assert questions[0]["question_type"] == "change_risk"
        assert "mismatching C4 parent hierarchy" in questions[0]["description"]

    # ── Merge Log (Story 2.5) ──────────────────────────────────────────

    def test_returns_3_tuple_with_merge_log(self):
        """deduplicate_and_merge_fragment returns 3-tuple: (model, questions, merge_log)."""
        pf = {"entities": [_entity_dict()], "relationships": []}
        result = deduplicate_and_merge_fragment(pf, {}, None, None)
        assert len(result) == 3
        model, questions, merge_log = result
        assert isinstance(model, dict)
        assert isinstance(questions, list)
        assert isinstance(merge_log, list)

    def test_merge_log_empty_when_no_merges(self):
        pf = {"entities": [_entity_dict(id="svc-new")], "relationships": []}
        running = {"entities": [_entity_dict(id="svc-existing")], "relationships": []}
        _, _, merge_log = deduplicate_and_merge_fragment(pf, running, None, None)
        assert merge_log == []

    def test_merge_log_records_exact_id_merge(self):
        pf = {
            "entities": [_entity_dict(id="user-service")],
            "relationships": [],
        }
        running = {
            "entities": [_entity_dict(id="user_service")],
            "relationships": [],
        }
        _, _, merge_log = deduplicate_and_merge_fragment(pf, running, None, None)
        assert len(merge_log) == 1
        entry = merge_log[0]
        assert "merged_entity_id" in entry
        assert "source_entity_ids" in entry
        assert len(entry["source_entity_ids"]) == 2
        assert entry["merge_type"] == "exact_id"

    def test_merge_log_entry_structure(self):
        pf = {
            "entities": [_entity_dict(id="user-service")],
            "relationships": [],
        }
        running = {
            "entities": [_entity_dict(id="user_service")],
            "relationships": [],
        }
        _, _, merge_log = deduplicate_and_merge_fragment(pf, running, None, None)
        entry = merge_log[0]
        assert isinstance(entry["merged_entity_id"], str)
        assert isinstance(entry["source_entity_ids"], list)
        assert all(isinstance(eid, str) for eid in entry["source_entity_ids"])
        assert entry["merge_type"] in ("exact_id", "similarity")
