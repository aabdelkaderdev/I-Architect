"""Unit tests for relationship requirement_ids preservation in deduplication."""

from raa.judge.deduplication import (
    _rewrite_relationship_ids,
    deduplicate_and_merge_fragment,
)
from raa.state.models import C4Entity, C4Relationship


def test_relationship_requirement_ids_survives_validation():
    """C4Relationship.requirement_ids survives model_validate()."""
    data = {
        "id": "rel_1",
        "source_id": "src_1",
        "target_id": "tgt_1",
        "description": "test relationship",
        "requirement_ids": ["R1", "R2"],
    }
    rel = C4Relationship.model_validate(data)
    assert rel.requirement_ids == ["R1", "R2"]


def test_relationship_requirement_ids_defaults_to_empty():
    """C4Relationship.requirement_ids defaults to empty list when omitted."""
    rel = C4Relationship.model_validate({
        "id": "rel_1",
        "source_id": "src_1",
        "target_id": "tgt_1",
    })
    assert rel.requirement_ids == []


def test_rewrite_relationship_ids_preserves_requirement_ids():
    """_rewrite_relationship_ids copies requirement_ids to rewritten relationships."""
    rel = C4Relationship(
        id="rel_1",
        source_id="old_a",
        target_id="old_b",
        requirement_ids=["R3"],
    )
    rewritten = _rewrite_relationship_ids([rel], "old_a", "new_a")
    assert len(rewritten) == 1
    assert rewritten[0].source_id == "new_a"
    assert rewritten[0].target_id == "old_b"
    assert rewritten[0].requirement_ids == ["R3"]


def test_dedup_and_merge_preserves_relationship_requirement_ids():
    """deduplicate_and_merge_fragment preserves requirement_ids on relationships."""
    entity_a = C4Entity(id="e_a", name="Entity A", description="desc a")
    entity_b = C4Entity(id="e_b", name="Entity B", description="desc b")
    rel = C4Relationship(
        id="rel_ab",
        source_id="e_a",
        target_id="e_b",
        requirement_ids=["R10"],
    )
    fragment = {
        "entities": [entity_a.model_dump()],
        "relationships": [rel.model_dump()],
    }
    running_model = {
        "entities": [entity_b.model_dump()],
        "relationships": [],
    }
    updated, _, _ = deduplicate_and_merge_fragment(
        fragment, running_model, cache=None, model=None,
    )
    updated_rels = updated["relationships"]
    assert len(updated_rels) == 1
    assert updated_rels[0]["requirement_ids"] == ["R10"]
