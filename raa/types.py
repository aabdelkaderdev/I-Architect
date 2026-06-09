from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

from langchain_core.language_models import BaseChatModel

C4Level = Literal["system", "container", "component"]
"""C4 model hierarchy level: system (top), container (mid), component (bottom)."""

C4Type = Literal["service", "database", "gateway", "queue", "store", "external", "actor"]
"""Element type classification. "actor" carries no mandatory naming suffix — the name stands alone (e.g. "EndUser", "SystemAdmin")."""


class ConcernDefinition(TypedDict):
    concern_id: str
    # Format: "CCG-NNN" (zero-padded). Assigned by the Concern Clustering Graph (CCG).
    nominal_condition: str
    # The condition under which this concern is operational.
    # Example: "when traffic exceeds 10,000 concurrent users".


MergeStrategy = Literal[
    "overwrite", "append", "append_unique", "merge_by_key", "never", "append_filtered"
]
"""Field merge strategy governing how partial batch updates combine with existing state.

Every TypedDict field in downstream state models carries its merge strategy
as ``[MERGE: <strategy>]`` in its docstring.
"""

class EntityVariant(TypedDict):
    """Concern-specific attribute overrides stored inside a RegistryEntry, keyed by batch_id."""

    technology: NotRequired[str]
    # Technology stack for this entity under the keying concern.
    # Examples: "PostgreSQL Primary-Replica", "Redis Cluster".
    # Omitted when concern-invariant or inapplicable (actors, most external systems).
    # [MERGE: overwrite]

    description_note: NotRequired[str]
    # Concern-specific nuance appended to the canonical description.
    # Example: "In high-traffic mode, operates in read-only failover."
    # [MERGE: overwrite]


class RegistryEntry(TypedDict):
    """Canonical, persistent entity record. The Judge is the sole writer."""

    canonical_id: str
    # Unique identifier. Format: "ENT-NNN" (zero-padded). Assigned at first registration. Immutable.
    # Foreign key in Relationship.source_id / target_id.
    # [VALIDATE] Regex: ^ENT-\d{3,}$
    # [MERGE: never]

    canonical_name: str
    # PascalCase name with mandatory type suffix per naming rules (actors carry no suffix).
    # Set at first registration. Never overwritten by any subsequent batch.
    # [VALIDATE] PascalCase + type suffix (unless c4_type == "actor").
    # [MERGE: never]

    c4_level: C4Level
    # C4 abstraction level (system, container, component). Set at first registration.
    # [MERGE: never]

    c4_type: C4Type
    # C4 element type (service, database, gateway, queue, store, external, actor).
    # Set at first registration.
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


class EntityProposal(TypedDict):
    """Ephemeral structure emitted by ASR and Non-ASR subgraphs. Never persisted directly."""

    proposed_name: str
    # PascalCase name with mandatory type suffix, pre-validated by the output parser.
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
    # [VALIDATE] Must be non-empty. Output parser rejects empty lists.

    proposing_subgraph: Literal["asr", "non_asr"]
    # Maps directly to authority in the registry upon acceptance.
    # In an authority conflict, asr wins; non_asr source_requirements are merged only.

    concern_technology: NotRequired[str]
    # Technology scoped to this batch's concern; stored as a variant keyed by batch_id on acceptance.
    # Omitted for actors and technology-agnostic entities.

    justification: str
    # Subgraph's reasoning evaluated by the Judge during SAAM. Not persisted; discarded after evaluation.


class JudgedProposal(TypedDict):
    """The Judge's internal working state during SAAM. Discarded after batch completes."""

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
    # Includes authority conflicts; resolved per authority rules before registration.


class Relationship(TypedDict):
    """Level-agnostic diagram edge between two registered entities.

    Constructed exclusively by the Judge after deduplication,
    guaranteeing both endpoints exist in the registry.
    Natural key: (source_id, target_id, label).
    """

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


class RegistrySnapshot(TypedDict):
    """Point-in-time registry state consumed by the Orchestrator.

    Provides an audit trail of registry lineage across the sequential execution chain.
    """

    entries: dict[str, RegistryEntry]
    # All registered entities at snapshot time, keyed by canonical_id.
    # Empty dict for the first concern batch's snapshot (no prior registrations exist).
    # [MERGE: merge_by_key]

    snapshot_after_batch: str
    # batch_id of the last batch that wrote before this snapshot. Value is "none" for the first batch.
    # Provides an audit trail of registry lineage across the sequential execution chain.
    # [MERGE: overwrite]


class RegistryDelta(TypedDict):
    """Per-batch mutation record emitted by the Judge, consumed by the Assembler for cross-batch state merging."""

    new_entries: list[RegistryEntry]
    # Entities registered for the first time by this batch's Judge.
    # [MERGE: append]

    enriched_ids: list[str]
    # canonical_ids of existing entries enriched by this batch
    # (new source_requirements or variants appended).
    # [VALIDATE] Must not overlap with new_entries.canonical_id values.
    # [MERGE: append_unique]


class ASREntry(TypedDict):
    """Input contract for RAA-A (ASR) subgraph. Ephemeral — never merged across batches."""

    id: str
    # Requirement ID. Example: "REQ-001".

    text: str
    # Full requirement text, enriched by the Orchestrator.

    quality_attributes: list[str]
    # QA labels from ARLO. Example: ["Performance Efficiency"].


class NonASREntry(TypedDict):
    """Input contract for RAA-B (Non-ASR) subgraph. Ephemeral — never merged across batches."""

    id: str
    # Requirement ID. Example: "REQ-042".

    text: str
    # Full requirement text, enriched by the Orchestrator.


class DecisionEntry(TypedDict):
    """Input contract for RAA-C (Decision) subgraph. Ephemeral — never merged across batches."""

    selected_pattern: str
    # The winning architectural pattern for this decision slot.
    # Example: "Distributed Cache (Redis)", "Microservices".


MERGE_STRATEGY_DOCS: dict[MergeStrategy, str] = {
    "overwrite": (
        "New value replaces old value. Default for most scalar and list fields."
    ),
    "append": (
        "New items are concatenated to the existing list. "
        "Order is preserved: prior items first, new items second."
    ),
    "append_unique": (
        "Same as append, but items already present in the list are skipped. "
        "Used for cumulative requirement ID tracking where duplicates would corrupt traceability."
    ),
    "merge_by_key": (
        "Dicts are shallow-merged; keys from the new dict are added, and existing keys "
        "are overwritten by the new value. Used for RegistryEntry.variants (keyed by "
        "batch_id) and RegistrySnapshot.entries (keyed by canonical_id)."
    ),
    "never": (
        "The field is immutable after its first write. Any subsequent attempt to set it "
        "is a contract violation. Used for identifiers, canonical names, and authority markers."
    ),
    "append_filtered": (
        "Same as append, but only items meeting a predicate are concatenated. "
        "Used for RAAOutput.conflicts where only unresolved conflicts propagate."
    ),
}


# ── FG-Phase-05: Batch Input Discriminated Union ───────────────────────


class _CommonBatchInputFields(TypedDict):
    """Shared fields for all batch input types. The Orchestrator constructs the concrete type per batch."""

    batch_id: str
    # Unique identifier.
    # [VALIDATE] Format: "concern_batch_N" (N starting at 1) or "foundation_batch".

    asrs: list[ASREntry]
    # ASRs belonging to this batch's condition group (cluster == -1 for the foundation batch).

    non_asrs: list[NonASREntry]
    # Concern batches: non-ASRs assigned by embedding similarity.
    # Foundation batch: orphan non-ASRs below SIMILARITY_THRESHOLD for all concern groups.

    quality_weights: dict[str, int]
    # Global normalized QA priorities from RAAInput.quality_weights. Identical across all batches.

    registry_snapshot: RegistrySnapshot
    # Frozen registry state at the start of this batch. Read-only for subgraphs and Judge.


class ConcernBatchInput(_CommonBatchInputFields):
    """Batch input for a concern-scoped batch. Carries concern-level decisions and condition."""

    batch_type: Literal["concern"]

    decisions: list[DecisionEntry]
    # Concern-level architectural decisions from ARLO. Present for concern batches only.

    condition: str
    # The nominal_condition for this concern. Propagates to ContainerDescription.condition.


class FoundationBatchInput(_CommonBatchInputFields):
    """Batch input for the foundation batch. Processes orphan requirements only — no decisions or condition."""

    batch_type: Literal["foundation"]


BatchInput = ConcernBatchInput | FoundationBatchInput
"""Discriminated union on ``batch_type`` for all batch input variants."""


# ── FG-Phase-07a: CoverageGap & ConflictRecord ─────────────────────────
# (needed by FG-Phase-06 batch output types)


class CoverageGap(TypedDict):
    """Requirement with no satisfying entity after SAAM Step 4. Surfaced in BatchOutput; propagates to RAAOutput."""

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
    """Conflict between two or more requirements detected during SAAM Step 5. Unresolved conflicts propagate to RAAOutput."""

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
    # asr_wins   → authority conflict resolved in favor of the ASR subgraph.
    # merged     → non-ASR details folded into the ASR entity; no behavioral conflict remains.
    # unresolved → genuine mutual exclusion requiring human review; propagated to RAAOutput.conflicts.


# ── FG-Phase-06: Batch Output Discriminated Union ──────────────────────


class _CommonBatchOutputFields(TypedDict):
    """Shared fields for all batch output types. The assembler narrows on the discriminator."""

    batch_id: str
    registry_delta: RegistryDelta
    coverage_gaps: list[CoverageGap]
    # Requirements unsatisfied after SAAM Step 4.
    # [MERGE: append]
    conflicts: list[ConflictRecord]
    # Requirement conflicts from SAAM Step 5.
    # [MERGE: append]


class ConcernBatchOutput(_CommonBatchOutputFields):
    """Batch output for a concern-scoped batch. Carries L2 and L3 descriptions for this concern."""

    batch_type: Literal["concern"]

    container_description: ContainerDescription
    # L2 description for this concern. Concern-specific containers only (all is_backbone=False).
    # The RAA assembler merges backbone containers from the foundation output before RAAOutput.

    component_descriptions: list[ComponentDescription]
    # L3 descriptions for each qualifying container in this concern.
    # Empty list when no container has sufficient component-level requirements.


class FoundationBatchOutput(_CommonBatchOutputFields):
    """Batch output for the foundation batch. Carries L1 context and backbone L2 descriptions."""

    batch_type: Literal["foundation"]

    system_context_description: SystemContextDescription
    # L1 system context description, assembled after the full registry is populated.

    backbone_description: ContainerDescription
    # Backbone containers shared across all concern L2 diagrams (all is_backbone=True).
    # concern_id is "foundation"; condition is "under any circumstances".


BatchOutput = ConcernBatchOutput | FoundationBatchOutput
"""Discriminated union on ``batch_type`` for all batch output variants."""


# ── FG-Phase-08: C4 Supporting Entry Types ─────────────────────────────


class ActorEntry(TypedDict):
    """Inline entry re-expressing registry actor data for L1 diagrams. Preserves canonical_id as foreign key."""

    canonical_id: str
    # Foreign key into the Global Entity Registry.

    name: str
    # Canonical name (no suffix for actors).
    # [VALIDATE] No type suffix when c4_type == "actor".

    description: str
    # Canonical description from the registry.

    source_requirements: list[str]
    # Requirement IDs that surface this actor.


class ExternalSystemEntry(TypedDict):
    """Inline entry re-expressing registry external system data for L1 diagrams."""

    canonical_id: str
    # Foreign key into the Global Entity Registry.

    name: str
    # canonical_name from the registry (carries "System" suffix).

    description: str
    # Canonical description from the registry.

    source_requirements: list[str]
    # Requirement IDs that surface this external system.


class ContainerEntry(TypedDict):
    """Inline entry re-expressing registry container data for L2 diagrams."""

    canonical_id: str
    # Foreign key into the Global Entity Registry.

    name: str
    # canonical_name from the registry.

    description: str
    # Canonical or concern-specific description for this container.

    technology: NotRequired[str]
    # Concern-specific technology, sourced from registry variants.

    responsibilities: list[str]
    # What this container does within this concern's scope.

    is_backbone: bool
    # True  → originates from the Foundation Batch; present in every L2 diagram.
    # False → specific to this concern's operational mode only.
    # [VALIDATE] Per-batch: all containers in foundation backbone_description MUST have is_backbone=True.
    #            All containers in concern container_description MUST have is_backbone=False.

    source_requirements: list[str]


class ComponentEntry(TypedDict):
    """Inline entry re-expressing registry component data for L3 diagrams."""

    canonical_id: str
    # Foreign key into the Global Entity Registry.

    name: str
    # canonical_name from the registry.

    description: str
    # Canonical description from the registry.

    technology: NotRequired[str]
    # Concern-specific technology, sourced from registry variants.

    responsibilities: list[str]
    # What this component does within its parent container.

    interfaces: list[str]
    # Named interaction points this component exposes or consumes.
    # Example: ["REST endpoint /api/auth", "Kafka consumer: user-events"].
    # Empty list (never absent) when no source requirement specifies interface details.

    source_requirements: list[str]


# ── FG-Phase-09: C4 Description Schemas (L1, L2, L3) ───────────────────


class SystemContextDescription(TypedDict):
    """L1 system context diagram description. One instance per RAA run, assembled after all batches complete."""

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


class ContainerDescription(TypedDict):
    """L2 container diagram description. One per concern batch plus one from the Foundation Batch (backbone)."""

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
    # [MERGE: append_unique]

    relationships: list[Relationship]
    # All inter-container edges. Flat diagram-level list.
    # [MERGE: append_unique]

    source_requirements: list[str]
    # Union of source_requirements across all containers and relationships.
    # [VALIDATE] Must equal the set-union of sub-field source_requirements at assembly time.
    # [MERGE: append_unique]


class ComponentDescription(TypedDict):
    """L3 component diagram description. One per (container, concern) pair."""

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


# ── FG-Phase-07b: RAAOutput ────────────────────────────────────────────


class RAAOutput(TypedDict):
    """Final aggregated output of a full RAA run, assembled after all batches complete."""

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
    # [MERGE: append_filtered]


# ── FG-Phase-02 (supplement): Merge Strategy Reference Table ───────────


MERGE_REFERENCE_TABLE: list[dict[str, str]] = [
    # Relationship
    {"schema": "Relationship", "field": "source_id", "strategy": "never", "reason": "Natural key component; immutable"},
    {"schema": "Relationship", "field": "target_id", "strategy": "never", "reason": "Natural key component; immutable"},
    {"schema": "Relationship", "field": "label", "strategy": "never", "reason": "Natural key component; immutable"},
    {"schema": "Relationship", "field": "description", "strategy": "overwrite", "reason": "Later batch supplements on merge"},
    {"schema": "Relationship", "field": "protocol", "strategy": "overwrite", "reason": "Later batch supplements on merge"},
    # EntityVariant
    {"schema": "EntityVariant", "field": "technology", "strategy": "overwrite", "reason": "Scalar within dict value"},
    {"schema": "EntityVariant", "field": "description_note", "strategy": "overwrite", "reason": "Scalar within dict value"},
    # RegistryEntry
    {"schema": "RegistryEntry", "field": "canonical_id", "strategy": "never", "reason": "Immutable after first registration"},
    {"schema": "RegistryEntry", "field": "canonical_name", "strategy": "never", "reason": "Phase 1 §7.4 Rule 1"},
    {"schema": "RegistryEntry", "field": "c4_level", "strategy": "never", "reason": "Set at first registration"},
    {"schema": "RegistryEntry", "field": "c4_type", "strategy": "never", "reason": "Set at first registration"},
    {"schema": "RegistryEntry", "field": "source_requirements", "strategy": "append_unique", "reason": "Cumulative across all batches"},
    {"schema": "RegistryEntry", "field": "authority", "strategy": "never", "reason": "Set at first registration"},
    {"schema": "RegistryEntry", "field": "variants", "strategy": "merge_by_key", "reason": "Accumulates per batch_id"},
    {"schema": "RegistryEntry", "field": "description", "strategy": "never", "reason": "Stable across all concerns"},
    # RegistrySnapshot
    {"schema": "RegistrySnapshot", "field": "entries", "strategy": "merge_by_key", "reason": "Dict keyed by canonical_id"},
    {"schema": "RegistrySnapshot", "field": "snapshot_after_batch", "strategy": "overwrite", "reason": "Tracks last batch that wrote"},
    # RegistryDelta
    {"schema": "RegistryDelta", "field": "new_entries", "strategy": "append", "reason": "Per-batch delta list"},
    {"schema": "RegistryDelta", "field": "enriched_ids", "strategy": "append_unique", "reason": "Per-batch delta list"},
    # SystemContextDescription
    {"schema": "SystemContextDescription", "field": "relationships", "strategy": "append_unique", "reason": "Assembler merges across batches"},
    {"schema": "SystemContextDescription", "field": "source_requirements", "strategy": "append_unique", "reason": "Union of sub-field source_requirements"},
    # ContainerDescription
    {"schema": "ContainerDescription", "field": "containers", "strategy": "append_unique", "reason": "Assembler merges backbone + concern containers"},
    {"schema": "ContainerDescription", "field": "relationships", "strategy": "append_unique", "reason": "Assembler merges across batches"},
    {"schema": "ContainerDescription", "field": "source_requirements", "strategy": "append_unique", "reason": "Union of sub-field source_requirements"},
    # ComponentDescription
    {"schema": "ComponentDescription", "field": "components", "strategy": "append", "reason": "Per-concern list (no cross-batch merge)"},
    {"schema": "ComponentDescription", "field": "relationships", "strategy": "append_unique", "reason": "Per-concern list"},
    {"schema": "ComponentDescription", "field": "source_requirements", "strategy": "append_unique", "reason": "Union of sub-field source_requirements"},
    # RAAOutput
    {"schema": "RAAOutput", "field": "coverage_gaps", "strategy": "append", "reason": "Union across all batches"},
    {"schema": "RAAOutput", "field": "conflicts", "strategy": "append_filtered", "reason": "Union of unresolved only"},
]
"""Complete merge strategy reference for every field across all schemas. Fields not listed default to ``overwrite``."""


# ── FG-Phase-10: RAAConfigSchema & LLM Configuration Strategy ──────────


class RAAConfigSchema(TypedDict, total=False):
    """Runtime configuration injected via ``RunnableConfig.configurable`` at graph invocation time.

    LLM instances are never injected at graph construction time and never stored in graph state.
    Every LLM-calling node resolves its designated model from ``config["configurable"]`` and
    binds it to a structured output model via ``with_structured_output`` inside the node body.
    """

    asr_llm: BaseChatModel
    # LLM instance for the ASR Subgraph. Binds to a Pydantic model wrapping list[EntityProposal].

    non_asr_llm: BaseChatModel
    # LLM instance for the Non-ASR Subgraph. Binds to a Pydantic model wrapping list[EntityProposal].

    judge_llm: BaseChatModel
    # LLM instance for the Judge. Uses separate structured output models per SAAM step.

    thread_id: str
    # LangGraph checkpoint namespace for conversation persistence.

    db_path: str
    # SqliteSaver path, e.g. "./raa_checkpoint.db".


# ── FG-Phase-40: RAAInput (Orchestrator boundary type) ────────────────


class RAAInput(TypedDict):
    """Minimal, non-redundant transformation of ARLO's raw output into four fields.

    Constructed by the Orchestrator. Contains all data needed for embedding,
    batch construction, and graph evaluation.
    """

    condition_groups: list[dict]
    # Primary working structure. All ASRs organized by semantically equivalent
    # conditions. The cluster == -1 group is the conditionless group.
    # Each group dict has: cluster (int), nominal_condition (str), requirements (list[{id, text}]).

    concerns: list[dict]
    # Optimizer output from ARLO, stripped to essentials. One concern per
    # co-satisfiable condition group (CCG). Each concern carries the winning
    # architectural pattern per decision.

    non_asr: list[NonASREntry]
    # Requirements dismissed by ARLO as non-architecturally significant.
    # Enriched by the Orchestrator from bare IDs to {id, text} dicts.

    quality_weights: dict[str, int]
    # Global normalized QA priorities derived from ASR frequency across the
    # entire system. Example: {"Security": 20, "Performance Efficiency": 40}.
