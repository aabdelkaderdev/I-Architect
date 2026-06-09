import pytest
from sa.utils.traversal import (
    reconstruct_hierarchy,
    build_traceability_matrix,
    extract_orphaned_requirements,
    extract_tech_and_patterns
)
from sa.nodes.preparation import node_preparation

def test_reconstruct_hierarchy():
    entities = [
        {"id": "s1", "c4_type": "system"},
        {"id": "c1", "c4_type": "container", "parent_system_id": "s1"},
        {"id": "comp1", "c4_type": "component", "parent_container_id": "c1"}
    ]
    tree = reconstruct_hierarchy(entities)
    assert len(tree["systems"]) == 1
    assert tree["systems"][0]["id"] == "s1"
    assert len(tree["systems"][0]["children"]) == 1
    assert tree["systems"][0]["children"][0]["id"] == "c1"
    assert len(tree["systems"][0]["children"][0]["children"]) == 1
    assert tree["systems"][0]["children"][0]["children"][0]["id"] == "comp1"

def test_build_traceability_matrix():
    entities = [
        {"id": "s1", "c4_type": "system", "requirement_ids": ["req1", "req2"]},
        {"id": "c1", "c4_type": "container", "requirement_ids": ["req1"]}
    ]
    matrix = build_traceability_matrix(entities)
    assert "req1" in matrix
    assert len(matrix["req1"]) == 2
    
    # req1 is mapped to system and container, so deepest level is container
    for entry in matrix["req1"]:
        assert entry["deepest_level"] == "container"
        
    assert matrix["req2"][0]["deepest_level"] == "system"

def test_extract_orphaned_requirements():
    matrix = {"req1": [{"entity_id": "s1"}]}
    req_data = {
        "asrs": ["req1", "req3"],
        "non_asr": ["req2"]
    }
    orphans = extract_orphaned_requirements(matrix, req_data)
    assert set(orphans) == {"req2", "req3"}

def test_node_preparation():
    state = {
        "arch_model": {
            "entities": [
                {"id": "s1", "c4_type": "system", "requirement_ids": ["req1"]}
            ]
        },
        "requirements_data": {
            "asrs": ["req1"],
            "non_asr": ["req2"]
        }
    }
    
    updates = node_preparation(state)
    assert "traceability_matrix" in updates
    assert "req1" in updates["traceability_matrix"]
    assert "req2" in updates["orphaned_reqs"]
