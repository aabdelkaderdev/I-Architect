# Architecture Generation Agent (AGA) — Product Requirements Document

> **Document Type:** High-Level PRD (No Implementation)
> **Status:** Draft
> **Date:** 2025-05-25
> **Source Plan:** [AGA_Plan.md](./AGA_Plan.md)
> **Pipeline Position:** RAA JSON model → **AGA** → PNG diagrams + .puml source

---

## 1) Purpose & Scope

The AGA is the **terminal rendering stage** of the I-Architect pipeline. It receives a C4-compliant architecture model (as a flat JSON dictionary parsed from file) and produces **rendered PNG architecture diagrams** and their corresponding **PlantUML (.puml) source files**.

The AGA is a **standalone LangGraph StateGraph** invoked by the parent orchestrator after RAA completes. It is **not** a subgraph composed inside RAA. The orchestrator calls:

```
aga_graph.invoke({"arch_model": parsed_json_dict}, config, context)
```

### What AGA Does

- Parses the input JSON dictionary to identify entities, relationships, and their `diagram_scope` assignments
- Groups entities and relationships by diagram scope (`context`, `container`, `component`)
- Uses a ReAct agent with LangChain-native agentic skills to generate PlantUML code per diagram
- Encodes PlantUML via the local `planturl` binary
- Submits to PlantUML server, inspects results, self-corrects on error
- Saves PNG and .puml outputs to orchestrator-configured directories

### What AGA Does Not Do

- Modify the architecture model (pure rendering agent)
- Derive or invent entities/relationships not in the input
- Perform structural analysis or SAAM evaluation

---

## 2) Input Contract — Flat JSON Dictionary

### 2A — Input Source

The AGA receives its input as a **Python dictionary** parsed from a JSON file (e.g., `arch_model_test_result-1.json`). This dictionary is provided by the orchestrator as a state channel value. The JSON uses a **flat entity/relationship structure** (not the hierarchical nested model described in the original AGA_Plan).

### 2B — Top-Level JSON Structure

The input dictionary contains these top-level keys:

| Key | Type | Description |
|-----|------|-------------|
| `entities` | `list[dict]` | Flat list of all C4 entities (systems, containers, components, persons, external systems) |
| `relationships` | `list[dict]` | Flat list of all relationships, each carrying a `diagram_scope` field |
| `boundary_groups` | `list[dict]` | Boundary grouping metadata (similarity scores, rationales) |
| `cross_cutting_candidates` | `list` | Cross-cutting concern candidates |
| `assumption_flags` | `list[str]` | Entity IDs flagged as assumptions |
| `status` | `str` | Model status (e.g., `"final"`) |

### 2C — Entity Schema (per item in `entities`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical entity ID |
| `name` | `str` | Human-readable display name |
| `description` | `str` | Short description of the entity's purpose |
| `c4_type` | `str` | One of: `system`, `container`, `component`, `person`, `external_system` |
| `technology` | `str` | Technology stack annotation (may be empty string) |
| `parent_system_id` | `str \| null` | ID of the parent system (for containers) |
| `parent_container_id` | `str \| null` | ID of the parent container (for components) |
| `requirement_ids` | `list[str]` | Requirement IDs this entity traces to |
| `saam_score` | `float` | SAAM coverage score |
| `metadata` | `dict` | Additional metadata (boundary group, assumption flags, etc.) |

### 2D — Relationship Schema (per item in `relationships`)

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Relationship ID |
| `source_id` | `str` | Source entity ID |
| `target_id` | `str` | Target entity ID |
| `description` | `str` | Interaction description (verb phrase) |
| `relationship_type` | `str` | e.g., `uses`, `contains` |
| `diagram_scope` | `str` | **Routing key** — one of: `context`, `container`, `component` |
| `requirement_ids` | `list[str]` | Traced requirement IDs |
| `metadata` | `dict` | Additional metadata |

### 2E — Diagram Scope as Routing Key

The `diagram_scope` field on each relationship is the **authoritative routing key** that determines which diagram a relationship belongs to. The AGA uses this field to partition relationships into diagram groups:

- `diagram_scope = "context"` → System Context diagrams
- `diagram_scope = "container"` → Container diagrams
- `diagram_scope = "component"` → Component diagrams

Entity inclusion per diagram is derived from the relationships: an entity appears in a diagram if it is referenced as `source_id` or `target_id` by any relationship in that scope.

---

## 3) Diagram Scope Resolution Strategy

### 3A — Manifest Derivation from Flat Input

Since the flat JSON does not include a pre-built `diagram_manifest`, the AGA must **derive the diagram work queue** from the input data:

1. **Collect unique systems:** Scan entities where `c4_type = "system"`. Each system produces a potential context diagram and a potential container diagram.
2. **Collect unique containers:** Scan entities where `c4_type = "container"`. Each container (with components inside it) produces a potential component diagram.
3. **Scope-filter relationships:** Group relationships by `diagram_scope`. Only generate a diagram if at least one relationship exists for that scope + focus entity combination.

### 3B — Focus Entity Resolution per Diagram Type

| Diagram Type | Focus Entity | Included Entities | Included Relationships |
|-------------|-------------|-------------------|----------------------|
| **Context** | A `system` entity | The focus system + all persons, external systems, and other systems referenced in `diagram_scope = "context"` relationships involving the focus system | All relationships where `diagram_scope = "context"` and either `source_id` or `target_id` matches the focus system or its related actors |
| **Container** | A `system` entity | All containers with `parent_system_id` matching the focus system + persons and external systems referenced in `diagram_scope = "container"` relationships | All relationships where `diagram_scope = "container"` involving containers of the focus system |
| **Component** | A `container` entity | All components with `parent_container_id` matching the focus container + other containers or external systems referenced in `diagram_scope = "component"` relationships | All relationships where `diagram_scope = "component"` involving components of the focus container |

### 3C — Diagram ID Convention

Derived diagram IDs follow the stable canonical pattern:

- Context: `ctx-{system_id}` (e.g., `ctx-sys1`)
- Container: `cnt-{system_id}` (e.g., `cnt-sys1`)
- Component: `cmp-{container_id}` (e.g., `cmp-container2`)

### 3D — Output Filename Convention

- PNG files: `{diagram_id}.png` (e.g., `ctx-sys1.png`)
- PlantUML source: `{diagram_id}.puml` (e.g., `ctx-sys1.puml`)
- Metadata sidecar: `{diagram_id}_metadata.json`

---

## 4) Folder Structure

The AGA module follows the same directory layout established by ARLO (`arlo/`) and RAA (`raa/`):

```
aga/
├── __init__.py                    # Module init, public API exports
├── Skills/
│   ├── SKILL.md                   # Skill manifest (frontmatter + references index)
│   └── references/
│       └── c4.md                  # C4 PlantUML syntax reference (tag-indexed)
├── graphs/
│   ├── __init__.py
│   └── aga_graph.py               # Main StateGraph definition, node wiring, compilation
├── nodes/
│   ├── __init__.py
│   ├── input_parsing.py           # Parse flat JSON dict → internal DiagramSpec queue
│   ├── diagram_generation.py      # ReAct agent loop: generate → encode → fetch → validate
│   ├── output_assembly.py         # Collect completed diagrams, build session report
│   └── server_guard.py            # PlantUML server availability pre-check
├── prompts/
│   ├── agent_instruction.md       # ReAct agent system prompt (mustache template)
│   ├── code_generation.md         # C4 PlantUML code generation prompt (mustache template)
│   └── error_correction.md        # Syntax error correction prompt (mustache template)
├── state/
│   ├── __init__.py
│   ├── config.py                  # AGAConfig dataclass (runtime configuration)
│   ├── models.py                  # Pydantic models: DiagramSpec, CompletedDiagram, etc.
│   └── schemas.py                 # AGAInput / AGAOutput / AGAState TypedDicts
├── tools/
│   ├── __init__.py
│   ├── encode_plantuml.py         # planturl binary invocation wrapper
│   ├── fetch_plantuml_png.py      # HTTP fetch + SVG error detection
│   ├── os_detection.py            # OS/arch detection → binary path resolution
│   └── planturl/                  # Pre-compiled planturl binaries (existing)
│       └── Bin/
│           ├── aarch64-apple-darwin/planturl
│           ├── apple-darwin/planturl
│           ├── linux-gnu/planturl
│           ├── linux-musl/planturl
│           └── windows-msvc/planturl.exe
└── utils/
    ├── __init__.py
    ├── prompt_loader.py           # Mustache template loader with skill injection
    └── skill_loader.py            # Skill tag resolver (shared pattern from RAA)
```

### Structural Alignment with ARLO & RAA

| Concern | ARLO | RAA | AGA |
|---------|------|-----|-----|
| State schemas | `arlo/state/schemas.py` | `raa/state/schemas.py` | `aga/state/schemas.py` |
| Runtime config | `arlo/state/config.py` | `raa/state/config.py` | `aga/state/config.py` |
| Graph definition | `arlo/graphs/core.py` | `raa/graphs/execution_loop.py` | `aga/graphs/aga_graph.py` |
| Processing nodes | `arlo/nodes/*.py` | `raa/nodes/*.py` | `aga/nodes/*.py` |
| Prompt templates | `arlo/prompts/*.md` | `raa/prompts/*.md` | `aga/prompts/*.md` |
| Skills bundle | N/A (uses prompts) | `raa/Skills/SKILL.md` | `aga/Skills/SKILL.md` |
| Utilities | `arlo/utils/*.py` | `raa/utils/*.py` | `aga/utils/*.py` |

---

## 5) State Schema (Three-Schema Pattern)

Following the ARLO/RAA three-schema pattern (`Input` / `Output` / `State`):

### 5A — AGAInput (provided by orchestrator)

| Channel | Type | Description |
|---------|------|-------------|
| `arch_model` | `dict` | Flat JSON model dictionary parsed from the JSON file |

### 5B — AGAOutput (returned to orchestrator)

| Channel | Type | Description |
|---------|------|-------------|
| `completed_diagrams` | `list[dict]` | Successfully rendered diagrams |
| `failed_diagrams` | `list[dict]` | Diagrams that exhausted retry limit |
| `session_report` | `dict` | Full session metadata |

### 5C — AGAState (full internal state)

| Channel | Type | Reducer | Description |
|---------|------|---------|-------------|
| `arch_model` | `dict` | overwrite | Input model (read-only within AGA) |
| `diagram_queue` | `list[dict]` | overwrite | Derived ordered list of DiagramSpec dicts |
| `current_diagram` | `dict \| None` | overwrite | Currently processing diagram spec |
| `current_puml_code` | `str` | overwrite | PlantUML code being worked on |
| `current_encoded_url` | `str` | overwrite | Encoded URL from planturl |
| `retry_count` | `int` | overwrite | Correction attempts for current diagram |
| `last_error` | `dict \| None` | overwrite | Last error record |
| `completed_diagrams` | `list[dict]` | `add` | Accumulates successful renders |
| `failed_diagrams` | `list[dict]` | `add` | Accumulates failed renders |
| `diagram_cursor` | `int` | overwrite | Current position in diagram queue |
| `planturl_bin_path` | `str` | overwrite | Resolved binary path (cached) |
| `session_report` | `dict` | overwrite | Session metadata |

### 5D — AGAConfig (runtime configuration dataclass)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_retries` | `int` | `5` | Max correction attempts per diagram |
| `plantuml_server_url` | `str` | `"http://www.plantuml.com/plantuml"` | PlantUML server base URL |
| `checkpoint_db_path` | `str` | *(required, no default)* | SQLite checkpoint path from orchestrator |
| `output_dir_png` | `str` | *(required, no default)* | Directory for PNG output files |
| `output_dir_puml` | `str` | *(required, no default)* | Directory for .puml source files |
| `output_dir_diagrams` | `str` | *(required, no default)* | Combined diagram output directory |
| `read_timeout_seconds` | `int` | `30` | HTTP read timeout for PlantUML server |

The `checkpoint_db_path`, `output_dir_png`, and `output_dir_puml` fields have **no defaults** — the orchestrator **must** provide them. This follows the Orchestrator Plan §7C convention: `projects/{project_name}/checkpoints/aga.db` for checkpoints and `projects/{project_name}/output/aga/` for diagram outputs.

---

## 6) Configurable Output Paths

### 6A — Orchestrator-Provided Paths

All output locations are **configurable by the orchestrator** at invocation time. The AGA never hardcodes output paths. The orchestrator provides paths via the `configurable` dict in `RunnableConfig`:

```python
config = {
    "configurable": {
        "thread_id": f"{run_id}:aga",
        "checkpoint_db_path": f"projects/{project_name}/checkpoints/aga.db",
        "output_dir": f"projects/{project_name}/output/aga/",
        "plantuml_server_url": "http://www.plantuml.com/plantuml",
    }
}
```

### 6B — Output Directory Layout

```
projects/{project_name}/output/aga/
├── ctx-sys1.png                    # Context diagram PNG
├── ctx-sys1.puml                   # Context diagram PlantUML source
├── ctx-sys1_metadata.json          # Context diagram metadata sidecar
├── cnt-sys1.png                    # Container diagram PNG
├── cnt-sys1.puml                   # Container diagram PlantUML source
├── cnt-sys1_metadata.json          # Container diagram metadata sidecar
├── cmp-container2.png              # Component diagram PNG
├── cmp-container2.puml             # Component diagram PlantUML source
├── cmp-container2_metadata.json    # Component diagram metadata sidecar
└── aga_report.json                 # Session report
```

### 6C — Checkpoint Directory

```
projects/{project_name}/checkpoints/
└── aga.db                          # SQLite checkpoint database
```

The orchestrator creates these directories before invoking AGA. The AGA module **must not** create directories — this is the orchestrator's responsibility (per Orchestrator Plan §2C).

---

## 7) LangChain-Native Agentic Architecture

### 7A — LangGraph StateGraph

The AGA is built as a **LangGraph StateGraph** using LangChain-native constructs:

- **StateGraph** with `AGAState` as the state schema
- **SqliteSaver** checkpointer (path from orchestrator)
- **LangChain tools** (`@tool` decorated functions) for `encode_plantuml` and `fetch_plantuml_png`
- **ReAct agent** created via `create_react_agent()` or equivalent LangGraph agent builder
- **LLM** passed via `context={}` dict (never in state channels, per Orchestrator Plan §3C)

### 7B — Graph Topology

```
START
  │
  ▼
[server_guard]          ── HEAD check PlantUML server availability
  │
  ▼
[input_parsing]         ── Parse flat JSON → derive diagram queue
  │
  ▼
[diagram_loop_entry]    ── Pop next diagram from queue
  │
  ▼
[react_agent_node]      ── ReAct agent: generate → encode → fetch → validate
  │                        (self-correction loop up to max_retries)
  ├── success ──▶ [record_success] → [advance_queue]
  └── failure ──▶ [record_failure] → [advance_queue]
                                          │
                              ┌───────────┤
                              ▼           ▼
                    [diagram_loop_entry]  [output_assembly]
                    (more diagrams)       (queue exhausted)
                                          │
                                          ▼
                                         END
```

### 7C — Tool Definitions (LangChain @tool)

Two LangChain-native tools are bound to the ReAct agent:

1. **`encode_plantuml`** — Wraps the planturl binary invocation
2. **`fetch_plantuml_png`** — HTTP fetch with SVG-based error detection

### 7D — Checkpointing Strategy

- **SqliteSaver** with WAL mode, matching the RAA pattern in `execution_loop.py`
- One checkpoint per completed diagram (not per ReAct step)
- Checkpoint DB path received from orchestrator — no default
- On resume, the `diagram_cursor` determines where to continue

---

## 8) Mustache Prompt Templates

### 8A — Template Loading Pattern

Following the RAA pattern (`raa/utils/prompt_loader.py`), AGA uses **chevron** for mustache rendering with skill tag injection:

- Templates live in `aga/prompts/*.md`
- Skill declarations use the `{{! skill: <tag> as <key> }}` directive
- Context variables use `{{variable}}` (escaped) and `{{{variable}}}` (unescaped/triple-stache for injected skill content)
- The `prompt_loader.py` resolves skill tags → loads reference content → injects into template → renders

### 8B — Agent Instruction Template (`agent_instruction.md`)

```mustache
{{! skill: c4:rules as c4_plantuml_rules }}

You are the Architecture Generation Agent (AGA). Your task is to generate
C4-compliant PlantUML diagrams from an architecture model.

## C4 PlantUML Rules (STRICT)
{{{c4_plantuml_rules}}}

## Diagram Specification
- Diagram ID: {{diagram_id}}
- Diagram Type: {{diagram_type}}
- Focus Entity: {{focus_entity_id}}
- Focus Entity Label: {{focus_entity_label}}

## Entities in Scope
{{entities_json}}

## Relationships in Scope
{{relationships_json}}

## Retry Policy
- Maximum {{max_retries}} correction attempts per diagram
- On syntax error: read the error, identify the faulty construct, fix minimally
- Do not restructure the entire diagram on a single error

## Constraints
- Do NOT invent entities or relationships not listed above
- Every PlantUML alias MUST exactly match a canonical entity ID
- Do NOT modify the architecture model — only translate it to diagram code
```

### 8C — Code Generation Template (`code_generation.md`)

```mustache
{{! skill: c4:rules as c4_rules }}

Generate PlantUML code for a {{diagram_type}} diagram.

## Focus Entity
- ID: {{focus_entity_id}}
- Label: {{focus_entity_label}}
- Description: {{focus_entity_description}}

## Elements
{{{elements_block}}}

## Relationships
{{{relationships_block}}}

## Generation Rules
{{{c4_rules}}}

Produce valid PlantUML wrapped in @startuml / @enduml.
Include LAYOUT_WITH_LEGEND() at the end.
```

### 8D — Error Correction Template (`error_correction.md`)

```mustache
The PlantUML server returned a syntax error for diagram {{diagram_id}}.

## Error Text
{{{error_text}}}

## Current PlantUML Code
{{{current_puml_code}}}

## Instructions
1. Quote the error text verbatim
2. Locate the offending construct in the code
3. Apply the minimal fix to resolve the error
4. Return the corrected PlantUML code

Attempt {{retry_count}} of {{max_retries}}.
```

---

## 9) Skills Bundle

### 9A — SKILL.md Manifest

The AGA skill manifest follows the same frontmatter-based pattern as RAA:

```yaml
---
name: c4-plantuml-syntax
description: Authoritative reference for generating C4 architecture diagrams
  using PlantUML. Covers element types, relationship syntax, and diagram layout.
metadata:
  version: "2.0"
  target: aga
---
```

### 9B — Skill Tag Registry

| Tag | Reference File | Content |
|-----|---------------|---------|
| `c4:rules` | `references/c4.md` | C4 PlantUML syntax rules, element macros, relationship arrows |
| `c4:context_example` | `references/c4.md` | Context diagram example |
| `c4:container_example` | `references/c4.md` | Container diagram example |
| `c4:component_example` | `references/c4.md` | Component diagram example |

### 9C — Skill Injection at Runtime

The `prompt_loader.py` resolves skill declarations in templates:

```
{{! skill: c4:rules as c4_plantuml_rules }}
```

This loads the tagged section from `aga/Skills/references/c4.md`, validates statement word limits, and injects the content into the render context under key `c4_plantuml_rules`.

---

## 10) Tools Specification

### 10A — `encode_plantuml`

| Attribute | Value |
|-----------|-------|
| **Signature** | `encode_plantuml(puml_code: str) → str` |
| **Behaviour** | Write code to temp `.puml` file → invoke planturl binary → return encoded URL |
| **Binary Args** | `-s <tmpfile> -u <server_url> -t png -c deflate` |
| **Error Surface** | `EncodingException` on non-zero exit; `IOError` on temp file failure |

### 10B — `fetch_plantuml_png`

| Attribute | Value |
|-----------|-------|
| **Signature** | `fetch_plantuml_png(encoded_url: str) → PngResult \| PlantumlErrorRecord` |
| **Step 1** | HEAD pre-check to server base URL (3s timeout) |
| **Step 2** | GET request to encoded URL (30s timeout) |
| **Step 3** | SVG-based error detection (substitute `/png/` with `/svg/`, parse for error strings) |
| **Transient Retries** | 2 retries with exponential backoff for network errors |

### 10C — OS Detection

| OS | Architecture | Binary Path |
|----|-------------|-------------|
| Windows | any | `tools/planturl/Bin/windows-msvc/planturl.exe` |
| macOS | ARM64 | `tools/planturl/Bin/aarch64-apple-darwin/planturl` |
| macOS | x86_64 | `tools/planturl/Bin/apple-darwin/planturl` |
| Linux | glibc | `tools/planturl/Bin/linux-gnu/planturl` |
| Linux | musl | `tools/planturl/Bin/linux-musl/planturl` |

---

## 11) Output Contract

### 11A — AGAOutput Schema

| Field | Type | Description |
|-------|------|-------------|
| `completed_diagrams` | `list[CompletedDiagram]` | Successfully rendered diagrams |
| `failed_diagrams` | `list[FailedDiagram]` | Diagrams that exhausted retries |
| `session_report` | `SessionReport` | Full session metadata |

### 11B — CompletedDiagram

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | Canonical ID (e.g., `ctx-sys1`) |
| `diagram_type` | `str` | `context`, `container`, or `component` |
| `png_bytes` | `bytes` | Rendered PNG data |
| `plantuml_source` | `str` | PlantUML source code |
| `output_path` | `str` | Filesystem path where PNG was written |

### 11C — SessionReport

| Field | Type | Description |
|-------|------|-------------|
| `completed_count` | `int` | Number of successful diagrams |
| `failed_count` | `int` | Number of failed diagrams |
| `total_diagrams_expected` | `int` | Total diagrams in queue |
| `planturl_binary` | `str` | Binary path used |
| `detected_os` | `str` | OS/architecture detected |
| `plantuml_server_url` | `str` | Server URL used |
| `wall_clock_seconds` | `float` | Total execution time |

---

## 12) Error Handling & Halt Conditions

| Error Type | Source | Agent Response |
|------------|--------|----------------|
| `ServerUnavailableException` | HEAD check failed | **Halt immediately** — no diagrams attempted |
| `BinaryNotExecutableException` | Binary path check failed | **Halt immediately** at startup |
| `encoding_error` | planturl non-zero exit | Agent inspects stderr, rewrites code, retries |
| `syntax_error` | SVG error text detected | Agent reads error, applies minimal fix, retries |
| `http_error` (4xx) | Server returned 4xx | Agent adjusts code, retries encode step |
| `http_error` (5xx) | Server returned 5xx | 2 submission retries with backoff, then skip |
| Retry limit exhausted | 5 failed attempts | Record failure, proceed to next diagram |

---

## 13) Integration Points

### 13A — Orchestrator → AGA

The orchestrator provides:
- `arch_model` dict via state channel
- LLM instance via `context={"llm": aga_llm}`
- Checkpoint DB path via `configurable["checkpoint_db_path"]`
- Output directory via `configurable["output_dir"]`
- Thread ID via `configurable["thread_id"]` (pattern: `{run_id}:aga`)

### 13B — AGA → Downstream (SA, RGA)

The AGA returns `AGAOutput` to the orchestrator, which threads:
- `completed_diagrams` → SA (for diagram accuracy scoring)
- `completed_diagrams` + `failed_diagrams` + `session_report` → RGA (for PDF report)
- `plantuml_source` in each `CompletedDiagram` → SA (for sub-tree inclusion validation)

### 13C — SA Regeneration Loop

When SA determines diagram regeneration is needed:
- Orchestrator re-invokes AGA with `targeted_diagrams` filter from SA's `FeedbackState`
- AGA only regenerates the specified diagram IDs, skipping already-valid ones

---

## 14) Assumption Flag Handling

Entities listed in `assumption_flags` carry an `assumed: true` marker in their metadata. When generating PlantUML code for these entities, the AGA appends `[assumed]` to the entity description string. This makes assumptions visible to diagram reviewers without breaking rendering.

---

## 15) Validation & Acceptance Criteria

### Unit Tests
- OS detection returns correct binary path for all 5 targets
- `encode_plantuml` produces non-empty URL for valid input
- `fetch_plantuml_png` classifies SVG error responses correctly
- Diagram queue derivation from flat JSON produces correct count and ordering

### Integration Tests
- End-to-end with `arch_model_test_result-1.json`: agent generates all derivable diagrams
- Syntax error injection → agent corrects and renders on retry
- Server unavailability → agent halts with structured failure report

### Functional Tests
- All PNGs are valid (magic bytes check)
- All .puml files round-trip through PlantUML server
- No entity alias in generated code references an ID not in the input model
- Assumed entities appear with `[assumed]` annotation

---

## 16) Open Design Decisions

| # | Question | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Parallel vs sequential diagram generation | Sequential (simpler) vs asyncio.gather (faster) | Sequential for v1, parallel as optimization |
| 2 | PlantUML source persistence | .puml alongside PNG vs embedded in metadata JSON | Both: .puml file + metadata sidecar |
| 3 | Diagram deduplication | Skip diagrams with identical entity sets | Defer — manifest-driven approach prevents most duplicates |
| 4 | Self-hosted PlantUML fallback | Auto-fallback to local Docker instance | Explicit config only — no silent fallback |
