# RAA PRD — Phase 2: Output Schemas & Data Structures

**Version:** 1.1
**Status:** Draft
**Depends on:** RAA PRD Phase 1 v1.0
**Changes in 1.1:** Split BatchInput/BatchOutput into discriminated union types,
added merge-strategy annotations on all fields, added Relationship natural key,
added ConcernDefinition type, added [VALIDATE] tags on cross-field constraints,
added §2.1 Field Merge Semantics and §3.4 reference table.
**Scope:** All Python TypedDict definitions for inputs, outputs, intermediate structures,
and registry schemas used by the RAA. No technology choices, prompt templates, error
handling, or folder structure — those belong to later phases.

---

## 1. Overview

This PRD closes every schema gap deferred in Phase 1 §10. Schemas are ordered from
foundational (no intra-document dependencies) to composite. Two cross-cutting decisions apply:

- **Relationships are diagram-level** — a flat `relationships` list lives on each C4 description
  schema, not on individual entity entries.
- **C4 description schemas are self-contained** — they re-express registry data inline while
  preserving `canonical_id` as a foreign-key link for AGA resolution.

---

## 2. Shared Type Aliases

```python
from __future__ import annotations
from typing import TypedDict, NotRequired, Literal

C4Level = Literal["system", "container", "component"]
C4Type  = Literal["service", "database", "gateway", "queue", "store", "external", "actor"]
# "actor": a human user or role that interacts with the system.
# Actors carry no mandatory suffix — the name stands alone (e.g. "EndUser", "SystemAdmin").


class ConcernDefinition(TypedDict):
    concern_id: str
    # Format: "CCG-NNN" (zero-padded). Assigned by the Concern Clustering Graph (CCG) in Phase 1 §6.

    nominal_condition: str
    # The condition under which this concern is operational.
    # Example: "when traffic exceeds 10,000 concurrent users".
```

### 2.1 Field Merge Semantics

Each field belongs to one of five merge strategies that govern how partial updates
combine with existing state. The strategy determines what happens when a later batch
writes to a field that already holds a value from a prior batch.

| Strategy | Behavior |
|----------|----------|
| `overwrite` | New value replaces old value. Default for most scalar and list fields. |
| `append` | New items are concatenated to the existing list. Order is preserved: prior items first, new items second. |
| `append_unique` | Same as `append`, but items already present in the list are skipped. Used for cumulative requirement ID tracking where duplicates would corrupt traceability. |
| `merge_by_key` | Dicts are shallow-merged; keys from the new dict are added, and existing keys are overwritten by the new value. Used for `RegistryEntry.variants` (keyed by `batch_id`) and `RegistrySnapshot.entries` (keyed by `canonical_id`). |
| `never` | The field is immutable after its first write. Any subsequent attempt to set it is a contract violation. Used for identifiers, canonical names, and authority markers. |

Every field carries its merge strategy in its docstring as `[MERGE: <strategy>]`.
A complete reference table appears in §3.4.

---

## 3. Foundational Shared Types

### 3.1 `Relationship`

Level-agnostic diagram edge between two registered entities. Constructed exclusively by the
Judge after deduplication, guaranteeing both endpoints exist in the registry.

**Natural key:** `(source_id, target_id, label)` uniquely identifies a relationship. When two
batches emit the same natural key, the assembler merges them — the later batch's `description`
and `protocol` (if present) supplement the earlier entry. Conflicting `label` values for the
same `(source_id, target_id)` pair are treated as separate relationships.

```python
class Relationship(TypedDict):
    source_id: str
    # canonical_id of the originating entity. Guaranteed to exist in the registry at construction time.
    # [MERGE: never]

    target_id: str
    # canonical_id of the terminating entity. Same guarantee as source_id.
    # [MERGE: never]

    label: str
    # Active-voice verb phrase rendered verbatim on the diagram edge.
    # [VALIDATE] Hard limit: six words. Rejected by output parser if exceeded.
    # Examples: "sends requests to", "reads from", "publishes events to".
    # [MERGE: never]

    description: str
    # Full prose description of what is exchanged and why. Used by AGA for relationship narratives.
    # [MERGE: overwrite] — later batch's description supplements the earlier entry on merge.

    protocol: NotRequired[str]
    # Communication protocol. Examples: "REST/HTTPS", "gRPC", "AMQP", "JDBC".
    # Omitted when no source requirement specifies a protocol.
    # Cross-concern protocol variation → model as two separate Relationship entries.
    # [MERGE: overwrite]
```

### 3.2 `EntityVariant`

Concern-specific attribute overrides stored inside a `RegistryEntry`, keyed by `batch_id`.

```python
class EntityVariant(TypedDict):
    technology: NotRequired[str]
    # Technology stack for this entity under the keying concern.
    # Examples: "PostgreSQL Primary-Replica", "Redis Cluster".
    # Omitted when concern-invariant or inapplicable (actors, most external systems).
    # [MERGE: overwrite] — scalar field within a dict value.

    description_note: NotRequired[str]
    # Concern-specific nuance appended to the canonical description.
    # Example: "In high-traffic mode, operates in read-only failover."
    # [MERGE: overwrite] — scalar field within a dict value.
```

### 3.3 `RegistryEntry`

Canonical, persistent entity record. The Judge is the sole writer. Formalizes Phase 1 §7.3.

```python
class RegistryEntry(TypedDict):
    canonical_id: str
    # Unique identifier. Format: "ENT-NNN" (zero-padded). Assigned at first registration. Immutable.
    # Foreign key in Relationship.source_id / target_id.
    # [VALIDATE] Regex: ^ENT-\d{3,}$
    # [MERGE: never]

    canonical_name: str
    # PascalCase name with mandatory type suffix per Phase 1 §7.5 (actors carry no suffix).
    # Set at first registration. Never overwritten by any subsequent batch (Phase 1 §7.4 Rule 1).
    # [VALIDATE] PascalCase + type suffix (unless c4_type == "actor").
    # [MERGE: never]

    c4_level: C4Level
    # [MERGE: never]

    c4_type: C4Type
    # [MERGE: never]

    source_requirements: list[str]
    # Cumulative list of all requirement IDs referencing this entity, across all batches.
    # Appended on each enrichment — never reset. Complete traceability record.
    # [MERGE: append_unique]

    authority: Literal["asr", "non_asr"]
    # Subgraph class that first established this entity. Set at first registration. Never overwritten.
    # [MERGE: never]

    variants: dict[str, EntityVariant]
    # Concern-specific overrides keyed by batch_id. Empty dict when no variation exists.
    # Variants accumulate across batches — new batch_ids are merged in.
    # [MERGE: merge_by_key]

    description: str
    # Canonical description of this entity's role. Stable across all concerns.
    # Concern-specific nuances belong in variants.description_note, not here.
    # [MERGE: never]
```

### 3.4 Merge Strategy Reference Table

Every field across all schemas is listed below with its merge strategy. Fields not listed
default to `overwrite`.

| Schema | Field | Strategy | Reason |
|--------|-------|----------|--------|
| Relationship | `source_id` | `never` | Natural key component; immutable |
| Relationship | `target_id` | `never` | Natural key component; immutable |
| Relationship | `label` | `never` | Natural key component; immutable |
| Relationship | `description` | `overwrite` | Later batch supplements on merge |
| Relationship | `protocol` | `overwrite` | Later batch supplements on merge |
| EntityVariant | `technology` | `overwrite` | Scalar within dict value |
| EntityVariant | `description_note` | `overwrite` | Scalar within dict value |
| RegistryEntry | `canonical_id` | `never` | Immutable after first registration |
| RegistryEntry | `canonical_name` | `never` | Phase 1 §7.4 Rule 1 |
| RegistryEntry | `c4_level` | `never` | Set at first registration |
| RegistryEntry | `c4_type` | `never` | Set at first registration |
| RegistryEntry | `source_requirements` | `append_unique` | Cumulative across all batches |
| RegistryEntry | `authority` | `never` | Set at first registration |
| RegistryEntry | `variants` | `merge_by_key` | Accumulates per batch_id |
| RegistryEntry | `description` | `never` | Stable across all concerns |
| RegistrySnapshot | `entries` | `merge_by_key` | Dict keyed by canonical_id |
| RegistrySnapshot | `snapshot_after_batch` | `overwrite` | Tracks last batch that wrote |
| RegistryDelta | `new_entries` | `append` | Per-batch delta list |
| RegistryDelta | `enriched_ids` | `append_unique` | Per-batch delta list |
| SystemContextDescription | `relationships` | `append_unique` | Assembler merges across batches |
| SystemContextDescription | `source_requirements` | `append_unique` | Union of sub-field source_requirements |
| ContainerDescription | `containers` | `append_unique` | Assembler merges backbone + concern containers |
| ContainerDescription | `relationships` | `append_unique` | Assembler merges across batches |
| ContainerDescription | `source_requirements` | `append_unique` | Union of sub-field source_requirements |
| ComponentDescription | `components` | `append` | Per-concern list (no cross-batch merge) |
| ComponentDescription | `relationships` | `append_unique` | Per-concern list |
| ComponentDescription | `source_requirements` | `append_unique` | Union of sub-field source_requirements |
| RAAOutput | `coverage_gaps` | `append` | Union across all batches |
| RAAOutput | `conflicts` | `append_filtered` | Union of unresolved only |

---

## 4. Entity Proposal Schemas

### 4.1 `EntityProposal`

Ephemeral structure emitted by ASR and Non-ASR subgraphs. Never persisted directly.
Output parser validates naming compliance before any proposal reaches the Judge.

```python
class EntityProposal(TypedDict):
    proposed_name: str
    # PascalCase name with mandatory type suffix (Phase 1 §7.5), pre-validated by the output parser.
    # Becomes canonical_name in the registry if accepted; discarded entirely if rejected.
    # [VALIDATE] PascalCase + type suffix (unless c4_type == "actor").

    c4_level: C4Level
    c4_type: C4Type

    description: str
    # One-to-two sentence description. Becomes the initial canonical description if accepted.
    # [VALIDATE] 1-2 sentences.

    responsibilities: list[str]
    # Ordered list of what this entity does within its C4 scope.
    # Used by the Judge in SAAM Step 5 to identify load-bearing entities.

    source_requirements: list[str]
    # IDs of requirements in this batch justifying the proposal.
    # [VALIDATE] Must be non-empty. Output parser rejects empty lists (Phase 1 §5).

    proposing_subgraph: Literal["asr", "non_asr"]
    # Maps directly to authority in the registry upon acceptance.
    # In an authority conflict, asr wins; non_asr source_requirements are merged only (Phase 1 §7.4 Rule 3).

    concern_technology: NotRequired[str]
    # Technology scoped to this batch's concern; stored as a variant keyed by batch_id on acceptance.
    # Omitted for actors and technology-agnostic entities.

    justification: str
    # Subgraph's reasoning evaluated by the Judge during SAAM. Not persisted; discarded after evaluation.
```

### 4.2 `JudgedProposal`

The Judge's internal working state during SAAM. Wraps an `EntityProposal` with evaluation
annotations. Never emitted externally; discarded after the batch completes.

```python
class JudgedProposal(TypedDict):
    proposal: EntityProposal
    # The original subgraph proposal, unmodified.

    scenario_classification: Literal["direct", "indirect"]
    # SAAM Step 3. Assigned exclusively by the Judge.
    # direct   → entity is explicitly named or described in a source requirement.
    # indirect → entity is implied by a quality attribute or architectural pattern.

    satisfied_requirements: list[str]
    # Requirement IDs this proposal satisfies (SAAM Step 4).

    conflicts_with: list[str]
    # proposed_names of proposals conflicting with this one (SAAM Step 5).
    # Includes authority conflicts; resolved per Phase 1 §7.4 Rule 3 before registration.
```

---

## 5. Registry Snapshot Schema

```python
class RegistrySnapshot(TypedDict):
    entries: dict[str, RegistryEntry]
    # All registered entities at snapshot time, keyed by canonical_id.
    # Empty dict for the first concern batch's snapshot (no prior registrations exist).
    # [MERGE: merge_by_key]

    snapshot_after_batch: str
    # batch_id of the last batch that wrote before this snapshot. Value is "none" for the first batch.
    # Provides an audit trail of registry lineage across the sequential execution chain.
    # [MERGE: overwrite]
```

---

## 6. C4 Description Sub-Schemas

### 6.1 Supporting Entry Types

Embedded within the three C4 description schemas. Re-express relevant registry data inline,
preserving `canonical_id` as a foreign-key link.

```python
class ActorEntry(TypedDict):
    canonical_id: str               # Foreign key into the Global Entity Registry.
    name: str                       # Canonical name (no suffix for actors).
    # [VALIDATE] No type suffix when c4_type == "actor".
    description: str                # Canonical description from the registry.
    source_requirements: list[str]  # Requirement IDs that surface this actor.


class ExternalSystemEntry(TypedDict):
    canonical_id: str               # Foreign key into the Global Entity Registry.
    name: str                       # canonical_name from the registry (carries "System" suffix).
    description: str                # Canonical description from the registry.
    source_requirements: list[str]  # Requirement IDs that surface this external system.


class ContainerEntry(TypedDict):
    canonical_id: str               # Foreign key into the Global Entity Registry.
    name: str                       # canonical_name from the registry.
    description: str                # Canonical or concern-specific description for this container.
    technology: NotRequired[str]    # Concern-specific technology, sourced from registry variants.
    responsibilities: list[str]     # What this container does within this concern's scope.
    is_backbone: bool
    # True  → originates from the Foundation Batch; present in every L2 diagram.
    # False → specific to this concern's operational mode only.
    # [VALIDATE] Per-batch: all containers in foundation backbone_description MUST have is_backbone=True.
    #            All containers in concern container_description MUST have is_backbone=False.
    source_requirements: list[str]


class ComponentEntry(TypedDict):
    canonical_id: str               # Foreign key into the Global Entity Registry.
    name: str                       # canonical_name from the registry.
    description: str                # Canonical description from the registry.
    technology: NotRequired[str]    # Concern-specific technology, sourced from registry variants.
    responsibilities: list[str]     # What this component does within its parent container.
    interfaces: list[str]
    # Named interaction points this component exposes or consumes.
    # Example: ["REST endpoint /api/auth", "Kafka consumer: user-events"].
    # Empty list (never absent) when no source requirement specifies interface details.
    source_requirements: list[str]
```

### 6.2 `SystemContextDescription` — L1

One instance per RAA run. Assembled last, after all concern and foundation batches complete,
so it reflects the full external interface of the system.

```python
class SystemContextDescription(TypedDict):
    system_name: str
    # Canonical name for the system as a whole, derived from the requirements corpus.

    system_description: str
    # Two-to-three sentence prose description of what the system does and for whom.
    # [VALIDATE] 2-3 sentences.

    system_boundary_description: str
    # What lies inside vs outside the system boundary; which responsibilities are owned
    # by the system vs delegated to external systems.

    actors: list[ActorEntry]
    # All human users and roles interacting with the system (c4_type == "actor" in registry).

    external_systems: list[ExternalSystemEntry]
    # All external software systems the system integrates with (c4_type == "external" in registry).

    relationships: list[Relationship]
    # All L1 diagram edges, connecting actors and external systems to the system boundary.
    # Flat diagram-level list — no relationship is owned by an individual actor or external system.
    # [MERGE: append_unique]

    source_requirements: list[str]
    # Union of all source_requirements across actors, external_systems, and relationships.
    # [VALIDATE] Must equal the set-union of sub-field source_requirements at assembly time.
    # [MERGE: append_unique]
```

### 6.3 `ContainerDescription` — L2

One instance per concern batch plus one from the Foundation Batch (backbone containers).
The RAA assembler merges both into final per-concern L2 descriptions before `RAAOutput`.

```python
class ContainerDescription(TypedDict):
    concern_id: str
    # Identifier of the concern (CCG) this L2 represents. Format: "CCG-NNN".
    # Value is "foundation" for backbone output.

    condition: str
    # The nominal_condition for this concern. Example: "when traffic exceeds 10,000 concurrent users".
    # Value is "under any circumstances" for the foundation backbone description.
    # [VALIDATE] Must equal "under any circumstances" when concern_id == "foundation".

    containers: list[ContainerEntry]
    # Raw batch output: backbone descriptions hold is_backbone=True only; concern outputs hold False only.
    # After RAA assembly: each concern's final description holds the full merged list.
    # [MERGE: append_unique] — Assembler concatenates backbone + concern containers.

    relationships: list[Relationship]
    # All inter-container edges. Flat diagram-level list.
    # [MERGE: append_unique]

    source_requirements: list[str]
    # Union of source_requirements across all containers and relationships.
    # [VALIDATE] Must equal the set-union of sub-field source_requirements at assembly time.
    # [MERGE: append_unique]
```

### 6.4 `ComponentDescription` — L3

One instance per (container, concern) pair. Count is not predetermined — determined by
requirements depth referencing each container.

```python
class ComponentDescription(TypedDict):
    parent_container_id: str
    # canonical_id of the L2 container this component diagram decomposes.

    concern_id: str
    # Concern this L3 description is scoped to. Format: "CCG-NNN".
    # L3 is always concern-scoped — components may differ across operational modes.

    components: list[ComponentEntry]
    # All components within the parent container under this concern's scope.
    # [MERGE: append]

    relationships: list[Relationship]
    # All inter-component edges within this L3 diagram. Flat diagram-level list.
    # Cross-container relationships belong in the L2 diagram, not here.
    # [MERGE: append_unique]

    source_requirements: list[str]
    # Union of source_requirements across all components and relationships.
    # [VALIDATE] Must equal the set-union of sub-field source_requirements at assembly time.
    # [MERGE: append_unique]
```

---

## 7. Batch I/O Schemas

### 7.1 Supporting Entry Types

```python
class ASREntry(TypedDict):
    id: str                         # Requirement ID. Example: "REQ-001".
    text: str                       # Full requirement text, enriched by the Orchestrator.
    quality_attributes: list[str]   # QA labels from ARLO. Example: ["Performance Efficiency"].


class NonASREntry(TypedDict):
    id: str     # Requirement ID.
    text: str   # Full requirement text, enriched by the Orchestrator.


class DecisionEntry(TypedDict):
    selected_pattern: str
    # The winning architectural pattern for this decision slot.
    # Example: "Distributed Cache (Redis)", "Microservices".


class RegistryDelta(TypedDict):
    new_entries: list[RegistryEntry]
    # Entities registered for the first time by this batch's Judge.
    # [MERGE: append]

    enriched_ids: list[str]
    # canonical_ids of existing entries enriched by this batch
    # (new source_requirements or variants appended).
    # [VALIDATE] Must not overlap with new_entries.canonical_id values.
    # [MERGE: append_unique]
```

### 7.2 Batch Input Schemas

Batch input uses a discriminated union on `batch_type`. The Orchestrator constructs the
appropriate concrete type per batch.

```python
class _CommonBatchInputFields(TypedDict):
    batch_id: str
    # Unique identifier.
    # [VALIDATE] Format: "concern_batch_N" (N starting at 1) or "foundation_batch".

    asrs: list[ASREntry]
    # ASRs belonging to this batch's condition group (cluster == -1 for the foundation batch).

    non_asrs: list[NonASREntry]
    # Concern batches: non-ASRs assigned by embedding similarity (Phase 1 §6.4).
    # Foundation batch: orphan non-ASRs below SIMILARITY_THRESHOLD for all concern groups.

    quality_weights: dict[str, int]
    # Global normalized QA priorities from RAAInput.quality_weights. Identical across all batches.

    registry_snapshot: RegistrySnapshot
    # Frozen registry state at the start of this batch. Read-only for subgraphs and Judge.


class ConcernBatchInput(_CommonBatchInputFields):
    batch_type: Literal["concern"]

    decisions: list[DecisionEntry]
    # Concern-level architectural decisions from ARLO. Present for concern batches only.

    condition: str
    # The nominal_condition for this concern. Propagates to ContainerDescription.condition.


class FoundationBatchInput(_CommonBatchInputFields):
    batch_type: Literal["foundation"]
    # No decisions or condition — foundation processes orphan requirements only.


BatchInput = ConcernBatchInput | FoundationBatchInput
```

### 7.3 Batch Output Schemas

Batch output uses a discriminated union on `batch_type`. The assembler narrows on the
discriminator to merge backbone containers into concern L2 descriptions.

```python
class _CommonBatchOutputFields(TypedDict):
    batch_id: str
    registry_delta: RegistryDelta
    coverage_gaps: list[CoverageGap]   # Requirements unsatisfied after SAAM Step 4.
    # [MERGE: append]
    conflicts: list[ConflictRecord]    # Requirement conflicts from SAAM Step 5.
    # [MERGE: append]


class ConcernBatchOutput(_CommonBatchOutputFields):
    batch_type: Literal["concern"]

    container_description: ContainerDescription
    # L2 description for this concern. Concern-specific containers only (all is_backbone=False).
    # The RAA assembler merges backbone containers from the foundation output before RAAOutput.

    component_descriptions: list[ComponentDescription]
    # L3 descriptions for each qualifying container in this concern.
    # Empty list when no container has sufficient component-level requirements.


class FoundationBatchOutput(_CommonBatchOutputFields):
    batch_type: Literal["foundation"]

    system_context_description: SystemContextDescription
    # L1 system context description, assembled after the full registry is populated.

    backbone_description: ContainerDescription
    # Backbone containers shared across all concern L2 diagrams (all is_backbone=True).
    # concern_id is "foundation"; condition is "under any circumstances".


BatchOutput = ConcernBatchOutput | FoundationBatchOutput
```

---

## 8. Coverage Gap & Conflict Records

Produced during SAAM Steps 4 and 5 respectively. Surfaced in `BatchOutput`; unresolved
conflicts propagate to `RAAOutput`.

```python
class CoverageGap(TypedDict):
    requirement_id: str
    # The requirement ID with no satisfying entity after SAAM Step 4.

    requirement_text: str
    # Full text of the unsatisfied requirement. Included for readability without registry lookups.

    batch_id: str
    # The batch in which this gap was detected.
    # [VALIDATE] Format: "concern_batch_N" or "foundation_batch".

    gap_reason: str
    # Judge's explanation of why no surviving entity satisfies this requirement.
    # Example: "No entity addresses the CSV export format implied by this requirement."


class ConflictRecord(TypedDict):
    requirement_ids: list[str]
    # Two or more requirement IDs whose interactions produce this conflict.

    entity_name: str
    # canonical_name of the entity both requirements reference — the locus of the conflict.

    conflict_description: str
    # Judge's prose description of the mutually exclusive behaviors demanded.
    # Example: "REQ-009 requires stateless sessions; REQ-014 requires server-side session persistence."

    batch_id: str
    # [VALIDATE] Format: "concern_batch_N" or "foundation_batch".

    resolution: Literal["asr_wins", "merged", "unresolved"]
    # asr_wins   → authority conflict resolved in favor of the ASR subgraph (Phase 1 §7.4 Rule 3).
    # merged     → non-ASR details folded into the ASR entity; no behavioral conflict remains.
    # unresolved → genuine mutual exclusion requiring human review; propagated to RAAOutput.conflicts.
```

---

## 9. Complete `RAAOutput`

Replaces the placeholder `dict` in Phase 1 §3.

```python
class RAAOutput(TypedDict):
    l1_description: SystemContextDescription
    # Single L1 system context description, assembled after all batches complete.

    l2_descriptions: list[ContainerDescription]
    # One per concern, with backbone containers merged in. Length equals number of concern batches.

    l3_descriptions: list[ComponentDescription]
    # One per (container, concern) pair with sufficient component-level requirements.
    # Not pre-grouped — AGA resolves grouping via parent_container_id and concern_id.

    entity_registry: dict[str, RegistryEntry]
    # Final state of the Global Entity Registry, keyed by canonical_id.
    # [MERGE: merge_by_key]

    coverage_gaps: list[CoverageGap]
    # Union of coverage_gaps across all batch outputs. Empty list if full coverage achieved.
    # [MERGE: append]

    conflicts: list[ConflictRecord]
    # Union of ConflictRecords with resolution == "unresolved". Resolved conflicts are not propagated.
    # [VALIDATE] All entries must have resolution == "unresolved".
    # [MERGE: append_filtered] — Only unresolved conflicts are propagated.
```

---

