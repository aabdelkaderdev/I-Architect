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
