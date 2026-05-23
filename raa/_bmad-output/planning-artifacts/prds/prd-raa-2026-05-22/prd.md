---
title: Requirements Analysis Agent (RAA)
status: final
created: 2026-05-22
updated: 2026-05-22
---

# PRD: Requirements Analysis Agent (RAA)

## 0. Document Purpose
This Product Requirements Document (PRD) defines the Requirements Analysis Agent (RAA) module, a core component in the three-agent C4 architecture generation pipeline. The RAA is responsible for transforming a set of raw software requirements (partitioned upstream by ARLO) into a C4-compliant JSON architecture model. This document bridges the interface gap between the ARLO requirement locator (upstream) and the AGA diagram renderer (downstream). It defines the RAA's execution phases, parallel subgraph extraction strategies, Judge reconciliation rules, offline embedding management, and the interactive review gate.

---

## 1. Vision
* **What it is**: The **Requirement Analysis Agent (RAA)** is a batch-sequential, strategy-parallel agent module that serves as the middle stage of a three-agent C4 diagram generation pipeline.
* **What it does**: RAA ingests classified requirements (ASR and non-ASR) from the upstream ARLO agent, normalizes them, and partitions them into cohesive batches. It then dispatches three parallel, strategy-specific extraction subgraphs (SAAM-first, pattern-driven, and bottom-up entity-driven) to propose architectural fragments. A central **Judge** reconciles these fragments, resolves conflicts, handles an interactive human-in-the-loop review gate, and runs a final residual pass to produce a C4-compliant JSON architecture model.
* **Why it matters**: Naive single-pass extraction tends to produce bloated, duplicate containers and breaks CQRS/intentional architectural separation. RAA uses a strategy-parallel approach and multi-signal heuristics (geometric similarity + structural coupling) to ensure high-fidelity diagram generation, clean entity-relationship hierarchy, and 100% requirements traceability for the downstream AGA renderer.

---

## 2. Target User

### 2.1 Primary Persona
* **Devin, the Pipeline Engineer**: Devin is building the "I-Architect" workflow. He needs a robust, non-crashing RAA stage that handles messy LLM extractions, saves state safely to SQLite, and provides clean API contracts for downstream rendering.
* **Alex, the Lead Architect**: Alex consumes the C4 diagrams and resolves architectural ambiguities. Alex wants to review high-context design decisions without dealing with diagram clutter, duplicate containers, or unresolvable layout orphans.

### 2.2 Jobs To Be Done (JTBD)
* **Functional**: Transform a flat list of requirements (ASRs and non-ASRs) into a strictly hierarchical C4 model description (JSON).
* **Functional**: Identify and surface cross-cutting concerns (e.g. security, compliance) as first-class components rather than repeating annotations.
* **Contextual**: Ensure 100% requirements coverage so no requirement is silently dropped from the architectural backlog.
* **Emotional / Quality**: Gain confidence that the AI-generated architecture model matches human-level C4 design principles (e.g. CQRS separation, proper relationship scope) without manual diagram cleanup.

### 2.3 Non-Users (v1)
* **Non-technical business clients**: They do not inspect JSON models or configure LangGraph checkpoints; they only consume final SVG/PlantUML diagrams.

### 2.4 Key User Journeys (UJ)

* **UJ-1: Devin runs a dry run of the RAA pipeline in autonomous mode.**
  * **Persona + context**: Devin, validating a new requirements set in a headless CI/CD script.
  * **Entry state**: Requirements normalized in Phase 1. `review_mode = autonomous` configured in the state graph's input schema.
  * **Path**: RAA processes the batches sequentially. For any open questions (`change_risk`, `hierarchy_conflict`), the Judge applies its pre-computed suggestions or documented assumptions autonomously.
  * **Climax**: RAA completes Phase 8, writing a fully resolved `arch_model.json` to the output folder.
  * **Resolution**: Devin's test suite parses the JSON, validating that all questions have non-null resolutions and `assumption_flag = true` is logged for auditability.

* **UJ-2: Alex resolves strategic tradeoffs during an interactive pipeline pause.**
  * **Persona + context**: Alex, reviewing a complex microservice project architecture before rendering diagrams.
  * **Entry state**: RAA completes Phase 6 with several `human_preferred` open questions. `review_mode = interactive` configured in the input schema.
  * **Path**: The graph issues a LangGraph interrupt and emits a `human_review_payload`. Alex opens a CLI tool or review dashboard, reads the high-context questions (e.g., "consolidate Service A and B or separate?"), and inputs resolutions.
  * **Climax**: Alex resumes the graph with `human_answers` mapped.
  * **Resolution**: RAA applies the answers authoritatively, resolves remaining low-priority questions autonomously, and produces the finalized architecture model.

---

## 3. Integration & Dependencies

### 3.1 Upstream Handoff (Orchestrator + ARLO → RAA)
RAA consumes the original requirements map from the parent Orchestrator plus output channels of the ARLO graph:
* **`requirements`**: `dict[str, str]` containing the full original requirement ID → description mapping. This is the authoritative description source for both ASR and Non-ASR enrichment.
* **`asrs`**: `list[dict]` containing requirement IDs, quality attributes, and condition texts.
* **`non_asr`**: `list[str]` containing raw non-ASR requirement IDs.
* **`condition_groups`**: `list[dict]` containing K-Means clusters of ASRs.
* **`quality_weights`**: `dict[str, int]` containing quality attribute frequencies.

RAA must not inspect ARLO or parent graph state to recover requirement descriptions. The parent Orchestrator owns the explicit handoff contract and must pass `requirements` in the RAA input state.

### 3.2 Downstream Handoff (RAA → AGA)
RAA writes its outputs to an orchestrator-specified directory:
* **`arch_model.json`**: The complete hierarchical C4 model and Diagram Manifest.
* **`open_questions`**: Auditable record of all decisions, including human answers and Judge assumptions.

---

## 4. Glossary

* **ARLO Output** — The upstream dataset parsed from the Architecturally-significant Requirements Locator & Organizer. Includes ASRs, Non-ASRs, Condition Groups, and Quality Weights.
* **ASR (Architecturally-Significant Requirement)** — A requirement identified by ARLO as having a direct impact on structural design, containing quality attributes and condition text.
* **Non-ASR** — A requirement classified by ARLO as non-structural but containing functional details that need mapping.
* **Condition Group** — A cluster of ASRs sharing similar conditions, generated by ARLO, which serves as the anchor for a requirement batch.
* **ArchFragment** — The semi-flat, intermediate C4 architecture model fragment produced by an individual parallel subgraph.
* **Running Architecture Model** — The accumulated, nested C4 model built batch-by-batch. It serves as a hard constraint for all subsequent batches.
* **C4 Model** — The structural architecture standard. RAA scopes its output strictly to the first three levels: System Context, Container, and Component.
* **Judge (Reconciliation Node)** — The central RAA node that scores subgraph fragments using SAAM scenarios, deduplicates entities, resolves structural conflicts, and merges them into the Running Architecture Model.
* **Open Question** — A structured conflict, risk, or gap flagged by the Judge during merging. Classified as either `human_preferred` or `judge_resolvable`.
* **Coverage Gap** — An unprocessed requirement that does not map to any C4 element (e.g. process/tooling rules), excluded from the model but tracked as an Open Question.
* **Deduplication Pass** — The Judge's semantic merging phase that prevents container/component bloat by clustering entities with high semantic similarity.
* **Residual Batch / Leftovers** — The set of unprocessed requirements evaluated in Phase 8 to ensure 100% requirements coverage.
* **Interactive Mode** — A pre-execution configuration that triggers a LangGraph interrupt at Phase 7, suspending the graph indefinitely until `human_answers` are supplied.
* **Autonomous Mode** — A pre-execution configuration that bypasses the Phase 7 interrupt, permitting the Judge to resolve all Open Questions using pre-computed suggestions or documented assumptions.
* **WAL Checkpointer** — A SQLite checkpointer configured with Write-Ahead Logging to handle concurrent state writes from parallel subgraphs without locking.

---

## 5. Schema & API Contracts

### 5.1 Diagram Manifest Contract
RAA must output a deterministic `diagram_manifest` array inside `arch_model.json`. The manifest serves as a work queue for AGA and must include exactly:
1. One **context diagram** per system.
2. One **container diagram** per system.
3. One **component diagram** per container.

$$\text{Total Diagrams} = (2 \times \text{number of systems}) + (\text{total containers across all systems})$$

[ASSUMPTION: The downstream AGA traverses this manifest sequentially without performing any independent filtering logic or entity layout discovery.]

### 5.2 Metamodel Validation Schema
All outputs must validate against a strict C4 JSON schema where:
* System, Container, and Component layers are strictly nested.
* All relationships refer to valid entity IDs.
* Relationship scopes match the hierarchy depth of their source and target endpoints.

---

## 6. Features & Functional Requirements

### 6.1 Feature: Inputs Normalization and SQLite Embedding Cache (Phase 1)
**Description:** 
Ingests raw inputs from ARLO and parent pipeline. Standardizes requirement IDs, fetches raw description text, generates dense vector embeddings using `mixedbread-ai/mxbai-embed-large-v1` via FastEmbed, and saves them to SQLite.

#### FR-1: Requirement Normalization & Enrichment
The RAA Orchestrator must enrich upstream ARLO outputs into fully populated requirement records before executing subsequent stages.
* **Consequences (testable):**
  * String IDs are standardized (e.g., ARLO int ID `5` → RAA string ID `"R5"`).
  * ASR and Non-ASR IDs are matched against the orchestrator-provided `requirements: dict[str, str]` to retrieve authoritative description text.
  * ARLO-provided ASR description text is fallback-only when the original requirements mapping has no usable entry for that requirement ID.
  * Non-ASR payloads default `is_asr = false`, `quality_attributes = []`, and `condition_text = null`.

#### FR-2: SQLite Embedding Generation and Cache Verification
The RAA Preparation node must generate 1024-dimensional dense vectors using the local FastEmbed cache and store them in SQLite.
* **Consequences (testable):**
  * RAA initializes FastEmbed using `cache_dir = "../models"` (resolved as `/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/models`).
  * If the model files do not exist at the local cache directory, RAA must throw an explicit model non-existent exception immediately.
  * Separate SQLite tables store ASR and Non-ASR embeddings.
  * If a text hash matches the cached database entry, embedding generation is skipped for that requirement.
  * Once verified/generated, `embeddings_ready` is set to `true`, gating downstream graph nodes.

---

### 6.2 Feature: Centroid-Anchored Batching and Bridging (Phases 2-3)
**Description:** 
Forms batches using ASR centroid anchors, extracts near-neighbor non-ASRs, and injects overlap bridge requirements.

#### FR-3: Centroid-Anchored Batch Construction
The Batch Construction node must query the SQLite embedding cache to compute a condition group's centroid and pull similar non-ASR requirements.
* **Consequences (testable):**
  * The group centroid is computed as the mean vector of the group's ASR embeddings.
  * Nearest-neighbor search retrieves non-ASR candidates with cosine similarity $\ge 0.65$.
  * Non-ASR candidates are capped at a maximum of 10 per batch.

#### FR-4: Overlap Bridging
The Overlap Bridging node must identify related condition groups (sharing a cluster ID or with centroid cosine similarity $\ge 0.65$) and inject shared bridge requirements.
* **Consequences (testable):**
  * Inserts 1 to 3 (hard cap: 3) highly similar non-ASRs into both adjacent batches.
  * Bridge requirement mappings are recorded in the graph's `bridge_requirements` channel.

---

### 6.3 Feature: Coherence Gating and Ordering (Phases 4-5)
**Description:** 
Verifies batch semantic coherence, splits incoherent batches, and orders the execution queue.

#### FR-5: Coherence Gating and Splitting
The Coherence Gate must verify that the average cosine similarity of a batch's requirement embeddings relative to its centroid is $\ge 0.55$.
* **Consequences (testable):**
  * If a batch score is $< 0.55$, RAA attempts to split it into two sub-clusters. If both sub-clusters pass, the original batch is replaced by two sub-batches.
  * If a split batch remains incoherent, it is run as a single-strategy batch (no parallel strategies) and marked with `reduced_confidence = true` (which applies a $0.5\times$ multiplier to its SAAM scoring).

#### FR-6: Queue Ordering
The Batch Queue Ordering node must sequence the execution queue according to risk weights associated with requirement quality attributes.
* **Consequences (testable):**
  * Security and reliability batches are sequenced to execute first.
  * Alternative sorting strategies (ASR count, quality weight frequency) are selectable via input parameters.
  * Leftover requirements not assigned to any batch are isolated in the `unprocessed_requirements` list.

---

### 6.4 Feature: Parallel Private Subgraph Strategy Execution (Phases 6a–6b)
**Description:** 
Concurrently dispatches three strategy-parallel subgraphs to extract C4 elements, utilizing private state schemas and concurrent WAL checkpointers.

#### FR-7: Strategy-Parallel Subgraph Dispatch
The RAA Execution Loop must concurrently spawn three parallel subgraphs, mapping parent state variables to each instance.
* **Consequences (testable):**
  * **RAA-A (SAAM-First)**: Quality attributes drive scenarios first, then derives entities.
  * **RAA-B (Pattern-Driven)**: Matches requirements to patterns from `matrix.json`, then extracts implementing entities. [ASSUMPTION: The transposing loader correctly handles the `matrix.json` schema.]
  * **RAA-C (Entity/Relationship-Driven)**: Extracts entities and relationships bottom-up from requirement descriptions.
  * *Exception*: Incoherent batches (`reduced_confidence = true`) run as a single-strategy call instead of three-parallel.

#### FR-8: C4 Metamodel Hierarchy Enforcement
Each subgraph must output an `ArchFragment` that strictly adheres to the C4 standard structure.
* **Consequences (testable):**
  * Containers must carry a valid `parent_system_id`.
  * Components must carry a valid `parent_container_id`.
  * Relationship scopes (`context`, `container`, `component`) must match their endpoint entity types.

#### FR-9: Concurrent WAL-Enabled State Persistence
All concurrent subgraph executions must persist state to SQLite checkpoints using Write-Ahead Logging (WAL).
* **Consequences (testable):**
  * Subgraphs write concurrently without causing lock delays, thread contention, or database corruption.
  * Private states and intermediate LLM outputs are isolated by subgraph run IDs.

---

### 6.5 Feature: Convergent Judge Reconciliation & Deduplication (Phase 6c)
**Description:** 
Reconciles subgraphs, scores scenarios, and merges fragments using semantic deduplication and policy promotion.

#### FR-10: SAAM-First Fragment Scoring
The Judge must score each subgraph's fragment using ARLO's quality weights to select the primary model structure.
* **Consequences (testable):**
  * Scenarios mapped by the subgraph are evaluated against quality weight frequencies.
  * The highest-scoring fragment is designated as the primary.
  * If a batch was incoherent, the Judge applies a $0.5\times$ multiplier to its score.

#### FR-11: Conservative Entity Deduplication and C4 Boundary Grouping
The Judge must scan entities globally across all batches to deduplicate redundant components while protecting CQRS separations.
* **Consequences (testable):**
  * Semantic similarity is calculated using SQLite-cached container descriptions.
  * If cosine similarity is $\ge 0.80$ and `requirement_ids` overlap, the entities are merged (longest description wins; technology tags are unioned).
  * If cosine similarity is $0.60$ to $0.80$, the Judge clusters the containers into logical **C4 boundary groupings** in the JSON output (preventing destructive merging of distinct deployment units).
  * Moderate-similarity entities are flagged with an `assumption_flag` or written to the `change_risk` / `high_coupling` open question list.

#### FR-12: Cross-Cutting Concern Promotion
The Judge must identify cross-cutting candidates in the `ArchFragments` and promote them to concrete structural boundary components.
* **Consequences (testable):**
  * Global annotations (e.g. "every connection must be TLS terminated") are promoted to a concrete C4 component (e.g. "TLS Termination Gateway").
  * Affected relationship arrows are updated to point directly to the promoted component.
  * The cross-cutting requirement is mapped to the promoted component's `requirement_ids` rather than being repeated on all arrows.

#### FR-13: SAAM Score Calibration
The Judge must calibrate final entity scoring to represent completeness and design quality.
* **Consequences (testable):**
  * A `saam_score` of `1.0` is reserved *only* for entities that have a component-level diagram, no functional overlap with other entities, and all direct scenarios passing.
  * Deduplicated or overlapping entities receive a reduced SAAM score.

---

### 6.6 Feature: Interactive Human Review Gate (Phase 7)
**Description:** 
Handles optional LangGraph interrupts to surface high-priority questions, waiting indefinitely for user inputs in interactive mode.

#### FR-14: Open Question Classification & Payload Emission
The Human Review Gate node must classify all collected open questions and construct a read-only review payload before pausing execution.
* **Consequences (testable):**
  * Questions are categorized by type: `change_risk`, `high_coupling`, `coverage_gap` are flagged as `human_preferred`; `contention`, `tie`, `hierarchy_conflict`, `scope_conflict` are flagged as `judge_resolvable`.
  * Pre-computed suggestions are automatically generated for all `judge_resolvable` entries.
  * The `human_review_payload` channel is populated with: open question contexts, a model summary (entity counts, system names), and the pre-computed resolutions.

#### FR-15: Indefinite LangGraph Interrupt
The Human Review Gate must trigger an interrupt in `interactive` mode or pass through immediately in `autonomous` mode.
* **Consequences (testable):**
  * If `review_mode = interactive`, a LangGraph interrupt is raised, suspending the graph indefinitely. The execution does *not* time out automatically.
  * If `review_mode = autonomous`, the interrupt is bypassed, and the graph proceeds immediately to Phase 8.

#### FR-16: Authoritative Human Answer Mapping
The RAA Orchestrator must apply human answers authoritatively to resolve open questions.
* **Consequences (testable):**
  * Human answers override any pre-computed Judge suggestions, even for `judge_resolvable` questions.
  * Applied human answers are marked in the final output with `assumption_flag = false` (since they were confirmed by a human).
  * Structurally invalid human text directions (e.g. attempting to violate nesting rules) are caught by the Judge, logged as a `scope_conflict`, and resolved using fallback constraints.

---

### 6.7 Feature: Phase 8 Final Merge & Residual Requirements Pass
**Description:** 
Performs global merge, applies final question resolutions, runs the residual requirements pass ladder, and executes schema validation.

#### FR-17: Principled Open Question Resolution
The Judge must resolve all remaining questions, ensuring no question in the final output has a `null` resolution.
* **Consequences (testable):**
  * For unresolved `human_preferred` questions, the Judge drafts a documented assumption based on the requirements text and sets `assumption_flag = true`.
  * For unresolved `judge_resolvable` questions, the Judge applies its pre-computed suggestions and sets `assumption_flag = false`.

#### FR-18: Residual Requirements Decision Ladder
The Judge must evaluate each element in `unprocessed_requirements` sequentially against the merged model using semantic and coupling criteria.
* **Consequences (testable):**
  * **Similarity > 0.75**: Auto-enrich the matching C4 container description and append the requirement ID.
  * **Similarity 0.50–0.75**: Check if the requirement shares actors or data flows with the container. If coupled, enrich the container and log an `assumption_flag`. If not, exclude and flag as a human review query.
  * **Similarity < 0.50**: 
    * If it implies architectural structure (e.g., database, API), propose a new minimal C4 entity and its relationships.
    * If non-architectural (e.g., process/tooling complexity), exclude the requirement and log it as a `coverage_gap` open question with a one-sentence rationale.

#### FR-19: 100% Requirements Accounting Audit
Before finalization, RAA must audit requirement traceability to verify that every input requirement is represented exactly once.
* **Consequences (testable):**
  * Every input requirement ID must be traceable to a batch, a mapped container/component, or a `coverage_gap` open question.
  * Bulk acceptance or bulk rejection of leftovers is prohibited.

#### FR-20: Diagram Manifest Construction & C4 JSON Schema Validation
The Finalize node must construct the downstream diagram rendering work queue and validate the C4 JSON metamodel.
* **Consequences (testable):**
  * A C4-compliant schema validation check is run against the generated model.
  * A diagram manifest is generated with length exactly equal to `(2 * number of systems) + total containers across all systems`.
  * Outputs are written to the output directory, and frontmatter `status` is updated to `final`.

---

## 7. Non-Goals (Explicit)
* **No Diagram Generation**: RAA does *not* render PlantUML, SVG, or any visual diagrams. It produces only a structured JSON model; diagram creation is owned by the downstream AGA.
* **No Code or Schema Generation**: RAA defines logical systems, containers, and components, but does *not* generate source code, database tables, or API implementation code.
* **No ASR Localization or K-Means Clustering**: RAA does *not* identify which requirements are architecturally significant, nor does it perform primary vector clustering. These are owned by ARLO.
* **No Vector Serialization in State**: RAA does *not* store 1024-dimensional embedding vectors inside the LangGraph state channels. State checkpoints must remain lean.
* **No JSON Writing by the Human Reviewer**: The interactive review gate must *never* ask a human to compose C4 JSON elements. Answers are free-text only.
* **No Auto-Detection of Execution Environment**: RAA does *not* guess if it is running in CI/CD or CLI. The calling orchestrator must configure `review_mode` explicitly at invocation.

---

## 8. MVP Scope

### 8.1 In Scope
* **8-Phase LangGraph Pipeline**: Full implementation of the sequential phases (1 through 8) with private subgraph execution.
* **Input Standardization**: Enrichment of ASR and Non-ASR records using orchestrator-provided original requirements text.
* **SQLite Embedding Persistence**: RAA-owned generation of ASR and Non-ASR embeddings using FastEmbed (`mxbai-embed-large-v1`) with text-hash caching.
* **Centroid Batching & Overlap Bridging**: Centroid calculation, nearest-neighbor non-ASR search ($\ge 0.65$), and injection of 1–3 bridge requirements.
* **Coherence Gate & Splitting**: Coherence checks ($< 0.55$), batch splitting, and reduced-confidence execution (with $0.5\times$ SAAM weight multiplier).
* **Parallel Private Subgraphs**: Isolated RAA-A (SAAM-first), RAA-B (Pattern-Driven), and RAA-C (Entity-Driven) subgraph nodes writing concurrently to a SQLite WAL-enabled checkpointer database.
* **Constant Matrix Integration**: Loading the quality-architecture matrix directly from the constant `matrix.json` file.
* **Judge Reconciliation**: SAAM scenario scoring, semantic deduplication ($\ge 0.80$), C4 boundary grouping ($0.60$ to $0.80$), cross-cutting concern promotion, and SAAM score calibration.
* **Indefinite Review Gate Interrupt**: Standard LangGraph interrupt with infinite wait (no timeout) for user answers, and configuration-driven autonomous bypass.
* **Phase 8 Residual Pass**: Sequential evaluation of unprocessed requirements using the decision ladder (similarity + coupling check, new entity proposals, or `coverage_gap` logging).
* **100% Coverage Audit**: Enforcement that every requirement appears in a batch, container/component, or as a coverage gap.
* **Schema Validation & Manifest**: Outputs validated against C4 JSON schema and diagram manifest compiled.

### 8.2 Out of Scope for MVP
* **Dynamic Matrix Reloading**: The quality-architecture matrix cannot be reloaded or edited mid-run.
* **GUI Review Dashboard**: Building a visual interface for resolving open questions. Alex will interact via a basic CLI wrapper or text file integration.
* **Dynamic Re-Embedding**: Updating existing SQLite vector records if their text hashes match.
* **Multi-User Collaboration**: Support for concurrent reviewers submitting answers. The system accepts only a single `human_answers` payload per interrupt.

---

## 9. Success Metrics

### 9.1 Primary Metrics
* **SM-1: Requirement Mapping Coverage**
  * *Metric*: Percentage of input requirements accounted for in the final model.
  * *Target*: **100%**.
  * *Validation*: Diff of all input requirement IDs against: (a) batch `requirement_ids`, (b) `unprocessed_requirements` resolved, and (c) `coverage_gap` open questions (no silent drops allowed).
* **SM-2: Entity Deduplication Precision**
  * *Metric*: Percentage of redundant or duplicate containers/components produced in the output model.
  * *Target*: **< 5%** (resolving the SAAM audit finding where duplicates inflated the model by 40%).
  * *Validation*: Checked against manual gold-standard C4 decompositions.

### 9.2 Secondary Metrics
* **SM-3: Checkpoint Resume Integrity**
  * *Metric*: Success rate of resuming interrupted runs from the last completed batch checkpoint.
  * *Target*: **100%** successful recovery without state corruption or duplicate writes.
  * *Validation*: Verified by running batch-failure integration tests.

### 9.3 Counter-Metrics (Do Not Optimize At All Costs)
* **SM-C1: CQRS Boundary Preservation (Deduplication Guard)**
  * *Metric*: Number of distinct deployment units (e.g. read database vs. write database in CQRS) mistakenly merged due to high semantic similarity.
  * *Target*: **0**.
  * *Validation*: Evaluated via the Pattern-Driven RAA-B strategy to ensure boundary groupings are created instead of destructive merges.

---

## 10. Open Questions
* **Orchestrator Input Schema Parameter Names**: What are the exact key names expected by the orchestrator for passing the SQLite database path and checkpointer paths (e.g. `sqlite_db_path` or `db_path`)?
* **Local FastEmbed Model Files Version**: Should the local cache path (`../models`) contain a specific version of the `mxbai-embed-large-v1` model, or does it accept any version present?

---

## 11. Assumptions Index
* **Assumption from Section 5.1**: The downstream AGA traverses the diagram manifest sequentially without performing any independent filtering logic or entity layout discovery.
* **Assumption from Section 6.4**: The transposing loader correctly handles the `matrix.json` schema.
