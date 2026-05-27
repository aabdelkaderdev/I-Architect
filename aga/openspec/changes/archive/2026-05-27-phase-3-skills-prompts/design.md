## Context

The Architecture Generation Agent (AGA) uses LangChain v1's `create_agent` (from `langchain.agents`) with tools exposed via a FastMCP stdio server (Phase 2). The agent currently has a hard-coded system prompt. This phase externalises the prompt content into versioned mustache templates and a skills bundle that packages C4 PlantUML reference material.

The LangChain v1 ecosystem provides two relevant prompt integration points:
1. **`create_agent(..., system_prompt=...)`** — accepts a static string for the system message.
2. **Middleware `@dynamic_prompt` / `before_model`** — allows generating the system prompt dynamically per invocation (e.g., to inject diagram-specific context).
3. **MCP Prompts** — `langchain-mcp-adapters` supports `client.get_prompt()` and `load_mcp_prompt()` to load reusable prompt templates from MCP servers as LangChain messages. This is an optional extension path.

## Goals / Non-Goals

**Goals:**
- Provide a C4-compliant PlantUML skill bundle with correct rules and syntax examples.
- Define mustache prompt templates for agent instruction, code generation, and error correction.
- Implement utility loaders (`prompt_loader.py` and `skill_loader.py`) that resolve skill tags and render templates at runtime.
- Ensure the rendered system prompt can be passed to `create_agent`'s `system_prompt` parameter or injected via middleware.

**Non-Goals:**
- Wiring the prompt loader into the agent graph (Phase 5).
- Exposing prompts as MCP server prompts via `@mcp.prompt()` (optional stretch goal, not required).
- Implementing middleware for dynamic prompt injection (Phase 4/5 concern).

## Decisions

- **Mustache templates with `chevron`:** We use `chevron` for mustache rendering. Skill injection uses a custom comment directive `{{! skill: c4:rules as c4_plantuml_rules }}` — this is an AGA-internal convention parsed by `prompt_loader.py` before `chevron.render()`. It is unrelated to LangSmith's mustache prompt format (which is for the Playground/Hub).
- **Separate skill manifest:** The skill (`aga/Skills/SKILL.md`) uses YAML frontmatter, and tags map to headed sections in `aga/Skills/references/c4.md`. This mirrors the existing RAA pattern and keeps domain knowledge decoupled from prompt logic.
- **`create_agent` integration path:** The rendered prompt string will be consumed by `create_agent(..., system_prompt=rendered_prompt)`. For per-diagram dynamic prompts (Phase 5), we will use a `before_model` middleware hook or `@dynamic_prompt` decorator to inject diagram-specific variables.
- **MCP interceptors vs middleware for error handling:** Per LangChain v1, tool error handling is done via `wrap_tool_call` middleware on `AgentMiddleware`, not via MCP `tool_interceptors`. MCP interceptors are for MCP-specific runtime concerns (accessing `runtime.context`, `runtime.store`, `runtime.state`). The Phase 2 `tool_interceptors` on `MultiServerMCPClient` remain valid for MCP-level concerns but agent-level tool error handling should use middleware.

## Risks / Trade-offs

- [Risk: Invalid template variables at render time] → Mitigation: `prompt_loader.py` validates required kwargs before calling `chevron.render()` and raises `ValueError` with a clear message listing missing keys.
- [Risk: Skill tag not found in reference file] → Mitigation: `skill_loader.py` raises `KeyError` with the unresolved tag name when a section heading cannot be matched.
- [Risk: Drift between mustache template variables and caller code] → Mitigation: Each template documents its expected variables in a YAML frontmatter block. The loader can optionally validate against this manifest.
