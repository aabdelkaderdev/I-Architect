import asyncio
import sys
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.interceptors import MCPToolCallRequest
from langchain.messages import ToolMessage


async def handle_tool_errors(
    request: MCPToolCallRequest,
    handler,
):
    """Intercept MCP tool calls and gracefully handle exceptions."""
    try:
        return await handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Error: Tool execution failed with exception: {str(e)}",
            tool_call_id=request.runtime.tool_call_id,
        )


async def build_agent(model):
    """
    Builds the ReAct agent using the current LangChain create_agent API.
    Wires the MCP tools and error-handling interceptor.
    """
    system_prompt = "You are an Architecture Generation Agent."

    client = MultiServerMCPClient(
        {
            "architecture": {
                "transport": "stdio",
                "command": sys.executable,
                "args": ["-m", "aga.tools.mcp_server"],
            }
        },
        tool_interceptors=[handle_tool_errors],
    )

    tools = await client.get_tools()

    return create_agent(
        model,
        tools=tools,
        system_prompt=system_prompt,
    )
