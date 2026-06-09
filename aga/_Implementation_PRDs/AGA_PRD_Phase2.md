# Product Requirements Document
## Architecture Generation Agent (AGA) — Phase 2: State Schema & Type Definitions
**Version:** 1.0
**Status:** Draft
**Scope:** All Python type definitions the AGA uses internally and exposes at its boundary. Covers the RAA output representation, the diagram work-item type, the LangGraph state schema (input / internal / output), and the supporting result/error types. No node logic is defined here.

---

## 1. Overview

This phase defines every named type the AGA works with. Types fall into three groups:

1. **RAA-boundary types** — Python representations of the RAA output dict that arrives from the Orchestrator.
2. **Internal work types** — `DiagramSpec` and supporting records used by the queue and agent loop.
3. **LangGraph state schema** — the three schema classes that parameterise the `StateGraph`.

All types are defined in a single file: `aga/schemas.py`. Types are plain Pydantic `BaseModel` or `TypedDict` as appropriate. No business logic lives in this file.

---

## 2. Files Created in This Phase

| File | Purpose |
|------|---------|
| `aga/schemas.py` | All type definitions — RAA boundary types, work types, state schemas |

`aga/graph.py` is updated in this phase to import the state schema and pass it to `StateGraph(...)`. No nodes are wired yet.

---

## 3. RAA Boundary Types

These types mirror the **actual** RAA output structure as observed in `raa_output.pkl`. They are used exclusively by the normalisation node (Phase 6) to validate and parse the raw dict received from the Orchestrator.

> **Note:** The RAA output is a plain `dict`. These types are used for internal documentation clarity and parsing — not for schema enforcement on the incoming dict (which would require the RAA's own Pydantic models as a dependency).

### 3.1 `RAAActorEntry`

Represents one actor from `l1_description["actors"]`.

| Field | Type | Source key |
|-------|------|------------|
| `canonical_id` | `str` | `"canonical_id"` |
| `name` | `str` | `"name"` |
| `description` | `str` | `"description"` |
| `source_requirements` | `list[str]` | `"source_requirements"` |

### 3.2 `RAAExternalSystemEntry`

Represents one entry from `l1_description["external_systems"]`.

| Field | Type | Source key |
|-------|------|------------|
| `canonical_id` | `str` | `"canonical_id"` |
| `name` | `str` | `"name"` |
| `description` | `str` | `"description"` |
| `source_requirements` | `list[str]` | `"source_requirements"` |

### 3.3 `RAARelationshipEntry`

Represents one relationship from any relationship list (L1, L2, or L3).

| Field | Type | Source key |
|-------|------|------------|
| `source_id` | `str` | `"source_id"` |
| `target_id` | `str` | `"target_id"` |
| `label` | `str` | `"label"` |
| `description` | `str` | `"description"` |

### 3.4 `RAAContainerEntry`

Represents one container from an `l2_descriptions[i]["containers"]` list.

| Field | Type | Source key |
|-------|------|------------|
| `canonical_id` | `str` | `"canonical_id"` |
| `name` | `str` | `"name"` |
| `description` | `str` | `"description"` |
| `source_requirements` | `list[str]` | `"source_requirements"` |

### 3.5 `RAAComponentEntry`

Represents one component from an `l3_descriptions[i]["components"]` list.

| Field | Type | Source key |
|-------|------|------------|
| `canonical_id` | `str` | `"canonical_id"` |
| `name` | `str` | `"name"` |
| `description` | `str` | `"description"` |
| `responsibilities` | `list[str]` | `"responsibilities"` |
| `interfaces` | `list[str]` | `"interfaces"` — may be empty |
| `source_requirements` | `list[str]` | `"source_requirements"` |

### 3.6 `RAAL1Description`

Top-level L1 block from `raa_output["l1_description"]`.

| Field | Type | Source key |
|-------|------|------------|
| `system_name` | `str` | `"system_name"` |
| `system_description` | `str` | `"system_description"` |
| `system_boundary_description` | `str` | `"system_boundary_description"` |
| `actors` | `list[RAAActorEntry]` | `"actors"` |
| `external_systems` | `list[RAAExternalSystemEntry]` | `"external_systems"` |
| `relationships` | `list[RAARelationshipEntry]` | `"relationships"` |
| `source_requirements` | `list[str]` | `"source_requirements"` |

### 3.7 `RAAL2Description`

One entry from `raa_output["l2_descriptions"]`.

| Field | Type | Source key |
|-------|------|------------|
| `concern_id` | `str` | `"concern_id"` |
| `condition` | `str` | `"condition"` |
| `containers` | `list[RAAContainerEntry]` | `"containers"` |
| `relationships` | `list[RAARelationshipEntry]` | `"relationships"` |
| `source_requirements` | `list[str]` | `"source_requirements"` |

### 3.8 `RAAL3Description`

One entry from `raa_output["l3_descriptions"]`.

| Field | Type | Source key |
|-------|------|------------|
| `parent_container_id` | `str` | `"parent_container_id"` |
| `concern_id` | `str` | `"concern_id"` |
| `components` | `list[RAAComponentEntry]` | `"components"` |
| `relationships` | `list[RAARelationshipEntry]` | `"relationships"` |
| `source_requirements` | `list[str]` | `"source_requirements"` |

### 3.9 `RAAEntityRegistryEntry`

One entry from `raa_output["entity_registry"]` (keyed by `ENT-NNN`).

| Field | Type | Source key |
|-------|------|------------|
| `canonical_id` | `str` | `"canonical_id"` |
| `canonical_name` | `str` | `"canonical_name"` |
| `c4_level` | `str` | `"c4_level"` — `"system"`, `"container"`, or `"component"` |
| `c4_type` | `str` | `"c4_type"` — e.g. `"service"`, `"database"`, `"gateway"`, `"actor"` |
| `description` | `str` | `"description"` |
| `source_requirements` | `list[str]` | `"source_requirements"` |
| `authority` | `str` | `"authority"` — `"asr"` or `"non_asr"` |
| `variants` | `dict[str, dict]` | `"variants"` — keyed by batch/concern ID |

### 3.10 `RAAOutput`

The fully-typed representation of the RAA output dict. Used by the normalisation node after parsing.

| Field | Type |
|-------|------|
| `l1_description` | `RAAL1Description` |
| `l2_descriptions` | `list[RAAL2Description]` |
| `l3_descriptions` | `list[RAAL3Description]` |
| `entity_registry` | `dict[str, RAAEntityRegistryEntry]` |
| `coverage_gaps` | `list[dict]` — passed through unmodified |
| `conflicts` | `list[dict]` — passed through unmodified |

---

## 4. Internal Work Types

### 4.1 `DiagramType`

A string literal union constraining diagram type values:

```python
DiagramType = Literal["context", "container", "component"]
```

### 4.2 `DiagramSpec`

The unit of work for one diagram. Produced by the queue builder (Phase 3) from the parsed `RAAOutput`.

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | Stable canonical ID. Format: `"ctx"` for context, `"cnt-{concern_id}"` for container, `"cmp-{parent_container_id}-{concern_id}"` for component. |
| `diagram_type` | `DiagramType` | One of `"context"`, `"container"`, `"component"`. |
| `label` | `str` | Human-readable label for logging and sidecars. |
| `output_filename` | `str` | Derived from `diagram_id`: `"{diagram_id}.png"`. |
| `source_l1` | `RAAL1Description \| None` | Populated for context diagrams only. |
| `source_l2` | `RAAL2Description \| None` | Populated for container diagrams only. |
| `source_l3` | `RAAL3Description \| None` | Populated for component diagrams only. |

Exactly one of `source_l1`, `source_l2`, `source_l3` is non-null for a given `DiagramSpec`. The agent uses the non-null source as its resolved sub-tree.

### 4.3 `CompletedDiagram`

A successfully rendered diagram record, accumulated into `AGAInternalState.completed_diagrams`.

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | From `DiagramSpec.diagram_id`. |
| `diagram_type` | `DiagramType` | From `DiagramSpec.diagram_type`. |
| `output_path` | `str` | Absolute filesystem path of the written PNG. |
| `plantuml_source` | `str` | Final PlantUML code that produced this PNG. |
| `retry_count` | `int` | Number of failed render attempts before success (0 = first render attempt succeeded). |

### 4.4 `FailedDiagram`

A diagram that exhausted `max_retries` without successful rendering.

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | From `DiagramSpec.diagram_id`. |
| `diagram_type` | `DiagramType` | From `DiagramSpec.diagram_type`. |
| `last_puml_code` | `str` | Final PlantUML code that failed. |
| `last_error` | `str` | Last error message from the rendering tool. |
| `retry_count` | `int` | Number of render attempts made (will equal `max_retries`). |

### 4.5 `SessionReport`

A summary record assembled at graph exit.

| Field | Type | Description |
|-------|------|-------------|
| `completed_count` | `int` | Number of successfully rendered diagrams. |
| `failed_count` | `int` | Number of diagrams that exceeded the retry limit. |
| `total_diagrams_expected` | `int` | Length of the diagram queue at startup. |
| `output_dir` | `str` | The output directory used for this run. |
| `plantuml_base_url` | `str` | The PlantUML server URL used. |
| `wall_clock_seconds` | `float` | Total elapsed time from graph entry to graph exit. |

---

## 5. LangGraph State Schema

The `StateGraph` is parameterised with three schemas following LangGraph's explicit input/output schema pattern.

### 5.1 `AGAInputState` (TypedDict)

What the Orchestrator passes to `.invoke()`.

| Channel | Type | Description |
|---------|------|-------------|
| `raa_output` | `dict` | Raw RAA output dict, exactly as returned by the RAA graph. The normalisation node (Phase 6) parses this into `RAAOutput`. |

### 5.2 `AGAInternalState` (TypedDict)

The full working state of the graph. All nodes read from and write to this schema.

| Channel | Type | Initialisation | Description |
|---------|------|----------------|-------------|
| `raa_output` | `dict` | Input | Raw input, carried through from `AGAInputState`. |
| `parsed_raa` | `RAAOutput \| None` | Set by `normalise_node` | Parsed and validated RAA output. |
| `diagram_queue` | `list[DiagramSpec]` | Set by `build_queue_node` | Ordered list of diagrams to render. Replaced each loop iteration. |
| `current_diagram` | `DiagramSpec \| None` | Optional; set only while processing | The diagram currently being processed, if the implementation chooses to expose it in state. |
| `current_puml_code` | `str` | Optional; derived from agent messages | PlantUML code string being worked on for the current diagram, if retained in state. |
| `retry_count` | `int` | Optional; derived from tool-call count | Render attempts for the current diagram. Reset implicitly for each diagram because each `agent_loop_node` invocation starts a fresh agent call. |
| `completed_diagrams` | `list[CompletedDiagram]` | Explicitly initialised to `[]` by `normalise_node` | Accumulates successfully rendered diagrams. Uses `Annotated[list, operator.add]` reducer. |
| `failed_diagrams` | `list[FailedDiagram]` | Explicitly initialised to `[]` by `normalise_node` | Accumulates failed diagrams. Uses `Annotated[list, operator.add]` reducer. |
| `session_start_time` | `float` | Set by `build_queue_node` | Unix timestamp recorded before diagram processing. Used to compute `wall_clock_seconds`. |

### 5.3 `AGAOutputState` (TypedDict)

What `.invoke()` returns to the Orchestrator.

| Channel | Type | Description |
|---------|------|-------------|
| `completed_diagrams` | `list[CompletedDiagram]` | All successfully rendered diagrams. |
| `failed_diagrams` | `list[FailedDiagram]` | All diagrams that exceeded the retry limit. |
| `session_report` | `SessionReport` | Summary of the run. |

### 5.4 StateGraph Parameterisation (in `graph.py`)

```python
builder = StateGraph(
    AGAInternalState,
    input_schema=AGAInputState,
    output_schema=AGAOutputState,
)
```

This uses LangGraph's explicit input/output schema pattern so the Orchestrator only sees `AGAInputState` on invoke and `AGAOutputState` on return.

---

## 6. Design Constraints Summary

| Constraint | Rule |
|------------|------|
| RAA types | Plain Pydantic `BaseModel` with no business validation — parsing correctness only |
| `DiagramSpec` source fields | Exactly one of `source_l1`, `source_l2`, `source_l3` is non-null per spec |
| Accumulator channels | `completed_diagrams` and `failed_diagrams` use `Annotated[list, operator.add]` |
| State schema file | All types in `aga/schemas.py` — no type definitions scattered across other modules |
| Output schema | Only `completed_diagrams`, `failed_diagrams`, `session_report` exposed to Orchestrator |
| `coverage_gaps` / `conflicts` | Passed through as raw `list[dict]` — AGA does not interpret them |

`TypedDict` definitions describe channel shape only; they do not provide runtime defaults. Channels that must exist even when empty are initialised explicitly by the graph nodes.

---

## 7. What This Phase Defers

| Concern | Phase |
|---------|-------|
| Queue builder logic (populating `diagram_queue` from `parsed_raa`) | Phase 3 |
| `@tool` adapter for `render_plantuml` | Phase 4 |
| Mustache prompt variable bindings | Phase 5 |
| Node implementations, reducers, edges | Phase 6 |
