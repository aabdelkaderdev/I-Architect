## Context

The AGA processes an architectural JSON model to produce C4 PlantUML diagrams. The input JSON is currently a flat list of entities and relationships without a pre-computed "manifest" of the exact diagrams to generate. Furthermore, the downstream graph relies on an external MCP server (implemented in Phase 2 using FastMCP) to provide PlantUML encoding and fetching tools. Without an early check on the MCP server's availability, the agent risks spending cycles generating PlantUML syntax only to fail when trying to invoke missing tools.

## Goals / Non-Goals

**Goals:**
- Systematically derive the correct diagram queue (manifest) from flat JSON.
- Filter out diagrams that have no meaningful contents (e.g., no relationships matching the required scope).
- Verify the Architecture MCP Server is available before beginning main graph processing.

**Non-Goals:**
- Validating the absolute semantic correctness of the flat JSON input (this assumes the JSON is structurally well-formed per the phase 1 models).
- Implementing retry logic for the server guard; we want to "fail fast".

## Decisions

- **Manifest Derivation Engine**: We will build specific scope-filtering logic inside `input_parsing`. It iterates through `system` entities (producing potential Context and Container diagrams) and `container` entities (producing potential Component diagrams), matching against relationships filtered by `diagram_scope`.
- **Diagram ID Schema**: We'll use a canonical prefix based on scope (`ctx-`, `cnt-`, `cmp-`) appended with the target `id` (e.g., `ctx-sys1`). This ensures unique and reproducible artifact filenames.
- **Server Guard Implementation**: Since diagram generation tools are hosted in an external MCP server (Phase 2), `server_guard` will use `langchain-mcp-adapters` to initialize the `MultiServerMCPClient` and call `get_tools()`. This ensures the MCP server subprocess is reachable before the graph generates any diagrams.

## Risks / Trade-offs

- **Risk: Extraneous Diagram Generation**
  If relationship scope matching is too loose, we might generate diagrams with a single element and no arrows.
  *Mitigation: Explicitly enforce that at least one relationship exists for that scope + focus entity combination.*

- **Risk: False Positives in Server Guard**
  The MCP server initialization might fail if the `fastmcp` process doesn't start in time.
  *Mitigation: Catch connection/transport errors explicitly and throw `ServerUnavailableException` so the orchestrator knows the tools are broken.*
