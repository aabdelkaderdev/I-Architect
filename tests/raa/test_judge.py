"""Unit tests for RAA judge node — SAAM scoring, deterministic merge,
conflict detection, coverage union, tree assembly, and state output."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from raa.nodes.judge import (
    LLM_JUDGE_KEY,
    JudgeScore,
    judge_batch,
    _canonical_id,
    _rel_key,
    _rel_key_str,
    _select_primary,
    _deduplicate_entities,
    _deduplicate_relationships,
    _coverage_union,
    _assemble_tree,
    _update_running_model,
    _score_fragments,
    _build_entity_type_index,
    _resolve_scope,
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
    OpenQuestion,
)


# =============================================================================
# T004 — Shared fixtures
# =============================================================================


@pytest.fixture
def fake_system():
    """Minimal ArchSystem fixture."""
    return ArchSystem(id="sys_a", label="System A", description="Primary system")


@pytest.fixture
def fake_container():
    """Minimal ArchContainer fixture."""
    return ArchContainer(
        id="cont_a", label="Container A", description="Web application",
        parent_system_id="sys_a",
    )


@pytest.fixture
def fake_component():
    """Minimal ArchComponent fixture."""
    return ArchComponent(
        id="comp_a", label="Component A", description="Auth service",
        parent_container_id="cont_a",
    )


@pytest.fixture
def arch_fragment_a() -> ArchFragment:
    """Candidate fragment from RAA-A (SAAM-first)."""
    return ArchFragment(
        systems=[
            ArchSystem(id="sys_a", label="System A", description="Primary system from A",
                       source_fragment="raa_a"),
        ],
        containers=[
            ArchContainer(
                id="cont_a", label="Container A", description="Web app from A",
                parent_system_id="sys_a", source_fragment="raa_a",
            ),
        ],
        components=[
            ArchComponent(
                id="comp_a", label="Component A", description="Auth service from A",
                parent_container_id="cont_a", source_fragment="raa_a",
            ),
        ],
        persons=[
            ArchPerson(id="user_1", label="End User", description="Primary user",
                       source_fragment="raa_a"),
        ],
        external_systems=[],
        relationships=[
            ArchRelationship(
                source_id="user_1", target_id="sys_a",
                interaction_type="uses", technology="HTTPS",
                diagram_scope="context", source_fragment="raa_a",
            ),
        ],
        patterns=[],
        rationale={"summary": "SAAM-first analysis"},
    )


@pytest.fixture
def arch_fragment_b() -> ArchFragment:
    """Candidate fragment from RAA-B (pattern-driven)."""
    return ArchFragment(
        systems=[
            ArchSystem(id="sys_a", label="System A", description="Primary system",
                       source_fragment="raa_b"),
            ArchSystem(id="sys_b", label="System B", description="Secondary system from B",
                       source_fragment="raa_b"),
        ],
        containers=[
            ArchContainer(
                id="cont_a", label="Container A", description="Web app from B (longer)",
                parent_system_id="sys_a", source_fragment="raa_b",
            ),
            ArchContainer(
                id="cont_b", label="Container B", description="API service from B",
                parent_system_id="sys_b", source_fragment="raa_b",
            ),
        ],
        components=[
            ArchComponent(
                id="comp_a", label="Component A", description="Auth module",
                parent_container_id="cont_a", source_fragment="raa_b",
            ),
            ArchComponent(
                id="comp_b", label="Component B", description="Payment module",
                parent_container_id="cont_b", source_fragment="raa_b",
            ),
        ],
        persons=[
            ArchPerson(id="user_1", label="End User", description="Primary end user",
                       source_fragment="raa_b"),
        ],
        external_systems=[
            ArchExternalSystem(id="ext_pay", label="Payment Gateway",
                               description="External payment provider",
                               source_fragment="raa_b"),
        ],
        relationships=[
            ArchRelationship(
                source_id="user_1", target_id="sys_a",
                interaction_type="uses", technology="HTTPS",
                diagram_scope="context", source_fragment="raa_b",
            ),
            ArchRelationship(
                source_id="sys_a", target_id="sys_b",
                interaction_type="calls", technology="gRPC",
                diagram_scope="context", source_fragment="raa_b",
            ),
        ],
        patterns=[],
        rationale={"summary": "Pattern-driven analysis"},
    )


@pytest.fixture
def arch_fragment_c() -> ArchFragment:
    """Candidate fragment from RAA-C (entity-driven)."""
    return ArchFragment(
        systems=[
            ArchSystem(id="sys_c", label="System C", description="Tertiary system from C",
                       source_fragment="raa_c"),
        ],
        containers=[
            ArchContainer(
                id="cont_c", label="Container C", description="Worker service",
                parent_system_id="sys_c", source_fragment="raa_c",
            ),
        ],
        components=[
            ArchComponent(
                id="comp_c1", label="Component C1", description="Queue processor",
                parent_container_id="cont_c", source_fragment="raa_c",
            ),
        ],
        persons=[],
        external_systems=[],
        relationships=[
            ArchRelationship(
                source_id="sys_a", target_id="sys_c",
                interaction_type="calls", technology="gRPC",
                diagram_scope="context", source_fragment="raa_c",
            ),
        ],
        patterns=[],
        rationale={"summary": "Entity-driven analysis"},
    )


@pytest.fixture
def fake_batch() -> dict:
    """Minimal batch dict for judge tests."""
    return {
        "batch_id": 0,
        "group_id": 1,
        "requirement_ids": ["R1", "R2"],
        "requirements": [
            {"id": "R1", "text": "The system shall authenticate users."},
            {"id": "R2", "text": "The system shall process payments."},
        ],
        "reduced_confidence": False,
    }


@pytest.fixture
def fake_reduced_confidence_batch() -> dict:
    """Batch with reduced_confidence flag."""
    return {
        "batch_id": 1,
        "group_id": 2,
        "requirement_ids": ["R3"],
        "requirements": [{"id": "R3", "text": "Unclear requirement."}],
        "reduced_confidence": True,
    }


@pytest.fixture
def fake_quality_weights() -> dict[str, int]:
    return {"security": 5, "performance": 3, "maintainability": 2}


@pytest.fixture
def fake_llm_judge() -> MagicMock:
    """Fake llm_judge returning SAAM scores for 3 fragments."""
    llm = MagicMock()
    llm.invoke.return_value = {
        "scores": [
            {
                "source_fragment": "raa_a",
                "base_score": 8.5,
                "covered_entity_ids": ["sys_a", "cont_a", "comp_a", "user_1"],
                "covered_relationship_keys": ["user_1->sys_a:uses"],
            },
            {
                "source_fragment": "raa_b",
                "base_score": 9.2,
                "covered_entity_ids": ["sys_a", "sys_b", "cont_a", "cont_b",
                                       "comp_a", "comp_b", "user_1", "ext_pay"],
                "covered_relationship_keys": ["user_1->sys_a:uses", "sys_a->sys_b:calls"],
            },
            {
                "source_fragment": "raa_c",
                "base_score": 6.0,
                "covered_entity_ids": ["sys_c", "cont_c", "comp_c1"],
                "covered_relationship_keys": ["sys_a->sys_c:calls"],
            },
        ]
    }
    return llm


@pytest.fixture
def fake_score_response() -> list[JudgeScore]:
    """Pre-built JudgeScore list for 3 fragments."""
    return [
        JudgeScore(
            source_fragment="raa_a",
            base_score=8.5,
            weighted_score=8.5,
            covered_entity_ids=["sys_a", "cont_a", "comp_a", "user_1"],
            covered_relationship_keys=["user_1->sys_a:uses"],
            reduced_confidence=False,
        ),
        JudgeScore(
            source_fragment="raa_b",
            base_score=9.2,
            weighted_score=9.2,
            covered_entity_ids=["sys_a", "sys_b", "cont_a", "cont_b",
                                "comp_a", "comp_b", "user_1", "ext_pay"],
            covered_relationship_keys=["user_1->sys_a:uses", "sys_a->sys_b:calls"],
            reduced_confidence=False,
        ),
        JudgeScore(
            source_fragment="raa_c",
            base_score=6.0,
            weighted_score=6.0,
            covered_entity_ids=["sys_c", "cont_c", "comp_c1"],
            covered_relationship_keys=["sys_a->sys_c:calls"],
            reduced_confidence=False,
        ),
    ]


@pytest.fixture
def fake_arch_model() -> ArchModel:
    """Empty ArchModel fixture."""
    return ArchModel()


@pytest.fixture
def fake_state(
    arch_fragment_a, arch_fragment_b, arch_fragment_c,
    fake_batch, fake_quality_weights,
) -> dict:
    """Minimal RAAState for judge tests with 3 fragment outputs."""
    return {
        "batch_outputs": {
            0: [arch_fragment_a, arch_fragment_b, arch_fragment_c],
        },
        "batch_cursor": 0,
        "batch_queue": [fake_batch],
        "quality_weights": fake_quality_weights,
        "running_arch_model": ArchModel(),
        "open_questions": [],
        "incoherent_batches": [],
    }


@pytest.fixture
def fake_config(fake_llm_judge) -> dict:
    """Runtime config with llm_judge in context."""
    return {"context": {LLM_JUDGE_KEY: fake_llm_judge}}


# =============================================================================
# T006 — judge_batch reads llm_judge from config["context"]
# =============================================================================


class TestLLMJudgeContext:
    """Tests that judge_batch reads llm_judge from config context, not state."""

    def test_reads_llm_judge_from_config(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)
        assert "batch_cursor" in result
        assert result["batch_cursor"] == 1

    def test_raises_when_config_is_none(self, fake_state):
        with pytest.raises(RuntimeError, match="Required LLM context key"):
            judge_batch(fake_state, None)

    def test_raises_when_context_missing_key(self, fake_state):
        with pytest.raises(RuntimeError, match="Required LLM context key"):
            judge_batch(fake_state, {"context": {}})

    def test_raises_when_llm_judge_is_none(self, fake_state):
        with pytest.raises(RuntimeError, match="Required LLM context key"):
            judge_batch(fake_state, {"context": {LLM_JUDGE_KEY: None}})

    def test_never_reads_llm_from_state(self, fake_config):
        """judge_batch must never look for an LLM in state dict."""
        state_with_llm_in_state = {
            "batch_outputs": {0: []},
            "batch_cursor": 0,
            "batch_queue": [{"batch_id": 0, "requirements": [], "reduced_confidence": False}],
            "quality_weights": {},
            "running_arch_model": ArchModel(),
            "open_questions": [],
            "llm_judge": MagicMock(),  # Should be ignored
        }
        # This should return early (no fragments), proving it didn't try
        # to use the state llm_judge
        result = judge_batch(state_with_llm_in_state, fake_config)
        assert result["batch_cursor"] == 1


# =============================================================================
# T007 — SAAM scoring invokes llm_judge
# =============================================================================


class TestSAAMScoring:
    """Tests for SAAM scoring pipeline."""

    def test_scoring_invokes_llm_judge(self, fake_llm_judge, fake_batch,
                                        fake_quality_weights, arch_fragment_a,
                                        arch_fragment_b, arch_fragment_c):
        fragments = [arch_fragment_a, arch_fragment_b, arch_fragment_c]
        names = ["raa_a", "raa_b", "raa_c"]

        scores = _score_fragments(
            fake_llm_judge, fake_batch, fake_quality_weights,
            fragments, names, reduced_confidence=False,
        )

        fake_llm_judge.invoke.assert_called_once()
        call_args = fake_llm_judge.invoke.call_args[0][0]
        assert "R1" in call_args
        assert "R2" in call_args
        assert "security" in call_args
        assert "System A" in call_args
        assert len(scores) == 3

    def test_scoring_includes_quality_weights(self, fake_llm_judge, fake_batch,
                                               fake_quality_weights, arch_fragment_a):
        _score_fragments(
            fake_llm_judge, fake_batch, fake_quality_weights,
            [arch_fragment_a], ["raa_a"], reduced_confidence=False,
        )
        call_args = fake_llm_judge.invoke.call_args[0][0]
        assert '"security"' in call_args
        assert '"performance"' in call_args

    def test_scoring_includes_batch_requirements(self, fake_llm_judge, fake_batch,
                                                   fake_quality_weights, arch_fragment_a):
        _score_fragments(
            fake_llm_judge, fake_batch, fake_quality_weights,
            [arch_fragment_a], ["raa_a"], reduced_confidence=False,
        )
        call_args = fake_llm_judge.invoke.call_args[0][0]
        assert "authenticate users" in call_args
        assert "process payments" in call_args


# =============================================================================
# T008 — Reduced-confidence scoring multiplier
# =============================================================================


class TestReducedConfidence:
    """Tests for 0.5x multiplier on reduced-confidence batches."""

    def test_applies_multiplier(self, fake_llm_judge, fake_reduced_confidence_batch,
                                  fake_quality_weights, arch_fragment_a):
        fake_llm_judge.invoke.return_value = {
            "scores": [{
                "source_fragment": "raa_a",
                "base_score": 8.0,
                "covered_entity_ids": ["sys_a"],
                "covered_relationship_keys": [],
            }]
        }

        scores = _score_fragments(
            fake_llm_judge, fake_reduced_confidence_batch, fake_quality_weights,
            [arch_fragment_a], ["raa_a"], reduced_confidence=True,
        )

        assert scores[0]["base_score"] == 8.0
        assert scores[0]["weighted_score"] == 4.0
        assert scores[0]["reduced_confidence"] is True

    def test_no_multiplier_for_normal_batch(self, fake_llm_judge, fake_batch,
                                              fake_quality_weights, arch_fragment_a):
        fake_llm_judge.invoke.return_value = {
            "scores": [{
                "source_fragment": "raa_a",
                "base_score": 8.0,
                "covered_entity_ids": ["sys_a"],
                "covered_relationship_keys": [],
            }]
        }

        scores = _score_fragments(
            fake_llm_judge, fake_batch, fake_quality_weights,
            [arch_fragment_a], ["raa_a"], reduced_confidence=False,
        )

        assert scores[0]["base_score"] == 8.0
        assert scores[0]["weighted_score"] == 8.0
        assert scores[0]["reduced_confidence"] is False


# =============================================================================
# T009 — Primary selection by weighted_score
# =============================================================================


class TestPrimarySelection:
    """Tests for deterministic primary fragment selection."""

    def test_selects_highest_weighted_score(self):
        scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_a", base_score=5.0, weighted_score=5.0,
                       covered_entity_ids=[], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                       covered_entity_ids=[], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_c", base_score=3.0, weighted_score=3.0,
                       covered_entity_ids=[], covered_relationship_keys=[],
                       reduced_confidence=False),
        ]
        frag_a = ArchFragment(systems=[ArchSystem(id="a", label="A", description="",
                                                   source_fragment="raa_a")])
        frag_b = ArchFragment(systems=[ArchSystem(id="b", label="B", description="",
                                                   source_fragment="raa_b")])
        frag_c = ArchFragment(systems=[ArchSystem(id="c", label="C", description="",
                                                   source_fragment="raa_c")])
        fragments = [frag_a, frag_b, frag_c]
        names = ["raa_a", "raa_b", "raa_c"]

        idx, primary, name = _select_primary(scores, fragments, names)

        assert idx == 1
        assert name == "raa_b"
        assert primary.systems[0].id == "b"

    def test_tie_breaks_by_fragment_order(self):
        """Ties resolved deterministically: raa_a > raa_b > raa_c."""
        scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_c", base_score=7.0, weighted_score=7.0,
                       covered_entity_ids=[], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_b", base_score=7.0, weighted_score=7.0,
                       covered_entity_ids=[], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_a", base_score=7.0, weighted_score=7.0,
                       covered_entity_ids=[], covered_relationship_keys=[],
                       reduced_confidence=False),
        ]
        frag_a = ArchFragment(systems=[ArchSystem(id="a", label="A", description="",
                                                   source_fragment="raa_a")])
        frag_b = ArchFragment(systems=[ArchSystem(id="b", label="B", description="",
                                                   source_fragment="raa_b")])
        frag_c = ArchFragment(systems=[ArchSystem(id="c", label="C", description="",
                                                   source_fragment="raa_c")])
        fragments = [frag_c, frag_b, frag_a]
        names = ["raa_c", "raa_b", "raa_a"]

        idx, _, name = _select_primary(scores, fragments, names)

        # raa_a has lowest tie-break value (0), so it should win
        assert name == "raa_a"


# =============================================================================
# T010 — Entity deduplication
# =============================================================================


class TestEntityDeduplication:
    """Tests for merging entities with deduplication."""

    def test_merges_same_id_keeps_longest_description(self):
        primary = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="System A", description="Short",
                                source_fragment="raa_a")],
        )
        residual = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="System A",
                                description="A much longer and more detailed description",
                                source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["sys_a"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert len(result.systems) == 1
        assert result.systems[0].description == "A much longer and more detailed description"

    def test_keeps_available_technology_on_containers(self):
        primary = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="Test",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_a")],
        )
        residual = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="Test",
                                       parent_system_id="sys_a",
                                       technology="Kubernetes",
                                       source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["cont_a"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert result.containers[0].technology == "Kubernetes"

    def test_adds_new_ids_from_residual(self):
        primary = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="A", description="Primary",
                                source_fragment="raa_a")],
        )
        residual = ArchFragment(
            systems=[ArchSystem(id="sys_b", label="B", description="New system",
                                source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["sys_b"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert len(result.systems) == 2
        ids = {s.id for s in result.systems}
        assert "sys_a" in ids
        assert "sys_b" in ids

    def test_deduplicates_persons_by_id(self):
        primary = ArchFragment(
            persons=[ArchPerson(id="user_1", label="User", description="Short desc",
                                source_fragment="raa_a")],
        )
        residual = ArchFragment(
            persons=[ArchPerson(id="user_1", label="User", description="Longer description",
                                source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["user_1"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert len(result.persons) == 1
        assert result.persons[0].description == "Longer description"

    def test_deduplicates_external_systems_by_id(self):
        primary = ArchFragment(
            external_systems=[ArchExternalSystem(id="ext_1", label="Ext", description="Short",
                                                  source_fragment="raa_a")],
        )
        residual = ArchFragment(
            external_systems=[ArchExternalSystem(id="ext_1", label="Ext",
                                                  description="Longer external description",
                                                  technology="REST",
                                                  source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["ext_1"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert len(result.external_systems) == 1
        assert result.external_systems[0].description == "Longer external description"
        assert result.external_systems[0].technology == "REST"


# =============================================================================
# T011 — Hierarchy conflict detection
# =============================================================================


class TestHierarchyConflict:
    """Tests for hierarchy conflict detection during entity deduplication."""

    def test_container_parent_system_id_conflict(self):
        primary = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="Test",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_a")],
        )
        residual = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="Test",
                                       parent_system_id="sys_other",
                                       source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["cont_a"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert len(open_questions) == 1
        assert open_questions[0].type == "hierarchy_conflict"
        assert open_questions[0].entity_id == "cont_a"

    def test_component_parent_container_id_conflict(self):
        primary = ArchFragment(
            components=[ArchComponent(id="comp_a", label="C", description="Test",
                                       parent_container_id="cont_a",
                                       source_fragment="raa_a")],
        )
        residual = ArchFragment(
            components=[ArchComponent(id="comp_a", label="C", description="Test",
                                       parent_container_id="cont_other",
                                       source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["comp_a"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert len(open_questions) == 1
        assert open_questions[0].type == "hierarchy_conflict"
        assert open_questions[0].entity_id == "comp_a"

    def test_no_conflict_when_same_parent(self):
        primary = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="Test",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_a")],
        )
        residual = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="Longer text",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_b")],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=["cont_a"], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_entities(primary, [(residual, "raa_b", score)], open_questions)

        assert len(open_questions) == 0
        assert len(result.containers) == 1


# =============================================================================
# T012 — Relationship deduplication and scope conflicts
# =============================================================================


class TestRelationshipDeduplication:
    """Tests for relationship deduplication and scope conflict detection."""

    def test_deduplicates_by_key(self):
        merged = ArchFragment(
            relationships=[
                ArchRelationship(source_id="a", target_id="b", interaction_type="uses",
                                 technology="HTTP", diagram_scope="context",
                                 source_fragment="raa_a"),
            ],
        )
        residual = ArchFragment(
            relationships=[
                ArchRelationship(source_id="a", target_id="b", interaction_type="uses",
                                 technology="gRPC", diagram_scope="context",
                                 source_fragment="raa_b"),
            ],
        )
        score_a = JudgeScore(source_fragment="raa_a", base_score=5.0, weighted_score=5.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        score_b = JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        all_scores = [score_a, score_b]
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_relationships(
            merged, [(residual, "raa_b", score_b)], open_questions, all_scores,
        )

        # Should still have 1 relationship (deduplicated)
        assert len(result.relationships) == 1
        # Higher-scored fragment's technology should win
        assert result.relationships[0].technology == "gRPC"

    def test_prefers_lower_scored_when_existing_higher(self):
        merged = ArchFragment(
            relationships=[
                ArchRelationship(source_id="a", target_id="b", interaction_type="uses",
                                 technology="gRPC", diagram_scope="context",
                                 source_fragment="raa_b"),
            ],
        )
        residual = ArchFragment(
            relationships=[
                ArchRelationship(source_id="a", target_id="b", interaction_type="uses",
                                 technology="HTTP", diagram_scope="context",
                                 source_fragment="raa_a"),
            ],
        )
        score_a = JudgeScore(source_fragment="raa_a", base_score=5.0, weighted_score=5.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        score_b = JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        all_scores = [score_a, score_b]
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_relationships(
            merged, [(residual, "raa_a", score_a)], open_questions, all_scores,
        )

        # Existing (raa_b, higher scored) should keep its technology
        assert len(result.relationships) == 1
        assert result.relationships[0].technology == "gRPC"

    def test_adds_new_relationship_keys(self):
        merged = ArchFragment(
            relationships=[
                ArchRelationship(source_id="a", target_id="b", interaction_type="uses",
                                 technology="HTTP", diagram_scope="context",
                                 source_fragment="raa_a"),
            ],
        )
        residual = ArchFragment(
            relationships=[
                ArchRelationship(source_id="c", target_id="d", interaction_type="calls",
                                 technology="gRPC", diagram_scope="context",
                                 source_fragment="raa_b"),
            ],
        )
        score = JudgeScore(source_fragment="raa_b", base_score=5.0, weighted_score=5.0,
                           covered_entity_ids=[], covered_relationship_keys=[],
                           reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_relationships(
            merged, [(residual, "raa_b", score)], open_questions, [score],
        )

        assert len(result.relationships) == 2

    def test_scope_conflict_recorded(self):
        merged = ArchFragment(
            systems=[ArchSystem(id="a", label="A", description="", source_fragment="raa_a")],
            relationships=[
                ArchRelationship(source_id="a", target_id="b", interaction_type="calls",
                                 technology="gRPC", diagram_scope="context",
                                 source_fragment="raa_b"),
            ],
        )
        residual = ArchFragment(
            relationships=[
                ArchRelationship(source_id="a", target_id="b", interaction_type="calls",
                                 technology="gRPC", diagram_scope="container",
                                 source_fragment="raa_a"),
            ],
        )
        score_a = JudgeScore(source_fragment="raa_a", base_score=5.0, weighted_score=5.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        score_b = JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        all_scores = [score_a, score_b]
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_relationships(
            merged, [(residual, "raa_a", score_a)], open_questions, all_scores,
        )

        # Should have scope_conflict recorded
        scope_conflicts = [oq for oq in open_questions if oq.type == "scope_conflict"]
        assert len(scope_conflicts) == 1


# =============================================================================
# T013 — Scope resolution chooses endpoint-consistent scope
# =============================================================================


class TestScopeResolution:
    """Tests for endpoint-type-based scope resolution."""

    def test_system_to_system_is_context(self):
        assert _resolve_scope("system", "system") == "context"

    def test_person_to_system_is_context(self):
        assert _resolve_scope("person", "system") == "context"

    def test_container_to_container_is_container(self):
        assert _resolve_scope("container", "container") == "container"

    def test_component_to_component_is_component(self):
        assert _resolve_scope("component", "component") == "component"

    def test_system_to_container_defaults_context(self):
        assert _resolve_scope("system", "container") == "context"

    def test_scope_resolution_during_merge(self):
        """Scope conflict resolves to endpoint-consistent scope."""
        merged = ArchFragment(
            containers=[
                ArchContainer(id="cont_a", label="C", description="",
                              parent_system_id="sys", source_fragment="raa_b"),
                ArchContainer(id="cont_b", label="C2", description="",
                              parent_system_id="sys", source_fragment="raa_b"),
            ],
            relationships=[
                ArchRelationship(source_id="cont_a", target_id="cont_b",
                                 interaction_type="calls", technology="gRPC",
                                 diagram_scope="context",  # wrong scope
                                 source_fragment="raa_b"),
            ],
        )
        residual = ArchFragment(
            containers=[
                ArchContainer(id="cont_a", label="C", description="",
                              parent_system_id="sys", source_fragment="raa_a"),
                ArchContainer(id="cont_b", label="C2", description="",
                              parent_system_id="sys", source_fragment="raa_a"),
            ],
            relationships=[
                ArchRelationship(source_id="cont_a", target_id="cont_b",
                                 interaction_type="calls", technology="gRPC",
                                 diagram_scope="container",  # correct scope
                                 source_fragment="raa_a"),
            ],
        )
        score_a = JudgeScore(source_fragment="raa_a", base_score=5.0, weighted_score=5.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        score_b = JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                             covered_entity_ids=[], covered_relationship_keys=[],
                             reduced_confidence=False)
        all_scores = [score_a, score_b]
        open_questions: list[OpenQuestion] = []

        result = _deduplicate_relationships(
            merged, [(residual, "raa_a", score_a)], open_questions, all_scores,
        )

        # Scope should be resolved to "container" (endpoint-consistent)
        assert result.relationships[0].diagram_scope == "container"

        scope_conflicts = [oq for oq in open_questions if oq.type == "scope_conflict"]
        assert len(scope_conflicts) == 1


# =============================================================================
# T014 — Residual scan with coverage metadata
# =============================================================================


class TestResidualCoverageScan:
    """Tests for coverage union during residual scan."""

    def test_carries_forward_covered_entities(self):
        primary = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="A", description="Primary",
                                source_fragment="raa_b")],
        )
        residual = ArchFragment(
            systems=[ArchSystem(id="sys_c", label="C", description="Tertiary",
                                source_fragment="raa_c")],
        )
        all_scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                       covered_entity_ids=["sys_a"], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                       covered_entity_ids=["sys_c"], covered_relationship_keys=[],
                       reduced_confidence=False),
        ]
        res_score = JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                               covered_entity_ids=["sys_c"], covered_relationship_keys=[],
                               reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _coverage_union(primary, [(residual, "raa_c", res_score)],
                                 all_scores, open_questions)

        assert len(result.systems) == 2
        ids = {s.id for s in result.systems}
        assert "sys_a" in ids
        assert "sys_c" in ids

    def test_skips_entities_not_in_coverage(self):
        primary = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="A", description="Primary",
                                source_fragment="raa_b")],
        )
        residual = ArchFragment(
            systems=[ArchSystem(id="sys_c", label="C", description="Tertiary",
                                source_fragment="raa_c")],
        )
        all_scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                       covered_entity_ids=["sys_a"], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                       covered_entity_ids=[],  # sys_c NOT covered
                       covered_relationship_keys=[],
                       reduced_confidence=False),
        ]
        res_score = JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                               covered_entity_ids=[], covered_relationship_keys=[],
                               reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _coverage_union(primary, [(residual, "raa_c", res_score)],
                                 all_scores, open_questions)

        # sys_c should NOT be carried forward (not in coverage)
        assert len(result.systems) == 1
        assert result.systems[0].id == "sys_a"

    def test_carries_forward_covered_relationships(self):
        primary = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="A", description="",
                                source_fragment="raa_b")],
            relationships=[
                ArchRelationship(source_id="user_1", target_id="sys_a",
                                 interaction_type="uses", technology="HTTPS",
                                 diagram_scope="context", source_fragment="raa_b"),
            ],
        )
        residual = ArchFragment(
            systems=[ArchSystem(id="sys_c", label="C", description="",
                                source_fragment="raa_c")],
            relationships=[
                ArchRelationship(source_id="sys_a", target_id="sys_c",
                                 interaction_type="calls", technology="gRPC",
                                 diagram_scope="context", source_fragment="raa_c"),
            ],
        )
        all_scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                       covered_entity_ids=["sys_a"],
                       covered_relationship_keys=["user_1->sys_a:uses"],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                       covered_entity_ids=["sys_c"],
                       covered_relationship_keys=["sys_a->sys_c:calls"],
                       reduced_confidence=False),
        ]
        res_score = JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                               covered_entity_ids=["sys_c"],
                               covered_relationship_keys=["sys_a->sys_c:calls"],
                               reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _coverage_union(primary, [(residual, "raa_c", res_score)],
                                 all_scores, open_questions)

        assert len(result.relationships) == 2


# =============================================================================
# T015 — Orphan prevention during coverage union
# =============================================================================


class TestOrphanPrevention:
    """Tests for orphan rejection and coverage_gap recording."""

    def test_orphan_container_rejected(self):
        primary = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="A", description="",
                                source_fragment="raa_b")],
        )
        residual = ArchFragment(
            containers=[ArchContainer(id="cont_orphan", label="Orphan",
                                       description="No parent",
                                       parent_system_id="sys_nonexistent",
                                       source_fragment="raa_c")],
        )
        all_scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                       covered_entity_ids=["sys_a"], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                       covered_entity_ids=["cont_orphan"], covered_relationship_keys=[],
                       reduced_confidence=False),
        ]
        res_score = JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                               covered_entity_ids=["cont_orphan"],
                               covered_relationship_keys=[],
                               reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _coverage_union(primary, [(residual, "raa_c", res_score)],
                                 all_scores, open_questions)

        # Orphan should NOT be added
        assert len(result.containers) == 0

        # coverage_gap should be recorded
        coverage_gaps = [oq for oq in open_questions if oq.type == "coverage_gap"]
        assert len(coverage_gaps) == 1
        assert coverage_gaps[0].entity_id == "cont_orphan"

    def test_orphan_component_rejected(self):
        primary = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_b")],
        )
        residual = ArchFragment(
            components=[ArchComponent(id="comp_orphan", label="Orphan",
                                       description="No parent",
                                       parent_container_id="cont_nonexistent",
                                       source_fragment="raa_c")],
        )
        all_scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                       covered_entity_ids=["cont_a"], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                       covered_entity_ids=["comp_orphan"], covered_relationship_keys=[],
                       reduced_confidence=False),
        ]
        res_score = JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                               covered_entity_ids=["comp_orphan"],
                               covered_relationship_keys=[],
                               reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _coverage_union(primary, [(residual, "raa_c", res_score)],
                                 all_scores, open_questions)

        # Orphan should NOT be added
        assert len(result.components) == 0

        # coverage_gap should be recorded
        coverage_gaps = [oq for oq in open_questions if oq.type == "coverage_gap"]
        assert len(coverage_gaps) == 1
        assert coverage_gaps[0].entity_id == "comp_orphan"

    def test_non_orphan_adopted(self):
        """Container with resolvable parent in running_model should be adopted."""
        primary = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="A", description="",
                                source_fragment="raa_b")],
        )
        residual = ArchFragment(
            containers=[ArchContainer(id="cont_ok", label="OK",
                                       description="Has parent",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_c")],
        )
        all_scores: list[JudgeScore] = [
            JudgeScore(source_fragment="raa_b", base_score=9.0, weighted_score=9.0,
                       covered_entity_ids=["sys_a"], covered_relationship_keys=[],
                       reduced_confidence=False),
            JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                       covered_entity_ids=["cont_ok"], covered_relationship_keys=[],
                       reduced_confidence=False),
        ]
        res_score = JudgeScore(source_fragment="raa_c", base_score=6.0, weighted_score=6.0,
                               covered_entity_ids=["cont_ok"],
                               covered_relationship_keys=[],
                               reduced_confidence=False)
        open_questions: list[OpenQuestion] = []

        result = _coverage_union(primary, [(residual, "raa_c", res_score)],
                                 all_scores, open_questions)

        assert len(result.containers) == 1
        assert result.containers[0].id == "cont_ok"
        assert len(open_questions) == 0


# =============================================================================
# T016 — Tree assembly
# =============================================================================


class TestTreeAssembly:
    """Tests for hierarchical tree assembly."""

    def test_nests_containers_under_systems(self):
        fragment = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="System A", description="",
                                source_fragment="raa_a")],
            containers=[ArchContainer(id="cont_a", label="Container A", description="",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_a")],
        )
        result = _assemble_tree(fragment)
        assert len(result.systems) == 1
        assert len(result.systems[0].containers) == 1
        assert result.systems[0].containers[0].id == "cont_a"

    def test_nests_components_under_containers(self):
        fragment = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="Container A", description="",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_a")],
            components=[ArchComponent(id="comp_a", label="Component A", description="",
                                       parent_container_id="cont_a",
                                       source_fragment="raa_a")],
        )
        result = _assemble_tree(fragment)
        assert len(result.containers) == 1
        assert len(result.containers[0].components) == 1
        assert result.containers[0].components[0].id == "comp_a"

    def test_distributes_context_relationships_to_systems(self):
        fragment = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="A", description="",
                                source_fragment="raa_a")],
            relationships=[
                ArchRelationship(source_id="sys_a", target_id="sys_b",
                                 interaction_type="calls", technology="gRPC",
                                 diagram_scope="context", source_fragment="raa_a"),
            ],
        )
        result = _assemble_tree(fragment)
        assert len(result.systems[0].context_relationships) == 1

    def test_distributes_container_relationships_to_containers(self):
        fragment = ArchFragment(
            containers=[ArchContainer(id="cont_a", label="C", description="",
                                       parent_system_id="sys_a",
                                       source_fragment="raa_a")],
            relationships=[
                ArchRelationship(source_id="cont_a", target_id="cont_b",
                                 interaction_type="calls", technology="gRPC",
                                 diagram_scope="container", source_fragment="raa_a"),
            ],
        )
        result = _assemble_tree(fragment)
        assert len(result.containers[0].container_relationships) == 1

    def test_distributes_component_relationships_to_components(self):
        fragment = ArchFragment(
            components=[ArchComponent(id="comp_a", label="C", description="",
                                       parent_container_id="cont_a",
                                       source_fragment="raa_a")],
            relationships=[
                ArchRelationship(source_id="comp_a", target_id="comp_b",
                                 interaction_type="calls", technology="gRPC",
                                 diagram_scope="component", source_fragment="raa_a"),
            ],
        )
        result = _assemble_tree(fragment)
        assert len(result.components[0].component_relationships) == 1

    def test_leaves_persons_and_ext_systems_flat(self):
        fragment = ArchFragment(
            persons=[ArchPerson(id="user_1", label="User", description="",
                                source_fragment="raa_a")],
            external_systems=[ArchExternalSystem(id="ext_1", label="Ext", description="",
                                                  source_fragment="raa_a")],
        )
        result = _assemble_tree(fragment)
        assert len(result.persons) == 1
        assert len(result.external_systems) == 1


# =============================================================================
# T017 — Consistency checking against running_arch_model
# =============================================================================


class TestRunningModelConsistency:
    """Tests for consistency checking when updating running model."""

    def test_merges_without_duplicating(self):
        running = ArchModel(
            systems=[ArchSystem(id="sys_a", label="System A", description="Existing",
                                source_fragment="raa_a")],
        )
        contribution = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="System A",
                                description="Updated description",
                                source_fragment="raa_b")],
        )
        open_questions: list[OpenQuestion] = []

        result = _update_running_model(running, contribution, open_questions)

        assert len(result.systems) == 1
        assert result.systems[0].description == "Updated description"

    def test_adds_new_systems(self):
        running = ArchModel(
            systems=[ArchSystem(id="sys_a", label="System A", description="",
                                source_fragment="raa_a")],
        )
        contribution = ArchFragment(
            systems=[ArchSystem(id="sys_b", label="System B", description="New",
                                source_fragment="raa_b")],
        )
        open_questions: list[OpenQuestion] = []

        result = _update_running_model(running, contribution, open_questions)

        assert len(result.systems) == 2

    def test_preserves_unrelated_branches(self):
        running = ArchModel(
            systems=[
                ArchSystem(id="sys_a", label="System A", description="Existing",
                           source_fragment="raa_a"),
            ],
            persons=[ArchPerson(id="user_1", label="User", description="Existing user",
                                source_fragment="raa_a")],
        )
        contribution = ArchFragment(
            systems=[ArchSystem(id="sys_b", label="System B", description="New",
                                source_fragment="raa_b")],
        )
        open_questions: list[OpenQuestion] = []

        result = _update_running_model(running, contribution, open_questions)

        assert len(result.systems) == 2
        assert len(result.persons) == 1
        assert result.persons[0].id == "user_1"

    def test_merges_nested_containers(self):
        """Containers inside assembled systems should merge recursively."""
        running = ArchModel(
            systems=[ArchSystem(id="sys_a", label="System A", description="",
                                source_fragment="raa_a",
                                containers=[
                                    ArchContainer(id="cont_a", label="C", description="Existing",
                                                  parent_system_id="sys_a",
                                                  source_fragment="raa_a"),
                                ])],
        )
        contribution = ArchFragment(
            systems=[ArchSystem(id="sys_a", label="System A", description="",
                                source_fragment="raa_b",
                                containers=[
                                    ArchContainer(id="cont_a", label="C",
                                                  description="Updated container description",
                                                  parent_system_id="sys_a",
                                                  source_fragment="raa_b"),
                                    ArchContainer(id="cont_b", label="C2", description="New",
                                                  parent_system_id="sys_a",
                                                  source_fragment="raa_b"),
                                ])],
        )
        open_questions: list[OpenQuestion] = []

        result = _update_running_model(running, contribution, open_questions)

        assert len(result.systems) == 1
        assert len(result.systems[0].containers) == 2


# =============================================================================
# T018 — Node output structure
# =============================================================================


class TestNodeOutput:
    """Tests for judge_batch output structure."""

    def test_writes_best_batch_output(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)

        assert "best_batch_output" in result
        assert 0 in result["best_batch_output"]
        assert isinstance(result["best_batch_output"][0], ArchFragment)

    def test_updates_running_arch_model(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)

        assert "running_arch_model" in result
        assert isinstance(result["running_arch_model"], ArchModel)

    def test_appends_open_questions(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)

        assert "open_questions" in result
        assert isinstance(result["open_questions"], list)

    def test_advances_batch_cursor(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)

        assert result["batch_cursor"] == 1

    def test_handles_empty_fragments(self, fake_config):
        """Empty fragments list should still advance cursor."""
        state = {
            "batch_outputs": {0: []},
            "batch_cursor": 0,
            "batch_queue": [{"batch_id": 0, "requirements": [], "reduced_confidence": False}],
            "quality_weights": {},
            "running_arch_model": ArchModel(),
            "open_questions": [],
        }
        result = judge_batch(state, fake_config)
        assert result["batch_cursor"] == 1

    def test_best_fragment_has_entities(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)
        best = result["best_batch_output"][0]

        # Should have entities from the merge
        assert len(best.systems) > 0


# =============================================================================
# T019 — Output excludes LLM objects
# =============================================================================


class TestOutputExcludesLLM:
    """Tests that judge_batch output never includes LLM objects."""

    def test_excludes_llm_judge(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)

        for key, value in result.items():
            assert not hasattr(value, "invoke"), f"Key '{key}' has .invoke attribute"
            if isinstance(value, dict):
                for dk, dv in value.items():
                    assert not hasattr(dv, "invoke"), \
                        f"Nested key '{key}.{dk}' has .invoke attribute"

    def test_excludes_any_invoke_object_in_return(self, fake_state, fake_config):
        result = judge_batch(fake_state, fake_config)

        def check_no_invoke(obj, path="root"):
            if hasattr(obj, "invoke") and callable(obj.invoke):
                raise AssertionError(f"LLM object found at {path}")
            if isinstance(obj, dict):
                for k, v in obj.items():
                    check_no_invoke(v, f"{path}.{k}")
            if isinstance(obj, list):
                for i, v in enumerate(obj):
                    check_no_invoke(v, f"{path}[{i}]")

        check_no_invoke(result)

    def test_llm_not_in_state_after_judge(self, fake_state, fake_config):
        """Output must not include 'llm_judge', 'llm', or similar keys."""
        result = judge_batch(fake_state, fake_config)

        for key in result:
            assert "llm" not in key.lower(), f"LLM-related key '{key}' found in result"
