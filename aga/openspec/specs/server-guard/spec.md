## ADDED Requirements

### Requirement: Architecture MCP Server Pre-flight Check
The system SHALL verify the availability of the Architecture MCP server (hosting the diagram generation tools) before initiating the diagram generation pipeline.

#### Scenario: Server is available
- **WHEN** the `server_guard` node initializes the `MultiServerMCPClient` and successfully fetches tools via `get_tools()`
- **THEN** execution proceeds to the `input_parsing` node.

#### Scenario: Server is unavailable
- **WHEN** the MCP server connection fails or the `get_tools()` request times out
- **THEN** the system raises a `ServerUnavailableException` and immediately halts execution.
