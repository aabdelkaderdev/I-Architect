import sys
import asyncio
from typing import Any
from langchain_core.runnables import RunnableConfig
from langchain_mcp_adapters.client import MultiServerMCPClient

from aga.state.schemas import AGAState

class ServerUnavailableException(Exception):
    """Exception raised when the Architecture MCP Server is unreachable."""
    pass

async def server_guard(state: AGAState, config: RunnableConfig) -> dict[str, Any]:
    """
    Initializes the MultiServerMCPClient to verify the Architecture MCP tools are reachable.
    Raises ServerUnavailableException if the server connection fails or times out.
    """
    try:
        client = MultiServerMCPClient(
            {
                "architecture": {
                    "transport": "stdio",
                    "command": sys.executable,
                    "args": ["-m", "aga.tools.mcp_server"],
                }
            }
        )
        
        # Call get_tools to test the connection.
        # Add a timeout to prevent hanging if the stdio process gets stuck.
        tools = await asyncio.wait_for(client.get_tools(), timeout=5.0)
        
        if not tools:
            raise ServerUnavailableException("Architecture MCP Server returned no tools.")
            
    except asyncio.TimeoutError:
        raise ServerUnavailableException("Connection to Architecture MCP Server timed out.")
    except Exception as e:
        if isinstance(e, ServerUnavailableException):
            raise
        raise ServerUnavailableException(f"Failed to connect to Architecture MCP Server: {str(e)}") from e
        
    return {}
