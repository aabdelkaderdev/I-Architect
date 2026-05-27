import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from langchain_core.runnables import RunnableConfig

from aga.nodes.server_guard import server_guard, ServerUnavailableException
from aga.state.schemas import AGAState

@pytest.mark.asyncio
async def test_server_guard_success():
    with patch("aga.nodes.server_guard.MultiServerMCPClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.get_tools = AsyncMock(return_value=["mock_tool"])
        
        config = RunnableConfig()
        state: AGAState = {}  # type: ignore
        
        result = await server_guard(state, config)
        assert result == {}

@pytest.mark.asyncio
async def test_server_guard_timeout():
    with patch("aga.nodes.server_guard.MultiServerMCPClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.get_tools = AsyncMock()
        
        with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError):
            config = RunnableConfig()
            state: AGAState = {}  # type: ignore
            
            with pytest.raises(ServerUnavailableException, match="Connection to Architecture MCP Server timed out"):
                await server_guard(state, config)

@pytest.mark.asyncio
async def test_server_guard_no_tools():
    with patch("aga.nodes.server_guard.MultiServerMCPClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.get_tools = AsyncMock(return_value=[])
        
        config = RunnableConfig()
        state: AGAState = {}  # type: ignore
        
        with pytest.raises(ServerUnavailableException, match="Architecture MCP Server returned no tools"):
            await server_guard(state, config)

@pytest.mark.asyncio
async def test_server_guard_other_exception():
    with patch("aga.nodes.server_guard.MultiServerMCPClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.get_tools = AsyncMock(side_effect=RuntimeError("Some error"))
        
        config = RunnableConfig()
        state: AGAState = {}  # type: ignore
        
        with pytest.raises(ServerUnavailableException, match="Failed to connect to Architecture MCP Server: Some error"):
            await server_guard(state, config)
