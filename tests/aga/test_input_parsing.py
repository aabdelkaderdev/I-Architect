import pytest

from aga.nodes.input_parsing import input_parsing


@pytest.mark.asyncio
async def test_input_parsing_deduplicates_relationships_and_rejects_missing_endpoints():
    arch_model = {
        "status": "ok",
        "entities": [
            {
                "id": "system-a",
                "name": "System A",
                "description": "System",
                "c4_type": "system",
            },
            {
                "id": "person-a",
                "name": "Person A",
                "description": "Person",
                "c4_type": "person",
            },
        ],
        "relationships": [
            {
                "id": "r1",
                "source_id": "person-a",
                "target_id": "system-a",
                "description": "Uses",
                "relationship_type": "uses",
                "diagram_scope": "context",
            },
            {
                "id": "r1-duplicate",
                "source_id": "person-a",
                "target_id": "system-a",
                "description": "Uses",
                "relationship_type": "uses",
                "diagram_scope": "context",
            },
        ],
        "boundary_groups": [{"id": "b1", "entity_ids": ["system-a"]}],
        "cross_cutting_candidates": [],
        "assumption_flags": ["assumed-link"],
    }

    updates = await input_parsing({"arch_model": arch_model})

    assert len(updates["diagram_queue"]) == 1
    diagram = updates["diagram_queue"][0]
    assert len(diagram["relationships"]) == 1
    assert diagram["boundary_groups"] == [{"id": "b1", "entity_ids": ["system-a"]}]
    assert diagram["assumption_flags"] == ["assumed-link"]

    broken = dict(arch_model)
    broken["relationships"] = [
        {
            "id": "missing",
            "source_id": "person-a",
            "target_id": "missing-system",
            "description": "Broken",
            "relationship_type": "uses",
            "diagram_scope": "context",
        }
    ]

    with pytest.raises(ValueError, match="missing endpoints"):
        await input_parsing({"arch_model": broken})
