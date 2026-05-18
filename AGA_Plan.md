# Architecture Generation Agent (AGA) — Implementation Plan

## 0) Goal of this Portion

Transform the **C4-compliant entity-relationship JSON model** produced by the RAA into **rendered PNG architecture diagrams**, using a ReAct agent that iteratively writes PlantUML code, encodes it via a local Rust binary (`planturl`), submits it to the PlantUML server, and self-corrects on error until a valid diagram is returned.

The AGA is the terminal stage of the architecture pipeline. It receives a fully validated, judge-merged JSON model from RAA and is solely responsible for diagram code generation, encoding, and rendering. It produces no further structural analysis.

> **Pipeline position:** RAA JSON model → **AGA** → PNG diagrams → downstream consumers (documentation, spec kit, review).

---

## 1) Inputs and Assumptions

### Input from RAA
- **C4-compliant JSON model** (`C4JsonModel`) — the final merged output of RAA §16. This is the same data structure as RAA's `ArchModel`, renamed at the AGA boundary for clarity. The model uses a **hierarchical, nested structure**: systems contain containers, containers contain components. Persons and external systems are global flat actors referenced by ID from within scoped relationships.

**`C4JsonModel`** (top-level):

| Field | Type | Description |
|-------|------|-------------|
| `systems` | `list[C4System]` | All systems in the architecture. Each system is fully self-contained with its own `context_relationships`, `containers`, and each container's nested `container_relationships` and `components`. |
| `persons` | `list[C4Person]` | Global flat list of persons (shared actors referenced across multiple systems). Never nested inside a system. |
| `external_systems` | `list[C4ExternalSystem]` | Global flat list of external systems, shared and referenced by ID from within scoped relationships. |
| `patterns` | `list[PatternSelection]` | Architectural patterns selected by the RAA optimizer with rationales (same structure as RAA's `ArchPattern`). |
| `diagram_manifest` | `list[DiagramManifestEntry]` | **Authoritative work queue** for all diagram generation. Produced deterministically by RAA during final merge. AGA must not derive the diagram list independently. |
| `confidence_metadata` | `dict[str, ConfidenceRecord]` | Per-entity confidence flags, keyed by entity ID. Includes `reduced_confidence` flags from incoherent batches. |
| `open_questions` | `list[OpenQuestion]` | Hotspot warnings, unresolved ties, coverage gaps, hierarchy conflicts, and scope conflicts from RAA judge. Passed through to session report; not consumed by AGA. |

**`DiagramManifestEntry`**:

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | Stable canonical ID prefixed by type. Examples: `ctx-{system_id}`, `cnt-{system_id}`, `cmp-{container_id}`. |
| `diagram_type` | `str` | One of: `context`, `container`, or `component`. |
| `focus_entity_id` | `str` | The system ID for context and container diagrams; the container ID for component diagrams. |
| `label` | `str` | Human-readable label for logging and reports. |

**`C4System`** — replaces the old flat `C4Entity` for system-level entities. Structural position in the hierarchy encodes type and containment implicitly (no `type` or `parent_id` fields):

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the system's purpose |
| `requirement_ids` | `list[int]` | Requirement IDs this system traces to |
| `source_fragment` | `str \| null` | Which RAA subgraph produced this system |
| `confidence` | `float \| null` | SAAM coverage score (1.0 = direct, 0.5 = indirect) |
| `context_relationships` | `list[C4Relationship]` | Relationships for the context diagram, each carrying `diagram_scope = context` |
| `containers` | `list[C4Container]` | Containers belonging to this system |

**`C4Container`** — replaces the old flat `C4Entity` for container-level entities:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the container's purpose |
| `technology` | `str \| null` | Technology stack annotation (required when determinable; null otherwise) |
| `requirement_ids` | `list[int]` | Requirement IDs this container traces to |
| `source_fragment` | `str \| null` | Which RAA subgraph produced this container |
| `confidence` | `float \| null` | SAAM coverage score |
| `container_relationships` | `list[C4Relationship]` | Relationships for the container diagram, each carrying `diagram_scope = container` |
| `components` | `list[C4Component]` | Components belonging to this container |

**`C4Component`** — replaces the old flat `C4Entity` for component-level entities:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the component's purpose |
| `technology` | `str \| null` | Technology stack annotation (required when determinable; null otherwise) |
| `requirement_ids` | `list[int]` | Requirement IDs this component traces to |
| `source_fragment` | `str \| null` | Which RAA subgraph produced this component |
| `confidence` | `float \| null` | SAAM coverage score |
| `component_relationships` | `list[C4Relationship]` | Relationships for the component diagram, each carrying `diagram_scope = component` |

**`C4Person`** — flat, global leaf type (replaces old `C4Entity` with `type = person`):

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the person/role |
| `requirement_ids` | `list[int]` | Requirement IDs this person traces to |
| `source_fragment` | `str \| null` | Which RAA subgraph produced this person |
| `confidence` | `float \| null` | SAAM coverage score |

**`C4ExternalSystem`** — flat, global leaf type (replaces old `C4Entity` with `type = external_system`):

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the external system's purpose |
| `technology` | `str \| null` | Technology stack annotation, if known |
| `requirement_ids` | `list[int]` | Requirement IDs this external system traces to |
| `source_fragment` | `str \| null` | Which RAA subgraph produced this external system |
| `confidence` | `float \| null` | SAAM coverage score |

**`C4Relationship`** — scoped relationship type. Relationships are distributed into the hierarchy, not stored in a flat list on the model root:

| Field | Type | Description |
|-------|------|-------------|
| `source_id` | `str` | ID of the source entity |
| `target_id` | `str` | ID of the target entity |
| `interaction_type` | `str` | Short verb phrase describing the interaction (e.g., "sends events to", "reads from") |
| `technology` | `str \| null` | Protocol or technology used (e.g., "HTTPS", "gRPC", "SQL") |
| `diagram_scope` | `str` | One of: `context`, `container`, `component`. Set by RAA. Informational for AGA — does not drive routing since relationships are already distributed into the correct scoped lists. |
| `requirement_ids` | `list[int]` | Requirement IDs this relationship traces to |
| `source_fragment` | `str \| null` | Which RAA subgraph produced this relationship |

**`PatternSelection`** — matches RAA's `ArchPattern` one-to-one:

| Field | Type | Description |
|-------|------|-------------|
| `pattern_name` | `str` | Name from the quality-architecture matrix (e.g., "Microservices", "Message-Based") |
| `rationale` | `str` | Why this pattern was selected (quality attribute coverage) |
| `quality_attributes` | `list[str]` | Quality attributes this pattern addresses |

**`ConfidenceRecord`**:

| Field | Type | Description |
|-------|------|-------------|
| `reduced_confidence` | `bool` | True if entity originated from an incoherent batch (0.5x SAAM multiplier) |
| `source_batch` | `int` | Batch index that produced this entity |
| `saam_score` | `float` | SAAM weighted score of the fragment this entity came from |

**`OpenQuestion`**:

| Field | Type | Description |
|-------|------|-------------|
| `entity_id` | `str \| null` | Related entity ID, if applicable |
| `type` | `str` | One of: `change_risk`, `high_coupling`, `contention`, `tie`, `coverage_gap`, `hierarchy_conflict`, `scope_conflict` |
| `description` | `str` | Human-readable description of the issue |
| `scenario_ids` | `list[str]` | Contributing scenario or requirement IDs |

### External Resources
- **planturl binaries**: precompiled Rust binaries located at `tools/planturl/Bin/` in the project root, one per target OS/architecture (see §7).
- **PlantUML public server**: `http://www.plantuml.com/plantuml` (default endpoint). Can be overridden via configuration to a self-hosted instance.

### Assumptions
- The RAA JSON model is structurally valid and schema-compliant before AGA receives it (hierarchy nesting, manifest completeness, orphan prevention — validated by RAA §19).
- The PlantUML server is expected to be reachable at the start of the run. If it is not, the AGA halts immediately (§11).
- The AGA does not modify the architecture model. It is a pure rendering agent; all structural decisions were finalised in RAA.
- The local `planturl` binary is used exclusively for encoding. The AGA uses its own HTTP client for server communication (§9), giving it full control over response inspection and error propagation.

### Integration Pattern
The AGA is implemented as a **standalone LangGraph StateGraph**, invoked by the parent pipeline after RAA completes. It is not composed as a subgraph inside the RAA graph. The parent pipeline calls `aga_graph.invoke({"arch_model": raa_output_model})` with the RAA's final C4 JSON model as input. This separation keeps the RAA and AGA graphs independently testable and avoids coupling their state schemas.

### Handling of RAA `open_questions`
The RAA output may include an `open_questions` list (hotspot warnings, unresolved ties, coverage gaps — see RAA §14/§16). The AGA does **not** consume or act on `open_questions`; it renders the model as-is. Open questions are passed through to the session report (§13) for downstream review, but they do not alter diagram generation or element inclusion.

### Project Structure
All AGA implementation code resides in the `aga/` directory at the project root. Prompt templates (Mustache `.md` files for the agent instruction prompt and skill prompts) are stored in `aga/prompts/`, following the same convention as ARLO (`arlo/prompts/`) and RAA (`raa/prompts/`).

---

## 2) C4 PlantUML Skill & Source Guidelines

### Purpose
The ReAct agent must generate PlantUML code that is (a) syntactically correct for the PlantUML server and (b) semantically correct for the C4 model level being rendered. A dedicated skill governs this generation.

### Authoritative Sources
The AGA references the same Source Register established in the RAA plan (§2 of the RAA plan), extended with PlantUML-specific sources:

| Source | URL | Governs |
|--------|-----|---------|
| C4-PlantUML library | https://github.com/plantuml-stdlib/C4-PlantUML | C4 macros, element types, relationship syntax for PlantUML |
| PlantUML server API | http://www.plantuml.com/plantuml | Encoding, endpoints, error response format |
| C4 Model notation | https://c4model.com/diagrams/notation | Element labels, descriptions, technology annotation rules |

### C4 PlantUML Normative Constraints (for the agent's skill prompt)

These are injected into the agent's code-generation skill as hard constraints, not suggestions:

**Structural rules:**
- Every diagram must begin with the appropriate C4-PlantUML `!include` directive for the target level: `C4_Context`, `C4_Container`, or `C4_Component`.
- Use macro-based element declarations (`Person`, `System`, `Container`, `Component`, `System_Ext`) — never raw PlantUML shapes as substitutes for C4 elements.
- Every element must include: an alias, a label (display name), and a short description string. The PlantUML alias for every element must be the canonical entity ID from the RAA model (lowercase, snake_case, as defined in the `id` field of the entity). Do not abbreviate, shorten, or invent aliases.
- Containers and components must include the `$techn` technology parameter when the RAA model provides it.
- All relationships must use `Rel` (or directional variants `Rel_D`, `Rel_U`, `Rel_L`, `Rel_R`) and include a label describing the interaction.
- Boundaries (`System_Boundary`, `Enterprise_Boundary`, `Container_Boundary`) must be used to group elements that belong to the same logical scope.

**Diagram hygiene rules:**
- Do not mix C4 levels in a single diagram (e.g., do not render Component-level elements inside a Context diagram).
- Alias names must be valid PlantUML identifiers: alphanumeric and underscores only, no spaces, no hyphens.
- The diagram must open with `@startuml` and close with `@enduml`.
- `LAYOUT_WITH_LEGEND()` should be included at the end of every diagram for readability.

**Multi-diagram strategy:**
- The AGA generates one diagram per entry in the `diagram_manifest`. The manifest is the sole authority on how many diagrams exist and what they represent.
- For a model with N systems where system _i_ has _kᵢ_ containers, the manifest contains N context entries, N container entries, and the sum of all containers' component entries. The total number of diagrams is therefore _(N × 2) + (k₁ + k₂ + ... + kₙ)_, which may be significantly larger than three for non-trivial models.
- Each diagram is generated, encoded, validated, and rendered independently.
- The queue ordering follows the manifest order, which RAA produces as: all context diagrams first (one per system, in the order systems appear in the model), then all container diagrams (one per system, same order), then all component diagrams (one per container per system, ordered by system then by container position within each system). This top-down ordering ensures that a reviewer can inspect context-level diagrams before detail diagrams.

---

## 3) High-Level Pipeline Overview

1. **Input parsing:** extract the C4 JSON model from RAA output; read the `diagram_manifest` from the model and use it directly as the ordered diagram queue. No derivation step is required.
2. **Per-diagram ReAct loop:**
   a. **Resolve focus:** agent traverses `arch_model` to locate the node identified by the `DiagramSpec`'s `focus_entity_id` and collects the relevant sub-tree.
   b. **Generate:** agent writes PlantUML code for the current diagram using the C4 PlantUML skill.
   c. **Encode:** agent calls the `encode_plantuml` tool, which selects the correct `planturl` binary for the host OS, writes the code to a temporary file, runs the binary, and returns the encoded URL.
   d. **Submit:** agent calls the `fetch_plantuml_png` tool, which sends the encoded URL to the PlantUML server and returns either a PNG payload or a structured error record.
   e. **Evaluate:** agent inspects the tool response.
      - On success: save PNG output, advance the diagram queue.
      - On syntax error: agent reads the error, reasons about the required correction, updates the PlantUML code, and retries from step (c).
      - On server unavailability: halt immediately with a `ServerUnavailableException` (§11).
3. **Output assembly:** collect all rendered PNGs into the final output structure.

---

## 4) State Schema

### Agent State Channels

| Channel | Type | Description |
|---------|------|-------------|
| `arch_model` | `C4JsonModel` | Input from RAA (schema defined in §1). Read-only within AGA. |
| `diagram_queue` | `list[DiagramSpec]` | Ordered list of diagrams to generate. Populated directly from `diagram_manifest` at startup — one `DiagramSpec` per `DiagramManifestEntry`, with `output_filename` derived from `diagram_id`. |
| `current_diagram` | `DiagramSpec` | The diagram currently being processed in the ReAct loop. |
| `current_puml_code` | `str` | The PlantUML code string currently being worked on by the agent. Updated on each generation or correction attempt. |
| `current_encoded_url` | `str` | The full encoded URL produced by `encode_plantuml` for the current code. |
| `retry_count` | `int` | Number of correction attempts for the current diagram. Reset to 0 at the start of each diagram. |
| `last_error` | `PlantumlErrorRecord \| null` | Structured error record from the last `fetch_plantuml_png` call. Null if last call was successful. |
| `completed_diagrams` | `list[CompletedDiagram]` | Accumulates successfully rendered diagrams. |
| `agent_scratchpad` | `list[ReActStep]` | The ReAct agent's internal thought/action/observation trace for the current diagram. |

### Supporting Types

**`DiagramSpec`**: `{ diagram_id: str, diagram_type: str, focus_entity_id: str, label: str, output_filename: str }`

The `output_filename` is derived from `diagram_id` (e.g., `ctx-payment_service.png`). The `entities` and `relationships` fields from the old schema are removed — AGA no longer receives a flat entity list to filter from. The agent traverses the hierarchy to locate the relevant sub-tree at generation time.

**`PlantumlErrorRecord`**: `{ http_status: int | null, error_type: str, raw_message: str, svg_error_text: str | null }`

**`CompletedDiagram`**: `{ diagram_id: str, diagram_type: str, png_bytes: bytes, plantuml_source: str, output_path: str }`

**`FailedDiagram`**: `{ diagram_id: str, diagram_type: str, final_error: PlantumlErrorRecord, retry_count: int, last_puml_code: str }`

`diagram_id` is the stable canonical ID from the manifest entry (e.g., `cmp-api_gateway`). The old `level` field is replaced by the pair `(diagram_id, diagram_type)` to make failure records unambiguous when multiple diagrams of the same type are present.

---

## 5) ReAct Agent Architecture

### Agent Type
A **ReAct (Reason + Act) agent** with a fixed tool set and a bounded retry limit per diagram. The agent alternates between reasoning steps (thinking about what to generate or how to correct an error) and action steps (calling tools).

### ReAct Loop per Diagram

```
[Thought]  Receive DiagramSpec with focus_entity_id and diagram_type.
           Traverse arch_model from root to locate the node identified by
           focus_entity_id, collect the relevant sub-tree.
           Plan the C4 PlantUML structure: boundaries, elements, relationships.
[Action]   Call: generate_puml_code (internal skill, not a tool call — produces text)
[Thought]  Review generated code against C4 PlantUML constraints from skill.
[Action]   Call: encode_plantuml(puml_code)
[Observe]  Receive encoded URL or encoding error.
[Action]   Call: fetch_plantuml_png(encoded_url)
[Observe]  Receive PNG bytes (success) or PlantumlErrorRecord (syntax/server error).
[Thought]  If success → done with this diagram.
           If error → read error message, identify the faulty construct,
           reason about the correction, update puml_code.
[Action]   Call: encode_plantuml(corrected_puml_code)  ← retry
... (loop until success or retry limit reached)
```

### Focus Entity Resolution (new instruction)

When beginning a new diagram, the agent must resolve `focus_entity_id` to the correct node in the hierarchy:

- **`context` diagram:** locate the `C4System` whose `id` matches `focus_entity_id`.
- **`container` diagram:** locate the same `C4System` whose `id` matches `focus_entity_id`, collect its `containers` list and `container_relationships`.
- **`component` diagram:** traverse all systems and their containers to find the `C4Container` whose `id` matches `focus_entity_id`, then collect its `components` and `component_relationships`.

This traversal is lightweight — the model is already in memory — and yields the complete, pre-scoped set of elements for that diagram.

### Retry Limit
Maximum 5 correction attempts per diagram (configurable via `max_retries` parameter). If the diagram cannot be successfully rendered within the limit, the agent logs the final error, records the diagram in a `failed_diagrams` list, and proceeds to the next diagram in the queue. A summary of all failures is included in the final output report.

### Agent Instruction Prompt
The agent's system prompt must include:
- The C4 PlantUML normative constraints from §2 (retrieved from the Prompt Resource Bundle in `aga/prompts/` by tags `c4:plantuml`, `c4:notation`).
- The focus entity resolution instructions (above).
- The retry policy and halt conditions.
- A reminder that it must not modify the architecture model, only translate it to valid diagram code.

### Checkpointing
The AGA is a short-lived agent (seconds per diagram). Full `SqliteSaver` persistence is not required. However, the agent should checkpoint after each successfully rendered diagram so that a crash mid-queue does not require re-rendering already-completed diagrams. This is more valuable under the hierarchical model because the total number of diagrams can be significantly larger than three. The checkpoint database path is **received from the orchestrator at runtime** — the orchestrator passes a project-scoped path `projects/{project_name}/checkpoints/aga.db` when calling `compile_for_production(db_path=...)` (see Orchestrator Plan §6C). One checkpoint per completed diagram is sufficient and unchanged.

---

## 6) C4 PlantUML Code Generation Skill

### Purpose
A dedicated **skill** (not a static template) governs the translation from C4 JSON model entities to PlantUML code. Code generation requires interpretation: the agent must choose boundary groupings, apply layout directives, omit reduced-confidence entities gracefully, and handle partial models at each C4 level.

### Input to the Skill
- The `DiagramSpec` for the current diagram (`diagram_id`, `diagram_type`, `focus_entity_id`, `label`, `output_filename`).
- The **resolved sub-tree** from `arch_model` for the current `DiagramSpec` — obtained by the agent traversing to `focus_entity_id` before invoking the skill:
  - **Context diagram:** the target `C4System` node plus the global `persons` and `external_systems` lists.
  - **Container diagram:** the target `C4System`'s `containers` list, `container_relationships`, plus the global `persons` and `external_systems`.
  - **Component diagram:** the target `C4Container`'s `components` list and `component_relationships`.
- C4 PlantUML constraints from the Prompt Resource Bundle (stored in `aga/prompts/`).

### Generation Strategy

**Step 1 — Header block:** emit `@startuml`, the appropriate `!include` for the C4 level, and any global layout directives (`skinparam`, `LAYOUT_TOP_DOWN()`).

**Step 2 — Boundary and element declaration:**
- The entities to render are exactly those present in the resolved sub-tree. No filtering by a `type` discriminator is required — structural position already encodes the level.
- **Context diagrams:** the elements are the system itself, any persons and external systems referenced in its `context_relationships`, and those relationships.
- **Container diagrams:** the elements are all containers in the system, any persons and external systems referenced in `container_relationships`, and those relationships. Group containers within a `System_Boundary`.
- **Component diagrams:** the elements are all components in the container, any other containers or external systems referenced in `component_relationships`, and those relationships. Group components within a `Container_Boundary`.
- For each element, populate alias, label, description, and technology from the RAA model fields.
- If an entity carries `reduced_confidence = true`, still include it in the diagram but append `[unverified]` to its description string. Do not omit it silently.

**Step 3 — Relationship declaration:**
- The relationships to render are exactly the scoped relationship list from the resolved sub-tree (`context_relationships`, `container_relationships`, or `component_relationships` depending on diagram type). No cross-level filtering is needed — RAA already scoped relationships before handoff.
- Emit one `Rel` call per directed relationship in scope.
- Use directional variants (`Rel_D`, `Rel_U`) only when the RAA model specifies a layout hint; otherwise use plain `Rel`.
- Label from the RAA relationship's `interaction_type` field.

**Step 4 — Footer block:** emit `LAYOUT_WITH_LEGEND()` then `@enduml`.

### What the Skill Does Not Do
- It does not invent entities or relationships not present in the RAA model.
- It does not select which C4 level to render (that is determined by the diagram manifest).
- It does not traverse the model hierarchy — traversal to the correct focus node is performed by the agent before invoking the skill. The skill receives a pre-resolved sub-tree.
- It does not call any tools. Tool calls are the agent's responsibility, not the skill's.

---

## 7) Tool: OS Detection and planturl Binary Selection

### Purpose
Before any encoding can occur, the correct `planturl` binary must be identified for the host operating system and architecture. This is a one-time detection at agent startup, with the result cached for the session.

### Binary Location
All binaries are located under `tools/planturl/Bin/` relative to the project root:

```
tools/
└── planturl/
    └── Bin/
        ├── aarch64-apple-darwin/planturl      ← macOS on Apple Silicon
        ├── apple-darwin/planturl              ← macOS on Intel x86_64
        ├── linux-gnu/planturl                 ← Linux with glibc
        ├── linux-musl/planturl                ← Linux with musl libc (Alpine, static envs)
        └── windows-msvc/planturl.exe          ← Windows
```

### Detection Logic

The detection proceeds in the following order:

1. **Operating system:** inspect the runtime platform string.
   - Windows → `windows-msvc/planturl.exe`.
   - macOS → proceed to architecture check.
   - Linux → proceed to libc variant check.

2. **macOS architecture check:** inspect the CPU architecture of the running process.
   - ARM64 (Apple Silicon, M-series) → `aarch64-apple-darwin/planturl`.
   - x86_64 (Intel) → `apple-darwin/planturl`.

3. **Linux libc variant check:** attempt to execute `ldd --version` and inspect the output string.
   - Output contains `musl` → `linux-musl/planturl`.
   - Output contains `glibc` or `GLIBC` (standard GNU libc) → `linux-gnu/planturl`.
   - If `ldd` is not available or the output is inconclusive, default to `linux-gnu/planturl` and log a warning.

4. **Executable permission check:** after selecting the binary path, verify the file exists and is executable. If not, raise a `BinaryNotExecutableException` with the full path and halt.

### Output
The resolved binary path is stored in agent session configuration as `planturl_bin_path`. It is not re-detected on subsequent calls within the same session.

---

## 8) Tool: `encode_plantuml`

### Signature
`encode_plantuml(puml_code: str) → str`

### Behaviour
1. Write `puml_code` to a named temporary file with a `.puml` extension. The file is created in the system's temp directory and deleted after the tool call completes.
2. Invoke the `planturl` binary at `planturl_bin_path` with the following arguments:
   - `-s <tmpfile>`: input source file.
   - `-u http://www.plantuml.com/plantuml`: base URL (or configured self-hosted URL).
   - `-t png`: request PNG-type encoding so the returned URL targets the `/png/` endpoint.
   - `-c deflate`: use deflate compression (default and most widely supported).
3. Capture stdout. The binary outputs the full encoded URL, e.g.: `http://www.plantuml.com/plantuml/png/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000`.
4. Return the encoded URL string.

### Error Handling within this Tool
- If the binary exits with a non-zero code, capture stderr and raise an `EncodingException` with the stderr content. This is distinct from a PlantUML syntax error (encoding failures are local, before any network call).
- If the temp file cannot be written, raise an `IOError` and halt.
- Do not suppress or swallow subprocess errors; all encoding failures must surface to the agent as observable error events so the ReAct loop can reason about them.

---

## 9) Tool: `fetch_plantuml_png`

### Signature
`fetch_plantuml_png(encoded_url: str) → PngResult | PlantumlErrorRecord`

### Behaviour

**Step 1 — Server availability pre-check:**
Before submitting the encoded URL, perform a lightweight HEAD request to the PlantUML server base URL (`http://www.plantuml.com/plantuml`). This check has a short timeout (3 seconds). If it fails due to a connection error or timeout, raise `ServerUnavailableException` immediately and halt (§11). Do not proceed to the main request.

**Step 2 — PNG fetch:**
Send an HTTP GET request to the `encoded_url`. Set a reasonable read timeout (30 seconds) to accommodate server rendering time for complex diagrams.

**Step 3 — Response inspection:**

The PlantUML server exhibits two distinct error modes that must be handled differently:

- **HTTP 4xx / 5xx response:** indicates a malformed encoded string or server-side fault. Capture the HTTP status code and response body. Construct a `PlantumlErrorRecord` with `error_type = "http_error"`, the status code, and the raw response body. Return this record to the agent.

- **HTTP 200 with error diagram (syntax error):** PlantUML's server returns HTTP 200 even when the submitted diagram contains a syntax error — the response is a PNG image depicting the error message text. To detect this case programmatically, the tool makes a **secondary request** to the SVG endpoint instead of the PNG endpoint. Derive the SVG URL by substituting `/png/` with `/svg/` in the encoded URL. Parse the returned SVG XML. If the SVG root element or any text node contains the string `"Syntax Error"` or `"cannot parse"`, construct a `PlantumlErrorRecord` with `error_type = "syntax_error"` and `svg_error_text` populated with the extracted error message from the SVG. Return this record to the agent.

- **HTTP 200 with valid SVG (no error text):** Fetch the PNG URL (original `encoded_url`) and return its bytes as a `PngResult` with `png_bytes` and `content_length` populated.

### Why SVG for Error Detection
SVG responses are XML text and can be inspected for error strings without image parsing. PNG responses are binary and cannot be reliably checked for error content without OCR or image analysis. This two-request strategy keeps error detection deterministic and cheap.

### Network Resilience
- Retry transient network errors (connection reset, read timeout) up to 2 times with exponential backoff before classifying the failure. Distinguish transient retries from the agent-level diagram retry loop (§5) — these are lower-level transport retries, invisible to the agent.
- Do not retry on HTTP 4xx or detected syntax errors; those are forwarded immediately to the agent for correction.

---

## 10) Error Classification and Agent Correction Loop

### Error Types and Agent Behaviour

| Error Type | Source | Agent Response |
|------------|--------|---------------|
| `encoding_error` | `encode_plantuml` returned non-zero exit | Agent inspects stderr, identifies malformed PlantUML syntax before server submission, rewrites code |
| `http_error` (4xx) | `fetch_plantuml_png` received 4xx | Agent reasons that the encoding may be corrupt or the URL malformed; retries encode step after minor code adjustment |
| `http_error` (5xx) | `fetch_plantuml_png` received 5xx | Agent waits briefly (configurable back-off) and retries submission. If 5xx persists after 2 submission retries, records as `server_fault` and skips diagram |
| `syntax_error` | SVG contained error text | **Primary correction path.** Agent reads `svg_error_text` from the error record, identifies the offending construct in `current_puml_code`, reasons about the fix, and regenerates code |
| `ServerUnavailableException` | HEAD check failed | Halt immediately. No further diagrams attempted (§11) |
| `BinaryNotExecutableException` | Binary path check failed at startup | Halt immediately (§7) |

### Correction Reasoning Guidance (injected into agent prompt)
When a `syntax_error` is received, the agent is instructed to:
1. Quote the `svg_error_text` verbatim in its thought step.
2. Locate the line or construct in `current_puml_code` most likely responsible.
3. Cross-reference the C4 PlantUML constraints from the skill (§6) to identify the violated rule.
4. Produce a corrected version of `current_puml_code` with the minimal change necessary to fix the error. Do not restructure the entire diagram on a single error.
5. Increment `retry_count`. If `retry_count` reaches `max_retries`, log the failure and move on.

---

## 11) Server Availability Guard and Halt Condition

### Guard Timing
The server availability check (HEAD request to `http://www.plantuml.com/plantuml`) is performed:
- Once at agent startup, before the diagram queue is processed.
- Again before each `fetch_plantuml_png` call (integrated into the tool — §9, Step 1).

### Halt Behaviour on `ServerUnavailableException`
- Log the exception with timestamp, attempted URL, and failure reason (timeout vs connection refused vs DNS failure).
- Do not attempt any further diagram generation or encoding for the current session.
- Return a structured failure report to the pipeline caller, indicating that zero diagrams were rendered due to server unavailability.
- Do not silently fall back to a local rendering path. If no server is reachable, the AGA halts cleanly and the caller is responsible for deciding whether to retry later or escalate.

### Self-Hosted Server Override
If the pipeline configuration specifies a `plantuml_base_url` override (e.g., a self-hosted instance), all tools use that URL instead of the public server. The availability guard checks the configured URL regardless of whether it is public or self-hosted.

---

## 12) Skills vs Static Templates

### Use Skills For
- C4 PlantUML code generation (§6) — requires interpretation of the model, contextual boundary grouping, and layout reasoning.
- Error correction reasoning — the agent must analyse free-form error text and relate it to specific code constructs.

### Use Static Templates For
- **Diagram queue construction** — direct population of `diagram_queue` from the `diagram_manifest` field in the `C4JsonModel`. The manifest is produced by RAA; AGA performs no derivation. Each `DiagramManifestEntry` is mapped one-to-one to a `DiagramSpec`, with `output_filename` derived from `diagram_id`. This is fully deterministic.
- OS detection and binary path resolution (§7) — fully deterministic branching logic.
- SVG error text extraction (§9) — deterministic XML parsing.
- PNG output assembly — deterministic file write.

### Rationale
The boundary between skill and template mirrors the RAA plan's principle: LLM reasoning is applied only where interpretation or generation is required. All deterministic operations are kept in code to ensure reproducibility and avoid hallucination in structural operations.

---

## 13) Final Output

### AGA Output Schema (`AGAOutput`)

The AGA graph returns an `AGAOutput` TypedDict to the parent pipeline caller:

| Field | Type | Description |
|-------|------|-------------|
| `completed_diagrams` | `list[CompletedDiagram]` | Successfully rendered diagrams (see §4 for type definition) |
| `failed_diagrams` | `list[FailedDiagram]` | Diagrams that exhausted retry limit without successful render |
| `open_questions` | `list[OpenQuestion]` | Passed through from RAA input, unmodified |
| `session_report` | `SessionReport` | Full session metadata |

**`CompletedDiagram`**:

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | Stable canonical ID from the manifest entry (e.g., `ctx-payment_service`) |
| `diagram_type` | `str` | One of: `context`, `container`, `component` |
| `png_bytes` | `bytes` | Rendered PNG image data |
| `plantuml_source` | `str` | The PlantUML source code that generated this diagram. Required by downstream consumers (SA) for sub-tree inclusion validation. |
| `output_path` | `str` | Filesystem path where the PNG was written |

**`FailedDiagram`**:

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | Stable canonical ID from the manifest entry identifying which diagram failed |
| `diagram_type` | `str` | One of: `context`, `container`, `component` |
| `final_error` | `PlantumlErrorRecord` | Last error record before retry limit was exhausted |
| `retry_count` | `int` | Number of correction attempts made |
| `last_puml_code` | `str` | Final PlantUML code that failed (for debugging) |

**`SessionReport`**:

| Field | Type | Description |
|-------|------|-------------|
| `completed_count` | `int` | Number of successfully rendered diagrams |
| `failed_count` | `int` | Number of diagrams that failed |
| `total_diagrams_expected` | `int` | Length of the `diagram_manifest` received from RAA. `completed_count + failed_count` should equal this value; any discrepancy indicates a pipeline fault. |
| `planturl_binary` | `str` | Path to the planturl binary used |
| `detected_os` | `str` | OS/architecture detected at startup |
| `plantuml_server_url` | `str` | PlantUML server URL used |
| `wall_clock_seconds` | `float` | Total execution time |
| `visible_patterns` | `list[str]` | Architectural pattern names from RAA model that are represented in rendered diagrams (traceability check) |

### Per-Diagram Output (Filesystem)
For each successfully rendered diagram:
- **PNG file** saved to the configured output directory, named using the `diagram_id` field from the manifest entry: `{diagram_id}.png`. For example, a context diagram for system `payment_service` is written as `ctx-payment_service.png`; its container diagram as `cnt-payment_service.png`; a component diagram for container `api_gateway` as `cmp-api_gateway.png`. This convention is stable and canonical because `diagram_id` values are themselves stable and canonical (derived from entity IDs in RAA §16).
- **Metadata sidecar** (JSON) alongside each PNG: `{ diagram_id: str, diagram_type: str, plantuml_source: str, encoded_url: str, render_timestamp: str, retry_count: int }`.

### Session Report (Filesystem)
A single `aga_report.json` written to the output directory, containing the serialized `SessionReport` fields defined above.

### Downstream Handoff
The output PNGs and metadata sidecars are the terminal artifacts of the architecture pipeline. They are consumed by the documentation and spec-kit generation stage (outside the scope of this plan).

---

## 14) Failure Modes and Mitigations

| Risk | Mitigation |
|------|------------|
| PlantUML server is down at startup | Availability guard halts immediately; structured exception returned to caller (§11) |
| planturl binary missing or not executable | Startup check raises `BinaryNotExecutableException` before any diagram processing begins (§7) |
| Wrong binary selected for OS | Detection logic covers all five targets; falls back to `linux-gnu` with a warning if libc detection is ambiguous (§7) |
| Syntax error in generated PlantUML | SVG error detection feeds structured error text back to agent; correction loop retries up to `max_retries` (§10) |
| Agent unable to correct within retry limit | Diagram is skipped; failure recorded in session report with `diagram_id` and `diagram_type`; remaining diagrams are still attempted |
| Server returns 5xx transiently | Two submission retries with back-off before classifying as server fault (§9) |
| Large diagram exceeds server rendering time | Read timeout configurable; set to 30s by default; adjustable for complex Component diagrams |
| Reduced-confidence entities cause visual confusion | Marked `[unverified]` in description; visible to diagram reviewer without breaking rendering. Checked per diagram: each diagram's sub-tree is checked independently for `reduced_confidence = true` entities via the `confidence_metadata` lookup. |
| Agent hallucinates entities not in RAA model | Skill prompt explicitly prohibits it; output is validated post-generation against the entities present in the resolved sub-tree for the current diagram before encoding. A global entity ID lookup (across all systems, containers, components, persons, and external systems in the hierarchical model) is used to check any ID referenced in the generated PlantUML code. Additionally, every alias in the generated PlantUML must exactly match a canonical entity ID — abbreviated or invented aliases are rejected as validation failures. |

---

## 15) Validation and Testing Criteria

### Unit Tests
- OS detection returns the correct binary path for each of the five targets given mocked platform/architecture strings.
- `encode_plantuml` produces a non-empty URL string for a valid minimal PlantUML input (`@startuml\nBob -> Alice\n@enduml`).
- `fetch_plantuml_png` correctly classifies a mocked SVG response containing `"Syntax Error"` as a `syntax_error` record.
- `fetch_plantuml_png` raises `ServerUnavailableException` when the HEAD pre-check fails (mocked connection timeout).
- Given a `C4JsonModel` with a `diagram_manifest` of known length and content, the queue builder produces exactly as many `DiagramSpec` entries as manifest entries, in manifest order, with `diagram_id`, `diagram_type`, `focus_entity_id`, and `output_filename` correctly populated. The test must cover a model with multiple systems and multiple containers per system.

### Integration Tests
- End-to-end with a synthetic RAA model containing two systems (each with two containers, each container with two components): agent generates all diagrams in the manifest (2 context + 2 container + 4 component = 8 total), encodes them, and receives successful PNG responses from the live PlantUML server. The specific counts are fixed in the test fixture so that the expected manifest length is deterministic and verifiable.
- Deliberate syntax error injection: agent receives a `syntax_error` record, corrects the code, and successfully renders on retry 2.
- Server unavailability simulation (mocked): agent halts after startup guard, produces a structured failure report, does not enter the diagram loop.

### Functional Tests
- All generated PNGs are valid PNG files (magic bytes check).
- All PlantUML source strings in metadata sidecars successfully round-trip through the PlantUML server (re-encode and fetch without error).
- No entity or relationship appears in any diagram that is not reachable from the focus node's sub-tree in the hierarchical model. The hallucination guard builds a whitelist of valid entity IDs by traversing the full model (all systems, containers, components, persons, external systems) and checks every alias declared in the generated PlantUML against that whitelist.
- For each `DiagramManifestEntry` of type `container`, the generated container diagram includes exactly the containers listed under the focus system's `containers` field and no containers from other systems. For each entry of type `component`, the generated component diagram includes exactly the components listed under the focus container's `components` field and no components from other containers.
- Reduced-confidence entities appear with `[unverified]` in their description in the rendered output.

### SAAM Alignment Check (inherited from RAA)
- The AGA does not perform SAAM evaluation. However, the session report should note which architectural patterns (from the RAA model's pattern rationales) are visible in the rendered diagrams, as a traceability check.

---

## 16) Deliverables for Spec Kit

1. **State schema** — all channels and supporting types (§4)
2. **ReAct agent configuration** — instruction prompt template, tool list, retry policy, halt conditions, focus entity resolution instructions (§5)
3. **C4 PlantUML code generation skill** — generation strategy, boundary grouping rules, reduced-confidence handling, pre-resolved sub-tree contract (§6)
4. **OS detection and binary selection logic** — decision tree, fallback policy, startup check (§7)
5. **`encode_plantuml` tool specification** — invocation arguments, temp file lifecycle, error surface (§8)
6. **`fetch_plantuml_png` tool specification** — SVG error detection strategy, availability guard, retry behaviour (§9)
7. **Error classification table and correction loop policy** — error types, agent responses, retry limits (§10)
8. **Server availability guard and halt specification** — guard timing, halt behaviour, self-hosted override (§11)
9. **Final output schema** — per-diagram files, metadata sidecars, session report structure (§13)
10. **Prompt Resource Bundle** — `c4:plantuml` and `c4:notation` excerpt blocks stored in `aga/prompts/` for AGA skill prompts (extends RAA §21)
