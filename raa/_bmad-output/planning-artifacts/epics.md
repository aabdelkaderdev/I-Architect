---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md'
  - '_bmad-output/planning-artifacts/architecture.md'
  - 'raa_module_specification.md'
---

# raa - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for raa, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

* **FR1: Requirement Normalization & Enrichment**
  * String IDs are standardized (e.g., ARLO integer ID `5` -> RAA string ID `"R5"`).
  - ASR and Non-ASR IDs are matched against the orchestrator-provided `requirements: dict[str, str]` to retrieve authoritative description text.
  - ARLO-provided ASR description text is fallback-only when the original requirements mapping has no usable entry for that requirement ID.
  - Non-ASR payloads default `is_asr = false`, `quality_attributes = []`, and `condition_text = null`.
* **FR2: SQLite Embedding Generation and Cache Verification**
  - RAA initializes FastEmbed using `cache_dir = "../models"` (resolved as `/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/models`).
  - If the model files do not exist at the local cache directory, RAA throws an explicit model non-existent exception immediately.
  - Separate SQLite tables store ASR and Non-ASR embeddings.
  - If a text hash matches the cached database entry, embedding generation is skipped for that requirement.
  - Once verified/generated, `embeddings_ready` is set to `true`, gating downstream graph nodes.
* **FR3: Centroid-Anchored Batch Construction**
  - The Batch Construction node queries the SQLite embedding cache to compute a condition group's centroid as the mean vector of the group's ASR embeddings.
  - Nearest-neighbor search retrieves non-ASR candidates with cosine similarity $\ge 0.65$.
  - Non-ASR candidates are capped at a maximum of 10 per batch.
* **FR4: Overlap Bridging**
  - The Overlap Bridging node identifies related condition groups (sharing a cluster ID or with centroid cosine similarity $\ge 0.65$) and injects shared bridge requirements.
  - Inserts 1 to 3 (hard cap: 3) highly similar non-ASRs into both adjacent batches.
  - Bridge requirement mappings are recorded in the graph's `bridge_requirements` channel.
* **FR5: Coherence Gating and Splitting**
  - The Coherence Gate verifies that the average cosine similarity of a batch's requirement embeddings relative to its centroid is $\ge 0.55$.
  - If a batch score is $< 0.55$, RAA attempts to split it into two sub-clusters. If both sub-clusters pass, the original batch is replaced by two sub-batches.
  - If a split batch remains incoherent, it is run as a single-strategy batch (no parallel strategies) and marked with `reduced_confidence = true` (which applies a $0.5\times$ multiplier to its SAAM scoring).
* **FR6: Queue Ordering**
  - The Batch Queue Ordering node sequences the execution queue according to risk weights associated with requirement quality attributes.
  - Security and reliability batches are sequenced to execute first.
  - Alternative sorting strategies (ASR count, quality weight frequency) are selectable via input parameters.
  - Leftover requirements not assigned to any batch are isolated in the `unprocessed_requirements` list.
* **FR7: Strategy-Parallel Subgraph Dispatch**
  - The RAA Execution Loop concurrently spawns three parallel subgraphs: RAA-A (SAAM-first), RAA-B (Pattern-Driven), and RAA-C (Entity/Relationship-Driven).
  - Maps parent state variables to each instance.
  - Exception: Incoherent batches (`reduced_confidence = true`) run as a single-strategy call (RAA-A only).
* **FR8: C4 Metamodel Hierarchy Enforcement**
  - Each subgraph must output an `ArchFragment` that strictly adheres to the C4 standard structure.
  - Containers must carry a valid `parent_system_id`.
  - Components must carry a valid `parent_container_id`.
  - Relationship scopes (`context`, `container`, `component`) must match their endpoint entity types.
* **FR9: Concurrent WAL-Enabled State Persistence**
  - All concurrent subgraph executions persist state to SQLite checkpoints using Write-Ahead Logging (WAL).
  - Private states and intermediate LLM outputs are isolated by subgraph run IDs.
* **FR10: SAAM-First Fragment Scoring**
  - The Judge scores each subgraph's fragment using ARLO's quality weights to select the primary model structure.
  - The highest-scoring fragment is designated as the primary.
  - If a batch was incoherent, the Judge applies a $0.5\times$ multiplier to its score.
* **FR11: Conservative Entity Deduplication and C4 Boundary Grouping**
  - Semantic similarity is calculated using SQLite-cached container descriptions.
  - If cosine similarity is $\ge 0.80$ and `requirement_ids` overlap, the entities are merged (longest description wins; technology tags are unioned).
  - If cosine similarity is $0.60$ to $0.80$, the Judge clusters the containers into logical C4 boundary groupings in the JSON output (preventing destructive merging of distinct deployment units).
  - Moderate-similarity entities are flagged with an `assumption_flag` or written to the `change_risk` / `high_coupling` open question list.
* **FR12: Cross-Cutting Concern Promotion**
  - The Judge identifies cross-cutting candidates in the `ArchFragments` and promotes them to concrete structural boundary components.
  - Affected relationship arrows are updated to point directly to the promoted component.
  - The cross-cutting requirement is mapped to the promoted component's `requirement_ids` rather than being repeated on all arrows.
* **FR13: SAAM Score Calibration**
  - A `saam_score` of `1.0` is reserved *only* for entities that have a component-level diagram, no functional overlap with other entities, and all direct scenarios passing.
  - Deduplicated or overlapping entities receive a reduced SAAM score.
* **FR14: Open Question Classification & Payload Emission**
  - Questions are categorized by type: `change_risk`, `high_coupling`, `coverage_gap` are flagged as `human_preferred`; `contention`, `tie`, `hierarchy_conflict`, `scope_conflict` are flagged as `judge_resolvable`.
  - Pre-computed suggestions are automatically generated for all `judge_resolvable` entries.
  - The `human_review_payload` channel is populated with: open question contexts, a model summary (entity counts, system names), and the pre-computed resolutions.
* **FR15: Indefinite LangGraph Interrupt**
  - If `review_mode = interactive`, a LangGraph interrupt is raised, suspending the graph indefinitely. The execution does *not* time out automatically.
  - If `review_mode = autonomous`, the interrupt is bypassed, and the graph proceeds immediately to Phase 8.
* **FR16: Authoritative Human Answer Mapping**
  - The RAA Orchestrator applies human answers authoritatively to resolve open questions, overriding any pre-computed Judge suggestions.
  - Applied human answers are marked in the final output with `assumption_flag = false`.
  - Structurally invalid human text directions are caught by the Judge, logged as a `scope_conflict`, and resolved using fallback constraints.
* **FR17: Principled Open Question Resolution**
  - The Judge resolves all remaining questions, ensuring no question in the final output has a `null` resolution.
  - For unresolved `human_preferred` questions, the Judge drafts a documented assumption based on the requirements text and sets `assumption_flag = true`.
  - For unresolved `judge_resolvable` questions, the Judge applies its pre-computed suggestions and sets `assumption_flag = false`.
* **FR18: Residual Requirements Decision Ladder**
  - The Judge evaluates each element in `unprocessed_requirements` sequentially against the merged model using semantic and coupling criteria.
  - Similarity > 0.75: Auto-enrich the matching C4 container description and append the requirement ID.
  - Similarity 0.50–0.75: Check if the requirement shares actors or data flows with the container. If coupled, enrich the container and log an `assumption_flag`. If not, exclude and flag as a human review query.
  - Similarity < 0.50: If it implies architectural structure, propose a new minimal C4 entity and its relationships. If non-architectural (e.g. process/tooling complexity), exclude the requirement and log it as a `coverage_gap` open question with a one-sentence rationale.
* **FR19: 100% Requirements Accounting Audit**
  - Before finalization, RAA audits requirement traceability to verify that every input requirement ID is represented exactly once (in a batch, a mapped container/component, or a `coverage_gap` open question).
  - Bulk acceptance or bulk rejection of leftovers is prohibited.
* **FR20: Diagram Manifest Construction & C4 JSON Schema Validation**
  - A C4-compliant schema validation check is run against the generated model.
  - A diagram manifest is generated with length exactly equal to `(2 * number of systems) + total containers across all systems`.
  - Outputs are written to the output directory, and frontmatter `status` is updated to `final`.

### NonFunctional Requirements

* **NFR1: Reliability - Checkpoint Recovery**
  * Support 100% checkpoint recovery from the last completed batch without state corruption or duplicate writes.
* **NFR2: Reliability - Zero Loss**
  * Ensure 100% requirements accounting (zero silent requirement drops) from raw inputs to output mappings.
* **NFR3: Data Integrity - Entity Deduplication**
  * Maintain entity deduplication precision with less than a 5% duplicate entity rate in the output model.
* **NFR4: Data Integrity - CQRS Boundaries**
  * Guarantee zero CQRS boundary violations through boundary grouping instead of destructive merging.
* **NFR5: Correctness - Metamodel Validation**
  * Strict C4 JSON schema validation on every run; strict hierarchy enforcement across all systems, containers, and components.
* **NFR6: Performance - CPU-Only Embedding**
  * Embedding computation must be CPU-only and O(n) per requirement using local FastEmbed cache.
* **NFR7: Performance - Memory Footprint**
  * Query embedding database by batch size (not full-corpus) to keep memory usage proportional to batch size.
* **NFR8: Concurrency - WAL Checkpoint**
  * Support 3 parallel subgraph writes to the SQLite checkpoint database concurrently without locking delays or thread contention.
* **NFR9: Determinism**
  * Merging, deduplication, tree assembly, and manifest generation must be deterministic algorithms (no LLM involvement in these specific steps).

### Additional Requirements

* **AR1: Shared Parent Execution Environment**
  * RAA must run in the parent project's shared virtual environment and be registered as a discoverable package in `pyproject.toml` (`include = ["arlo*", "raa*"]`).
* **AR2: Typed State Channels & Reducers**
  * LangGraph state channels must use typed `TypedDict` schemas. Append-merge reducers must be configured for concurrent-write channels (`batch_outputs`, `open_questions`, `incoherent_batches`).
* **AR3: Embedding Cache Decoupling**
  * All 1024-dimensional dense vectors must be stored in external SQLite databases on disk (`asr_embeddings.db`, `non_asr_embeddings.db`) instead of the LangGraph state channels.
* **AR4: Embedding Cache Abstraction**
  * All SQLite database read/write logic must be encapsulated in an `EmbeddingCache` class; operational nodes are prohibited from direct connection calls.
* **AR5: Dynamic LLM Runtime Injection**
  * Inject LLM wrappers dynamically through the `RunnableConfig` pattern via the `config` parameter (`config["configurable"]["<role>_llm"]`) rather than hardcoding.
* **AR6: Parallel dispatch**
  * Dispatch the three parallel subgraphs concurrently as async coroutines using `asyncio.gather`.
* **AR7: Fallback Single-Strategy Routing**
  * Incoherent batches (`reduced_confidence = true`) route to a single-strategy call (RAA-A SAAM-First only) with a 0.5× SAAM weight multiplier.
* **AR8: Indefinite LangGraph Interrupt**
  * Implement the Human Review Gate using standard LangGraph `interrupt()` to suspend execution indefinitely. Resume must use the standard `Command(resume=...)` API.
* **AR9: Type-Safe Structured Outputs**
  * Enforce LLM outputs via Pydantic v2 schemas using `with_structured_output(Model, include_raw=True)`.
* **AR10: Prompt Template Decoupling**
  * Externalize LLM prompts as Mustache `.md` files in `prompts/` and render at runtime using `chevron.render()`.
* **AR11: Excerpt-Based Prompt Policy**
  * Injected prompt templates must contain only relevant, tag-based excerpts (≤25 words each) rather than copying full reference documents.
* **AR12: Type-Safe Unit Testing**
  * Node unit tests must use LangChain's `GenericFakeChatModel` with pre-defined outputs, ensuring zero external network calls.

### UX Design Requirements

* **UX-DR1: None**
  * The RAA module is a pure Python backend processing pipeline and does not expose a user interface.

### FR Coverage Map

* **FR1:** Epic 1 - Ingestion & Normalization
* **FR2:** Epic 1 - SQLite Embedding Cache Creation
* **FR3:** Epic 1 - Centroid-Anchored Batch Construction
* **FR4:** Epic 1 - Overlap Bridging
* **FR5:** Epic 1 - Coherence Gating & Splitting
* **FR6:** Epic 1 - Risk-First Priority Queue Ordering
* **FR7:** Epic 2 - Parallel Subgraph Dispatch
* **FR8:** Epic 2 - C4 Hierarchy Enforcement
* **FR9:** Epic 2 - WAL Concurrent Checkpointing
* **FR10:** Epic 2 - SAAM Scenario Fragment Scoring
* **FR11:** Epic 2 - Semantic Deduplication & Boundary Grouping
* **FR12:** Epic 2 - Cross-Cutting Concern Promotion
* **FR13:** Epic 2 - SAAM Score Calibration
* **FR14:** Epic 3 - Human Review Payload Emission
* **FR15:** Epic 3 - LangGraph Interrupt Node
* **FR16:** Epic 3 - Human Answer Override Mapping
* **FR17:** Epic 4 - Principled Question Resolution & Assumptions
* **FR18:** Epic 4 - Residual Requirements Decision Ladder
* **FR19:** Epic 4 - 100% Requirements Traceability Audit
* **FR20:** Epic 4 - C4 Metamodel Validation & Manifest Compile

## Epic List

### Epic 1: Ingestion, Normalization, and Centroid-Anchored Batching (Phases 1–5)
Ingest raw requirements, verify or build vector embeddings, partition requirements into semantic batches, inject overlap bridges, and establish a risk-ordered execution queue.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6

### Epic 2: Strategy-Parallel Subgraph Execution and Judge Reconciliation (Phase 6)
Process requirement batches through three parallel analysis subgraphs (SAAM-first, pattern-driven, entity-driven) and reconcile their outputs via a Judge node using semantic deduplication, CQRS protection, and cross-cutting concern promotion.
**FRs covered:** FR7, FR8, FR9, FR10, FR11, FR12, FR13

### Epic 3: Interactive Human Review Gate (Phase 7)
Emit review payloads and halt execution with LangGraph interrupts for high-priority open questions in interactive mode, allowing authoritative human input with a fallback autonomous bypass.
**FRs covered:** FR14, FR15, FR16

### Epic 4: Global Consolidation, Residual Pass, and Validation (Phase 8)
Perform a global merge of all batch outputs, apply answers or draft documented assumptions, process leftovers in a residual pass, verify 100% requirements accounting, and validate the C4 JSON schema and diagram manifest.
**FRs covered:** FR17, FR18, FR19, FR20

## Epic 1: Ingestion, Normalization, and Centroid-Anchored Batching (Phases 1–5)

To ingest raw requirements, verify or build vector embeddings, partition requirements into semantic batches, inject overlap bridges, and establish a risk-ordered execution queue.

### Story 1.1: Input Normalization and Enrichment

As a Pipeline Engineer,
I want to normalize and enrich raw ASR and Non-ASR requirements,
So that all downstream nodes receive standardized requirement records.

**Acceptance Criteria:**

**Given** a raw ARLO output dictionary containing `asrs` (with integer IDs, QAs, and condition text) and `non_asr` (with list of bare string IDs), and orchestrator-provided `requirements: dict[str, str]` containing the original full requirement set (ID to description mapping)
**When** the normalization node is executed
**Then** it must transform all integer IDs to string IDs (e.g., ARLO ID `5` becomes `"R5"`)
**And** it must resolve description text for both ASR and Non-ASR requirements using the original requirements mapping, matching both raw and normalized requirement ID forms
**And** it may use ARLO-provided ASR description text only as a fallback when the original requirements mapping has no usable entry
**And** it must enrich Non-ASR requirement records with default values: `is_asr = false`, `quality_attributes = []`, and `condition_text = null`
**And** it must return a list of standardized requirement records matching the input IDs.

### Story 1.2: SQLite Embedding Caching and Verification

As a Pipeline Engineer,
I want to cache dense vector embeddings for requirements in external SQLite databases,
So that we prevent redundant vector computation and keep LangGraph checkpoints lean.

**Acceptance Criteria:**

**Given** normalized requirements and a runtime-configured path for the ASR and Non-ASR embedding SQLite databases
**When** the preparation node generates embeddings using FastEmbed and `mixedbread-ai/mxbai-embed-large-v1`
**Then** it must check if the pre-cached model files exist in the `cache_dir = "../models"`
**And** it must raise an explicit `ModelNonExistentException` immediately if the model files are absent
**And** it must check the text hash for each requirement in SQLite, and only compute embeddings for new or modified text (missing or stale hashes)
**And** it must store the generated 1024-dimensional dense vectors as binary blobs in SQLite, bypassing vectors inside the LangGraph state
**And** it must set the state channel `embeddings_ready` to `true` upon verification/generation.

### Story 1.3: Centroid-Anchored Batch Construction

As a Pipeline Engineer,
I want to assemble requirement batches using group ASR centroids and nearest-neighbor non-ASRs,
So that the pipeline clusters relevant functional requirements around architecturally significant anchors.

**Acceptance Criteria:**

**Given** standard ARLO condition groups, the standard non-ASR IDs, and the SQLite embedding databases
**When** batch construction is executed for a condition group
**Then** it must calculate the group's centroid as the mean vector of its ASR embeddings
**And** it must query the SQLite cache using cosine similarity to find non-ASRs with similarity $\ge 0.65$ relative to the group's centroid
**And** it must cap the selected non-ASRs at a maximum of 10 per batch
**And** it must assemble and store the batch with its group ID, centroid, and requirement mappings.

### Story 1.4: Overlap Bridging, Coherence Gating, and Priority Queue Ordering

As a Pipeline Engineer,
I want to inject bridge requirements, verify semantic coherence, and order the execution queue by risk,
So that the batches are optimized for execution and cross-batch context is preserved.

**Acceptance Criteria:**

**Given** constructed batches and quality weights from ARLO
**When** bridging, coherence gating, and queue ordering are executed
**Then** it must identify adjacent batches (sharing cluster ID or centroid similarity $\ge 0.65$) and inject 1 to 3 shared bridge requirements
**And** it must calculate average cosine similarity of each batch to its centroid; if similarity $< 0.55$, it must split the batch into two sub-batches (if both pass) or run the batch with `reduced_confidence = true`
**And** it must order the queue prioritizing batches associated with high-risk quality attributes
**And** it must isolate any requirements not assigned to any batch into the `unprocessed_requirements` list.

## Epic 2: Strategy-Parallel Subgraph Execution and Judge Reconciliation (Phase 6)

Process requirement batches through three parallel analysis subgraphs (SAAM-first, pattern-driven, entity-driven) and reconcile their outputs via a Judge node using semantic deduplication, CQRS protection, and cross-cutting concern promotion.

### Story 2.1: Concurrency Orchestrator and Parallel Subgraph Dispatch

As a Pipeline Engineer,
I want to concurrently execute three independent analysis subgraphs using SQLite WAL checkpointing,
So that we process batches through parallel design strategies without write contention.

**Acceptance Criteria:**

**Given** an execution batch, Quality Weights, and the running model
**When** the execution loop processes a batch
**Then** it must concurrently dispatch three parallel subgraphs (RAA-A SAAM-First, RAA-B Pattern-Driven, RAA-C Entity/Relationship-Driven) using `asyncio.gather`
**And** it must map parent state variables (running model, batch requirements, bridge requirements) to each subgraph instance
**And** it must persist state checkpoints concurrently to SQLite using Write-Ahead Logging (WAL) without locking delays
**And** it must route incoherent batches (`reduced_confidence = true`) to a single-strategy call (RAA-A only)
**And** it must accumulate raw `ArchFragment` outputs from each parallel run inside the state's concurrent-write `batch_outputs` channel using an append-merge reducer.

### Story 2.2: C4 Metamodel Hierarchy Enforcement in Private Subgraphs

As a Pipeline Engineer,
I want each subgraph to output structural C4 components and relationships that strictly adhere to nesting rules,
So that we prevent orphan components or out-of-scope relationship arrows from corrupting the running model.

**Acceptance Criteria:**

**Given** an execution batch, running model constraints, and a private subgraph LLM prompt template
**When** a subgraph extracts architectural elements (systems, containers, components, relationships)
**Then** it must ensure every container has a valid `parent_system_id` (pointing to a system in the fragment or the running model)
**And** it must ensure every component has a valid `parent_container_id` (pointing to a container in the fragment or the running model)
**And** it must assign each relationship a `diagram_scope` matching the endpoint types (System/Person/ExternalSystem → `context`, Container → `container`, Component → `component`)
**And** it must structure the output matching the `ArchFragment` Pydantic model.

### Story 2.3: SAAM-First Fragment Scoring

As a Pipeline Engineer,
I want the Judge to score each subgraph's fragment using ARLO quality weights,
So that we deterministically designate the highest-quality design as the primary structure.

**Acceptance Criteria:**

**Given** raw `ArchFragment` outputs from RAA-A, RAA-B, and RAA-C, and ARLO's Quality Weights
**When** the Judge reconciles the current batch's results
**Then** it must calculate a score for each fragment by mapping its scenarios to quality weights and frequencies
**And** it must select the highest-scoring fragment as the primary structural template for merging
**And** it must apply a 0.5× multiplier to the score of fragments generated from incoherent batches (`reduced_confidence = true`)
**And** it must fallback to the single RAA-A output if parallel execution was skipped.

### Story 2.4: Conservative Entity Deduplication and C4 Boundary Grouping

As an Architect,
I want the Judge to merge semantically duplicate entities and create boundary groupings for moderate-similarity deployment units,
So that we prevent entity count bloat while protecting CQRS architectural separation.

**Acceptance Criteria:**

**Given** the primary fragment, secondary fragments, the running architecture model, and the SQLite embedding database
**When** the Judge performs the reconciliation deduplication pass
**Then** it must normalize entity IDs to lowercase snake_case for initial matching
**And** it must calculate cosine similarity between entity descriptions using the SQLite cache
**And** if similarity is $\ge 0.80$ and their requirement IDs overlap, it must merge the entities (retaining the longest description and unioning technology tags)
**And** if similarity is between $0.60$ and $0.80$, it must not merge them but must cluster them into logical C4 boundary groupings in the JSON output
**And** it must flag moderate-similarity conflicts and write them to the `change_risk` or `high_coupling` open question list.

### Story 2.5: Cross-Cutting Concern Promotion and SAAM Score Calibration

As an Architect,
I want the Judge to promote global requirements to first-class components and calibrate SAAM scores,
So that cross-cutting infrastructure concerns are clearly modeled and design quality is accurately reflected.

**Acceptance Criteria:**

**Given** the reconciled batch fragment and the current model state
**When** the Judge finalizes the batch merge
**Then** it must scan for cross-cutting annotations matching global patterns (e.g., security, compliance) and promote them to concrete structural boundary components
**And** it must update all affected relationship arrows to point to the promoted component and link the requirement ID directly to the component
**And** it must calibrate the entity `saam_score` reserving a value of `1.0` *only* for entities with a component-level diagram, no functional overlap, and all direct scenarios passing
**And** it must assign a reduced SAAM score to deduplicated or overlapping entities.

## Epic 3: Interactive Human Review Gate (Phase 7)

Emit review payloads and halt execution with LangGraph interrupts for high-priority open questions in interactive mode, allowing authoritative human input with a fallback autonomous bypass.

### Story 3.1: Open Question Classification and Human Review Payload Generation

As a Pipeline Engineer,
I want the RAA Orchestrator to classify open questions and build a detailed human review payload,
So that interactive and autonomous execution steps have clear contexts and pre-computed solutions.

**Acceptance Criteria:**

**Given** a list of open questions accumulated in the `open_questions` channel from Phase 6
**When** question classification is executed
**Then** it must categorize each question: `change_risk`, `high_coupling`, and `coverage_gap` must be classified as `human_preferred`; `contention`, `tie`, `hierarchy_conflict`, and `scope_conflict` must be classified as `judge_resolvable`
**And** it must auto-generate a pre-computed suggested answer for each `judge_resolvable` question
**And** it must construct a `human_review_payload` dictionary containing: the list of categorized questions, details of the conflicting C4 elements, a model statistics summary (system count, container count), and the pre-computed suggested resolutions.

### Story 3.2: Indefinite LangGraph Interrupt Gate

As a Pipeline Engineer,
I want the RAA Orchestrator to trigger an indefinite LangGraph interrupt in interactive mode and bypass it in autonomous mode,
So that humans can review models interactively, but scripts can run without blocks.

**Acceptance Criteria:**

**Given** a populated `human_review_payload` and a config parameter `review_mode` set to `"interactive"` or `"autonomous"`
**When** the Human Review Gate node executes
**Then** if `review_mode` is `"interactive"`, it must trigger the standard LangGraph `interrupt(payload)` function containing the payload, suspending the graph execution indefinitely with no timeout
**And** it must not auto-resume or auto-resolve until a standard `Command(resume=...)` is received
**And** if `review_mode` is `"autonomous"`, it must bypass the interrupt entirely and transition immediately to the global resolution phase (Phase 8).

### Story 3.3: Authoritative Human Answer Mapping & Conflict Resolution

As a Pipeline Engineer,
I want the graph to apply human answers authoritatively to override pre-computed suggestions when resuming,
So that human design preferences override the autonomous agent's default choices.

**Acceptance Criteria:**

**Given** a suspended graph and a resume command payload containing human answers
**When** the graph resumes from the interrupt
**Then** it must apply the human answers to resolve matching open questions, overriding any pre-computed Judge suggestions
**And** it must set `assumption_flag = false` on all entities resolved directly by a human answer
**And** if the human text override is structurally invalid, it must catch the error, log a `scope_conflict`, and apply fallback constraints.

## Epic 4: Global Consolidation, Residual Pass, and Validation (Phase 8)

Perform a global merge of all batch outputs, apply answers or draft documented assumptions, process leftovers in a residual pass, verify 100% requirements accounting, and validate the C4 JSON schema and diagram manifest.

### Story 4.1: Global Model Merge & Principled Open Question Resolution

As a Pipeline Engineer,
I want the RAA Orchestrator to merge all batch outputs globally and resolve remaining open questions with assumptions or defaults,
So that the final output contains a single complete architectural structure with no unresolved conflicts.

**Acceptance Criteria:**

**Given** batch outputs, human review responses, and any unresolved open questions
**When** the global merge node executes
**Then** it must combine all batch fragments and running model states into a single unified C4 structure
**And** it must resolve all outstanding questions, ensuring no question in the final output has a `null` resolution
**And** for unresolved `human_preferred` questions, it must write a documented assumption based on the requirements and set `assumption_flag = true`
**And** for unresolved `judge_resolvable` questions, it must apply the pre-computed suggestion and set `assumption_flag = false`.

### Story 4.2: Residual Requirements Decision Ladder

As a Pipeline Engineer,
I want the Judge to process unassigned leftover requirements using the multi-step decision ladder,
So that all secondary requirements are integrated or categorized based on similarity and coupling.

**Acceptance Criteria:**

**Given** the merged C4 model and the list of `unprocessed_requirements`
**When** the residual pass executes
**Then** it must evaluate each leftover requirement sequentially using SQLite cosine similarity scores
**And** if similarity to a container is $> 0.75$, it must auto-enrich the container's description and append the requirement ID
**And** if similarity is between $0.50$ and $0.75$, it must check coupling; if coupled (sharing actors/flows), it must enrich the container and log `assumption_flag = true`, otherwise exclude it and flag it as a human review query
**And** if similarity is $< 0.50$ and it implies architectural structure, it must propose a minimal C4 entity and relationships
**And** if similarity is $< 0.50$ and it is non-architectural, it must exclude the requirement and log a `coverage_gap` open question with a clear rationale.

### Story 4.3: 100% Requirements Traceability Audit

As a Pipeline Engineer,
I want the RAA Orchestrator to execute a final traceability audit on all input requirement IDs,
So that we guarantee zero silent requirement drops and ensure 100% accounting.

**Acceptance Criteria:**

**Given** the list of all input requirement IDs and the final compiled model state
**When** the finalization audit executes
**Then** it must verify that every single input requirement ID is traceable to exactly one location (either a processed batch, a mapped container/component, or a `coverage_gap` question)
**And** it must fail the execution run immediately with a `TraceabilityAuditException` if any requirements are unmapped or missing
**And** it must prohibit any bulk acceptance or bulk rejection of leftovers.

### Story 4.4: Diagram Manifest Compile & C4 JSON Schema Validation

As a Pipeline Engineer,
I want to validate the final output model against the C4 JSON schema and compile the diagram manifest,
So that the output files are verified for metamodel correctness and ready for rendering.

**Acceptance Criteria:**

**Given** the audited merged model and output path configuration
**When** the validation and compilation node executes
**Then** it must validate the generated architecture model against the C4 JSON Schema and throw a validation exception if it fails
**And** it must compile a diagram manifest with length exactly equal to `(2 * number of systems) + total containers across all systems`
**And** it must write the finalized JSON files to the output directory
**And** it must update the frontmatter metadata status of the output model to `"final"`.


