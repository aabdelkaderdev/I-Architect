# Phase 1 — Foundation & State

> **Goal:** Establish the AGA module scaffold — folder structure, Pydantic models, TypedDict state schemas, and the AGAConfig dataclass. This phase creates everything that downstream phases import from.
>
> **Depends on:** Nothing (first phase)
> **Produces:** `aga/state/models.py`, `aga/state/schemas.py`, `aga/state/config.py`, `aga/state/__init__.py`, all `__init__.py` files, folder scaffold
> **Test fixture:** `arch_model_test_result-1.json`

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
