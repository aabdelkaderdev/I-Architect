"""Tests for Judge. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.subgraphs.judge_node import Judge


class _FakeStructuredLLM:
    def __init__(self, response):
        self._response = response

    async def ainvoke(self, _messages):
        if isinstance(self._response, Exception):
            raise self._response
        return self._response


class _FakeJudgeLLM:
    def __init__(self, response):
        self._response = response

    def with_structured_output(self, _schema, **_kwargs):
        return _FakeStructuredLLM(self._response)


class TestJudge:
    def test_develop_scenarios(self, sample_asrs, sample_non_asrs):
        """SAAM Step 1: all batch requirements become scenarios."""
        judge = Judge()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "asrs": sample_asrs,
            "non_asrs": sample_non_asrs,
        }
        scenarios = judge.develop_scenarios(batch)
        assert len(scenarios) == len(sample_asrs) + len(sample_non_asrs)

    def test_describe_architecture(self, sample_proposals):
        """SAAM Step 2: proposals from both subgraphs form the candidate architecture."""
        judge = Judge()
        asr = [p for p in sample_proposals if p["proposing_subgraph"] == "asr"]
        non_asr = [p for p in sample_proposals if p["proposing_subgraph"] == "non_asr"]
        arch = judge.describe_architecture(asr, non_asr)
        assert len(arch) == len(asr) + len(non_asr)

    def test_deduplicate(self):
        """Deduplicate merges same-named proposals, preserving ASR over non-ASR."""
        judge = Judge()
        judged = [
            {
                "proposal": {
                    "proposed_name": "AuthService",
                    "c4_level": "container",
                    "c4_type": "service",
                    "description": "Auth from ASR.",
                    "responsibilities": ["Validate"],
                    "source_requirements": ["REQ-001"],
                    "proposing_subgraph": "asr",
                    "justification": "ASR justification.",
                },
                "scenario_classification": "direct",
                "satisfied_requirements": ["REQ-001"],
                "conflicts_with": [],
            },
            {
                "proposal": {
                    "proposed_name": "AuthService",
                    "c4_level": "container",
                    "c4_type": "service",
                    "description": "Auth from non-ASR.",
                    "responsibilities": ["Validate", "Issue tokens"],
                    "source_requirements": ["REQ-010"],
                    "proposing_subgraph": "non_asr",
                    "justification": "Non-ASR justification.",
                },
                "scenario_classification": "direct",
                "satisfied_requirements": ["REQ-010"],
                "conflicts_with": [],
            },
        ]
        result = judge.deduplicate(judged, [])
        assert len(result) == 1
        # ASR proposal survives authority conflict
        assert result[0]["proposing_subgraph"] == "asr"
        # source_requirements merged
        assert "REQ-001" in result[0]["source_requirements"]
        assert "REQ-010" in result[0]["source_requirements"]

    def test_derive_relationships(self, sample_registry_snapshot):
        """Relationships are derived between actors, external systems, and internal services."""
        judge = Judge()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
        }
        proposals = [
            {
                "proposed_name": "EndUser",
                "c4_level": "system",
                "c4_type": "actor",
                "description": "End user.",
                "responsibilities": [],
                "source_requirements": ["REQ-010"],
                "proposing_subgraph": "non_asr",
                "justification": "User role.",
            },
            {
                "proposed_name": "ApiGateway",
                "c4_level": "container",
                "c4_type": "gateway",
                "description": "Routes requests.",
                "responsibilities": ["Route requests"],
                "source_requirements": ["REQ-001"],
                "proposing_subgraph": "asr",
                "justification": "Gateway pattern.",
            },
        ]
        rels = judge.derive_relationships(batch, proposals, sample_registry_snapshot)
        # Actor → internal service = "uses" relationship
        assert len(rels) >= 1
        assert rels[0]["label"] == "uses"

    def test_assemble_concern_descriptions(self, sample_proposals):
        """Concern batch output includes container_description with is_backbone=False."""
        judge = Judge()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "condition": "high traffic",
        }
        delta = {"new_entries": [], "enriched_ids": []}
        output = judge.assemble_descriptions(
            batch, sample_proposals, [], delta, [], [],
        )
        assert output["batch_type"] == "concern"
        assert "container_description" in output
        for c in output["container_description"]["containers"]:
            assert c["is_backbone"] is False

    def test_assemble_foundation_descriptions(self, sample_proposals):
        """Foundation batch output includes L1 and backbone with is_backbone=True."""
        judge = Judge()
        batch = {
            "batch_id": "foundation_batch",
            "batch_type": "foundation",
        }
        delta = {"new_entries": [], "enriched_ids": []}
        output = judge.assemble_descriptions(
            batch, sample_proposals, [], delta, [], [],
        )
        assert output["batch_type"] == "foundation"
        assert "system_context_description" in output
        assert "backbone_description" in output
        assert output["backbone_description"]["concern_id"] == "foundation"
        assert output["backbone_description"]["condition"] == "under any circumstances"
        for c in output["backbone_description"]["containers"]:
            assert c["is_backbone"] is True

    @pytest.mark.asyncio
    async def test_classification_preserves_trusted_proposal_provenance(self, sample_proposals):
        """Judge annotations must not replace ASR/Non-ASR proposal provenance."""
        corrupted_judged = [
            {
                "proposal": {
                    **sample_proposals[0],
                    "proposing_subgraph": "",
                },
                "scenario_classification": "direct",
                "satisfied_requirements": [],
                "conflicts_with": [],
            }
        ]
        judge = Judge()
        batch = {"batch_id": "concern_batch_1", "batch_type": "concern"}
        config = {
            "configurable": {
                "judge_llm": _FakeJudgeLLM({"classified": corrupted_judged})
            }
        }

        judged = await judge.classify_scenarios(batch, [sample_proposals[0]], config)

        assert judged[0]["proposal"] is sample_proposals[0]
        assert judged[0]["proposal"]["proposing_subgraph"] == "non_asr"

    @pytest.mark.asyncio
    async def test_coverage_preserves_trusted_proposal_provenance(self, sample_proposals):
        """Coverage can update annotations, but not immutable proposal fields."""
        base_judged = [
            {
                "proposal": sample_proposals[1],
                "scenario_classification": "indirect",
                "satisfied_requirements": [],
                "conflicts_with": [],
            }
        ]
        corrupted_judged = [
            {
                "proposal": {
                    **sample_proposals[1],
                    "proposing_subgraph": "",
                },
                "scenario_classification": "direct",
                "satisfied_requirements": ["REQ-001"],
                "conflicts_with": [],
            }
        ]
        judge = Judge()
        batch = {"batch_id": "concern_batch_1", "batch_type": "concern"}
        config = {
            "configurable": {
                "judge_llm": _FakeJudgeLLM(
                    {"judged": corrupted_judged, "coverage_gaps": []}
                )
            }
        }

        judged, gaps = await judge.evaluate_coverage(batch, base_judged, config)

        assert gaps == []
        assert judged[0]["proposal"] is sample_proposals[1]
        assert judged[0]["proposal"]["proposing_subgraph"] == "asr"
        assert judged[0]["satisfied_requirements"] == ["REQ-001"]

    @pytest.mark.asyncio
    async def test_interactions_preserves_trusted_proposal_provenance(self, sample_proposals):
        """Interaction output cannot corrupt proposal authority."""
        base_judged = [
            {
                "proposal": sample_proposals[2],
                "scenario_classification": "direct",
                "satisfied_requirements": ["REQ-002"],
                "conflicts_with": [],
            }
        ]
        corrupted_judged = [
            {
                "proposal": {
                    **sample_proposals[2],
                    "proposing_subgraph": "",
                },
                "scenario_classification": "direct",
                "satisfied_requirements": [],
                "conflicts_with": ["OtherDatabase"],
            }
        ]
        judge = Judge()
        batch = {"batch_id": "concern_batch_1", "batch_type": "concern"}
        config = {
            "configurable": {
                "judge_llm": _FakeJudgeLLM(
                    {"judged": corrupted_judged, "conflicts": []}
                )
            }
        }

        judged, conflicts = await judge.detect_interactions(batch, base_judged, config)

        assert conflicts == []
        assert judged[0]["proposal"] is sample_proposals[2]
        assert judged[0]["proposal"]["proposing_subgraph"] == "asr"
        assert judged[0]["satisfied_requirements"] == ["REQ-002"]
        assert judged[0]["conflicts_with"] == ["OtherDatabase"]

    @pytest.mark.asyncio
    async def test_coverage_validation_error_marks_coverage_unverified(self, sample_proposals):
        """Missing required structured fields should trigger fallback, not abort."""
        from pydantic import ValidationError

        from raa.schemas.structured_output import JudgeCoverageOutput

        base_judged = [
            {
                "proposal": sample_proposals[1],
                "scenario_classification": "direct",
                "satisfied_requirements": ["REQ-001"],
                "conflicts_with": [],
            }
        ]
        validation_error = None
        try:
            JudgeCoverageOutput()
        except ValidationError as exc:
            validation_error = exc

        assert validation_error is not None

        judge = Judge()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "asrs": [{"id": "REQ-001", "text": "Need auth."}],
            "non_asrs": [],
        }
        config = {
            "configurable": {
                "judge_llm": _FakeJudgeLLM(validation_error)
            }
        }

        judged, gaps = await judge.evaluate_coverage(batch, base_judged, config)

        assert judged == base_judged
        assert gaps == [
            {
                "requirement_id": "REQ-001",
                "requirement_text": "Need auth.",
                "batch_id": "concern_batch_1",
                "gap_reason": (
                    "Coverage evaluation failed; requirement coverage is unverified."
                ),
            }
        ]

    @pytest.mark.asyncio
    async def test_judge_matches_duplicate_names_by_proposal_ref(self):
        """Flattened Judge annotations use proposal_ref before duplicate names."""
        proposal_a = {
            "proposed_name": "AuthService",
            "c4_level": "container",
            "c4_type": "service",
            "description": "ASR auth.",
            "responsibilities": ["Authenticate"],
            "source_requirements": ["REQ-A"],
            "proposing_subgraph": "asr",
            "justification": "ASR.",
        }
        proposal_b = {
            **proposal_a,
            "description": "Non-ASR auth.",
            "source_requirements": ["REQ-B"],
            "proposing_subgraph": "non_asr",
            "justification": "Non-ASR.",
        }
        judge = Judge()
        batch = {"batch_id": "concern_batch_1", "batch_type": "concern"}
        config = {
            "configurable": {
                "judge_llm": _FakeJudgeLLM({
                    "classified": [
                        {
                            "proposal_ref": "P002",
                            "proposed_name": "AuthService",
                            "scenario_classification": "indirect",
                        },
                        {
                            "proposal_ref": "P001",
                            "proposed_name": "AuthService",
                            "scenario_classification": "direct",
                        },
                    ]
                })
            }
        }

        judged = await judge.classify_scenarios(batch, [proposal_a, proposal_b], config)

        assert judged[0]["proposal"] is proposal_a
        assert judged[0]["scenario_classification"] == "direct"
        assert judged[1]["proposal"] is proposal_b
        assert judged[1]["scenario_classification"] == "indirect"

    def test_actors_and_externals_excluded_from_l2_containers(self):
        """Concern L2 containers only include internal entities."""
        judge = Judge()
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "condition": "normal",
        }
        proposals = [
            {
                "proposed_name": "Officer",
                "c4_level": "container",
                "c4_type": "actor",
                "description": "Officer user.",
                "responsibilities": [],
                "source_requirements": ["REQ-A"],
                "proposing_subgraph": "non_asr",
                "justification": "User.",
            },
            {
                "proposed_name": "PartnerSystem",
                "c4_level": "container",
                "c4_type": "external",
                "description": "Partner system.",
                "responsibilities": [],
                "source_requirements": ["REQ-B"],
                "proposing_subgraph": "non_asr",
                "justification": "Integration.",
            },
            {
                "proposed_name": "ApiGateway",
                "c4_level": "container",
                "c4_type": "gateway",
                "description": "Gateway.",
                "responsibilities": ["Route"],
                "source_requirements": ["REQ-C"],
                "proposing_subgraph": "asr",
                "justification": "Ingress.",
            },
        ]

        output = judge.assemble_descriptions(
            batch, proposals, [], {"new_entries": [], "enriched_ids": []}, [], []
        )

        names = {
            container["name"]
            for container in output["container_description"]["containers"]
        }
        assert names == {"ApiGateway"}

    def test_l3_parent_container_assigned_by_requirement_overlap(self):
        """Components are grouped under a real parent container canonical_id."""
        judge = Judge()
        judge._registry.register({
            "canonical_id": "ENT-001",
            "canonical_name": "ApiService",
            "c4_level": "container",
            "c4_type": "service",
            "source_requirements": ["REQ-A"],
            "authority": "asr",
            "variants": {},
            "description": "API service.",
        })
        judge._registry.register({
            "canonical_id": "ENT-002",
            "canonical_name": "ApiControllerComponent",
            "c4_level": "component",
            "c4_type": "service",
            "source_requirements": ["REQ-A"],
            "authority": "asr",
            "variants": {},
            "description": "API controller.",
        })
        batch = {
            "batch_id": "concern_batch_1",
            "batch_type": "concern",
            "condition": "normal",
        }
        proposals = [
            {
                "proposed_name": "ApiService",
                "c4_level": "container",
                "c4_type": "service",
                "description": "API service.",
                "responsibilities": ["Serve API"],
                "source_requirements": ["REQ-A"],
                "proposing_subgraph": "asr",
                "justification": "API.",
            },
            {
                "proposed_name": "ApiControllerComponent",
                "c4_level": "component",
                "c4_type": "service",
                "description": "API controller.",
                "responsibilities": ["Handle requests"],
                "source_requirements": ["REQ-A"],
                "proposing_subgraph": "asr",
                "justification": "Controller.",
            },
        ]

        output = judge.assemble_descriptions(
            batch, proposals, [], {"new_entries": [], "enriched_ids": []}, [], []
        )

        l3 = output["component_descriptions"]
        assert len(l3) == 1
        assert l3[0]["parent_container_id"] == "ENT-001"
        assert l3[0]["source_requirements"] == ["REQ-A"]
