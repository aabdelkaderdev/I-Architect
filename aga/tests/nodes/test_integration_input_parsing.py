import pytest
import json
import os
from langchain_core.runnables import RunnableConfig

from aga.nodes.input_parsing import input_parsing
from aga.state.schemas import AGAState

@pytest.mark.asyncio
async def test_integration_input_parsing():
    # Load the real test JSON file
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    json_path = os.path.join(base_dir, "arch_model_test_result-1.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        arch_model = json.load(f)
        
    state: AGAState = {"arch_model": arch_model}  # type: ignore
    config = RunnableConfig()
    
    result = await input_parsing(state, config)
    
    assert "diagram_queue" in result
    assert result["diagram_cursor"] == 0
    
    queue = result["diagram_queue"]
    assert len(queue) > 0, "Should derive at least one diagram from the test model"
    
    # Verify the structure of the derived diagrams
    for d in queue:
        assert "diagram_id" in d
        assert "diagram_type" in d
        assert d["diagram_type"] in ["context", "container", "component"]
        assert "focus_entity_id" in d
        assert "entities" in d
        assert "relationships" in d
        assert len(d["entities"]) > 0
        assert len(d["relationships"]) > 0
