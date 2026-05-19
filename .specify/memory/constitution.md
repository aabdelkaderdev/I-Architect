<!--
  SYNC IMPACT REPORT
  ==================
  Version change: 0.0.0 (template) → 1.0.0
  Modified principles: N/A (initial creation from template)
  Added sections:
    - Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)
    - Principle II: Deterministic Data Pipeline
    - Principle III: LLM Isolation & Context Injection
    - Principle IV: Hierarchical Integrity (Orphan Prevention)
    - Principle V: Incremental Coherence (Batch-Sequential Model)
    - Section: Data Contracts & Boundary Rules
    - Section: Development Workflow & Quality Gates
    - Governance section filled
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ reviewed (Constitution Check
      gates align with new principles — no update needed; gates are
      dynamically filled per constitution)
    - .specify/templates/spec-template.md ✅ reviewed (no constitution-
      specific sections to add; FR/SC/Assumption structure is compatible)
    - .specify/templates/tasks-template.md ✅ reviewed (task categorisation
      already supports foundational/story/polish phasing; principle-driven
      task types like "schema validation" and "checkpoint testing" fit
      naturally into existing phases — no template change needed)
  Follow-up TODOs: None
-->

# I-Architect — RAA Subgraph Constitution

## Core Principles

### I. Spec-Driven Architecture (C4 + SAAM Compliance)

Every architectural entity and relationship produced by the RAA pipeline
MUST conform to the C4 model (Context, Container, Component levels) and
MUST be evaluated using the adapted 5-step SAAM process.

- RAA's sole output is a **C4-compliant entity-relationship JSON model**;
  it MUST NOT produce diagrams, code, or PlantUML — those responsibilities
  belong exclusively to the Architecture Generation Agent (AGA).
- Every element (system, container, component, person, external system)
  MUST carry: a canonical ID (lowercase, snake_case), a human-readable
  label, a short description, and clearly labelled relationships.
- Containers and components MUST specify a technology annotation when
  determinable from requirements; otherwise the field MUST be explicitly
  `null`.
- Relationships MUST state direction, an interaction-type verb phrase, and
  an explicit `diagram_scope` value (`context`, `container`, or
  `component`) assigned according to the endpoint-type scoping rules
  (RAA_Plan §12).
- The 5-step SAAM process (partition → map → choose QAs → define scenarios
  → evaluate) MUST be applied in order by the judge node. ARLO quality
  weights MUST inform step 3.
- All prompt-driven nodes MUST reference only the relevant excerpt blocks
  from the Prompt Resource Bundle — never the full bundle or raw source
  documents (RAA_Plan §7).
- Authoritative sources (C4 Model, SAAM SEI Report) are defined in the
  Source Register (RAA_Plan §2A). The direction of authority is:
  **Source Register → Prompt Resource Bundle → skill prompts**.

### II. Deterministic Data Pipeline

All non-LLM pipeline stages MUST produce identical output given identical
input, regardless of execution order, temperature settings, or model
version.

- Embedding vectors MUST be persisted in SQLite databases under
  `embeddings/` at the project root — **never** in LangGraph state
  channels. This keeps checkpoint snapshots lean and avoids serialising
  large float arrays at every super-step boundary.
- ASR and non-ASR embeddings MUST use the same FastEmbed model and version
  (`mixedbread-ai/mxbai-embed-large-v1`, 1024-dimensional) to preserve a
  shared vector space for meaningful cosine similarity.
- Cache integrity MUST be enforced via `text_hash` (SHA-256) columns in
  embedding databases. Stale embeddings (hash mismatch) MUST be
  recomputed, never silently reused.
- Entity deduplication (§13 merge algorithm) MUST operate per entity type
  with canonical ID normalisation (lowercase, snake_case, trimmed). The
  merge steps (deduplication → relationship deduplication → coverage union
  → tree assembly) MUST execute in deterministic order.
- Batch queue ordering, coherence gate scoring, and JSON schema assembly
  MUST be implemented as static templates (deterministic algorithms), not
  LLM-driven nodes.

### III. LLM Isolation & Context Injection

LLM instances MUST be injected via LangGraph's `context={}` dict at
invocation time and MUST NEVER be stored in state channels or serialised
into checkpoint state.

- RAA accepts **4 distinct LLM instances** from the orchestrator: one per
  functional role (`llm_raa_a`, `llm_raa_b`, `llm_raa_c`, `llm_judge`),
  passed via context keys (RAA_Plan §12).
- No uniqueness constraint is enforced — the user may assign the same
  model to all four slots or use different models per role.
- The conditional edge MUST read LLMs from context and forward them to
  each `Send` payload. Nodes MUST access their assigned `ChatModel` from
  `config["context"]`, never from state.
- This follows the orchestrator's mandate (Orchestrator Plan §3C) that LLM
  objects MUST never be serialised into checkpoint state.

### IV. Hierarchical Integrity (Orphan Prevention)

The architecture model MUST be strictly hierarchical: systems contain
containers, containers contain components. No orphaned entities are
permitted at any stage of the pipeline.

- A subgraph MUST NOT propose a component without ensuring a container
  exists (either in the same fragment or in `running_arch_model`) to host
  it. A subgraph MUST NOT propose a container without ensuring a system
  exists to host it.
- Every container MUST record `parent_system_id`; every component MUST
  record `parent_container_id`. These parent IDs MUST resolve to an
  existing entity in either the current fragment or the running model.
- The judge's coverage union step MUST verify parent existence before
  adding any entity from a non-selected fragment. Orphaned entities MUST
  be recorded in `open_questions` with type `coverage_gap` — never
  silently added to the model.
- Hierarchy conflicts (same canonical ID, different parent) MUST be
  recorded in `open_questions` with type `hierarchy_conflict` and MUST NOT
  be silently resolved by last-write-wins.
- No entity ID may appear at more than one level in the hierarchy (a
  system ID MUST NOT also appear as a container or component ID).

### V. Incremental Coherence (Batch-Sequential Model)

Batches MUST be processed sequentially — each batch waits for the previous
batch's judge step before starting. Within each batch, three RAA subgraphs
run in parallel.

- Before each batch's RAA subgraphs run, the current
  `running_arch_model` MUST be injected into all three prompts as hard
  constraints. Subgraphs MUST NOT rename, restructure, or contradict any
  entity or relationship already in the running model (RAA_Plan §15).
- The batch coherence gate (RAA_Plan §10) MUST split or flag batches with
  average intra-batch cosine similarity below 0.55. Incoherent batches
  MUST run as single-RAA (not three-parallel) with `reduced_confidence =
  true` and a 0.5× SAAM weight multiplier applied by the judge.
- Bridge requirements (1–3 per adjacent pair, hard cap: 3) MUST be
  injected into both adjacent batches to ensure cross-batch coherence
  (RAA_Plan §9).
- SQLite checkpointing (via `SqliteSaver`) MUST persist full LangGraph
  state after every super-step. The checkpoint database path MUST be
  received from the orchestrator — the RAA module MUST NOT hardcode or
  assume a default path. `batch_cursor` is the authoritative resume
  marker.
- The final merge (RAA_Plan §16) MUST produce a `diagram_manifest` by
  deterministic hierarchy traversal. The manifest length MUST equal
  `(2 × len(systems)) + sum(len(s.containers) for s in systems)`.

## Data Contracts & Boundary Rules

- **ARLO → RAA boundary:** RAA consumes `ARLOOutput` containing `asrs`,
  `non_asr`, `condition_groups`, and `quality_weights`. RAA also receives
  `requirements` (`dict[str, str]`) from the parent pipeline — this is not
  an ARLO output. All requirement dicts MUST be normalised into the
  unified schema (RAA_Plan §5) before any downstream processing.
- **RAA → AGA boundary:** RAA's output is a single C4-compliant JSON file
  (`arch_model.json`) written to the orchestrator-provided path
  `projects/{project_name}/output/raa/`. The output MUST include a
  `diagram_manifest` as AGA's work queue. AGA MUST NOT need to implement
  filtering or scoping logic.
- **Embedding persistence boundary:** `asr_embeddings.db` is written by
  ARLO and read-only from RAA's perspective. `non_asr_embeddings.db` is
  written and read by RAA during its preparation step. Both MUST use WAL
  mode. No concurrent write contention is possible because ARLO completes
  before RAA starts.
- **Checkpoint boundary:** The checkpoint database path
  (`projects/{project_name}/checkpoints/raa_graph.db`) MUST be received
  from the orchestrator as a required parameter with no default. Directory
  creation is the orchestrator's responsibility.
- **State channel reducers:** Channels written by multiple nodes in the
  same super-step (e.g., `batch_outputs` from three parallel subgraphs)
  MUST use an append or dict-merge reducer. Without a reducer, LangGraph
  applies last-write-wins, which would silently discard outputs.

## Development Workflow & Quality Gates

- **Unit tests** MUST verify: embedding model consistency across ASR and
  non-ASR databases, stale hash detection and recomputation, batch
  assembly completeness, bridge requirement hard caps, coherence gate
  split logic, and per-type entity deduplication with hierarchy conflict
  detection.
- **Integration tests** MUST verify: end-to-end multi-batch execution with
  bridge requirement injection, judge merge consistency against
  `running_arch_model`, and `reduced_confidence` propagation through to
  final output metadata.
- **Functional tests** MUST verify: structural integrity (every container
  nested in a system, every component nested in a container, no cross-
  level ID reuse, all relationship endpoints resolvable, all
  `diagram_scope` values consistent with endpoint types), manifest
  completeness, orphan prevention, and SAAM scoring correctness against
  golden fixtures.
- **Skill reference files** MUST follow the template structure defined in
  RAA_Plan §14: Purpose, Input, Normative rules, Decision guidelines,
  Output schema, Error cases, Examples.
- **Prompt changes** MUST be validated against the Prompt Resource Bundle
  tagging scheme (RAA_Plan §21C) to ensure nodes receive only relevant
  excerpt blocks.

## Governance

This constitution is the authoritative governance document for the RAA
subgraph feature of the I-Architect pipeline. It supersedes ad-hoc
decisions and informal agreements.

- **Amendment procedure:** Any change to this constitution MUST be
  documented with a version bump (MAJOR for principle removals or
  redefinitions, MINOR for new principles or material expansions, PATCH
  for clarifications) and a Sync Impact Report.
- **Compliance review:** All code contributions to the `raa/` directory
  MUST be verified against the principles in this document. The plan
  template's Constitution Check gate MUST reference these principles.
- **Versioning policy:** Semantic versioning (MAJOR.MINOR.PATCH). The
  version line below is the single source of truth for the current
  constitution version.
- **Authoritative plan:** `RAA_Plan.md` (v3) is the authoritative
  technical specification. This constitution encodes the non-negotiable
  subset of that plan as governance rules. Where the plan provides
  flexibility (e.g., `batch_ordering_strategy` configuration), the
  constitution does not constrain — those are implementation decisions.

**Version**: 1.0.0 | **Ratified**: 2026-05-19 | **Last Amended**: 2026-05-19
