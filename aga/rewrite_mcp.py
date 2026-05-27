import os

base_path = "d:/project/I-Architect-main/I-Architect-main/aga"

def rewrite(path, content):
    with open(os.path.join(base_path, path), "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Update specs and design
proposal = """
## Why

We need to build the core toolset for the agent to render PlantUML architectures and perform OS/architecture detection for binary resolution. In alignment with the current LangChain MCP (Model Context Protocol) documentation, we will implement these tools as an MCP Server using `fastmcp`.

## What Changes

We will introduce a FastMCP server exposing two tools:
1. OS/architecture detection for binary resolution (internal helper).
2. PlantUML encoding via the `planturl` binary (`encode_plantuml`).
3. PNG fetching with SVG-based error detection (`fetch_plantuml_png`).

These tools will be consumed by the LangChain agent via `MultiServerMCPClient` from `langchain-mcp-adapters`. Error handling for tool failures will use `tool_interceptors` on the MCP client.

## Capabilities

### New Capabilities
- `encode-plantuml`: Wraps the `planturl` binary to encode PlantUML code. Exposed via FastMCP.
- `fetch-plantuml-png`: Fetches the PNG image from the encoded URL. Exposed via FastMCP.
- `mcp_server`: A FastMCP stdio server hosting the architecture tools.

## Impact

- **New files**: `aga/tools/mcp_server.py`, `aga/tools/os_detection.py`, `aga/tools/encode_plantuml.py`, `aga/tools/fetch_plantuml_png.py`.
- **Dependencies**: `fastmcp`, `langchain-mcp-adapters`, `langchain`.
- **System**: The tools are decoupled into an MCP server, making them usable across different agents and environments.
"""

design = """
# Phase 2 — Tools (MCP Server)

## Architecture

We use the Model Context Protocol (MCP) to decouple the diagram tools from the core agent.
- **FastMCP Server**: The tools (`encode_plantuml` and `fetch_plantuml_png`) are hosted in a `fastmcp` stdio server.
- **MultiServerMCPClient**: The agent accesses the tools using `langchain-mcp-adapters`.
- **Tool Interceptors**: We use `tool_interceptors` on `MultiServerMCPClient` with `MCPToolCallRequest` from `langchain_mcp_adapters.interceptors` for handling tool exceptions.

## Decisions
- **`fastmcp` for Server**: Replaces local `@tool` decorators.
- **`stdio` transport**: The server runs as a subprocess via standard input/output.
- **`langchain-mcp-adapters`**: Used by the ReAct agent to fetch tools dynamically.
- **`tool_interceptors`**: Current LangChain MCP pattern for tool execution error handling via async interceptor functions.
"""

tasks = """
## 1. Init
- [x] 1.1 Create the `aga/tools/` directory
- [x] 1.2 Create `aga/tools/mcp_server.py`

## 2. OS Detection Implementation
- [x] 2.1 Create `aga/tools/os_detection.py`

## 3. Encode PlantUML Tool
- [x] 3.1 Create `aga/tools/encode_plantuml.py` implementing logic
- [x] 3.2 Add to FastMCP server

## 4. Fetch PlantUML PNG Tool
- [x] 4.1 Create `aga/tools/fetch_plantuml_png.py` implementing logic
- [x] 4.2 Add to FastMCP server

## 5. MCP Server
- [x] 5.1 Implement `fastmcp` server in `mcp_server.py`

## 6. Integration
- [x] 6.1 Use `MultiServerMCPClient` in `aga/agent.py` to connect to the MCP server
- [x] 6.2 Implement `tool_interceptors` on `MultiServerMCPClient` for error handling
"""

spec_encode = """
# Spec: encode-plantuml (MCP Tool)
Exposed via FastMCP.
"""

spec_fetch = """
# Spec: fetch-plantuml-png (MCP Tool)
Exposed via FastMCP.
"""

rewrite("openspec/changes/phase-2-tools/proposal.md", proposal)
rewrite("openspec/changes/phase-2-tools/design.md", design)
rewrite("openspec/changes/phase-2-tools/tasks.md", tasks)
rewrite("openspec/changes/phase-2-tools/specs/encode-plantuml/spec.md", spec_encode)
rewrite("openspec/changes/phase-2-tools/specs/fetch-plantuml-png/spec.md", spec_fetch)

# 2. Rewrite Python Code

mcp_server = """
from fastmcp import FastMCP
from aga.tools.encode_plantuml import encode_plantuml_logic
from aga.tools.fetch_plantuml_png import fetch_plantuml_png_logic

mcp = FastMCP("ArchitectureTools")

@mcp.tool()
def encode_plantuml(puml_code: str) -> str:
    \"\"\"
    Encodes PlantUML code into a URL by writing it to a temporary file and invoking the local planturl binary.
    \"\"\"
    return encode_plantuml_logic(puml_code)

@mcp.tool()
def fetch_plantuml_png(encoded_url: str) -> dict:
    \"\"\"
    Fetches the PNG image from the encoded PlantUML URL.
    Performs a HEAD request pre-check and handles transient network errors with retries.
    \"\"\"
    return fetch_plantuml_png_logic(encoded_url)

if __name__ == "__main__":
    mcp.run(transport="stdio")
"""

encode_logic = """
import subprocess
import tempfile
import os
from aga.tools.os_detection import get_planturl_binary_path

def encode_plantuml_logic(puml_code: str) -> str:
    tmp_path = None
    try:
        binary_path = get_planturl_binary_path()
        
        fd, tmp_path = tempfile.mkstemp(suffix=".puml")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(puml_code)
            
        server_url = "http://www.plantuml.com/plantuml"
            
        cmd = [
            binary_path,
            "-s", tmp_path,
            "-u", server_url,
            "-t", "png",
            "-c", "deflate"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    
    except subprocess.CalledProcessError as e:
        return f"Error: planturl binary execution failed with exit code {e.returncode}. stderr: {e.stderr}"
    except Exception as e:
        return f"Error: Failed to encode PlantUML code. Details: {str(e)}"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
"""

fetch_logic = """
import urllib.request
import urllib.error
import time

def fetch_plantuml_png_logic(encoded_url: str) -> dict:
    base_url = encoded_url.split("/png/")[0] if "/png/" in encoded_url else "http://www.plantuml.com/plantuml"
    
    try:
        req = urllib.request.Request(base_url, method="HEAD")
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status >= 400:
                return {"error": f"PlantUML server base URL returned status {response.status}"}
    except Exception as e:
        return {"error": f"PlantUML server base URL HEAD request failed: {str(e)}"}
        
    max_retries = 2
    retry_delay = 1.0
    
    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(encoded_url)
            with urllib.request.urlopen(req, timeout=30) as response:
                image_bytes = response.read()
                
                if "/png/" in encoded_url:
                    svg_url = encoded_url.replace("/png/", "/svg/")
                    try:
                        svg_req = urllib.request.Request(svg_url)
                        with urllib.request.urlopen(svg_req, timeout=10) as svg_resp:
                            svg_content = svg_resp.read().decode('utf-8', errors='ignore')
                            if "Syntax Error?" in svg_content or "class=\\"error\\"" in svg_content or "<text" in svg_content and "error" in svg_content.lower():
                                return {
                                    "error": "PlantUML Syntax Error",
                                    "details": "The generated SVG indicates a syntax error in the PlantUML code.",
                                    "svg_content": svg_content[:500]
                                }
                    except Exception:
                        pass
                        
                return {"image_bytes": image_bytes}
                
        except urllib.error.URLError as e:
            if attempt == max_retries:
                return {"error": f"Failed to fetch PlantUML PNG after {max_retries} retries. {str(e)}"}
            time.sleep(retry_delay)
            retry_delay *= 2
        except Exception as e:
            return {"error": f"Unexpected failure during GET request: {str(e)}"}
    
    return {"error": "Unknown failure in fetch_plantuml_png"}
"""

agent_code = """
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
    \"\"\"Intercept MCP tool calls and gracefully handle exceptions.\"\"\"
    try:
        return await handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Error: Tool execution failed with exception: {str(e)}",
            tool_call_id=request.runtime.tool_call_id,
        )


async def build_agent(model):
    \"\"\"
    Builds the ReAct agent using the current LangChain create_agent API.
    Wires the MCP tools and error-handling interceptor.
    \"\"\"
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
"""

rewrite("tools/mcp_server.py", mcp_server)
rewrite("tools/encode_plantuml.py", encode_logic)
rewrite("tools/fetch_plantuml_png.py", fetch_logic)
rewrite("agent.py", agent_code)

print("Rewrite complete.")
