# Data Model Specification: RAA State Contracts

This document details the Python `@dataclass` structures, validation rules, and structural mappings for the RAA State Contracts.

## 1. Dataclasses Schema

All entities are represented as standard Python dataclasses to ensure native compatibility with LangGraph's `JsonPlusSerializer`.

### ArchModel
The final aggregated, C4-compliant architectural model.
- `systems`: `list[ArchSystem]` — Software systems under design.
- `persons`: `list[ArchPerson]` — Human actors.
- `external_systems`: `list[ArchExternalSystem]` — External systems.
- `patterns`: `list[ArchPattern]` — Selected architectural patterns.
- `open_questions`: `list[OpenQuestion]` — Tracking for unresolved conflicts.

### ArchFragment
A partial architecture model representing the output of a single RAA subgraph.
- `systems`: `list[ArchSystem]`
- `containers`: `list[ArchContainer]` (with `parent_system_id`)
- `components`: `list[ArchComponent]` (with `parent_container_id`)
- `persons`: `list[ArchPerson]`
- `external_systems`: `list[ArchExternalSystem]`
- `relationships`: `list[ArchRelationship]`
- `patterns`: `list[ArchPattern]`
- `rationale`: `dict[str, object]` — Subgraph explanation, confidence notes.

### ArchSystem
- `id`: `str` — Canonical ID (lowercase, snake_case).
- `label`: `str` — Human-readable display name.
- `description`: `str`
- `requirement_ids`: `list[int]` — Traced requirement IDs.
- `source_fragment`: `str | null`
- `confidence`: `float | null`
- `context_relationships`: `list[ArchRelationship]`
- `containers`: `list[ArchContainer]`

### ArchContainer
- `id`: `str`
- `label`: `str`
- `description`: `str`
- `technology`: `str | null` — Target technology stack.
- `requirement_ids`: `list[int]`
- `source_fragment`: `str | null`
- `confidence`: `float | null`
- `parent_system_id`: `str` — Parent system association.
- `container_relationships`: `list[ArchRelationship]`
- `components`: `list[ArchComponent]`

### ArchComponent
- `id`: `str`
- `label`: `str`
- `description`: `str`
- `technology`: `str | null`
- `requirement_ids`: `list[int]`
- `source_fragment`: `str | null`
- `confidence`: `float | null`
- `parent_container_id`: `str` — Parent container association.
- `component_relationships`: `list[ArchRelationship]`

### ArchPerson
- `id`: `str`
- `label`: `str`
- `description`: `str`
- `requirement_ids`: `list[int]`
- `source_fragment`: `str | null`
- `confidence`: `float | null`

### ArchExternalSystem
- `id`: `str`
- `label`: `str`
- `description`: `str`
- `technology`: `str | null`
- `requirement_ids`: `list[int]`
- `source_fragment`: `str | null`
- `confidence`: `float | null`

### ArchRelationship
- `source_id`: `str`
- `target_id`: `str`
- `interaction_type`: `str` — Verb phrase (e.g. "sends requests to").
- `technology`: `str | null` — Protocol or communication channel.
- `requirement_ids`: `list[int]`
- `source_fragment`: `str | null`
- `diagram_scope`: `str` — C4 diagram level (`context`, `container`, or `component`).

### ArchPattern
- `name`: `str`
- `rationale`: `str`
- `quality_attributes`: `list[str]`

### OpenQuestion
- `entity_id`: `str | null`
- `type`: `str` — One of `change_risk`, `high_coupling`, `contention`, `tie`, `coverage_gap`, `hierarchy_conflict`, `scope_conflict`.
- `description`: `str`
- `scenario_ids`: `list[str]`

### IncoherentBatchRecord
- `batch_id`: `int`
- `coherence_score`: `float`
- `reduced_confidence`: `bool`

---

## 2. Validation & Boundary Rules

1. **Hierarchy Isolation Constraint**:
   - Every `ArchContainer` must have a non-empty `parent_system_id` linking to a valid `ArchSystem` ID.
   - Every `ArchComponent` must have a non-empty `parent_container_id` linking to a valid `ArchContainer` ID.
   - No ID may be reused across multiple levels (e.g., a system ID cannot be reused as a container or component ID).

2. **Diagram Scope Rules**:
   - `context`: Used when endpoints are between `system`, `person`, or `external_system`.
   - `container`: Used when endpoints are between `container` entities, or between a `container` and `person`/`external_system`.
   - `component`: Used when endpoints are between `component` entities, or between a `component` and `container`/`external_system`.
