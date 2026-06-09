import pytest

from aga.nodes.diagram_loop import diagram_loop_entry, record_diagram_result, should_continue_diagrams
from aga.nodes.input_parsing import input_parsing
from aga.nodes.output_assembly import output_assembly


PNG_BYTES = b"\x89PNG\r\n\x1a\npayload"


def _entity(entity_id: str, c4_type: str, **extra):
    payload = {
        "id": entity_id,
        "name": entity_id.replace("-", " ").title(),
        "description": f"{entity_id} description",
        "c4_type": c4_type,
        "technology": "",
    }
    payload.update(extra)
    return payload


def _relationship(rel_id: str, source: str, target: str, scope: str):
    return {
        "id": rel_id,
        "source_id": source,
        "target_id": target,
        "description": f"{source} to {target}",
        "relationship_type": "uses",
        "diagram_scope": scope,
        "requirement_ids": [],
        "metadata": {},
    }


def _arch_model_with_three_merged_diagrams():
    entities = [
        _entity("customer", "person"),
        _entity("system-a", "system"),
        _entity("external-system", "system"),
        _entity("container-a", "container", parent_system_id="system-a"),
        _entity("container-b", "container", parent_system_id="system-a"),
    ]
    relationships = [
        _relationship("r-context", "customer", "system-a", "context"),
        _relationship("r-container", "container-a", "container-b", "container"),
    ]

    for index in range(10):
        container_id = f"container-{index}"
        component_a = f"component-{index}-a"
        component_b = f"component-{index}-b"
        entities.append(_entity(container_id, "container", parent_system_id="system-a"))
        entities.append(_entity(component_a, "component", parent_container_id=container_id))
        entities.append(_entity(component_b, "component", parent_container_id=container_id))
        relationships.append(_relationship(f"r-component-{index}", component_a, component_b, "component"))

    return {
        "status": "ok",
        "entities": entities,
        "relationships": relationships,
        "boundary_groups": [],
        "cross_cutting_candidates": [],
        "assumption_flags": [],
    }


def test_one_item_queue_routes_to_agent_after_entry():
    state = {
        "diagram_queue": [
            {
                "diagram_id": "ctx-merged",
                "diagram_type": "context",
                "focus_entity_label": "System A",
                "entities": [],
                "relationships": [],
            }
        ],
        "diagram_cursor": 0,
    }

    updates = diagram_loop_entry(state)
    next_state = {**state, **updates}

    assert updates["diagram_cursor"] == 1
    assert should_continue_diagrams(next_state) == "agent_node"


@pytest.mark.asyncio
async def test_merged_diagram_loop_produces_exactly_three(tmp_path):
    """With the merged strategy, every C4 scope produces exactly one diagram."""
    state = {
        "arch_model": _arch_model_with_three_merged_diagrams(),
        "completed_diagrams": [],
        "failed_diagrams": [],
        "started_at_perf": 1.0,
    }
    state.update(await input_parsing(state))
    calls: list[str] = []

    while True:
        state.update(diagram_loop_entry(state))
        route = should_continue_diagrams(state)
        if route == "output_assembly":
            break

        diagram = state["current_diagram"]
        calls.append(diagram["diagram_id"])
        png_path = tmp_path / f"{diagram['diagram_id']}.png"
        png_path.write_bytes(PNG_BYTES)
        state.update(
            {
                "current_puml_code": "@startuml\n@enduml\n",
                "current_encoded_url": f"https://example.test/png/{diagram['diagram_id']}",
                "current_png_path": str(png_path),
            }
        )
        result_update = record_diagram_result(
            state,
            {"configurable": {"output_dir": str(tmp_path)}},
        )
        state["completed_diagrams"] += result_update.get("completed_diagrams", [])
        state["failed_diagrams"] += result_update.get("failed_diagrams", [])

    state.update(output_assembly(state, {"configurable": {"output_dir": str(tmp_path)}}))

    completed = state["completed_diagrams"]
    failed = state["failed_diagrams"]
    report = state["session_report"]

    # Exactly 3 merged diagrams: ctx-merged, cnt-merged, cmp-merged
    assert len(calls) == 3
    assert set(calls) == {"ctx-merged", "cnt-merged", "cmp-merged"}
    assert len(completed) == 3
    assert failed == []
    assert report["completed_count"] == 3
    assert report["failed_count"] == 0
    assert report["total_diagrams_expected"] == 3
    assert {d["diagram_id"] for d in completed} == {"ctx-merged", "cnt-merged", "cmp-merged"}
