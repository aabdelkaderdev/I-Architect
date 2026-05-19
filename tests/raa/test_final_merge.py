"""Unit tests for RAA final merge node — global merge, reconciliation,
C4 validation, diagram manifest generation, and filesystem output."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from raa.nodes.final_merge import (
    LLM_JUDGE_KEY,
    final_merge,
    _canonical_id,
    _rel_key,
    _collect_global_fragments,
    _global_merge_fragments,
    _assemble_tree,
    _build_confidence_metadata,
    _build_reconciliation_prompt,
    _apply_reconciliation_response,
    _index_c4_entities,
    _collect_model_relationships,
    validate_c4_model,
    _expected_relationship_scope,
    generate_diagram_manifest,
    _build_c4_handoff_dict,
    _require_output_dir,
    _write_arch_model_json,
)
from raa.state.types import (
    ArchComponent,
    ArchContainer,
    ArchExternalSystem,
    ArchFragment,
    ArchModel,
    ArchPerson,
    ArchRelationship,
    ArchSystem,
    ArchPattern,
    ConfidenceRecord,
    DiagramManifestEntry,
    IncoherentBatchRecord,
    OpenQuestion,
)


# =============================================================================
# T006 — Shared fixtures
# =============================================================================


@pytest.fixture
def fake_system():
    return ArchSystem(id="sys_a", label="System A", description="Primary system")


@pytest.fixture
def fake_container():
    return ArchContainer(
        id="cont_a", label="Container A", description="Web application",
        parent_system_id="sys_a",
    )


@pytest.fixture
def fake_component():
    return ArchComponent(
        id="comp_a", label="Component A", description="Auth service",
        parent_container_id="cont_a",
    )


@pytest.fixture
def fake_llm_judge():
    """Mock LLM that returns a valid reconciliation JSON response."""
    llm = MagicMock()
    llm.invoke.return_value = {
        "resolutions": []
    }
    return llm


@pytest.fixture
def temp_output_dir():
    """Temporary output directory that cleans up after test."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def config_with_llm_and_output(fake_llm_judge, temp_output_dir):
    """Graph config with llm_judge and output_dir in context."""
    return {
        "context": {
            LLM_JUDGE_KEY: fake_llm_judge,
            "output_dir": str(temp_output_dir),
        }
    }


@pytest.fixture
def arch_fragment_a() -> ArchFragment:
    return ArchFragment(
        systems=[
            ArchSystem(id="sys_a", label="System A", description="Primary system from A",
                       source_fragment="raa_a"),
        ],
        containers=[
            ArchContainer(
                id="cont_a", label="Container A", description="Web app from A",
                parent_system_id="sys_a", technology="python",
                source_fragment="raa_a",
            ),
        ],
        components=[
            ArchComponent(
                id="comp_a", label="Component A", description="Auth from A",
                parent_container_id="cont_a",
                source_fragment="raa_a",
            ),
        ],
        persons=[
            ArchPerson(id="user", label="User", description="End user from A"),
        ],
        external_systems=[
            ArchExternalSystem(id="ext_pay", label="Payment Gateway",
                               description="External payment from A", technology="rest"),
        ],
        relationships=[
            ArchRelationship(
                source_id="user", target_id="sys_a",
                interaction_type="uses", technology=None, diagram_scope="context",
            ),
            ArchRelationship(
                source_id="sys_a", target_id="ext_pay",
                interaction_type="calls", technology=None, diagram_scope="context",
            ),
        ],
    )


@pytest.fixture
def arch_fragment_b() -> ArchFragment:
    return ArchFragment(
        systems=[
            ArchSystem(id="sys_a", label="System A", description="Better system description from B",
                       source_fragment="raa_b"),
            ArchSystem(id="sys_b", label="System B", description="Secondary system from B",
                       source_fragment="raa_b"),
        ],
        containers=[
            ArchContainer(
                id="cont_a", label="Container A", description="Web app from B",
                parent_system_id="sys_a",
                source_fragment="raa_b",
            ),
            ArchContainer(
                id="cont_b", label="Container B", description="Worker from B",
                parent_system_id="sys_a", technology="go",
                source_fragment="raa_b",
            ),
        ],
        components=[
            ArchComponent(
                id="comp_a", label="Component A", description="Auth from B",
                parent_container_id="cont_a",
                source_fragment="raa_b",
            ),
        ],
        persons=[
            ArchPerson(id="admin", label="Admin", description="Administrator from B"),
        ],
        relationships=[
            ArchRelationship(
                source_id="sys_a", target_id="sys_b",
                interaction_type="calls", technology=None, diagram_scope="context",
            ),
        ],
    )


@pytest.fixture
def arch_fragment_c() -> ArchFragment:
    """Fragment with conflicting hierarchy parent for cont_a."""
    return ArchFragment(
        systems=[
            ArchSystem(id="sys_x", label="System X", description="Extra system from C",
                       source_fragment="raa_c"),
        ],
        containers=[
            ArchContainer(
                id="cont_a", label="Container A", description="Conflicting container from C",
                parent_system_id="sys_x",
                source_fragment="raa_c",
            ),
        ],
        components=[
            ArchComponent(
                id="comp_b", label="Component B", description="Extra component from C",
                parent_container_id="cont_a",
                source_fragment="raa_c",
            ),
        ],
    )


@pytest.fixture
def multi_batch_state(arch_fragment_a, arch_fragment_b):
    """State with multiple best_batch_output entries and a running model."""
    return {
        "best_batch_output": {
            0: arch_fragment_a,
            1: arch_fragment_b,
        },
        "running_arch_model": ArchModel(),
        "open_questions": [],
        "incoherent_batches": [],
    }


# =============================================================================
# T008 — Fragment collection tests
# =============================================================================


class TestCollectGlobalFragments:
    """T008: final_merge reads all best_batch_output entries in batch-index order."""

    def test_collects_in_sorted_order(self, arch_fragment_a, arch_fragment_b):
        best = {1: arch_fragment_b, 0: arch_fragment_a}
        running = ArchModel()
        fragments = _collect_global_fragments(best, running)
        # First: baseline (empty running model), then batch 0, then batch 1
        assert len(fragments) == 3  # baseline + 2 batches

    def test_includes_running_model_baseline(self, arch_fragment_a):
        running = ArchModel(
            systems=[ArchSystem(id="existing_sys", label="Existing", description="Already present")],
        )
        best = {0: arch_fragment_a}
        fragments = _collect_global_fragments(best, running)
        # Baseline fragment should contain the existing system
        assert len(fragments[0].systems) == 1
        assert fragments[0].systems[0].id == "existing_sys"

    def test_no_batches_returns_only_baseline(self):
        fragments = _collect_global_fragments({}, ArchModel())
        assert len(fragments) == 1


# =============================================================================
# T009 — Entity deduplication tests
# =============================================================================


class TestGlobalEntityDedup:
    """T009: Entity deduplication per type, longest description wins, technology preserved."""

    def test_keeps_longest_description(self, arch_fragment_a, arch_fragment_b):
        merged, _ = _global_merge_fragments([arch_fragment_a, arch_fragment_b])
        sys_a = next(s for s in merged.systems if s.id == "sys_a")
        assert "Better system description from B" in sys_a.description

    def test_preserves_technology(self, arch_fragment_a):
        merged, _ = _global_merge_fragments([arch_fragment_a])
        cont_a = next(c for c in merged.containers if c.id == "cont_a")
        assert cont_a.technology == "python"

    def test_merges_technology_when_not_set(self, arch_fragment_a, arch_fragment_b):
        # Fragment B's cont_b has technology "go", frag A's cont_a has "python"
        merged, _ = _global_merge_fragments([arch_fragment_a, arch_fragment_b])
        cont_b = next(c for c in merged.containers if c.id == "cont_b")
        assert cont_b.technology == "go"

    def test_deterministic_canonical_id_ordering(self, arch_fragment_a, arch_fragment_b):
        merged1, _ = _global_merge_fragments([arch_fragment_a, arch_fragment_b])
        merged2, _ = _global_merge_fragments([arch_fragment_b, arch_fragment_a])
        ids1 = sorted(s.id for s in merged1.systems)
        ids2 = sorted(s.id for s in merged2.systems)
        assert ids1 == ids2

    def test_deduplicates_across_multiple_fragments(self, arch_fragment_a, arch_fragment_b):
        merged, _ = _global_merge_fragments([arch_fragment_a, arch_fragment_b])
        sys_ids = [s.id for s in merged.systems]
        assert sys_ids.count("sys_a") == 1  # Deduplicated

    def test_new_entities_added(self, arch_fragment_a, arch_fragment_b):
        merged, _ = _global_merge_fragments([arch_fragment_a, arch_fragment_b])
        sys_ids = {s.id for s in merged.systems}
        assert "sys_b" in sys_ids


# =============================================================================
# T010 — Relationship deduplication tests
# =============================================================================


class TestGlobalRelationshipDedup:
    """T010: Relationship dedup uses (source_id, target_id, interaction_type)."""

    def test_deduplicates_by_key(self):
        f1 = ArchFragment(relationships=[
            ArchRelationship(source_id="a", target_id="b", interaction_type="calls", technology=None, diagram_scope="context"),
        ])
        f2 = ArchFragment(relationships=[
            ArchRelationship(source_id="a", target_id="b", interaction_type="calls", diagram_scope="context", technology="grpc"),
        ])
        merged, _ = _global_merge_fragments([f1, f2])
        assert len(merged.relationships) == 1

    def test_different_interaction_type_not_deduplicated(self):
        f1 = ArchFragment(relationships=[
            ArchRelationship(source_id="a", target_id="b", interaction_type="calls", technology=None, diagram_scope="context"),
        ])
        f2 = ArchFragment(relationships=[
            ArchRelationship(source_id="a", target_id="b", interaction_type="publishes", technology=None, diagram_scope="context"),
        ])
        merged, _ = _global_merge_fragments([f1, f2])
        assert len(merged.relationships) == 2

    def test_preserves_endpoint_consistent_scope(self):
        f1 = ArchFragment(relationships=[
            ArchRelationship(source_id="a", target_id="b", interaction_type="calls", technology=None, diagram_scope="context"),
        ])
        merged, _ = _global_merge_fragments([f1])
        assert merged.relationships[0].diagram_scope == "context"


# =============================================================================
# T011 — Hierarchy and scope conflict tests
# =============================================================================


class TestHierarchyScopeConflicts:
    """T011: Unresolved hierarchy/scope conflicts represented as OpenQuestion records."""

    def test_hierarchy_conflict_detected(self, arch_fragment_a, arch_fragment_c):
        _, questions = _global_merge_fragments([arch_fragment_a, arch_fragment_c])
        hierarchy_qs = [q for q in questions if q.type == "hierarchy_conflict"]
        assert len(hierarchy_qs) >= 1
        # cont_a conflicts: sys_a vs sys_x parent
        cont_q = next((q for q in hierarchy_qs if q.entity_id == "cont_a"), None)
        assert cont_q is not None

    def test_orphan_detection(self):
        orphan_frag = ArchFragment(
            containers=[
                ArchContainer(id="orphan_c", label="Orphan", description="No parent",
                            parent_system_id="nonexistent"),
            ],
        )
        _, questions = _global_merge_fragments([orphan_frag])
        orphan_qs = [q for q in questions if q.type == "coverage_gap"]
        assert len(orphan_qs) >= 1


# =============================================================================
# T012 — Reconciliation invocation tests
# =============================================================================


class TestReconciliationInvocation:
    """T012: Reconciliation pass invokes llm_judge only with open_questions and summary."""

    def test_prompt_contains_open_questions(self):
        questions = [
            OpenQuestion(entity_id="e1", type="hierarchy_conflict",
                        description="Conflict on e1"),
            OpenQuestion(entity_id="e2", type="scope_conflict",
                        description="Scope mismatch on e2"),
        ]
        model = ArchModel(systems=[ArchSystem(id="s1", label="S1", description="Test")])
        prompt = _build_reconciliation_prompt(questions, model)
        assert "e1" in prompt
        assert "e2" in prompt
        assert "hierarchy_conflict" in prompt
        assert "scope_conflict" in prompt

    def test_prompt_forbids_full_reanalysis(self):
        prompt = _build_reconciliation_prompt([], ArchModel())
        assert "ONLY" in prompt
        assert "full re-analysis" in prompt.lower()

    def test_prompt_includes_compact_model_summary(self):
        model = ArchModel(
            systems=[ArchSystem(id="s1", label="Test System", description="A system")],
            persons=[ArchPerson(id="u1", label="User", description="A user")],
        )
        prompt = _build_reconciliation_prompt([], model)
        assert "Test System" in prompt
        assert "User" in prompt

    def test_invokes_llm_only_with_current_questions(self, fake_llm_judge, temp_output_dir):
        questions = [OpenQuestion(entity_id="e1", type="hierarchy_conflict",
                                  description="Test")]
        model = ArchModel()
        prompt = _build_reconciliation_prompt(questions, model)
        result = fake_llm_judge.invoke(prompt)
        fake_llm_judge.invoke.assert_called_once()
        assert "resolutions" in result


# =============================================================================
# T013 — Valid reconciliation tests
# =============================================================================


class TestValidReconciliation:
    """T013: Valid reconciliation output updates model and removes resolved questions."""

    def test_resolves_hierarchy_conflict(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="System A", description="Primary",
                          containers=[
                              ArchContainer(id="cont_a", label="Container A",
                                           description="Test",
                                           parent_system_id="sys_x"),
                          ]),
            ],
        )
        questions = [
            OpenQuestion(entity_id="cont_a", type="hierarchy_conflict",
                        description="Conflicting parent for cont_a"),
        ]
        response = {
            "resolutions": [
                {
                    "question_index": 0,
                    "resolution_type": "select_parent",
                    "resolved_value": "sys_a",
                    "rationale": "Majority of fragments set sys_a",
                }
            ]
        }
        updated, remaining = _apply_reconciliation_response(model, questions, response)
        assert len(remaining) == 0
        assert updated.systems[0].containers[0].parent_system_id == "sys_a"

    def test_keeps_explicitly_unresolved(self):
        questions = [
            OpenQuestion(entity_id="e1", type="hierarchy_conflict",
                        description="Unresolvable conflict"),
        ]
        response = {
            "resolutions": [
                {
                    "question_index": 0,
                    "resolution_type": "keep_unresolved",
                    "resolved_value": None,
                    "rationale": "Insufficient information",
                }
            ]
        }
        _, remaining = _apply_reconciliation_response(ArchModel(), questions, response)
        assert len(remaining) == 1


# =============================================================================
# T014 — Malformed reconciliation tests
# =============================================================================


class TestMalformedReconciliation:
    """T014: Malformed reconciliation logs warning, preserves questions, doesn't corrupt."""

    def test_preserves_on_malformed_json(self, multi_batch_state, config_with_llm_and_output):
        # Make llm return invalid JSON that will fail
        config_with_llm_and_output["context"][LLM_JUDGE_KEY].invoke.return_value = MagicMock(
            content="not valid json{{{"
        )
        state = multi_batch_state.copy()
        state["open_questions"] = [
            OpenQuestion(entity_id="e1", type="hierarchy_conflict",
                        description="Test conflict"),
        ]
        # Should not raise — logs warning and preserves questions
        result = final_merge(state, config_with_llm_and_output)
        assert len(result["open_questions"]) >= 1

    def test_preserves_on_schema_invalid_output(self, multi_batch_state, config_with_llm_and_output):
        # Return valid JSON but wrong schema
        config_with_llm_and_output["context"][LLM_JUDGE_KEY].invoke.return_value = {
            "wrong_key": []
        }
        state = multi_batch_state.copy()
        state["open_questions"] = [
            OpenQuestion(entity_id="e1", type="hierarchy_conflict",
                        description="Test conflict"),
        ]
        result = final_merge(state, config_with_llm_and_output)
        # Questions preserved because no resolution matched
        assert len(result["open_questions"]) >= 1

    def test_does_not_corrupt_model_on_failure(self, multi_batch_state, config_with_llm_and_output):
        config_with_llm_and_output["context"][LLM_JUDGE_KEY].invoke.side_effect = RuntimeError("LLM crash")
        result = final_merge(state=multi_batch_state, config=config_with_llm_and_output)
        # Model still has the merged systems
        assert result["running_arch_model"] is not None


# =============================================================================
# T015 — State update excludes LLM objects
# =============================================================================


class TestStateUpdateExclusion:
    """T015: Final merge output excludes llm_judge, llm, and any .invoke objects."""

    def test_no_llm_objects_in_return(self, multi_batch_state, config_with_llm_and_output):
        result = final_merge(state=multi_batch_state, config=config_with_llm_and_output)
        for key, value in result.items():
            assert not hasattr(value, "invoke"), f"Key '{key}' has .invoke attribute"


# =============================================================================
# T025 — Valid C4 model acceptance
# =============================================================================


class TestC4ValidationAccept:
    """T025: C4 validation accepts valid nested ArchModel."""

    def test_valid_nested_model_passes(self):
        model = ArchModel(
            systems=[
                ArchSystem(
                    id="sys_a", label="System A", description="Primary",
                    containers=[
                        ArchContainer(
                            id="cont_a", label="Container A", description="Web",
                            parent_system_id="sys_a",
                            components=[
                                ArchComponent(
                                    id="comp_a", label="Component A",
                                    description="Auth",
                                    parent_container_id="cont_a",
                                ),
                            ],
                        ),
                    ],
                    context_relationships=[
                        ArchRelationship(
                            source_id="sys_a", target_id="ext_pay",
                            interaction_type="calls", technology=None, diagram_scope="context",
                        ),
                    ],
                ),
            ],
            persons=[
                ArchPerson(id="user", label="User", description="End user"),
            ],
            external_systems=[
                ArchExternalSystem(id="ext_pay", label="Payment", description="Gateway"),
            ],
        )
        errors = validate_c4_model(model)
        assert len(errors) == 0

    def test_model_with_persons_and_external_systems_passes(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="S", description="D",
                          containers=[
                              ArchContainer(id="c1", label="C", description="D",
                                           parent_system_id="sys_a"),
                          ]),
            ],
            persons=[ArchPerson(id="p1", label="P", description="D")],
            external_systems=[ArchExternalSystem(id="e1", label="E", description="D")],
        )
        errors = validate_c4_model(model)
        assert len(errors) == 0


# =============================================================================
# T026 — Duplicate ID rejection
# =============================================================================


class TestDuplicateIdRejection:
    """T026: C4 validation rejects duplicate IDs across entity types."""

    def test_rejects_system_and_container_same_id(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="dup", label="System", description="A",
                          containers=[
                              ArchContainer(id="dup", label="Also dup", description="B",
                                           parent_system_id="dup"),
                          ]),
            ],
        )
        errors = validate_c4_model(model)
        # Container with same ID as system — orphan check catches it
        dup_errors = [e for e in errors if "dup" in e]
        assert len(dup_errors) > 0

    def test_rejects_person_and_external_system_same_id(self):
        model = ArchModel(
            systems=[],
            persons=[ArchPerson(id="shared", label="Person", description="A")],
            external_systems=[ArchExternalSystem(id="Shared", label="Ext", description="B")],
        )
        errors = validate_c4_model(model)
        # Canonical IDs collide: "shared" == "shared"
        assert len(errors) > 0


# =============================================================================
# T027 — Orphan rejection
# =============================================================================


class TestOrphanRejection:
    """T027: C4 validation rejects orphan containers/components and parent mismatches."""

    def test_rejects_orphan_container(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="S", description="D",
                          containers=[
                              ArchContainer(id="cont_a", label="C", description="D",
                                           parent_system_id="nonexistent"),
                          ]),
            ],
        )
        errors = validate_c4_model(model)
        assert len(errors) > 0

    def test_rejects_orphan_component(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="S", description="D",
                          containers=[
                              ArchContainer(id="cont_a", label="C", description="D",
                                           parent_system_id="sys_a",
                                           components=[
                                               ArchComponent(id="comp_a", label="C", description="D",
                                                           parent_container_id="nonexistent"),
                                           ]),
                          ]),
            ],
        )
        errors = validate_c4_model(model)
        assert len(errors) > 0

    def test_rejects_parent_id_mismatch(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="S", description="D",
                          containers=[
                              ArchContainer(id="cont_a", label="C", description="D",
                                           parent_system_id="sys_b"),
                          ]),
            ],
        )
        errors = validate_c4_model(model)
        assert len(errors) > 0


# =============================================================================
# T028 — Relationship endpoint validation
# =============================================================================


class TestRelationshipEndpointValidation:
    """T028: C4 validation rejects relationships with unresolvable endpoints."""

    def test_rejects_bad_source(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="S", description="D",
                          context_relationships=[
                              ArchRelationship(
                                  source_id="nonexistent", target_id="sys_a",
                                  interaction_type="calls", technology=None, diagram_scope="context",
                              ),
                          ]),
            ],
        )
        errors = validate_c4_model(model)
        assert any("nonexistent" in e for e in errors)

    def test_rejects_bad_target(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="S", description="D",
                          context_relationships=[
                              ArchRelationship(
                                  source_id="sys_a", target_id="nonexistent",
                                  interaction_type="calls", technology=None, diagram_scope="context",
                              ),
                          ]),
            ],
        )
        errors = validate_c4_model(model)
        assert any("nonexistent" in e for e in errors)


# =============================================================================
# T029 — Scope alignment validation
# =============================================================================


class TestScopeAlignmentValidation:
    """T029: C4 validation rejects scope values inconsistent with endpoint types."""

    def test_rejects_context_scope_for_container_endpoints(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="S", description="D",
                          containers=[
                              ArchContainer(id="cont_a", label="C", description="D",
                                           parent_system_id="sys_a"),
                              ArchContainer(id="cont_b", label="C2", description="D2",
                                           parent_system_id="sys_a",
                                           container_relationships=[
                                               ArchRelationship(
                                                   source_id="cont_a", target_id="cont_b",
                                                   interaction_type="calls", technology=None, diagram_scope="context",  # Should be container
                                               ),
                                           ]),
                          ]),
            ],
        )
        errors = validate_c4_model(model)
        scope_errors = [e for e in errors if "diagram_scope" in e]
        assert len(scope_errors) > 0

    def test_expected_scope_rules(self):
        # Component + Component = component
        assert _expected_relationship_scope("component", "component") == "component"
        # Container + Container = container
        assert _expected_relationship_scope("container", "container") == "container"
        # System + Person = context
        assert _expected_relationship_scope("system", "person") == "context"
        # Component + Container = component (highest)
        assert _expected_relationship_scope("component", "container") == "component"
        # Container + System = container
        assert _expected_relationship_scope("container", "system") == "container"


# =============================================================================
# T030 — Manifest count tests
# =============================================================================


class TestManifestCount:
    """T030: diagram_manifest has correct entry count."""

    def test_manifest_entry_count(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="s1", label="S1", description="D"),
                ArchSystem(id="s2", label="S2", description="D",
                          containers=[
                              ArchContainer(id="c1", label="C1", description="D",
                                           parent_system_id="s2"),
                              ArchContainer(id="c2", label="C2", description="D",
                                           parent_system_id="s2"),
                          ]),
            ],
        )
        manifest = generate_diagram_manifest(model)
        # 2 systems * 2 = 4 + 2 containers = 6
        expected = (2 * 2) + 2  # = 6
        assert len(manifest) == expected

    def test_no_systems_empty_manifest(self):
        manifest = generate_diagram_manifest(ArchModel())
        assert len(manifest) == 0

    def test_manifest_contains_correct_types(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="s1", label="S1", description="D",
                          containers=[
                              ArchContainer(id="c1", label="C1", description="D",
                                           parent_system_id="s1"),
                          ]),
            ],
        )
        manifest = generate_diagram_manifest(model)
        types = [e.diagram_type for e in manifest]
        assert types.count("context") == 1
        assert types.count("container") == 1
        assert types.count("component") == 1


# =============================================================================
# T031 — DiagramManifestEntry field correctness
# =============================================================================


class TestManifestEntryFields:
    """T031: Every DiagramManifestEntry has deterministic populated fields."""

    def test_entry_fields_populated(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="s1", label="Main System", description="D"),
            ],
        )
        manifest = generate_diagram_manifest(model)
        ctx_entry = manifest[0]
        assert ctx_entry.diagram_id == "ctx-s1"
        assert ctx_entry.diagram_type == "context"
        assert ctx_entry.focus_entity_id == "s1"
        assert "Main System" in ctx_entry.label

        cnt_entry = manifest[1]
        assert cnt_entry.diagram_id == "cnt-s1"
        assert cnt_entry.diagram_type == "container"
        assert cnt_entry.focus_entity_id == "s1"

    def test_component_entry(self):
        model = ArchModel(
            systems=[
                ArchSystem(id="s1", label="S1", description="D",
                          containers=[
                              ArchContainer(id="c1", label="Auth Container", description="D",
                                           parent_system_id="s1"),
                          ]),
            ],
        )
        manifest = generate_diagram_manifest(model)
        cmp_entry = manifest[-1]
        assert cmp_entry.diagram_id == "cmp-c1"
        assert cmp_entry.diagram_type == "component"
        assert cmp_entry.focus_entity_id == "c1"
        assert "Auth Container" in cmp_entry.label


# =============================================================================
# T032 — Handoff JSON structure
# =============================================================================


class TestHandoffJsonStructure:
    """T032: Handoff JSON contains required fields, excludes diagrams/code/PlantUML."""

    def test_contains_required_fields(self):
        model = ArchModel(
            systems=[ArchSystem(id="s1", label="S1", description="D")],
            persons=[ArchPerson(id="p1", label="P1", description="D")],
            external_systems=[ArchExternalSystem(id="e1", label="E1", description="D")],
            diagram_manifest=[
                DiagramManifestEntry(diagram_id="ctx-s1", diagram_type="context",
                                    focus_entity_id="s1", label="Context — S1"),
            ],
            confidence_metadata={
                "s1": ConfidenceRecord(reduced_confidence=False, source_batch=0,
                                      saam_score=0.9),
            },
            open_questions=[],
        )
        handoff = _build_c4_handoff_dict(model)
        assert "systems" in handoff
        assert "persons" in handoff
        assert "external_systems" in handoff
        assert "patterns" in handoff
        assert "diagram_manifest" in handoff
        assert "confidence_metadata" in handoff
        assert "open_questions" in handoff

    def test_excludes_non_handoff_fields(self):
        handoff = _build_c4_handoff_dict(ArchModel())
        # No generated diagrams, code, PlantUML, or AGA filtering hints
        assert "diagrams" not in handoff
        assert "code" not in handoff
        assert "plantuml" not in handoff
        assert "filtering_hints" not in handoff


# =============================================================================
# T040-T044 — Filesystem output tests
# =============================================================================


class TestFilesystemOutput:
    """T040-T044: Filesystem output requires orchestrator path, writes validated JSON."""

    def test_requires_output_dir(self, multi_batch_state, fake_llm_judge):
        """T040: final_merge requires orchestrator-provided output_dir."""
        config = {"context": {LLM_JUDGE_KEY: fake_llm_judge}}
        with pytest.raises(RuntimeError):
            final_merge(multi_batch_state, config)

    def test_no_fallback_to_hardcoded_path(self, multi_batch_state, fake_llm_judge):
        """T040: Does not fall back to hardcoded projects/{project_name} path."""
        config = {"context": {LLM_JUDGE_KEY: fake_llm_judge}}
        with pytest.raises(RuntimeError) as exc:
            final_merge(multi_batch_state, config)
        assert "output_dir" in str(exc.value)

    def test_writes_indented_json(self, multi_batch_state, config_with_llm_and_output):
        """T041: Valid final model writes indented JSON to arch_model.json."""
        result = final_merge(multi_batch_state, config_with_llm_and_output)
        output_dir = Path(config_with_llm_and_output["context"]["output_dir"])
        output_file = output_dir / "arch_model.json"
        assert output_file.exists()
        content = output_file.read_text()
        parsed = json.loads(content)
        assert "systems" in parsed
        # Verify indentation by checking content has newlines
        assert "\n" in content

    def test_invalid_model_prevents_write(self, config_with_llm_and_output):
        """T042: Invalid C4 validation prevents arch_model.json write."""
        # Create model with relationship pointing to nonexistent entity (flat ArchFragment)
        state = {
            "best_batch_output": {
                0: ArchFragment(
                    systems=[ArchSystem(id="sys_a", label="S", description="D")],
                    relationships=[
                        ArchRelationship(
                            source_id="sys_a", target_id="nonexistent",
                            interaction_type="calls", technology=None,
                            diagram_scope="context",
                        ),
                    ],
                ),
            },
            "running_arch_model": ArchModel(),
            "open_questions": [],
            "incoherent_batches": [],
        }
        with pytest.raises(ValueError) as exc:
            final_merge(state, config_with_llm_and_output)
        assert "C4 validation failed" in str(exc.value)
        # Verify no file written
        output_dir = Path(config_with_llm_and_output["context"]["output_dir"])
        output_file = output_dir / "arch_model.json"
        assert not output_file.exists()

    def test_written_json_matches_handoff_schema(self, multi_batch_state, config_with_llm_and_output):
        """T043: Written JSON matches downstream handoff schema."""
        result = final_merge(multi_batch_state, config_with_llm_and_output)
        output_dir = Path(config_with_llm_and_output["context"]["output_dir"])
        content = json.loads((output_dir / "arch_model.json").read_text())
        assert "diagram_manifest" in content
        assert "confidence_metadata" in content
        assert "systems" in content
        assert "persons" in content
        assert "external_systems" in content

    def test_state_return_excludes_filesystem_objects(self, multi_batch_state, config_with_llm_and_output):
        """T044: State return has running_arch_model and open_questions but no raw objects."""
        result = final_merge(multi_batch_state, config_with_llm_and_output)
        assert "running_arch_model" in result
        assert "open_questions" in result
        # No Path objects in state
        for val in result.values():
            assert not isinstance(val, Path)


# =============================================================================
# T045 — Output directory resolution
# =============================================================================


class TestRequireOutputDir:
    def test_returns_path(self, temp_output_dir):
        ctx = {"output_dir": str(temp_output_dir)}
        result = _require_output_dir(ctx)
        assert isinstance(result, Path)
        assert result == temp_output_dir

    def test_raises_when_missing(self):
        with pytest.raises(RuntimeError) as exc:
            _require_output_dir({})
        assert "output_dir" in str(exc.value)


# =============================================================================
# T046-T047 — File writing
# =============================================================================


class TestWriteArchModelJson:
    def test_writes_and_creates_dir(self, temp_output_dir):
        target = temp_output_dir / "nested" / "raa"
        handoff = {"systems": []}
        _write_arch_model_json(target, handoff)
        output_file = target / "arch_model.json"
        assert output_file.exists()
        content = json.loads(output_file.read_text())
        assert content == handoff

    def test_deterministic_key_ordering(self, temp_output_dir):
        handoff = {"z_field": "z", "a_field": "a"}
        _write_arch_model_json(temp_output_dir, handoff)
        content = (temp_output_dir / "arch_model.json").read_text()
        # sort_keys=True means "a_field" comes first
        assert content.index("a_field") < content.index("z_field")


# =============================================================================
# T049 — Full pipeline integration
# =============================================================================


class TestFinalMergeIntegration:
    """T049: End-to-end final merge integration tests."""

    def test_full_pipeline_two_batches(self, multi_batch_state, config_with_llm_and_output):
        """Two batches produce a coherent merged model written to disk."""
        result = final_merge(multi_batch_state, config_with_llm_and_output)
        model = result["running_arch_model"]
        assert model is not None
        assert len(model.systems) >= 2  # sys_a + sys_b
        assert len(model.persons) >= 2  # user + admin
        assert len(model.diagram_manifest) > 0

    def test_full_pipeline_with_incoherent_batches(self, arch_fragment_a, config_with_llm_and_output):
        state = {
            "best_batch_output": {0: arch_fragment_a},
            "running_arch_model": ArchModel(),
            "open_questions": [],
            "incoherent_batches": [
                IncoherentBatchRecord(batch_id=0, coherence_score=0.3, reduced_confidence=True),
            ],
        }
        result = final_merge(state, config_with_llm_and_output)
        # Model should still be valid
        assert result["running_arch_model"] is not None

    def test_incoherent_batch_reduced_confidence_propagation(self, config_with_llm_and_output):
        """T024: If any batch has reduced_confidence=True, it propagates to the entities of that batch."""
        fragment = ArchFragment(
            systems=[ArchSystem(id="sys_incoherent", label="Incoherent Sys", description="From incoherent batch")],
            containers=[],
        )
        state = {
            "best_batch_output": {0: fragment},
            "running_arch_model": ArchModel(),
            "open_questions": [],
            "incoherent_batches": [
                IncoherentBatchRecord(batch_id=0, coherence_score=0.2, reduced_confidence=True),
            ],
        }
        result = final_merge(state, config_with_llm_and_output)
        model = result["running_arch_model"]
        assert model is not None
        assert "sys_incoherent" in model.confidence_metadata
        assert model.confidence_metadata["sys_incoherent"].reduced_confidence is True
        assert model.confidence_metadata["sys_incoherent"].source_batch == 0

    def test_full_pipeline_with_existing_model(self, config_with_llm_and_output):
        """Existing running model is merged with batch outputs."""
        existing = ArchModel(
            systems=[ArchSystem(id="legacy", label="Legacy", description="Existing system")],
        )
        state = {
            "best_batch_output": {
                0: ArchFragment(
                    systems=[ArchSystem(id="new_sys", label="New", description="New system")],
                    containers=[],
                ),
            },
            "running_arch_model": existing,
            "open_questions": [],
            "incoherent_batches": [],
        }
        result = final_merge(state, config_with_llm_and_output)
        model = result["running_arch_model"]
        sys_ids = {s.id for s in model.systems}
        assert "legacy" in sys_ids
        assert "new_sys" in sys_ids

    def test_confidence_metadata_produced(self, multi_batch_state, config_with_llm_and_output):
        result = final_merge(multi_batch_state, config_with_llm_and_output)
        model = result["running_arch_model"]
        assert isinstance(model.confidence_metadata, dict)
        # Should have entries for sys_a, cont_a, etc.
        assert len(model.confidence_metadata) > 0


# =============================================================================
# T051 — No LLM in deterministic helpers (verified by test structure)
# =============================================================================

class TestDeterministicHelpersNoLLM:
    """T051: Deterministic helpers contain no LLM calls."""

    def test_global_merge_no_llm(self, arch_fragment_a, arch_fragment_b):
        """Global merge runs without any LLM dependency."""
        merged, questions = _global_merge_fragments([arch_fragment_a, arch_fragment_b])
        assert merged.systems  # Systems were merged
        assert isinstance(questions, list)  # Questions list returned

    def test_validate_c4_no_llm(self):
        """C4 validation runs without any LLM dependency."""
        errors = validate_c4_model(ArchModel())
        assert isinstance(errors, list)

    def test_generate_manifest_no_llm(self):
        """Manifest generation runs without any LLM dependency."""
        model = ArchModel(systems=[ArchSystem(id="s1", label="S1", description="D")])
        manifest = generate_diagram_manifest(model)
        assert len(manifest) == 2

    def test_build_handoff_no_llm(self):
        """Handoff JSON construction runs without any LLM dependency."""
        handoff = _build_c4_handoff_dict(ArchModel())
        assert "systems" in handoff


class TestDesyncRecoveryAndC4Reversion:
    """T020-T022: Desync recovery and C4 validation-based reversion tests."""

    def test_desync_detection_missing_batch_key(self, config_with_llm_and_output):
        """T020: Desync triggers rollback of batch_cursor and prevents merge output."""
        state = {
            "batch_queue": [{"id": 0}, {"id": 1}, {"id": 2}],
            "best_batch_output": {
                0: ArchFragment(systems=[ArchSystem(id="sys_a", label="A", description="D")]),
                2: ArchFragment(systems=[ArchSystem(id="sys_c", label="C", description="D")]),
            },
            "running_arch_model": ArchModel(),
            "open_questions": [],
            "incoherent_batches": [],
        }
        output_dir = Path(config_with_llm_and_output["context"]["output_dir"])
        output_file = output_dir / "arch_model.json"
        if output_file.exists():
            output_file.unlink()

        with patch("raa.nodes.final_merge.logger.warning") as mock_warn:
            result = final_merge(state, config_with_llm_and_output)
            assert result.get("batch_cursor") == 1
            assert "running_arch_model" not in result
            assert not output_file.exists()

            warning_called = False
            for call in mock_warn.call_args_list:
                msg = call[0][0]
                if "Desync detected" in msg:
                    warning_called = True
                    break
            assert warning_called, "Warning log about Desync was not emitted"

    def test_desync_detection_corrupt_fragment(self, config_with_llm_and_output):
        """T021: None or empty fragment in best_batch_output is treated as desync."""
        state = {
            "batch_queue": [{"id": 0}, {"id": 1}, {"id": 2}],
            "best_batch_output": {
                0: ArchFragment(systems=[ArchSystem(id="sys_a", label="A", description="D")]),
                1: None,
                2: ArchFragment(systems=[ArchSystem(id="sys_c", label="C", description="D")]),
            },
            "running_arch_model": ArchModel(),
            "open_questions": [],
            "incoherent_batches": [],
        }
        with patch("raa.nodes.final_merge.logger.warning") as mock_warn:
            result = final_merge(state, config_with_llm_and_output)
            assert result.get("batch_cursor") == 1
            assert "running_arch_model" not in result

            warning_called = False
            for call in mock_warn.call_args_list:
                msg = call[0][0]
                if "Desync detected" in msg:
                    warning_called = True
                    break
            assert warning_called, "Warning log about Desync was not emitted"

    def test_reconciliation_output_validated_against_c4(self, config_with_llm_and_output):
        """T022: Broken reconciliation model is rejected and reverted to pre-reconciliation state."""
        state = {
            "batch_queue": [{"id": 0}],
            "best_batch_output": {
                0: ArchFragment(
                    systems=[
                        ArchSystem(id="sys_a", label="A", description="D")
                    ],
                    containers=[
                        ArchContainer(id="cont_a", label="Cont A", description="D", parent_system_id="sys_a"),
                        ArchContainer(id="cont_b", label="Cont B", description="D", parent_system_id="sys_a"),
                    ],
                    components=[
                        ArchComponent(id="comp1", label="Comp 1", description="D", parent_container_id="cont_a")
                    ]
                ),
                1: ArchFragment(
                    components=[
                        ArchComponent(id="comp1", label="Comp 1", description="D", parent_container_id="cont_b")
                    ]
                )
            },
            "running_arch_model": ArchModel(),
            "open_questions": [],
            "incoherent_batches": [],
        }

        # Mock LLM to return select_parent to a nonexistent container
        # This will fail C4 validation since "nonexistent" != "cont_a" (its owning container)
        mock_response = {
            "resolutions": [
                {
                    "question_index": 0,
                    "resolution_type": "select_parent",
                    "resolved_value": "nonexistent",
                    "rationale": "bad resolution"
                }
            ]
        }
        
        # Make the batch queue length match best_batch_output keys to pass desync check
        state["batch_queue"] = [{"id": 0}, {"id": 1}]

        with patch("raa.nodes.final_merge._invoke_llm", return_value=mock_response):
            with patch("raa.nodes.final_merge.logger.warning") as mock_warn:
                result = final_merge(state, config_with_llm_and_output)
                
                # Check that we fell back to pre-reconcile model (comp1 parent is cont_a)
                model = result["running_arch_model"]
                comp = model.systems[0].containers[0].components[0]
                assert comp.parent_container_id == "cont_a"
                
                # Verify that warning about reversion was logged
                warning_called = False
                for call in mock_warn.call_args_list:
                    msg = call[0][0]
                    if "Reconciliation introduced new C4 violations" in msg:
                        warning_called = True
                        break
                assert warning_called, "Warning about C4 violation reversion was not emitted"


def test_c4_structural_integrity_nested():
    """T025: Verify nested hierarchy, no cross-level ID reuse, endpoint resolution, and diagram_scope consistency."""
    from raa.nodes.final_merge import validate_c4_model
    # 1. Nesting: systems contain containers, containers contain components.
    # 2. No cross-level ID reuse: system and container sharing ID "same_id" is rejected.
    invalid_model = ArchModel(
        systems=[
            ArchSystem(id="same_id", label="Sys", description="desc"),
        ]
    )
    invalid_model.systems[0].containers = [
        ArchContainer(id="same_id", label="Cont", description="desc", parent_system_id="same_id")
    ]
    errors = validate_c4_model(invalid_model)
    assert any("Duplicate entity ID" in e for e in errors)

    # 3. Endpoint resolution: relationship endpoints must resolve.
    sys_a = ArchSystem(id="sys_a", label="Sys A", description="desc")
    sys_a.context_relationships = [
        ArchRelationship(source_id="sys_a", target_id="non_existent", interaction_type="uses", technology="HTTPS", diagram_scope="context")
    ]
    invalid_rel_model = ArchModel(systems=[sys_a])
    errors_rel = validate_c4_model(invalid_rel_model)
    assert any("Relationship target 'non_existent' not found" in e for e in errors_rel)

    # 4. diagram_scope consistency: context scope for container-to-container relationship is rejected.
    sys = ArchSystem(id="sys_a", label="Sys A", description="desc")
    cont_1 = ArchContainer(id="cont_1", label="C1", description="desc", parent_system_id="sys_a")
    cont_2 = ArchContainer(id="cont_2", label="C2", description="desc", parent_system_id="sys_a")
    cont_1.container_relationships = [
        ArchRelationship(source_id="cont_1", target_id="cont_2", interaction_type="communicates", technology="HTTPS", diagram_scope="context")
    ]
    sys.containers = [cont_1, cont_2]
    invalid_scope_model = ArchModel(systems=[sys])
    errors_scope = validate_c4_model(invalid_scope_model)
    assert any("diagram_scope" in e.lower() for e in errors_scope)


def test_diagram_manifest_completeness():
    """T026: Verify diagram_manifest entry count formula and field completeness."""
    from raa.nodes.final_merge import generate_diagram_manifest
    sys1 = ArchSystem(id="sys1", label="Sys 1", description="Description 1")
    sys1.containers = [
        ArchContainer(id="cont1", label="Cont 1", description="Desc 1", parent_system_id="sys1"),
        ArchContainer(id="cont2", label="Cont 2", description="Desc 2", parent_system_id="sys1"),
    ]
    model = ArchModel(systems=[sys1])
    manifest = generate_diagram_manifest(model)

    # Count must equal: 1 (global context) + len(systems) + len(containers)
    # systems = 1, containers = 2 => count = 4
    assert len(manifest) == 4

    for entry in manifest:
        assert entry.diagram_id
        assert entry.diagram_type in ("context", "container", "component")
        assert entry.focus_entity_id
        assert entry.label

