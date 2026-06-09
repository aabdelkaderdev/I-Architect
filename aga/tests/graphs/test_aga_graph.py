import pytest
import json
import asyncio
from unittest.mock import patch, MagicMock

from langgraph.runtime import Runtime
from langgraph.checkpoint.sqlite import SqliteSaver

from aga.graphs.aga_graph import create_aga_graph, Context
from aga.state.schemas import AGAState
from aga.nodes.server_guard import ServerUnavailableException

@pytest.fixture
def mock_arch_model():
    with open("arch_model_test_result-1.json", "r") as f:
        return json.load(f)

@pytest.fixture
def memory_checkpointer():
    import sqlite3
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    # LangGraph checkpoint sqlite requires a setup
    saver = SqliteSaver(conn)
    saver.setup()
    return saver

@pytest.mark.asyncio
@patch("aga.nodes.server_guard.MultiServerMCPClient")
@patch("aga.nodes.diagram_generation.create_agent")
async def test_server_unavailable(mock_create_agent, mock_mcp_client):
    # Simulate a 503 Server Unavailable response in server_guard by raising the exception
    mock_mcp_client.return_value.get_tools = MagicMock(side_effect=asyncio.TimeoutError())
    
    graph = create_aga_graph()
    state = {"arch_model": {}}
    
    # Graph execution should halt and raise ServerUnavailableException
    with pytest.raises(ServerUnavailableException):
        await graph.ainvoke(state)

@pytest.mark.asyncio
@patch("aga.nodes.server_guard.MultiServerMCPClient")
@patch("aga.nodes.diagram_loop.record_diagram_result")
async def test_end_to_end_success(mock_record_result, mock_mcp_client, mock_arch_model, memory_checkpointer):
    # Mock server_guard to succeed
    mock_mcp_client.return_value.get_tools = MagicMock(return_value=[{"name": "test"}])
    
    # We will patch the agent_node execution by replacing it in the graph?
    # Better to just patch the compiled agent node function, but we can't easily patch `diagram_agent` directly 
    # since it's already bound to the graph. Let's patch its invoke instead.
    
    graph = create_aga_graph(checkpointer=memory_checkpointer)
    
    # Replace the agent_node with a fake node that just pretends to succeed
    def fake_agent(state, runtime):
        return {"messages": [{"name": "fetch_plantuml_png", "content": {"image_bytes": b"fake_png"}}]}
    
    # Hack to replace node function in the compiled graph for testing
    for node_name, node in graph.nodes.items():
        if node_name == "agent_node":
            node.func = fake_agent
            
    # Also fake the record result to simulate successful diagram
    def fake_record(state, runtime):
        return {"completed_diagrams": [{"diagram_id": state["current_diagram"]["diagram_id"], "png_bytes": b"fake_png"}]}
    
    for node_name, node in graph.nodes.items():
        if node_name == "record_diagram_result":
            node.func = fake_record

    config = {"configurable": {"thread_id": "1"}}
    state = {"arch_model": mock_arch_model, "diagram_queue": [], "completed_diagrams": [], "failed_diagrams": []}
    
    final_state = await graph.ainvoke(state, config=config)
    
    # Verify that we generated some diagrams (based on the fixture)
    assert "session_report" in final_state
    assert final_state["session_report"]["completed_count"] > 0
    assert final_state["session_report"]["failed_count"] == 0

@pytest.mark.asyncio
@patch("aga.nodes.server_guard.MultiServerMCPClient")
async def test_syntax_error_correction(mock_mcp_client, mock_arch_model, memory_checkpointer):
    # This tests the agent loop logic, which is slightly complex without a real LLM.
    # We will test the middleware logic manually instead of running the whole graph.
    
    from aga.nodes.diagram_generation import DiagramGenerationMiddleware
    middleware = DiagramGenerationMiddleware()
    
    state = {"retry_count": 5}
    # It should return {"jump_to": "end"} if retry_count >= 5
    result = middleware.before_model(state, None)
    assert result == {"jump_to": "end"}
    
    # Test after_model increments retry_count when tool is called
    class FakeToolMessage:
        def __init__(self):
            self.tool_calls = [{"name": "test"}]
            
    state2 = {"retry_count": 0, "messages": [FakeToolMessage()]}
    result2 = middleware.after_model(state2, None)
    assert result2 == {"retry_count": 1}
