"""
Unit tests for C4 metamodel hierarchy enforcement (FR-8).

Pure-function tests — no LangGraph runtime, no LLM calls.
"""
from __future__ import annotations

import pytest

from raa.state.models import ArchFragment, C4Entity, C4Relationship
from raa.utils.c4_validator import enforce_fragment_hierarchy


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_running_model(systems=None, containers=None):
    """Build a running model dict in a common shape."""
    model: dict = {}
    if systems is not None:
        model["systems"] = systems
    if containers is not None:
        model["containers"] = containers
    return model


# ── Container parent enforcement ──────────────────────────────────────────────


class TestContainerParentEnforcement:

    def test_valid_parent_in_fragment_kept(self):
        """Container with parent_system_id matching a system in the fragment is kept."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="sys1", name="System", c4_type="system"),
                C4Entity(id="ctr1", name="Container", c4_type="container",
                         parent_system_id="sys1"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        entity_ids = {e.id for e in cleaned.entities}
        assert "ctr1" in entity_ids
        assert questions == []

    def test_valid_parent_in_running_model_kept(self):
        """Container referencing a system in the running model is kept."""
        running_model = _make_running_model(systems=[
            {"id": "sys_rm", "name": "RunningModelSystem"},
        ])
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="Container", c4_type="container",
                         parent_system_id="sys_rm"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, running_model, batch_id="b1", strategy="raa_b",
        )
        assert len(cleaned.entities) == 1
        assert questions == []

    def test_orphan_container_excluded(self):
        """Container referencing nonexistent system is excluded and creates open question."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="Orphan", c4_type="container",
                         parent_system_id="missing_sys"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert len(cleaned.entities) == 0
        assert len(questions) == 1
        q = questions[0]
        assert q["type"] == "hierarchy_conflict"
        assert q["reason"] == "orphan_container"
        assert q["entity_id"] == "ctr1"

    def test_container_missing_parent_flagged(self):
        """Container with no parent_system_id is kept but flagged as coverage gap."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="NoParent", c4_type="container"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_c",
        )
        assert len(cleaned.entities) == 1
        assert len(questions) == 1
        assert questions[0]["reason"] == "container_missing_parent_system"


# ── Component parent enforcement ──────────────────────────────────────────────


class TestComponentParentEnforcement:

    def test_valid_component_parent_in_fragment_kept(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="Container", c4_type="container",
                         parent_system_id="sys1"),
                C4Entity(id="sys1", name="System", c4_type="system"),
                C4Entity(id="comp1", name="Component", c4_type="component",
                         parent_container_id="ctr1"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        entity_ids = {e.id for e in cleaned.entities}
        assert "comp1" in entity_ids

    def test_valid_component_parent_in_running_model_kept(self):
        running_model = _make_running_model(systems=[
            {"id": "sys1", "containers": [{"id": "ctr_rm"}]},
        ])
        fragment = ArchFragment(
            entities=[
                C4Entity(id="comp1", name="Component", c4_type="component",
                         parent_container_id="ctr_rm"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, running_model, batch_id="b1", strategy="raa_b",
        )
        assert len(cleaned.entities) == 1

    def test_orphan_component_excluded(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="comp1", name="OrphanComp", c4_type="component",
                         parent_container_id="missing_ctr"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert len(cleaned.entities) == 0
        q = questions[0]
        assert q["reason"] == "orphan_component"
        assert q["entity_id"] == "comp1"

    def test_component_missing_parent_flagged(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="comp1", name="NoParentComp", c4_type="component"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert len(cleaned.entities) == 1
        assert questions[0]["reason"] == "component_missing_parent_container"


# ── Relationship validation ──────────────────────────────────────────────────


class TestRelationshipValidation:

    def test_valid_relationship_kept(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="sys1", name="S", c4_type="system"),
                C4Entity(id="sys2", name="T", c4_type="system"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="sys1", target_id="sys2",
                               description="connects"),
            ],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert len(cleaned.relationships) == 1

    def test_unresolved_endpoint_excluded(self):
        """After orphan entity removal, relationship with dangling endpoint is removed."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="Orphan", c4_type="container",
                         parent_system_id="missing"),
                C4Entity(id="sys1", name="System", c4_type="system"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="ctr1", target_id="sys1"),
            ],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert len(cleaned.relationships) == 0
        # One question for orphan container, one for relationship
        reasons = {q["reason"] for q in questions}
        assert "orphan_container" in reasons
        assert "unresolved_relationship_endpoint" in reasons


# ── Scope assignment ──────────────────────────────────────────────────────────


class TestScopeAssignment:

    def test_context_scope_for_system_endpoints(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="sys1", name="S1", c4_type="system"),
                C4Entity(id="sys2", name="S2", c4_type="system"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="sys1", target_id="sys2"),
            ],
        )
        cleaned, _ = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert cleaned.relationships[0].diagram_scope == "context"

    def test_container_scope(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="sys1", name="S", c4_type="system"),
                C4Entity(id="ctr1", name="C", c4_type="container",
                         parent_system_id="sys1"),
                C4Entity(id="ctr2", name="C2", c4_type="container",
                         parent_system_id="sys1"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="ctr1", target_id="ctr2"),
            ],
        )
        cleaned, _ = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_b",
        )
        assert cleaned.relationships[0].diagram_scope == "container"

    def test_component_scope(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="sys1", name="S", c4_type="system"),
                C4Entity(id="ctr1", name="C", c4_type="container",
                         parent_system_id="sys1"),
                C4Entity(id="comp1", name="Cmp", c4_type="component",
                         parent_container_id="ctr1"),
                C4Entity(id="comp2", name="Cmp2", c4_type="component",
                         parent_container_id="ctr1"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="comp1", target_id="comp2"),
            ],
        )
        cleaned, _ = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_c",
        )
        assert cleaned.relationships[0].diagram_scope == "component"

    def test_mixed_endpoint_deepest_wins(self):
        """Container -> Component = component scope."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="sys1", name="S", c4_type="system"),
                C4Entity(id="ctr1", name="C", c4_type="container",
                         parent_system_id="sys1"),
                C4Entity(id="comp1", name="Cmp", c4_type="component",
                         parent_container_id="ctr1"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="ctr1", target_id="comp1"),
            ],
        )
        cleaned, _ = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert cleaned.relationships[0].diagram_scope == "component"


# ── Open question metadata ────────────────────────────────────────────────────


class TestOpenQuestionMetadata:

    def test_question_includes_batch_and_strategy(self):
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="Orphan", c4_type="container",
                         parent_system_id="missing"),
            ],
            relationships=[],
        )
        _, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="batch_abc", strategy="raa_b",
        )
        q = questions[0]
        assert q["batch_id"] == "batch_abc"
        assert q["strategy"] == "raa_b"
        assert "suggested_resolution" in q

    def test_person_and_external_system_always_valid(self):
        """Person and external_system entities are never filtered."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="person1", name="User", c4_type="person"),
                C4Entity(id="ext1", name="Payment Gateway", c4_type="external_system"),
            ],
            relationships=[],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert len(cleaned.entities) == 2
        assert questions == []

    def test_invalid_entity_removal_before_relationship_validation(self):
        """Orphan entities are removed first, then relationships checked against valid set."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="OrphanCtr", c4_type="container",
                         parent_system_id="missing"),
                C4Entity(id="sys1", name="System", c4_type="system"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="ctr1", target_id="sys1"),
                C4Relationship(id="r2", source_id="sys1", target_id="ctr1"),
            ],
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        # Both relationships removed because ctr1 is excluded
        assert len(cleaned.relationships) == 0

    def test_preserves_non_entity_fields(self):
        """Cross-cutting candidates, assumption flags, and metadata pass through."""
        fragment = ArchFragment(
            entities=[],
            relationships=[],
            cross_cutting_candidates=["auth", "logging"],
            assumption_flags=["assume_lb"],
            metadata={"source": "test"},
        )
        cleaned, _ = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a",
        )
        assert cleaned.cross_cutting_candidates == ["auth", "logging"]
        assert cleaned.assumption_flags == ["assume_lb"]
        assert cleaned.metadata == {"source": "test"}

    def test_relationship_to_existing_model_entity_kept(self):
        """Relationships linking to existing entities in the running model are preserved."""
        running_model = _make_running_model(systems=[
            {"id": "sys_existing", "name": "Existing System"}
        ])
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr_new", name="New Container", c4_type="container", parent_system_id="sys_existing")
            ],
            relationships=[
                C4Relationship(id="r1", source_id="ctr_new", target_id="sys_existing")
            ]
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, running_model, batch_id="b1", strategy="raa_a"
        )
        assert len(cleaned.relationships) == 1
        assert cleaned.relationships[0].id == "r1"
        assert questions == []

    def test_cascading_orphan_component_excluded(self):
        """If a parent container is excluded as an orphan, any child component is also excluded."""
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr_orphan", name="Orphan Container", c4_type="container", parent_system_id="nonexistent_sys"),
                C4Entity(id="comp_child", name="Child Component", c4_type="component", parent_container_id="ctr_orphan")
            ],
            relationships=[]
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, {}, batch_id="b1", strategy="raa_a"
        )
        entity_ids = {e.id for e in cleaned.entities}
        assert "ctr_orphan" not in entity_ids
        assert "comp_child" not in entity_ids
        reasons = {q["reason"] for q in questions}
        assert "orphan_container" in reasons
        assert "orphan_component" in reasons

    def test_model_containers_handles_non_dict_defensively(self):
        """_model_containers ignores elements in systems list that are not dicts."""
        running_model = {
            "systems": [
                "just_a_string_id",
                {"id": "sys_dict", "containers": [{"id": "ctr_ok"}]}
            ]
        }
        fragment = ArchFragment(
            entities=[
                C4Entity(id="comp_ok", name="Component", c4_type="component", parent_container_id="ctr_ok")
            ],
            relationships=[]
        )
        cleaned, questions = enforce_fragment_hierarchy(
            fragment, running_model, batch_id="b1", strategy="raa_a"
        )
        assert len(cleaned.entities) == 1
        assert cleaned.entities[0].id == "comp_ok"
        assert questions == []
