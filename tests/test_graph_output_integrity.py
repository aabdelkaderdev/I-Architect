"""Round 3 output integrity regressions for final graph assembly."""

from __future__ import annotations

import pytest

from raa.graph import _assemble_output


def _entry(cid: str, name: str, c4_level: str, c4_type: str, reqs: list[str]) -> dict:
    return {
        "canonical_id": cid,
        "canonical_name": name,
        "c4_level": c4_level,
        "c4_type": c4_type,
        "source_requirements": reqs,
        "authority": "asr",
        "variants": {},
        "description": f"{name} description.",
    }


@pytest.mark.asyncio
async def test_l1_enriched_with_registry_externals_and_relationships():
    """Final L1 includes actors/externals found outside the foundation batch."""
    state = {
        "entity_registry_entries": [
            _entry("ENT-001", "ApiGateway", "container", "gateway", ["REQ-A"]),
            _entry("ENT-002", "Officer", "system", "actor", ["REQ-B"]),
            _entry("ENT-003", "PartnerSystem", "system", "external", ["REQ-C"]),
        ],
        "batch_outputs": [
            {
                "batch_id": "foundation_batch",
                "batch_type": "foundation",
                "registry_delta": {"new_entries": [], "enriched_ids": []},
                "coverage_gaps": [],
                "conflicts": [],
                "system_context_description": {
                    "system_name": "System",
                    "system_description": "System derived from requirements corpus.",
                    "system_boundary_description": "System boundary.",
                    "actors": [],
                    "external_systems": [],
                    "relationships": [],
                    "source_requirements": [],
                },
                "backbone_description": {
                    "concern_id": "foundation",
                    "condition": "under any circumstances",
                    "containers": [],
                    "relationships": [],
                    "source_requirements": [],
                },
            }
        ],
    }

    output = (await _assemble_output(state, {}))["raa_output"]
    l1 = output["l1_description"]

    assert [actor["name"] for actor in l1["actors"]] == ["Officer"]
    assert [external["name"] for external in l1["external_systems"]] == ["PartnerSystem"]
    assert set(l1["source_requirements"]) == {"REQ-B", "REQ-C"}
    assert ("ENT-002", "ENT-001", "uses") in {
        (rel["source_id"], rel["target_id"], rel["label"])
        for rel in l1["relationships"]
    }
    assert ("ENT-001", "ENT-003", "calls") in {
        (rel["source_id"], rel["target_id"], rel["label"])
        for rel in l1["relationships"]
    }


@pytest.mark.asyncio
async def test_l2_source_requirements_recomputed_after_backbone_merge():
    """Backbone container requirements are included in final concern L2."""
    state = {
        "entity_registry_entries": [
            _entry("ENT-001", "BackboneService", "container", "service", ["REQ-F"]),
            _entry("ENT-002", "ConcernService", "container", "service", ["REQ-C"]),
        ],
        "batch_outputs": [
            {
                "batch_id": "foundation_batch",
                "batch_type": "foundation",
                "registry_delta": {"new_entries": [], "enriched_ids": []},
                "coverage_gaps": [],
                "conflicts": [],
                "system_context_description": {
                    "system_name": "System",
                    "system_description": "System derived from requirements corpus.",
                    "system_boundary_description": "System boundary.",
                    "actors": [],
                    "external_systems": [],
                    "relationships": [],
                    "source_requirements": [],
                },
                "backbone_description": {
                    "concern_id": "foundation",
                    "condition": "under any circumstances",
                    "containers": [
                        {
                            "canonical_id": "ENT-001",
                            "name": "BackboneService",
                            "description": "Backbone.",
                            "responsibilities": ["Support"],
                            "is_backbone": True,
                            "source_requirements": ["REQ-F"],
                        }
                    ],
                    "relationships": [],
                    "source_requirements": ["REQ-F"],
                },
            },
            {
                "batch_id": "concern_batch_1",
                "batch_type": "concern",
                "registry_delta": {"new_entries": [], "enriched_ids": []},
                "coverage_gaps": [],
                "conflicts": [],
                "container_description": {
                    "concern_id": "concern_batch_1",
                    "condition": "high load",
                    "containers": [
                        {
                            "canonical_id": "ENT-002",
                            "name": "ConcernService",
                            "description": "Concern.",
                            "responsibilities": ["Handle concern"],
                            "is_backbone": False,
                            "source_requirements": ["REQ-C"],
                        }
                    ],
                    "relationships": [],
                    "source_requirements": ["REQ-C"],
                },
                "component_descriptions": [],
            },
        ],
    }

    output = (await _assemble_output(state, {}))["raa_output"]
    l2 = output["l2_descriptions"][0]

    assert [container["name"] for container in l2["containers"]] == [
        "BackboneService",
        "ConcernService",
    ]
    assert l2["source_requirements"] == ["REQ-C", "REQ-F"]
