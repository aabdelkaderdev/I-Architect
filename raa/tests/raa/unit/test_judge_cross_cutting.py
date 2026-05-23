"""
Unit tests for cross-cutting concern promotion engine (Story 2.5).
"""
from __future__ import annotations

import pytest

from raa.judge.cross_cutting import (
    detect_cross_cutting_candidates,
    promote_cross_cutting_to_component,
    rewrite_relationships_for_promotion,
    promote_all_cross_cutting,
)
from raa.state.models import C4Entity


# ── Helpers ─────────────────────────────────────────────────────────────────


def _entity_dict(
    id="entity-1",
    name="Test Entity",
    description="Test description",
    c4_type="container",
    technology="",
    requirement_ids=None,
    metadata=None,
):
    return {
        "id": id,
        "name": name,
        "description": description,
        "c4_type": c4_type,
        "technology": technology,
        "parent_system_id": None,
        "parent_container_id": None,
        "requirement_ids": requirement_ids or [],
        "saam_score": 0.0,
        "metadata": metadata or {},
    }


def _rel_dict(source_id="a", target_id="b", description="uses", metadata=None):
    return {
        "id": f"rel-{source_id}-{target_id}",
        "source_id": source_id,
        "target_id": target_id,
        "description": description,
        "relationship_type": "uses",
        "diagram_scope": "",
        "metadata": metadata or {},
    }


# ── Detection ───────────────────────────────────────────────────────────────


class TestDetectCrossCuttingCandidates:
    def test_no_cross_cutting_candidates_returns_empty(self):
        model = {"entities": [], "relationships": [], "cross_cutting_candidates": []}
        result = detect_cross_cutting_candidates(model)
        assert result == []

    def test_no_matching_patterns_returns_empty(self):
        model = {
            "entities": [_entity_dict()],
            "relationships": [],
            "cross_cutting_candidates": ["unknown_pattern_xyz"],
        }
        result = detect_cross_cutting_candidates(model)
        assert result == []

    def test_detects_security_pattern(self):
        model = {
            "entities": [
                _entity_dict(
                    id="auth-svc",
                    name="Authentication Service",
                    description="Handles security and authentication",
                    requirement_ids=["R1", "R2"],
                )
            ],
            "relationships": [],
            "cross_cutting_candidates": ["security_component", "logging_service"],
        }
        result = detect_cross_cutting_candidates(model)
        patterns = {d["candidate_pattern"] for d in result}
        assert "security" in patterns
        assert "logging" in patterns

    def test_detects_pattern_from_entity_metadata(self):
        model = {
            "entities": [
                _entity_dict(
                    id="mon-svc",
                    name="Monitor",
                    description="Monitoring service",
                    metadata={"cross_cutting_candidates": ["monitoring", "logging"]},
                )
            ],
            "relationships": [],
            "cross_cutting_candidates": [],
        }
        result = detect_cross_cutting_candidates(model)
        patterns = {d["candidate_pattern"] for d in result}
        assert "monitoring" in patterns
        assert "logging" in patterns

    def test_deduplicates_same_pattern(self):
        model = {
            "entities": [_entity_dict()],
            "relationships": [],
            "cross_cutting_candidates": ["security_service", "security_check"],
        }
        result = detect_cross_cutting_candidates(model)
        assert len(result) == 1
        assert result[0]["candidate_pattern"] == "security"

    def test_collects_related_entity_ids(self):
        model = {
            "entities": [
                _entity_dict(id="auth-1", name="Auth Service", description="Handles authentication"),
                _entity_dict(id="unrelated", name="Data Store", description="Stores data"),
            ],
            "relationships": [],
            "cross_cutting_candidates": ["authentication_check"],
        }
        result = detect_cross_cutting_candidates(model)
        assert len(result) == 1
        assert "auth-1" in result[0]["related_entity_ids"]
        assert "unrelated" not in result[0]["related_entity_ids"]

    def test_collects_requirement_ids_from_related_entities(self):
        model = {
            "entities": [
                _entity_dict(id="auth-1", name="Auth", description="authentication", requirement_ids=["R1", "R2"]),
                _entity_dict(id="auth-2", name="Login", description="authentication", requirement_ids=["R2", "R3"]),
            ],
            "relationships": [],
            "cross_cutting_candidates": ["authentication"],
        }
        result = detect_cross_cutting_candidates(model)
        assert len(result) == 1
        assert set(result[0]["requirement_ids"]) == {"R1", "R2", "R3"}

    def test_matches_infra_keywords(self):
        model = {
            "entities": [_entity_dict(name="Every", description="all things")],
            "relationships": [],
            "cross_cutting_candidates": ["all_things", "every_service"],
        }
        result = detect_cross_cutting_candidates(model)
        patterns = {d["candidate_pattern"] for d in result}
        assert "all" in patterns
        assert "every" in patterns

    def test_entity_tech_matches_pattern(self):
        model = {
            "entities": [_entity_dict(id="s1", name="Svc", technology="security-library, caching-layer")],
            "relationships": [],
            "cross_cutting_candidates": ["security"],
        }
        result = detect_cross_cutting_candidates(model)
        assert len(result) == 1
        assert "s1" in result[0]["related_entity_ids"]


# ── Promotion ───────────────────────────────────────────────────────────────


class TestPromoteCrossCuttingToComponent:
    def test_creates_component_with_correct_c4_type(self):
        detection = {
            "candidate_pattern": "security",
            "related_entity_ids": ["auth-svc"],
            "requirement_ids": ["R1", "R2"],
        }
        model = {"entities": [], "relationships": []}
        promoted, affected = promote_cross_cutting_to_component(detection, model)
        assert promoted.c4_type == "component"
        assert promoted.id == "cc_security"
        assert promoted.name == "Security (Cross-Cutting)"
        assert set(promoted.requirement_ids) == {"R1", "R2"}

    def test_returns_affected_entity_ids(self):
        detection = {
            "candidate_pattern": "logging",
            "related_entity_ids": ["log-svc", "audit-svc"],
            "requirement_ids": [],
        }
        model = {"entities": [], "relationships": []}
        promoted, affected = promote_cross_cutting_to_component(detection, model)
        assert set(affected) == {"log-svc", "audit-svc"}

    def test_finds_parent_container(self):
        detection = {
            "candidate_pattern": "security",
            "related_entity_ids": [],
            "requirement_ids": [],
        }
        model = {
            "entities": [
                _entity_dict(id="api", name="API", c4_type="system"),
                _entity_dict(id="backend", name="Backend", description="security container", c4_type="container"),
            ],
            "relationships": [],
        }
        promoted, _ = promote_cross_cutting_to_component(detection, model)
        assert promoted.parent_container_id == "backend"

    def test_no_parent_container_when_none_match(self):
        detection = {
            "candidate_pattern": "monitoring",
            "related_entity_ids": [],
            "requirement_ids": [],
        }
        model = {
            "entities": [_entity_dict(id="api", name="API Gateway", c4_type="system")],
            "relationships": [],
        }
        promoted, _ = promote_cross_cutting_to_component(detection, model)
        assert promoted.parent_container_id is None


# ── Relationship Rewriting ──────────────────────────────────────────────────


class TestRewriteRelationshipsForPromotion:
    def test_rewrites_source_when_affected_and_mentions_pattern(self):
        rels = [
            _rel_dict(source_id="auth-svc", target_id="db", description="security check"),
            _rel_dict(source_id="auth-svc", target_id="cache", description="data access"),
        ]
        result = rewrite_relationships_for_promotion(
            rels, affected_entity_ids=["auth-svc"],
            promoted_component_id="cc_security", pattern="security",
        )
        assert result[0]["source_id"] == "cc_security"
        assert result[0]["target_id"] == "db"
        assert result[1]["source_id"] == "auth-svc"  # not rewritten — doesn't mention pattern

    def test_rewrites_target_when_affected_and_mentions_pattern(self):
        rels = [
            _rel_dict(source_id="client", target_id="auth-svc", description="authentication"),
        ]
        result = rewrite_relationships_for_promotion(
            rels, affected_entity_ids=["auth-svc"],
            promoted_component_id="cc_authentication", pattern="authentication",
        )
        assert result[0]["target_id"] == "cc_authentication"

    def test_no_rewrite_when_not_affected(self):
        rels = [
            _rel_dict(source_id="unrelated", target_id="db", description="security audit"),
        ]
        result = rewrite_relationships_for_promotion(
            rels, affected_entity_ids=["auth-svc"],
            promoted_component_id="cc_security", pattern="security",
        )
        assert result[0]["source_id"] == "unrelated"
        assert result[0]["target_id"] == "db"

    def test_no_rewrite_when_pattern_not_mentioned(self):
        rels = [
            _rel_dict(source_id="auth-svc", target_id="db", description="reads data"),
        ]
        result = rewrite_relationships_for_promotion(
            rels, affected_entity_ids=["auth-svc"],
            promoted_component_id="cc_security", pattern="security",
        )
        assert result[0]["source_id"] == "auth-svc"

    def test_pattern_in_metadata_triggers_rewrite(self):
        rels = [
            _rel_dict(source_id="auth-svc", target_id="db", description="uses",
                       metadata={"concern": "security_check"}),
        ]
        result = rewrite_relationships_for_promotion(
            rels, affected_entity_ids=["auth-svc"],
            promoted_component_id="cc_security", pattern="security",
        )
        assert result[0]["source_id"] == "cc_security"


# ── Full Pipeline ───────────────────────────────────────────────────────────


class TestPromoteAllCrossCutting:
    def test_no_candidates_returns_model_unchanged(self):
        model = {
            "entities": [_entity_dict()],
            "relationships": [_rel_dict()],
            "boundary_groups": [],
            "cross_cutting_candidates": [],
        }
        result, questions = promote_all_cross_cutting(model)
        assert len(result["entities"]) == 1
        assert len(result["relationships"]) == 1
        assert questions == []

    def test_promotes_detected_cross_cutting(self):
        model = {
            "entities": [
                _entity_dict(id="auth-svc", name="Auth Service",
                             description="Handles authentication and authorization",
                             requirement_ids=["R1", "R2"]),
            ],
            "relationships": [
                _rel_dict(source_id="auth-svc", target_id="db", description="authentication request"),
            ],
            "boundary_groups": [],
            "cross_cutting_candidates": ["authentication"],
        }
        result, questions = promote_all_cross_cutting(model)
        # Promoted component added
        entity_ids = {e["id"] for e in result["entities"]}
        assert "cc_authentication" in entity_ids
        # Relationship rewritten
        assert result["relationships"][0]["source_id"] == "cc_authentication"

    def test_multiple_cross_cutting_patterns(self):
        model = {
            "entities": [
                _entity_dict(id="svc-1", name="Security Service", description="security", requirement_ids=["R1"]),
                _entity_dict(id="svc-2", name="Log Service", description="logging", requirement_ids=["R2"]),
            ],
            "relationships": [],
            "boundary_groups": [],
            "cross_cutting_candidates": ["security", "logging"],
        }
        result, questions = promote_all_cross_cutting(model)
        entity_ids = {e["id"] for e in result["entities"]}
        assert "cc_security" in entity_ids
        assert "cc_logging" in entity_ids

    def test_removes_requirement_ids_from_affected_entities(self):
        model = {
            "entities": [
                _entity_dict(id="auth-svc", name="Auth", description="authentication",
                             requirement_ids=["R1", "R2"]),
            ],
            "relationships": [],
            "boundary_groups": [],
            "cross_cutting_candidates": ["authentication"],
        }
        result, _ = promote_all_cross_cutting(model)
        auth_entity = next(e for e in result["entities"] if e["id"] == "auth-svc")
        assert auth_entity["requirement_ids"] == []

    def test_open_question_when_no_parent_container(self):
        model = {
            "entities": [
                _entity_dict(id="svc", name="Service", description="security thing", c4_type="system"),
            ],
            "relationships": [],
            "boundary_groups": [],
            "cross_cutting_candidates": ["security"],
        }
        result, questions = promote_all_cross_cutting(model)
        assert len(questions) == 1
        assert questions[0]["source"] == "cross_cutting_promotion"
        assert "cc_security" in questions[0]["description"]

    def test_deterministic_same_input_same_output(self):
        model = {
            "entities": [
                _entity_dict(id="svc", name="Auth Service", description="security auth",
                             requirement_ids=["R1"]),
            ],
            "relationships": [_rel_dict(source_id="svc", target_id="db")],
            "boundary_groups": [],
            "cross_cutting_candidates": ["security"],
        }
        r1, q1 = promote_all_cross_cutting(model)
        r2, q2 = promote_all_cross_cutting(model)
        assert r1 == r2
        assert q1 == q2

    def test_entity_without_cross_cutting_is_unchanged(self):
        model = {
            "entities": [
                _entity_dict(id="svc-1", name="Auth Service", description="authentication", requirement_ids=["R1"]),
                _entity_dict(id="svc-2", name="Data Store", description="stores data", requirement_ids=["R2"]),
            ],
            "relationships": [],
            "boundary_groups": [],
            "cross_cutting_candidates": ["authentication"],
        }
        result, _ = promote_all_cross_cutting(model)
        data_entity = next(e for e in result["entities"] if e["id"] == "svc-2")
        assert data_entity["requirement_ids"] == ["R2"]
