# Full RAA Implementation Plan — v3

## 0) Goal of this Portion

Partition a large requirements set into **coherent, overlapping batches** for RAA (Requirement Analysis Agent) subgraphs, using **ARLO condition groups as anchors**, then orchestrate **parallel RAA runs + judge** to incrementally build a consistent architecture model. Minimize compute while maximizing architectural accuracy and coherence.

> **Pipeline position note:** RAA is the middle stage. ARLO (fully implemented) feeds it. The Architecture Generation Agent (AGA) consumes its output and handles all diagram/code generation including PlantUML. RAA's sole output is a **C4-compliant entity-relationship JSON model**; it produces no diagrams or code.

---

## 1) Inputs and Assumptions

### Inputs from ARLO (via `ARLOOutput` state schema)
- **`asrs`** (`list[dict]`) — architecturally significant requirements. Each dict contains `id` (int), `is_architecturally_significant` (bool), `quality_attributes` (list[str]), and `condition_text` (str). The requirement description text is not included; it must be resolved from the original `requirements` input if needed.
- **`non_asr`** (`list[dict]`) — requirements not marked architecturally significant. Same dict structure as `asrs`. Added to `ARLOOutput` as part of this plan's ARLO compatibility modifications (see §1B).
- **`condition_groups`** (`list[dict]`) — groups of ASRs sharing equivalent conditions, anchored by K-Means clustering over ASR embeddings. Each group dict contains `nominal_condition` (str), `conditions` (list[int] — ASR indices), `requirements` (list[dict] — full ASR dicts), and `cluster` (int — K-Means cluster ID). Added to `ARLOOutput` as part of this plan's ARLO compatibility modifications (see §1B).
- **`quality_weights`** (`dict[str, int]`) — aggregate quality attribute frequency counts across all satisfiable groups. Values are raw counts (not normalised percentages); the SAAM scoring formula (§13, SAAM.md) uses them as relative weights, so normalisation is not required.

### Inputs from Parent Pipeline
- **`requirements`** (`dict[str, str]`) — the original full requirement set (ID → description), passed directly from the parent pipeline input. Not an ARLO output — ARLO receives and passes through the same input. Used during requirement normalisation (§5) to resolve requirement description text for ASR and non-ASR dicts.

### ASR Embeddings (via Shared SQLite Persistence)
ARLO's embedding node (`generate_embeddings`) produces 1024-dimensional dense vectors for all ASR condition texts using `mixedbread-ai/mxbai-embed-large-v1` via FastEmbed. These embeddings are **not passed through the LangGraph state graph**. Instead, ARLO writes them to a local SQLite database at `embeddings/asr_embeddings.db` in the project root, keyed by requirement ID. RAA loads ASR embeddings from this database on demand (see §6).

> **Why SQLite instead of state channels:** Embedding vectors are large (1024 floats per ASR). Passing them through LangGraph state channels would inflate every checkpoint snapshot, increase serialisation cost at every super-step boundary, and provide no benefit — embeddings are immutable once computed. SQLite persistence decouples embedding storage from graph state, keeps checkpoints lean, and allows both ARLO and RAA to access embeddings independently.

### 1B — Required ARLO Compatibility Modifications

This plan requires the following additions to ARLO's existing implementation:

1. **Expand `ARLOOutput`** to include two new keys: `non_asr` (`list[dict]`) and `condition_groups` (`list[dict]`). Both are already computed in `ARLOState` (internal) but not currently exposed to downstream consumers.
2. **Modify `generate_embeddings`** in `arlo/nodes/embedding.py` to persist ASR embeddings (requirement ID + embedding vector) to `embeddings/asr_embeddings.db` via SQLite after computing them. The existing state channel write (`{"embeddings": embeddings}`) remains unchanged for internal ARLO use (K-Means clustering). The SQLite write is an additional side-effect.
3. **Create the `embeddings/` directory** at the project root. This directory is shared between ARLO and RAA and must be listed in `.gitignore`.

### Constraints
- Requirements count can be large (hundreds+).
- Avoid full cosine similarity matrix.
- Batches must overlap by **1–3 requirements** across adjacent groups.
- Within each batch, three RAA subgraphs run in parallel. Batches themselves are processed sequentially.
- Judge runs **per batch**.

---

## 2) Authoritative Source Register

**Purpose:** Ensure all prompt-driven nodes are anchored to authoritative C4 and SAAM sources, with explicit normative constraints rather than vague citations.

### 2A — Source Register Table

Maintained as a spec section. Updated on retrieval.

| Source | URL | Retrieval Date | Governs |
|--------|-----|----------------|---------|
| C4 Model — Diagrams | https://c4model.com/diagrams | (set on retrieval) | Level definitions, element types, relationship notation |
| C4 Model — Notation | https://c4model.com/diagrams/notation | (set on retrieval) | Labelling rules, technology annotation, description requirements |
| SAAM — SEI Technical Report | https://sei.cmu.edu/documents/150/2007_019_001_29297.pdf | (set on retrieval) | 5-step SAAM evaluation method |

### 2B — Normative Prompt Constraints (Derived from Sources)

These are paraphrased constraints embedded directly into skill prompts, not raw document text.

**C4 constraints:**
- Must address the three C4 levels used by the pipeline: Context, Container, and Component.
- Every element must carry: a type label, a short description, and clearly labelled relationships.
- Containers and components must specify technology stack when determinable from requirements.
- Relationships must state direction and a short interaction description.

**SAAM constraints:**
- Apply the 5-step SAAM process in order:
  1. Canonical partitioning of the architecture
  2. Map requirements to architectural structures
  3. Choose quality attributes (informed by ARLO quality weights)
  4. Define evaluation scenarios per quality attribute
  5. Evaluate architectural structures against scenarios

### 2C — Doc Excerpt Blocks

Short paraphrases (≤25 words each) stored in a **Prompt Resource Bundle** file. One excerpt per normative rule. Injected per-node, not globally.

The bundle is stored inside the RAA code directory at `raa/prompts/` (see §21 for full structure). This follows the same convention as ARLO (`arlo/prompts/`).

### 2D — Retrieval Policy

- Each LLM node receives only the excerpts relevant to its function (e.g., a relationship-extraction node receives C4 relationship constraints; a tradeoff node receives SAAM steps).
- Full source documents are never copied into prompts.
- The Prompt Resource Bundle is the runtime-ready extraction from the Source Register. Direction of authority: **Source Register → Prompt Resource Bundle → skill prompts**.
- The **Skill Resource Bundle** (`Skills/RAA/`) provides the skill definition and reference documents (SAAM adaptation, etc.) and is separate from the runtime Prompt Resource Bundle.

---

## 3) High-Level Pipeline Overview

1. **Preparation:** normalize all requirements into a shared schema; load ASR embeddings from SQLite; embed non-ASR requirements and persist to SQLite.
2. **Batch Construction:** for each ARLO condition group, find top-k similar non-ASRs and build the batch.
3. **Overlap Bridging:** add 1–3 bridge requirements between adjacent batches.
4. **Coherence Gate:** verify batch semantic cohesion; split or flag if too heterogeneous.
5. **Batch Queue:** order batches by risk priority; store as an ordered list.
6. **Execution Loop** (batches processed one at a time):
   - Run 3 RAA subgraphs in parallel within the batch.
   - Judge evaluates, merges, updates the running model.
   - Next batch receives the accumulated model as a constraint.
7. **Final Merge:** combine all best batch outputs into a single C4-compliant JSON model.

> **Note:** All diagram/code generation (PlantUML, C4 diagrams) is performed downstream by the Architecture Generation Agent. RAA is responsible only for the structured JSON model.

---

## 4) State Schema

### New State Channels

| Channel | Type | Reducer | Description |
|---------|------|---------|-------------|
| `batch_queue` | `list[Batch]` | overwrite | Ordered list of batches. Each batch: list of requirement IDs + payload + group metadata. Written once during batch construction. |
| `batch_cursor` | `int` | overwrite | Current batch index. Advanced by judge node after each batch. |
| `batch_outputs` | `dict[int, list]` | dict-merge (append per key) | Raw outputs from each RAA subgraph per batch, keyed by batch index. Three parallel subgraphs write to this channel in the same super-step; the reducer must merge their entries, not overwrite. |
| `best_batch_output` | `dict[int, ArchFragment]` | dict-merge | Judge-selected and merged output per batch. One entry added per batch index. Records the assembled fragment's contribution (as additions and updates to the running tree) rather than a flat list. `ArchFragment` defined in §4 State Channel Type Definitions. |
| `running_arch_model` | `ArchModel` | overwrite | Accumulated architecture model in hierarchical form (systems containing containers containing components, plus global persons and external systems). Updated by judge after each batch (single writer per super-step). The judge builds it incrementally by inserting merged entities into the correct position in the hierarchy tree after each batch. `ArchModel` defined in §4 State Channel Type Definitions. |
| `open_questions` | `list[OpenQuestion]` | append (`operator.add`) | Unresolved or conflicting items flagged by judge (type defined in §4 State Channel Type Definitions). Multiple sources may append questions across batches; reducer concatenates lists. |
| `bridge_requirements` | `dict[tuple, list[str]]` | overwrite | Map of adjacent group pair → list of bridge requirement IDs. Written once during overlap bridging. |
| `incoherent_batches` | `list[IncoherentBatchRecord]` | append (`operator.add`) | Batches that failed the coherence gate after splitting. `IncoherentBatchRecord` defined in §4 State Channel Type Definitions. Coherence gate may append multiple records. |
| `embeddings_ready` | `bool` | overwrite | Flag set to `true` after the preparation node has verified that ASR embeddings exist in SQLite and non-ASR embeddings have been computed and persisted. Downstream nodes gate on this flag. |

> **Reducer note:** Channels written by multiple nodes in the same LangGraph super-step (e.g., `batch_outputs` from three parallel RAA subgraphs) **must** use an append or dict-merge reducer. Without a reducer, LangGraph applies last-write-wins semantics, which would silently discard outputs from all but one subgraph. Channels written by a single node per super-step can safely use the default overwrite behaviour.

> **Embedding storage note:** Embedding vectors are **not stored in LangGraph state channels**. They are persisted in SQLite databases under `embeddings/` at the project root (see §6). This keeps checkpoint snapshots lean and avoids serialising large float arrays at every super-step boundary.

> **LLM injection note:** LLM instances (`llm_raa_a`, `llm_raa_b`, `llm_raa_c`, `llm_judge`) are **not stored in state channels**. They are passed to the graph via LangGraph's `context={}` dict at invocation time (see §12 for the injection pattern). This follows the orchestrator's mandate (Orchestrator Plan §3C) that LLM objects must never be serialised into checkpoint state. The orchestrator resolves UI-assigned instance names to instantiated `ChatModel` objects and injects them as context.

### Existing State Reused from ARLO

| Channel | Source | Used For |
|---------|--------|----------|
| `asrs` | `ARLOOutput` | ASR dicts for batch assembly and SAAM scenario derivation |
| `non_asr` | `ARLOOutput` | Non-ASR requirement dicts for embedding, batch inclusion, and bridge selection |
| `condition_groups` | `ARLOOutput` | Batch anchors — each condition group seeds one batch |
| `quality_weights` | `ARLOOutput` | Judge SAAM scoring weights, batch queue risk ordering |

### Shared Embedding Persistence (SQLite)

| Database | Location | Written By | Read By | Schema |
|----------|----------|------------|---------|--------|
| `asr_embeddings.db` | `embeddings/asr_embeddings.db` | ARLO embedding node | RAA batch construction (§8), coherence gate (§10) | `requirement_id` (int, PK), `embedding` (blob — 1024 floats), `text_hash` (str), `model_name` (str) |
| `non_asr_embeddings.db` | `embeddings/non_asr_embeddings.db` | RAA preparation node (§6) | RAA batch construction (§8), overlap bridging (§9), coherence gate (§10) | `requirement_id` (int, PK), `embedding` (blob — 1024 floats), `text_hash` (str), `model_name` (str) |

Both databases use the same schema. The `text_hash` column enables cache integrity checks — if a requirement's text changes, the embedding is stale and must be recomputed. The `model_name` column records the FastEmbed model used, ensuring reproducibility.

### State Channel Type Definitions

**`ArchModel`** — the accumulated architecture model built incrementally by the judge after each batch. This is the internal working type; at final merge (§16) it is serialised as a C4-compliant JSON object and handed to AGA as `C4JsonModel` (identical structure, renamed at the boundary). The model is strictly hierarchical: systems contain containers, containers contain components. Persons and external systems are global, shared actors referenced by ID from relationships.

| Field | Type | Description |
|-------|------|-------------|
| `systems` | `list[ArchSystem]` | All software systems under design. Each recursively contains its containers and their components. |
| `persons` | `list[ArchPerson]` | Global list of human actors. Shared across all systems; referenced by ID from relationships. |
| `external_systems` | `list[ArchExternalSystem]` | Global list of external software systems. Shared across all systems; referenced by ID from relationships. |
| `patterns` | `list[ArchPattern]` | Patterns selected by the ILP or Greedy optimizer |
| `open_questions` | `list[OpenQuestion]` | Unresolved or conflicting items carried forward across batches |

**`ArchFragment`** — partial output from a single RAA subgraph run (RAA-A, B, or C). Uses a semi-flat structure with explicit parent ID fields to make inter-fragment deduplication and merge (§13) straightforward without requiring the judge to navigate a deep tree. The judge constructs the fully nested `ArchModel` as its final act after merge, not as an intermediate working structure.

| Field | Type | Description |
|-------|------|-------------|
| `systems` | `list[ArchSystem]` | Software systems proposed by this subgraph |
| `containers` | `list[ArchContainer]` | Containers proposed by this subgraph. Each carries a `parent_system_id` field recording which system it belongs to (either a system in this same fragment or one already in `running_arch_model`). |
| `components` | `list[ArchComponent]` | Components proposed by this subgraph. Each carries a `parent_container_id` field recording which container it belongs to. |
| `persons` | `list[ArchPerson]` | Person actors proposed by this subgraph |
| `external_systems` | `list[ArchExternalSystem]` | External system actors proposed by this subgraph |
| `relationships` | `list[ArchRelationship]` | Directed relationships proposed by this subgraph. Each carries a `diagram_scope` field. |
| `patterns` | `list[ArchPattern]` | Patterns selected by this subgraph's optimizer |
| `rationale` | `dict[str, object]` | Explanation of subgraph choices; includes `gaps` (list[str] of unsolved requirement IDs), `strategy` (str — "SAAM-first", "pattern-driven", or "entity-driven"), and `confidence_notes` (list[str]) |

**`ArchSystem`** — a software system under design. Its position in the hierarchy makes its type implicit; no `type` discriminator or `parent_id` is needed.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the system's purpose |
| `requirement_ids` | `list[int]` | Requirement IDs this system traces to |
| `source_fragment` | `str \| null` | Which subgraph produced this system |
| `confidence` | `float \| null` | SAAM coverage score |
| `context_relationships` | `list[ArchRelationship]` | Relationships at the context level — between this system, persons, and external systems |
| `containers` | `list[ArchContainer]` | Deployable units within this system |

**`ArchContainer`** — a deployable unit within a system.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the container's purpose |
| `technology` | `str \| null` | Technology annotation (required when determinable from requirements) |
| `requirement_ids` | `list[int]` | Requirement IDs this container traces to |
| `source_fragment` | `str \| null` | Which subgraph produced this container |
| `confidence` | `float \| null` | SAAM coverage score |
| `parent_system_id` | `str` | ID of the system this container belongs to. Used in `ArchFragment` for merge; in the final nested `ArchModel`, the nesting makes this implicit. |
| `container_relationships` | `list[ArchRelationship]` | Relationships scoped to the container diagram — between containers, and between containers and persons or external systems |
| `components` | `list[ArchComponent]` | Internal building blocks within this container |

**`ArchComponent`** — an internal building block within a container.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the component's purpose |
| `technology` | `str \| null` | Technology annotation (required when determinable from requirements) |
| `requirement_ids` | `list[int]` | Requirement IDs this component traces to |
| `source_fragment` | `str \| null` | Which subgraph produced this component |
| `confidence` | `float \| null` | SAAM coverage score |
| `parent_container_id` | `str` | ID of the container this component belongs to. Used in `ArchFragment` for merge; in the final nested `ArchModel`, the nesting makes this implicit. |
| `component_relationships` | `list[ArchRelationship]` | Relationships scoped to the component diagram — between components, and between components and external containers or external systems |

**`ArchPerson`** — a human actor. A flat leaf entity; never nested. Always referenced by ID from within relationships.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the person's role |
| `requirement_ids` | `list[int]` | Requirement IDs this person traces to |
| `source_fragment` | `str \| null` | Which subgraph produced this person |
| `confidence` | `float \| null` | SAAM coverage score |

**`ArchExternalSystem`** — an external software system. A flat leaf entity; never nested. Always referenced by ID from within relationships.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Canonical ID (lowercase, snake_case) |
| `label` | `str` | Human-readable display name |
| `description` | `str` | Short description of the external system's purpose |
| `technology` | `str \| null` | Technology annotation when known |
| `requirement_ids` | `list[int]` | Requirement IDs this external system traces to |
| `source_fragment` | `str \| null` | Which subgraph produced this external system |
| `confidence` | `float \| null` | SAAM coverage score |

**`ArchRelationship`**:

| Field | Type | Description |
|-------|------|-------------|
| `source_id` | `str` | Source entity ID |
| `target_id` | `str` | Target entity ID |
| `interaction_type` | `str` | Short verb phrase (e.g., "sends events to") |
| `technology` | `str \| null` | Protocol or technology used |
| `requirement_ids` | `list[int]` | Requirement IDs this relationship traces to |
| `source_fragment` | `str \| null` | Which subgraph produced this relationship |
| `diagram_scope` | `str` | Which C4 diagram level this relationship is visible in: `context`, `container`, or `component`. Determined by endpoint types — see scoping rules in §12. |

**`ArchPattern`**:

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Pattern name from the quality-architecture matrix |
| `rationale` | `str` | Why this pattern was selected |
| `quality_attributes` | `list[str]` | Quality attributes addressed |

**`OpenQuestion`**:

| Field | Type | Description |
|-------|------|-------------|
| `entity_id` | `str \| null` | Related entity ID, if applicable |
| `type` | `str` | One of: `change_risk`, `high_coupling`, `contention`, `tie`, `coverage_gap`, `hierarchy_conflict`, `scope_conflict` |
| `description` | `str` | Human-readable description |
| `scenario_ids` | `list[str]` | Contributing scenario or requirement IDs |

**`IncoherentBatchRecord`**:

| Field | Type | Description |
|-------|------|-------------|
| `batch_id` | `int` | Batch index |
| `coherence_score` | `float` | Final coherence score after split attempts |
| `reduced_confidence` | `bool` | True; flag for judge weight multiplier |

**`ConfidenceRecord`**:

| Field | Type | Description |
|-------|------|-------------|
| `reduced_confidence` | `bool` | True if entity originated from an incoherent batch (0.5× SAAM weight multiplier applied) |
| `source_batch` | `int` | Batch index that produced this entity |
| `saam_score` | `float` | SAAM weighted score of the fragment this entity came from |

---

## 5) Requirement Normalization

### Purpose
Ensure every requirement has consistent fields before embedding, search, and clustering. ARLO produces ASR and non-ASR dicts with slightly different field conventions; this step unifies them.

### ARLO Output Format (as-is)

Each dict in `asrs` and `non_asr` contains:

```json
{
  "id": 1,
  "is_architecturally_significant": true,
  "quality_attributes": ["Security", "Reliability"],
  "condition_text": "when the system is under load"
}
```

Note: `id` is an **integer** (positional, matching ARLO's `ParsedRequirement.id`). The requirement description text is not included — it must be resolved from the parent pipeline's `requirements` dict (`dict[str, str]`, keyed by string ID like `"R1"`).

### Normalized Schema

The normalization step enriches each ARLO dict into the following unified format used by all downstream RAA nodes:

```json
{
  "id": "string",
  "text": "string",
  "is_asr": true,
  "quality_attributes": ["string"],
  "condition_text": "string | null"
}
```

**Transform rules:**
- `id` is converted from int to string and mapped to the original requirement key (e.g., `1` → `"R1"`).
- `text` is resolved from the parent pipeline's `requirements` dict using the mapped key.
- `is_architecturally_significant` is renamed to `is_asr` for brevity.
- `condition_text` defaults to `null` for non-ASR requirements that lack conditions.
- `quality_attributes` defaults to an empty list for non-ASR requirements with no QA classification.

Non-ASR requirements with no quality attributes or condition text are normalized with null/empty values; they remain eligible for non-ASR embedding and batch inclusion.

---

## 6) Embedding Strategy (ASR Load + Non-ASR Generation)

### Overview

Embeddings are persisted in SQLite databases under `embeddings/` at the project root, not in LangGraph state channels. The RAA preparation node performs two tasks:

1. **Verify ASR embeddings** — confirm that `embeddings/asr_embeddings.db` exists and contains an embedding for every ASR in the `asrs` state channel. If any ASR is missing (e.g., ARLO was run before the SQLite persistence modification), raise an error instructing the operator to re-run ARLO.
2. **Generate non-ASR embeddings** — embed all non-ASR requirement texts from the `non_asr` state channel and write the results to `embeddings/non_asr_embeddings.db`.

After both steps complete, set `embeddings_ready = true` in the graph state. Downstream nodes (batch construction, overlap bridging, coherence gate) gate on this flag.

### Model

Use the **same FastEmbed model and version** that ARLO used for ASR embeddings: `mixedbread-ai/mxbai-embed-large-v1` (1024-dimensional, CPU-only via FastEmbed). This preserves the shared vector space required for meaningful cosine similarity comparison between ASR centroids and non-ASR candidates.

### What Text Is Embedded

- **ASR embeddings** (written by ARLO): the `condition_text` field of each ASR dict.
- **Non-ASR embeddings** (written by RAA): the requirement description text resolved from the parent pipeline's `requirements` dict, since non-ASR dicts typically lack meaningful `condition_text`.

### SQLite Schema

Both databases use an identical schema (see §4, Shared Embedding Persistence table):
- `requirement_id` (int, primary key) — matches the `id` field in ARLO's ASR/non-ASR dicts.
- `embedding` (blob) — the 1024-float vector, stored as a binary blob.
- `text_hash` (str) — SHA-256 hash of the embedded text, for cache integrity. If the hash doesn't match the current requirement text, the embedding is stale.
- `model_name` (str) — the FastEmbed model identifier used to produce this embedding.

### Cache Behaviour

On resume or re-run, the preparation node checks `text_hash` for each requirement against the current text. Only requirements with missing or stale hashes are re-embedded. This avoids redundant computation when the pipeline is resumed after a crash or when only a subset of requirements has changed.

### Downstream Access Pattern

Nodes that need embeddings (batch construction §8, overlap bridging §9, coherence gate §10) query the SQLite databases directly by requirement ID. They do not load all embeddings into memory at once — they load per-batch or per-group as needed. This keeps memory usage proportional to batch size, not total requirement count.

---

## 7) Prompt Constraint Injection Policy

**Purpose:** Keep prompts authoritative, scoped, and consistent across all LLM nodes.

**Rules:**
- Every LLM node that depends on C4 or SAAM receives only the **relevant excerpt blocks** from the Prompt Resource Bundle (§2C), not the full bundle.
- Excerpts are context-specific: a relationship-extraction node receives C4 relationship rules; a tradeoff node receives SAAM steps; a pattern-selection node receives C4 level definitions.
- Each prompt must explicitly restate the applicable C4 compliance rules as hard constraints (not suggestions).
- Each prompt running tradeoff analysis must explicitly restate the 5-step SAAM flow in order.
- Prompt injection is retrieval-based: the node queries the bundle by tag (e.g., `c4:relationships`, `saam:steps`), not by pasting the whole bundle.

---

## 8) Batch Construction Logic (Condition-Group Anchored)

### Anchor Representation
For each ARLO condition group:
- Preferred: **average of ASR embeddings** in the group (centroid vector). ASR embeddings are loaded from `embeddings/asr_embeddings.db` by the requirement IDs listed in the condition group's `conditions` field.
- Fallback: condition group `nominal_condition` text re-embedded on the fly using the same FastEmbed model.

### Non-ASR Candidate Selection
1. Run approximate nearest-neighbour (ANN) search against non-ASR embeddings (loaded from `embeddings/non_asr_embeddings.db`) using the group centroid.
2. Apply similarity threshold ≥ 0.65 to filter noise.
3. Cap at max 10 non-ASR candidates per group.

### Batch Assembly
- Batch = all ASRs in the condition group + selected non-ASR candidates.
- Stored with: group ID, group centroid, per-requirement similarity scores.

---

## 9) Overlap Bridging (1–3 Shared Requirements)

### Purpose
Ensure cross-batch coherence and enable shared architectural components to be discovered by multiple RAA runs.

### Strategy
1. Identify **adjacent or related condition groups** (same cluster ID or cosine similarity above threshold between centroids).
2. For each adjacent pair, find non-ASRs with high similarity to **both** group centroids.
3. Select 1–3 of these as **bridge requirements**. Hard cap: 3.
4. Inject bridge requirements into both batches.
5. Record in `bridge_requirements[pair] = [req_ids]`.

---

## 10) Batch Coherence Gate

### Rationale
Condition groups may exhibit semantic drift when their ASRs span multiple quality attributes loosely.

### Procedure

> **Metric clarification:** The coherence score here is the **average intra-batch cosine similarity** between each requirement embedding and the batch centroid. This is distinct from the per-requirement similarity threshold (≥ 0.65) used in §8 for non-ASR candidate selection, which measures individual requirement-to-group-centroid similarity.

1. Compute centroid of all requirement embeddings in the batch.
2. Compute average cosine distance from each requirement to the centroid.
3. **If coherence score < 0.55:**
   - Split into 2 sub-clusters; re-score each.
   - If both sub-clusters pass: replace batch with the two sub-batches in queue.
   - If still incoherent after split: add to `incoherent_batches` with `reduced_confidence = true`. Run as a single-RAA batch (not three-parallel). The judge receives the `reduced_confidence` flag and discounts this batch's output proportionally when updating `running_arch_model`.

---

## 11) Batch Queue Ordering

### Primary Strategy: Risk-First (default)
Sort batches by highest-risk quality attribute cluster first — security and reliability batches precede performance and usability. This ensures the most consequential architectural decisions are made earliest, when the `running_arch_model` is still sparse and most flexible.

Rationale: consistent with SAAM's emphasis on scenario-driven evaluation; high-risk decisions made late inherit more constraints and are harder to revise.

### Override Options (configurable)
- **By ASR count:** largest condition groups first (maximizes early coverage).
- **By aggregate quality weight:** groups with the highest summed ARLO quality weights first.

Configure via pipeline parameter `batch_ordering_strategy ∈ {risk_first (default), asr_count, quality_weight}`.

### Result
`batch_queue = [batch_1, batch_2, ...]` with full metadata per batch including ordering score and strategy used.

---

## 12) RAA Parallel Subgraphs per Batch

### Structure
Within each batch, **three RAA subgraphs run in parallel** using LangGraph's **Send API**. A conditional edge emits three `Send` objects — one per strategy (RAA-A, RAA-B, RAA-C) — each targeting the corresponding subgraph node with the batch state **and its assigned `ChatModel` instance**. All three execute in the same super-step. Results are collected into `batch_outputs` via its dict-merge append reducer.

Batches themselves are processed **sequentially** — each batch waits for the previous batch's judge step before starting.

**Exception:** Batches flagged as incoherent by the coherence gate (§10, `reduced_confidence = true`) run a **single RAA subgraph** instead of three parallel runs. The strategy for the single run defaults to RAA-A (SAAM-first), as it provides the broadest quality-attribute coverage for an uncertain batch. The judge receives the `reduced_confidence` flag and applies the 0.5× SAAM weight multiplier accordingly.

### LLM Instance Configuration

RAA accepts **4 distinct LLM instances** from the orchestrator, one per functional role. All four are passed via LangGraph's `context={}` dict — **never via state channels** — to prevent LLM objects from being serialised into checkpoints (per Orchestrator Plan §3C).

| Role | Context Key | Used By |
|------|-------------|---------|
| RAA-A LLM | `llm_raa_a` | RAA-A subgraph (SAAM-first strategy) |
| RAA-B LLM | `llm_raa_b` | RAA-B subgraph (Pattern-driven strategy) |
| RAA-C LLM | `llm_raa_c` | RAA-C subgraph (Entity-driven strategy) |
| Judge LLM | `llm_judge` | Judge node (SAAM scoring, merge conflict reconciliation) |

The orchestrator resolves UI-assigned instance names to instantiated `ChatModel` objects and passes them via the `context` parameter at graph invocation:

```python
# Orchestrator invokes RAA with all 4 LLMs in context
raa_graph.invoke(
    state_payload,
    {"configurable": {"thread_id": thread_id}},
    context={
        "llm_raa_a": raa_a_instance,
        "llm_raa_b": raa_b_instance,
        "llm_raa_c": raa_c_instance,
        "llm_judge": raa_judge_instance,
    },
)
```

Within the graph, nodes access their assigned LLM from the runtime context. The conditional edge reads LLMs from context and forwards them to each `Send` payload:

```python
# Conditional edge emitting three Send objects with per-subgraph LLMs from context
def fan_out_subgraphs(state, config):
    ctx = config.get("context", {})
    batch = state["batch_queue"][state["batch_cursor"]]
    common = {
        "batch": batch,
        "quality_weights": state["quality_weights"],
        "running_arch_model": state["running_arch_model"],
    }
    return [
        Send("raa_a", {**common, "llm": ctx["llm_raa_a"]}),
        Send("raa_b", {**common, "llm": ctx["llm_raa_b"]}),
        Send("raa_c", {**common, "llm": ctx["llm_raa_c"]}),
    ]
```

The judge node reads `config["context"]["llm_judge"]` from the runtime context. No uniqueness constraint is enforced — the user may assign the same model to all four slots or use different models per role. Since LangGraph nodes are plain functions that receive state and config, each node simply calls its assigned `ChatModel` instance from context. No special LangGraph configuration is required to support heterogeneous models.

### Subgraph Strategies

| Subgraph | Strategy | Prompt Focus |
|----------|----------|--------------|
| RAA-A | Conservative, SAAM-first | Quality attribute scenarios drive entity selection |
| RAA-B | Pattern-driven | Architectural patterns (layered, event-driven, CQRS, etc.) mapped to requirements |
| RAA-C | Entity/relationship-driven | Bottom-up entity extraction, C4 relationship mapping |

### Input to Each RAA Subgraph
- Current batch requirements (normalized)
- ARLO quality weights
- `running_arch_model` constraints from judge (entities and relationships already decided; must not contradict)
- Bridge requirements context (if applicable)
- Relevant Prompt Resource Bundle excerpts (§7)

### Output per Subgraph
A partial `ArchFragment`: typed lists of systems, containers, components, persons, external_systems + directed relationships (each with `diagram_scope`) + selected patterns + rationale. No diagrams. No code.

### Hierarchy Placement Responsibilities

Each of the three parallel RAA subgraphs (RAA-A, RAA-B, RAA-C) is responsible for not only extracting entities and relationships but also for placing each entity at the correct level in the hierarchy and recording its parent association.

**Container parent assignment:** When a subgraph proposes a container entity, it must also propose which system that container belongs to by recording `parent_system_id` in the fragment's container entry. If the subgraph is introducing a new system in the same fragment to host that container, it must include that system in the fragment's `systems` list. If the container belongs to a system already present in `running_arch_model`, the subgraph uses that system's existing canonical ID.

**Component parent assignment:** When a subgraph proposes a component entity, it must record `parent_container_id` pointing to the container that houses it. That container must either be present in the same fragment or already exist in `running_arch_model`. A subgraph must never propose a component without also ensuring a container is present (either in the same fragment or in `running_arch_model`), and must never propose a container without ensuring a system is present. This prevents orphan entities from entering the merge pipeline.

**Relationship scoping rules:** Every relationship must carry an explicit `diagram_scope` value. The rules are:

| Endpoint types | `diagram_scope` |
|---|---|
| system ↔ system, system ↔ person, system ↔ external_system | `context` |
| container ↔ container, container ↔ person, container ↔ external_system | `container` |
| component ↔ component, component ↔ container, component ↔ external_system | `component` |

**Prompt updates:** The relevant prompts for all three subgraphs are updated to include these scoping rules as hard constraints, drawn from the C4 Level Mapping skill (§14, `C4_Level_Mapping.md`). The cross-batch constraint injection (§15) serialises the current `running_arch_model` hierarchy (systems with their containers, containers with their components) in the prompt so each subgraph can see which parent nodes already exist and assign parents correctly.

---

## 13) Judge Node (Per-Batch)

### Responsibilities
1. Receive the three `ArchFragment` outputs from RAA-A, B, C.
2. Run SAAM scenario scoring (§2B SAAM constraints) weighted by ARLO quality weights. Uses `state["llm_judge"]` for all LLM calls (conflict reconciliation, gap analysis).
3. Select the best candidate fragment as the primary output.
4. **Merge useful parts** from the non-selected fragments via the merge algorithm below.
5. Consistency-check the merged output against `running_arch_model`.
6. Run residual scan before discarding losing fragments (§13 Residual Scan).
7. Update `running_arch_model`, `open_questions`, and advance `batch_cursor`.

### Merge Algorithm
The judge merges fragments in four deterministic steps:

1. **Entity deduplication (per-type):** Deduplication operates per entity type — systems against systems, containers against containers, components against components, persons against persons, external systems against external systems. Canonical ID normalisation is unchanged (lowercase, snake_case, trimmed). Entities present in multiple fragments are merged: longest description wins; technology annotation from any fragment that provides one is retained.

    **Hierarchy conflict detection:** When two fragments both propose a container with the same canonical ID but different `parent_system_id` values, this is treated as a conflict (not a duplicate) and recorded in `open_questions` with type `hierarchy_conflict`. When `parent_system_id` matches, normal deduplication applies. The same rule applies to components with conflicting `parent_container_id` values.

2. **Relationship deduplication:** canonical key = `(source_id, target_id, interaction_type)`. If two fragments define the same canonical key with conflicting descriptions, prefer the fragment with the higher SAAM score. The judge additionally verifies that the `diagram_scope` of a deduplicated relationship is consistent across fragments. If two fragments assign the same relationship to different scopes, the judge selects the scope consistent with the endpoint types (using the scoping rules defined in §12) and records a warning in `open_questions` with type `scope_conflict`. Flag irreconcilable conflicts.

3. **Coverage union with orphan prevention:** any entity or relationship present in a non-selected fragment that is not already in the primary selection and has SAAM scenario coverage > 0 is considered for addition. Before adding an entity from a non-selected fragment via the union step, the judge verifies that its parent entity (system for a container, container for a component) either already exists in the merged output or is being added in the same union pass. An orphaned container (no system parent resolvable) or orphaned component (no container parent resolvable) is **not added** to the merged output; it is instead recorded in `open_questions` with type `coverage_gap` noting the missing parent.

4. **Tree assembly:** After the three merge steps complete, the judge assembles the final `ArchModel` contribution for this batch. The flat merged lists (systems, containers, components, persons, external_systems, relationships) are nested into the hierarchical structure: containers are inserted into their parent system's `containers` list, components are inserted into their parent container's `components` list, and relationships are distributed into the correct `context_relationships`, `container_relationships`, or `component_relationships` list based on `diagram_scope`. Context-level relationships (scope = `context`) are placed on the system node. Container-level relationships (scope = `container`) are placed on the container node. Component-level relationships (scope = `component`) are placed on the component node. This tree-assembly step is deterministic and requires no LLM involvement.

The `best_batch_output` for this batch records the assembled fragment's contribution (as additions and updates to the running tree) rather than a flat list.

### Residual Scan
Before discarding a losing fragment, the judge checks: does it contain any entity or relationship with SAAM coverage that the selected fragment lacks? If yes, carry it forward via the coverage union step above.

### Reduced-Confidence Batches
If the current batch has `reduced_confidence = true` (set by coherence gate §10), the judge applies a 0.5× weight multiplier to all SAAM scores from this batch when updating `running_arch_model`. The flag is recorded in the model metadata.

### Decision Output
- `best_batch_output[batch_index]`: merged fragment for this batch
- Updated `running_arch_model`
- Updated `open_questions`
- Advanced `batch_cursor`

---

## 14) Skills vs Static Templates

### Skill Resource Bundle

The **Skill Resource Bundle** is the `Skills/RAA/` directory. It contains:

- `SKILL.MD` — the RAA skill definition (pipeline overview, execution model, state channels, constraints)
- `references/` — authoritative and skill-specific reference documents

This bundle is a **design-time reference** — it documents what RAA does and how it works. It does not contain runtime prompt templates or code. Those live in the `RAA/` code directory (see §21).

#### Existing Reference Files

| File | Type | Covers |
|------|------|--------|
| `references/SAAM.md` | Authoritative adaptation | Adapted 5-step SAAM process for judge scoring, scenario classification rules, merge algorithm, tie-breaking, hotspot detection |

#### Reference Files To Create

Six operational skills are listed below (§14 Use Skills For). Each requires a reference file in `Skills/RAA/references/`. Two additional authoritative references are needed for the C4 model and quality attribute taxonomy.

**Authoritative references:**

| # | File | Type | Covers | Referenced By |
|---|------|------|--------|---------------|
| 1 | `references/C4.md` | Authoritative | C4 model adapted for RAA: the three levels (Context, Container, Component), element types (`system`, `container`, `component`, `person`, `external_system`), notation rules (labels, descriptions, technology annotations), relationship syntax (direction, interaction descriptions), boundary grouping rules, and level-mixing prohibition. Source: https://c4model.com | Entity extraction, Relationship extraction, C4 level mapping |
| 2 | `references/Quality_Attributes.md` | Authoritative | ISO/IEC 25010 quality attributes as used in the pipeline: Performance Efficiency, Compatibility, Usability, Reliability, Security, Maintainability, Portability, Cost Efficiency. Each attribute defined with representative ASR condition examples and scenario-evaluation prompts for SAAM scoring. | Pattern selection, SAAM judge, Entity extraction |

**Skill-specific references (one per LLM skill node):**

| # | File | Type | Covers | Used By |
|---|------|------|--------|---------|
| 3 | `references/Entity_Extraction.md` | Skill | Guidelines for extracting C4 entities from normalized requirements: when to introduce a System vs Container vs Component; naming conventions (canonical ID derivation); parent-child boundary assignment (`parent_system_id` and `parent_container_id`); technology annotation confidence thresholds; handling ambiguous or underspecified requirements. **Hard rule:** a subgraph must never propose a component without also ensuring a container is present (either in the same fragment or in `running_arch_model`), and must never propose a container without ensuring a system is present. This prevents orphan entities from entering the merge pipeline. References C4.md for type definitions. | RAA-A, RAA-B, RAA-C subgraphs |
| 4 | `references/Relationship_Extraction.md` | Skill | Guidelines for deriving directed relationships from requirement text: interaction type verb phrases; technology inference for relationship protocols; cardinality and directionality rules; handling transitive and implicit relationships; conflict resolution when two requirements imply contradictory relationships. **Hard rule:** every proposed relationship must carry an explicit `diagram_scope` value assigned according to the scoping rules in §12 (system-level interactions → `context`, container-level → `container`, component-level → `component`). References C4.md for relationship syntax. | RAA-A, RAA-B, RAA-C subgraphs |
| 5 | `references/Pattern_Selection.md` | Skill | Guidelines for selecting architectural patterns from the quality-architecture matrix (`data/matrix.json`): ILP optimizer constraints, greedy fallback rules, quality-attribute-to-pattern mapping rationale, pattern combination compatibility rules (which patterns can coexist). References Quality_Attributes.md for attribute definitions. | RAA-B subgraph (pattern-driven) |
| 6 | `references/Technology_Inference.md` | Skill | Guidelines for inferring technology stack annotations from requirement text: signal keywords for common stacks (databases, message brokers, API protocols, deployment targets), confidence levels for inference, when to leave technology as null vs make a best-effort guess, handling conflicting technology signals. | RAA-A, RAA-B, RAA-C subgraphs |
| 7 | `references/C4_Level_Mapping.md` | Skill | Guidelines for assigning entities to C4 levels: rules for promoting/demoting entities between Context, Container, and Component based on scope and granularity; handling entities that span levels; ensuring the three-level hierarchy is internally consistent. **Expanded coverage:** how to assign `parent_system_id` when a container's owning system is implicit in the requirements; how to assign `parent_container_id` when a component's owning container must be inferred; how to handle a requirement that implies a component without any container context (the rule is: the subgraph must propose a container to host it, naming it conservatively based on the component's domain); and the `diagram_scope` assignment rules for all relationship endpoint combinations. References C4.md for level definitions. | All RAA subgraphs (entity output validation) |

#### Skill Reference File Template

Each skill reference file follows a consistent structure:

1. **Purpose** — what the skill does, when it is invoked
2. **Input** — what data the skill receives from the RAA state
3. **Normative rules** — hard constraints the LLM must follow (bulleted, testable)
4. **Decision guidelines** — heuristics for ambiguous cases (not hard rules, but strong defaults)
5. **Output schema** — what the skill must produce (references ArchSystem / ArchContainer / ArchComponent / ArchPerson / ArchExternalSystem / ArchRelationship / ArchPattern types from §4)
6. **Error cases** — known failure modes and how the skill should handle them
7. **Examples** — one worked example from the custom requirements dataset (`data/requirements.json`)

Authoritative references (C4.md, Quality_Attributes.md) omit the Input/Output sections — they define the domain, not a skill contract.

#### Updated Skills Directory Layout

```
Skills/RAA/
├── SKILL.MD
└── references/
    ├── SAAM.md                    # Adapted SAAM process (existing)
    ├── C4.md                      # C4 model adapted for RAA (to create)
    ├── Quality_Attributes.md      # ISO/IEC 25010 quality attributes (to create)
    ├── Entity_Extraction.md       # Entity extraction guidelines (to create)
    ├── Relationship_Extraction.md # Relationship mapping guidelines (to create)
    ├── Pattern_Selection.md       # Architectural pattern selection (to create)
    ├── Technology_Inference.md    # Technology stack inference (to create)
    └── C4_Level_Mapping.md        # C4 level assignment rules (to create)
```

### Use Skills For (interpretation/generation nodes)
- Entity extraction
- Relationship extraction
- Pattern selection
- Technology stack inference
- C4 level mapping (Context / Container / Component)

### Use Static Templates For (deterministic nodes)
- SAAM scenario scoring (weighted formula, not LLM)
- JSON schema assembly
- Batch queue construction
- Entity deduplication and merge (deterministic algorithm per §13)

**Reason:** Skills enforce specialization and reduce context drift. Static templates enforce determinism where the output must be reproducible regardless of temperature or model version.

---

## 15) Cross-Batch Coherence Injection

### Rule
Before each batch's RAA subgraphs run, inject the current `running_arch_model` into all three RAA prompts as hard constraints. The serialised `running_arch_model` injected into subgraph prompts is the hierarchical tree (systems with their containers, containers with their components). This is more informative than the old flat list because subgraphs can see not just that a container exists but which system it belongs to, making coherent parent assignment easier in subsequent batches.

> "The following components and relationships are already part of the architecture model. You must be consistent with them. Do not rename, restructure, or contradict any listed entity or relationship."

This prevents naming collisions and contradictory architecture decisions accumulating across batches.

---

## 16) Final Merge (After All Batches)

### Input
All `best_batch_output` fragments + final `running_arch_model`.

### Merge Process
1. Apply the same deterministic merge algorithm from §13 globally across all batch fragments.
2. Resolve any remaining `open_questions` via a single focused LLM reconciliation pass (strictly scoped to listed conflicts; not a full re-analysis).
3. Validate output against C4 schema (§19).

### Output
**C4-compliant JSON** — a serialised `ArchModel` instance, structurally identical to the `C4JsonModel` schema defined in the AGA plan (§1). The model is strictly hierarchical: entity type is encoded by structural position, not a discriminator field. Contains:

| Field | Type | Description |
|-------|------|-------------|
| `systems` | `list[ArchSystem]` | All software systems, each fully populated with its `context_relationships` list and its `containers` list. Each container in turn contains its `container_relationships` list and its `components` list. Each component contains its `component_relationships` list. |
| `persons` | `list[ArchPerson]` | Flat global list of human actors, deduplicated across all batches |
| `external_systems` | `list[ArchExternalSystem]` | Flat global list of external software systems, deduplicated across all batches |
| `patterns` | `list[ArchPattern]` | Selected architectural patterns with rationales |
| `diagram_manifest` | `list[DiagramManifestEntry]` | Deterministically generated work queue for AGA — one entry per diagram to produce. Generated during final merge by traversing the hierarchy; no LLM involvement. |
| `confidence_metadata` | `dict[str, ConfidenceRecord]` | Per-entity confidence flags, keyed by entity ID. Applies to any entity type (system, container, component, person, or external system). Includes `reduced_confidence` for incoherent-batch entities. |
| `open_questions` | `list[OpenQuestion]` | Unresolved hotspots, ties, and coverage gaps passed through to AGA for the session report |

### Diagram Manifest

The `diagram_manifest` is a deterministically generated list produced during final merge by traversing the hierarchy. AGA uses this manifest as its work queue — it does not traverse the JSON independently to discover what diagrams to draw. For a model with N systems where system `i` has `k_i` containers, the manifest contains `N` context diagram entries, `N` container diagram entries, and `k_1 + k_2 + ... + k_N` component diagram entries. Total diagrams = `(number of systems × 2) + (total number of containers across all systems)`.

**`DiagramManifestEntry`**:

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | Stable, canonical string derived from the entity ID (e.g., `ctx-{system_id}`, `cnt-{container_id}`, `cmp-{component_id}`) |
| `diagram_type` | `str` | One of `context`, `container`, or `component` |
| `focus_entity_id` | `str` | The system ID for context and container diagrams, the container ID for component diagrams |
| `label` | `str` | Human-readable diagram label (e.g., "System Context — payment_service") |

**Diagram generation contract:** There is exactly one context diagram per system entity (showing the system alongside any persons and external systems it directly interacts with at the context level). There is exactly one container diagram per system entity (zooming into the system to show its containers with the persons and external systems those containers interact with). There is exactly one component diagram per container entity (zooming into the container to show its components with any other containers or external systems those components interact with). AGA's only responsibility is to traverse to the `focus_entity_id` in the hierarchy for each manifest entry, collect the relevant sub-tree and relationships, and render the diagram. No filtering or scoping logic is needed in AGA — the manifest provides a precise, ordered work queue.

### Downstream Handoff
This JSON is the input to the **Architecture Generation Agent (AGA)**, which handles all code and diagram generation including PlantUML and C4 diagram rendering. AGA no longer needs to implement any filtering or scoping logic to discover which entities belong to which diagram. The `diagram_manifest` gives it a precise, ordered work queue. AGA's only responsibility is to traverse to the `focus_entity_id` in the hierarchy for each manifest entry, collect the relevant sub-tree and relationships, and render the diagram. RAA does not produce any diagrams or code.

### Filesystem Output

The final merged C4-compliant JSON model is written to the project-scoped output directory at `projects/{project_name}/output/raa/arch_model.json`. The output directory path is **provided by the orchestrator** at invocation time — the RAA module does not hardcode or assume a default output path. The orchestrator creates the `output/raa/` directory before RAA invocation (per Orchestrator Plan §2C).

---

## 17) Performance & Cost Profile

| Operation | Complexity |
|-----------|------------|
| Non-ASR embedding | O(n) where n = non-ASR count |
| ANN similarity search | O(k × m) where k = condition groups, m = non-ASR pool |
| Cosine similarity matrix | Not computed — ANN only |
| RAA LLM calls | 3 per batch × number of batches (reduced to 1 for incoherent/reduced-confidence batches per §10). Each subgraph may use a different model (context keys `llm_raa_a/b/c`); cost varies per model selection. |
| Judge LLM calls | 1 per batch (deterministic merge; LLM only for conflict reconciliation). Uses context key `llm_judge`, which may be a different model than subgraph LLMs. |

Memory: per-batch embedding loads from SQLite, O(batch_size). Full embedding corpus stays on disk, not in memory.

---

## 18) Failure Modes & Mitigations

| Risk | Mitigation |
|------|------------|
| Condition group has semantic drift | Coherence gate (§10) splits or flags with reduced confidence |
| No good non-ASR matches for a group | Allow empty non-ASR list; batch proceeds with ASRs only |
| Cross-batch entity naming collisions | `running_arch_model` constraint injection (§15) + entity deduplication in judge (§13) |
| Overlap exceeds 3 bridge requirements | Hard cap enforced in §9 |
| Judge discards a useful artifact | Residual scan before fragment discard (§13) |
| Incoherent batch degrades model | `reduced_confidence` flag + 0.5× SAAM weight multiplier in judge |
| Reconciliation LLM introduces new conflicts | Reconciliation pass is strictly scoped to listed `open_questions`; output validated against C4 schema before acceptance |
| ASR embedding DB missing or incomplete | RAA preparation node (§6) verifies all ASR IDs are present in `asr_embeddings.db` before proceeding; raises a blocking error with instructions to re-run ARLO if any are missing |
| Embedding text hash mismatch (stale embedding) | Preparation node recomputes embeddings for requirements whose `text_hash` does not match current text; logs a warning for each stale entry |
| Embedding DB corrupted or locked | Fall back to full recomputation of affected DB (ASR or non-ASR); emit a `WARNING` log. Non-ASR DB can always be rebuilt; ASR DB requires ARLO re-run if unrecoverable |

---

## 19) Validation & Testing Criteria

### Unit Tests
- Non-ASR embeddings in `non_asr_embeddings.db` use identical FastEmbed model version (`model_name` column) as ASR embeddings in `asr_embeddings.db`.
- Preparation node rejects startup if `asr_embeddings.db` is missing or incomplete (missing ASR IDs).
- Stale `text_hash` entries trigger recomputation, not silent reuse.
- Batch assembly includes all ASRs from the condition group.
- Bridge requirement overlap does not exceed 3 per adjacent pair.
- Coherence gate correctly splits a synthetic heterogeneous batch and passes a homogeneous one.
- Entity deduplication operates per entity type (systems, containers, components, persons, external_systems) and produces canonical IDs in deterministic order regardless of fragment input order. Hierarchy conflicts (same ID, different parent) are correctly detected and recorded in `open_questions`.

### Integration Tests
- End-to-end for 3 batches with known overlaps: verify bridge requirements appear in both adjacent batches.
- Judge correctly merges and updates `running_arch_model`; entities from batch N+1 do not contradict entities from batch N.
- Incoherent batch produces `reduced_confidence = true` in final model metadata.

### Functional Tests
- **Structural integrity:** every container in the JSON must be nested inside a system node; every component must be nested inside a container node; no entity ID appears at more than one level in the hierarchy (a string ID used as a system ID cannot also appear as a container ID); every relationship's `source_id` and `target_id` resolve to an entity that exists somewhere in the model (systems, containers, components, persons, or external_systems); and every relationship's `diagram_scope` is consistent with the types of its endpoints according to the scoping rules defined in §12.
- **Manifest completeness:** the `diagram_manifest` list must contain exactly one context entry and one container entry per system, and exactly one component entry per container. The manifest length must equal `(2 × len(systems)) + sum(len(s.containers) for s in systems)`.
- **Orphan prevention:** given a synthetic fragment containing a component with a `parent_container_id` that does not exist anywhere in the running model or the same fragment, the judge must record a `coverage_gap` open question and must not add the component to the merged output.
- Cross-batch entities remain consistent: same canonical ID, no contradictory relationship directions.
- **SAAM scoring correctness:** given two synthetic RAA fragments with known quality-attribute coverage profiles, judge must rank higher the fragment with greater weighted SAAM scenario coverage. Verified against a golden fixture with ground-truth expected ranking.

---

## 20) Deliverables for Spec Kit

1. **State schema** — all channels, types, and ownership (§4)
2. **Batch construction node** — anchor computation, ANN search, assembly (§8)
3. **Overlap bridging logic** — adjacent group detection, bridge selection, hard cap (§9)
4. **Coherence gate** — scoring, split procedure, `incoherent_batches` fallback (§10)
5. **Parallel RAA orchestration** — three-subgraph structure, input contracts, output schema (§12)
6. **Judge node — scoring, merge algorithm, and residual scan** (§13)
7. **Final JSON builder** — deterministic merge + reconciliation pass + C4 validation (§16)
8. **Prompt Resource Bundle** — Source Register, normative C4 and SAAM constraints, Doc Excerpt Blocks, retrieval tagging scheme (§2)
9. **Skill Resource Bundle** — `Skills/RAA/` directory with SKILL.MD and 8 reference files (§14): SAAM.md (existing), C4.md, Quality_Attributes.md, Entity_Extraction.md, Relationship_Extraction.md, Pattern_Selection.md, Technology_Inference.md, C4_Level_Mapping.md

---

## 21) Project Directory Layout & Resource Bundles

RAA follows the same directory convention as ARLO. Two separate directories serve distinct purposes. Additionally, a shared `embeddings/` directory at the project root stores embedding SQLite databases produced by ARLO and consumed/extended by RAA.

### 21A-0 — Shared Embedding Persistence (`embeddings/`)

```
<project_root>/
└── embeddings/
    ├── asr_embeddings.db         # Written by ARLO; read by RAA
    └── non_asr_embeddings.db     # Written and read by RAA
```

This directory is **not version-controlled** (add to `.gitignore`). Both databases use the schema defined in §4 (Shared Embedding Persistence). The `embeddings/` directory is created by ARLO's embedding node on first run; RAA creates `non_asr_embeddings.db` during its preparation step.

### 21A — Skill Resource Bundle (`Skills/RAA/`)

Design-time reference for agents and developers. Contains the skill definition and authoritative reference documents. Does **not** contain runtime code or prompt templates.

```
Skills/RAA/
├── SKILL.MD                              # RAA skill definition (pipeline, execution model, constraints)
└── references/
    ├── SAAM.md                           # Adapted SAAM process for judge scoring
    ├── C4.md                             # C4 model adapted for RAA (three levels, element types, notation)
    ├── Quality_Attributes.md             # ISO/IEC 25010 quality attribute definitions
    ├── Entity_Extraction.md              # Entity extraction guidelines
    ├── Relationship_Extraction.md        # Relationship mapping guidelines
    ├── Pattern_Selection.md              # Architectural pattern selection guidelines
    ├── Technology_Inference.md           # Technology stack inference guidelines
    └── C4_Level_Mapping.md               # C4 level assignment rules
```

### 21B — Code & Prompt Template Directory (`raa/`)

Runtime code and prompt templates. Follows the same structure as `arlo/` (which contains `arlo/prompts/`, `arlo/nodes/`, `arlo/state/`, etc.). The directory is **lowercase** (`raa/`) to match the naming convention of all other agent code directories (`arlo/`, `sa/`, `reporting/`, `orchestrator/`).

```
raa/
├── __init__.py
├── llm.py
├── runner.py
├── graphs/
├── models/
├── nodes/
├── state/
├── utils/
└── prompts/                              # Runtime prompt templates (§2C) — matches arlo/prompts/
    ├── source_register.md                # §2A table: source name, URL, retrieval date, scope
    ├── c4_constraints.md                 # §2B C4 normative rules as prompt constraints
    ├── saam_constraints.md               # §2B SAAM 5-step constraints as prompt constraints
    └── excerpts/
        ├── c4_levels.txt                 # ≤25-word excerpt: level definitions
        ├── c4_notation.txt               # ≤25-word excerpt: labelling and relationship rules
        ├── c4_technology.txt             # ≤25-word excerpt: technology annotation requirement
        ├── saam_steps.txt                # ≤25-word excerpt: 5-step process summary
        └── saam_scenarios.txt            # ≤25-word excerpt: scenario selection guidance
```

> **Convention parallel:** Just as `arlo/` contains both code (`arlo/nodes/`, `arlo/state/`) and prompt templates (`arlo/prompts/`), `raa/` uses `raa/prompts/` for the same purpose. The `Skills/` directory is for skill definitions only — never for runtime resources.

### 21C — Tagging Scheme for Prompt Retrieval

**Tagging scheme for retrieval:**

| Node | Tags requested |
|------|---------------|
| Entity extraction | `c4:levels`, `c4:notation` |
| Relationship extraction | `c4:notation`, `c4:technology` |
| Pattern selection | `c4:levels` |
| SAAM tradeoff (judge) | `saam:steps`, `saam:scenarios` |
| Final merge / reconciliation | `c4:levels`, `c4:notation`, `c4:technology` |

### 21D — Authority Direction

```
Source Register (§2A)  →  Prompt Resource Bundle (raa/prompts/)  →  Skill prompts (runtime)
                              ↑
                    Skill Resource Bundle (Skills/RAA/) documents what/why
```

---

## 22) SQLite Checkpointing & Crash Recovery

### Purpose

The RAA pipeline is long-running: non-ASR embedding, multi-batch sequential execution, three parallel RAA subgraphs per batch, and a per-batch judge pass can span minutes to hours depending on requirements volume. If the process is interrupted — kernel OOM kill, network timeout, operator error — all in-progress state is lost and the pipeline must restart from scratch. SQLite checkpointing eliminates this cost by persisting the full LangGraph state after every super-step, enabling resumption from the last committed checkpoint.

---

### 22A — Checkpointer Configuration

Use `SqliteSaver` from the `langgraph-checkpoint-sqlite` package (installed separately from `langgraph`). The checkpoint database path is **received from the orchestrator at runtime** — the orchestrator passes a project-scoped path `projects/{project_name}/checkpoints/raa_graph.db` when calling `compile_for_production(db_path=...)` (see Orchestrator Plan §6C). The RAA module's `compile_for_production()` accepts `db_path` as a **required parameter** with no default, ensuring the caller (orchestrator) always provides the project-scoped path.

```
projects/{project_name}/
└── checkpoints/
    └── raa_graph.db       # SQLite database written by SqliteSaver
```

Initialize `SqliteSaver` by passing it a `sqlite3` connection pointing to the orchestrator-provided `db_path`. The RAA module does **not** create the `checkpoints/` directory itself — directory creation is the orchestrator's responsibility.

---

### 22B — Graph Compilation

Pass the checkpointer at compile time so LangGraph automatically persists state at every super-step boundary. No further instrumentation is required. LangGraph writes a checkpoint after each super-step completes; the checkpoint captures the full `RAAState` channel snapshot at that moment.

---

### 22C — Thread Identity & Run Configuration

Each pipeline execution is identified by a **`thread_id`**. The thread ID is the key used to retrieve and resume a specific run. Use a stable, deterministic identifier derived from the input set — specifically a SHA-256 hash of the ARLO output version hash concatenated with a run label, truncated to 16 hex characters, prefixed with `raa-`. This ensures the same run can be targeted by monitoring tools or a manual resume command, and that the ID is reproducible across restarts for the same input.

The thread ID is passed to the graph via the `configurable` dict in the run configuration: `{"configurable": {"thread_id": "<computed_id>"}}`.

---

### 22D — Entry Point: Fresh Start vs. Resume

At process startup, query the checkpointer for an existing state snapshot using `graph.get_state(run_config)` before invoking the graph. If a snapshot exists and its `batch_cursor` is non-zero, the pipeline resumes from that point — LangGraph replays from the last committed checkpoint, skipping all completed batches. If no snapshot exists or `batch_cursor` is zero, the pipeline starts fresh with the initial state.

**Invariant:** `batch_cursor` is the authoritative resume marker. It is advanced by the judge node at the end of each batch (§13, Decision Output). Because the checkpoint is written after the judge's super-step commits, a resume will never re-execute an already-judged batch.

---

### 22E — Checkpoint Granularity & What Is Persisted

LangGraph creates a checkpoint at each **super-step boundary** — a super-step is a single tick of the graph where all nodes scheduled for that step execute (potentially in parallel). Within a super-step, individual node outputs are stored as **pending writes** (task-level entries) for fault tolerance: if one node in a super-step fails, successfully completed nodes' writes are preserved and not re-executed on resume. Full `StateSnapshot` checkpoints are committed only when the entire super-step completes.

The RAA pipeline's critical state channels persisted at each checkpoint are:

| State Channel | Checkpoint Significance |
|---|---|
| `batch_cursor` | Primary resume marker; determines which batch to start from next. |
| `batch_queue` | Full ordered batch list; rebuilt from checkpoint, not recomputed. |
| `embeddings_ready` | If `true`, the preparation node (§6) is skipped on resume — ASR and non-ASR embeddings are already persisted in SQLite. |
| `running_arch_model` | Accumulated architecture decisions in hierarchical form (systems → containers → components); injected into next batch's RAA prompts (§15). LangGraph's `JsonPlusSerializer` handles nested dataclasses. |
| `best_batch_output` | Per-batch judge decisions; available for final merge (§16) without re-running. |
| `open_questions` | Unresolved conflicts carried forward across batches. |
| `bridge_requirements` | Overlap mappings; not recomputed on resume. |
| `incoherent_batches` | Coherence gate records; preserved so final merge receives correct confidence flags. |

All channels in the `RAAState` TypedDict are serialised by LangGraph's default serialiser (`JsonPlusSerializer`). Custom dataclasses (`ArchModel`, `ArchFragment`, `ArchSystem`, `ArchContainer`, `ArchComponent`, `ArchPerson`, `ArchExternalSystem`, `ArchRelationship`, `ArchPattern`) must be serialisable by `JsonPlusSerializer`, which supports standard Python types, dataclasses, and nested dataclass structures. The hierarchical `ArchModel` (systems containing containers containing components) is handled natively by `JsonPlusSerializer` — no additional serialisation annotation is required. For types not supported by the default serialiser, annotate with a LangGraph-compatible `Annotated` reducer or ensure `__dict__`-compatible serialisation.

---

### 22F — Checkpoint Lifecycle & Cleanup

**Retention policy:** Checkpoint files are not deleted automatically. Completed runs should be archived or pruned by a post-run hook to prevent unbounded growth of `raa_graph.db`.

After a successful final merge (§16), move the checkpoint database to an archive subdirectory at `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db`. This archive operation must occur **only after** the final merged JSON output has been written to disk and validated against the C4 schema (§19). Archiving before validation risks losing the checkpoint if post-merge validation fails.

**Failed runs:** If the final merge fails validation, the checkpoint remains in place at the orchestrator-provided `db_path` and can be resumed or inspected without data loss.

---

### 22G — Failure Mode Coverage

| Failure Mode | Checkpointing Behaviour |
|---|---|
| Process killed mid-embedding (§6) | Non-ASR embedding SQLite writes are transactional — partial writes are rolled back. On resume, the preparation node checks `embeddings_ready` in the checkpoint; if `false` or absent, it re-runs the embedding step. The SQLite cache-check (`text_hash`) skips requirements that were already successfully persisted before the crash, so only the incomplete portion is recomputed. |
| Process killed mid-batch (inside a parallel RAA subgraph) | The interrupted super-step has not committed a full checkpoint; however, any subgraphs that completed before the kill have their outputs stored as pending writes. On resume, LangGraph re-runs only the failed subgraph(s) within the batch, not all three. `batch_cursor` still points to the interrupted batch. |
| Process killed after judge commits | `batch_cursor` has advanced past the completed batch; the judge's super-step checkpoint is committed. Resume starts the next batch with the correct `running_arch_model` already in state. |
| Process killed during final merge (§16) | Final merge node has not committed; resume re-runs the merge from all `best_batch_output` fragments already in state. No batch re-execution needed. |
| Checkpoint DB corrupted | LangGraph raises on `get_state`; handle with a try/except that falls back to a fresh start with a warning. Never silently discard a corrupt checkpoint without operator acknowledgement. |

---

### 22H — Integration with §18 Failure Modes Register

Add the following rows to the §18 table:

| Risk | Mitigation |
|---|---|
| Process killed mid-pipeline (OOM, timeout, SIGKILL) | SQLite checkpoint (§22) persists state after every super-step; resume skips completed batches. |
| Checkpoint DB unavailable at startup | Fall back to fresh start; emit a `WARNING` log; do not crash. |
| `batch_cursor` desync (checkpoint advanced but output not written) | Final merge (§16) validates all `best_batch_output` keys before running; missing keys trigger a targeted batch re-run rather than full restart. |
| Embedding SQLite DB missing at RAA startup | `asr_embeddings.db` missing → blocking error; operator must re-run ARLO. `non_asr_embeddings.db` missing → preparation node rebuilds it from scratch. |
| Embedding SQLite DB locked (concurrent access) | Both ARLO and RAA open embedding DBs in WAL mode with read-only access from RAA batch nodes. Write contention is impossible because ARLO and RAA never write to the same DB concurrently (ARLO writes `asr_embeddings.db` before RAA starts; RAA writes `non_asr_embeddings.db` during preparation, before batch nodes read). |
