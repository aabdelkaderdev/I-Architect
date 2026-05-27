## Why

The Architecture Generation Agent (AGA) needs a structured way to feed C4 PlantUML domain knowledge into its LLM calls, and a templating system to compose the system/user prompts that drive diagram generation and error correction. Currently, prompts are hard-coded strings. This change extracts them into versioned templates, paired with a skills bundle that packages the C4 reference material, making prompts maintainable and the agent's knowledge base extensible.

## What Changes

- Create the AGA skills bundle manifest (`aga/Skills/SKILL.md`) and C4 PlantUML reference (`aga/Skills/references/c4.md`).
- Create three mustache prompt templates in `aga/prompts/`:
  - `agent_instruction.md` — system prompt for the agent (injected via `create_agent`'s `system_prompt` or middleware `before_model`).
  - `code_generation.md` — user-turn prompt for generating a diagram.
  - `error_correction.md` — user-turn prompt for correcting syntax errors.
- Implement utility loaders in `aga/utils/`:
  - `skill_loader.py` — resolves skill tags (e.g. `c4:rules`) to reference file content.
  - `prompt_loader.py` — parses mustache templates, resolves embedded skill tags via `skill_loader`, then renders with `chevron`.
  - `__init__.py` — package init.
- **Optionally expose prompts via MCP**: The `langchain-mcp-adapters` library supports `client.get_prompt()` / `load_mcp_prompt()` for loading prompts from MCP servers. The AGA FastMCP server from Phase 2 could register these prompt templates as MCP prompts, making them discoverable by any MCP client. This is a stretch goal and not required for Phase 3.

## Capabilities

### New Capabilities
- `skills-bundle`: Define and reference C4 PlantUML syntax rules and examples via a skill manifest and tagged reference files.
- `prompt-templates`: Maintain agent instruction, code generation, and error correction prompts as external mustache templates with dynamic skill injection.
- `template-loaders`: Load and render mustache templates at runtime, resolving skill tag directives and injecting reference content into the render context.

### Modified Capabilities
- (None)

## Impact

- Adds/updates directories: `aga/Skills/`, `aga/Skills/references/`, `aga/prompts/`, `aga/utils/`.
- The rendered system prompt will be passed to `create_agent(..., system_prompt=...)` (LangChain v1 API) or injected dynamically via `@dynamic_prompt` / `before_model` middleware.
- Dependencies: `chevron` (mustache rendering), `pyyaml` (frontmatter parsing). No new LangChain dependencies beyond what Phase 2 already established (`langchain`, `langchain-mcp-adapters`, `fastmcp`).
