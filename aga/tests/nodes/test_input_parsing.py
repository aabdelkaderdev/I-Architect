import pytest
from langchain_core.runnables import RunnableConfig

from aga.nodes.input_parsing import input_parsing
from aga.state.schemas import AGAState

@pytest.mark.asyncio
async def test_input_parsing():
    # Mock ArchModel JSON
    arch_model = {
        "entities": [
            {"id": "sys1", "name": "System 1", "c4_type": "system"},
            {"id": "ext1", "name": "External System", "c4_type": "external_system"},
            {"id": "cnt1", "name": "Container 1", "c4_type": "container", "parent_system_id": "sys1"},
            {"id": "cmp1", "name": "Component 1", "c4_type": "component", "parent_container_id": "cnt1"},
            {"id": "cmp2", "name": "Component 2", "c4_type": "component", "parent_container_id": "cnt1"}
        ],
        "relationships": [
            {"id": "r1", "source_id": "ext1", "target_id": "sys1", "diagram_scope": "context", "relationship_type": "uses"},
            {"id": "r2", "source_id": "ext1", "target_id": "cnt1", "diagram_scope": "container", "relationship_type": "uses"},
            {"id": "r3", "source_id": "cmp1", "target_id": "cmp2", "diagram_scope": "component", "relationship_type": "uses"}
        ]
    }
    
    state: AGAState = {"arch_model": arch_model}  # type: ignore
    config = RunnableConfig()
    
    result = await input_parsing(state, config)
    
    assert "diagram_queue" in result
    assert result["diagram_cursor"] == 0
    
    queue = result["diagram_queue"]
    assert len(queue) == 3
    
    # Verify Context Diagram
    ctx_diagram = next(d for d in queue if d["diagram_id"] == "ctx-sys1")
    assert ctx_diagram["diagram_type"] == "context"
    assert ctx_diagram["focus_entity_id"] == "sys1"
    assert len(ctx_diagram["entities"]) == 2  # sys1 and ext1
    assert len(ctx_diagram["relationships"]) == 1
    assert ctx_diagram["relationships"][0]["id"] == "r1"
    
    # Verify Container Diagram
    cnt_diagram = next(d for d in queue if d["diagram_id"] == "cnt-sys1")
    assert cnt_diagram["diagram_type"] == "container"
    assert cnt_diagram["focus_entity_id"] == "sys1"
    assert len(cnt_diagram["entities"]) == 2  # cnt1 and ext1
    assert len(cnt_diagram["relationships"]) == 1
    assert cnt_diagram["relationships"][0]["id"] == "r2"
    
    # Verify Component Diagram
    cmp_diagram = next(d for d in queue if d["diagram_id"] == "cmp-cnt1")
    assert cmp_diagram["diagram_type"] == "component"
    assert cmp_diagram["focus_entity_id"] == "cnt1"
    assert len(cmp_diagram["entities"]) == 2  # cmp1 and cmp2
    assert len(cmp_diagram["relationships"]) == 1
    assert cmp_diagram["relationships"][0]["id"] == "r3"

@pytest.mark.asyncio
async def test_input_parsing_no_relationships_skips_diagram():
    # If a system has no relationships in a scope, it shouldn't produce a diagram
    arch_model = {
        "entities": [
            {"id": "sys1", "name": "System 1", "c4_type": "system"},
        ],
        "relationships": []
    }
    
    state: AGAState = {"arch_model": arch_model}  # type: ignore
    config = RunnableConfig()
    
    result = await input_parsing(state, config)
    assert len(result["diagram_queue"]) == 0
