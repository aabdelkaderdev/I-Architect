# Scoring Agent (SA) — Implementation Plan

## 0) Goal of this Portion

Evaluate the architectural integrity, requirement satisfaction, and diagrammatic accuracy of the generated architecture using a **strictly sequential LangGraph workflow**. The Scoring Agent (SA) takes the hierarchical JSON model originally produced by the Requirement Analysis Agent (RAA) and received through the AGA boundary as `C4JsonModel` (AGA §1), the rendering results from the Architecture Generation Agent (AGA), and the original requirements set. It computes a definitive **100-point grade** across three axes (Functional, Quality Attributes, and Diagram Accuracy) and produces an executive markdown report plus a standardized, machine-parseable JSON report. An optional `FeedbackState` output (Node 6) contains a patched copy of the RAA's `C4JsonModel` — the orchestrator uses this to re-trigger AGA without re-running RAA.

> **Pipeline position:** RAA (JSON) + AGA (Diagrams) → **SA** → Final Grade & Report (+ optional FeedbackState).

---

## 1) Inputs and Assumptions

### Inputs
- **`arch_model` (`C4JsonModel`)**: The hierarchical architecture model (systems → containers → components) produced by RAA and received via AGA. The `C4JsonModel` type definition is authoritative in AGA §1; it is structurally identical to RAA's `ArchModel` (RAA §4/§16). Includes the `diagram_manifest`, `patterns`, and `open_questions`.
- **`aga_output` (`AGAOutput`)**: The output from AGA, containing `completed_diagrams` (list of `CompletedDiagram`, each carrying `plantuml_source`) and `failed_diagrams` (list of `FailedDiagram`).
- **`requirements_data` (`dict`)**: Packed by the orchestrator before invoking SA. Structure: `{"requirements": dict[str, str], "asrs": list[str], "non_asr": list[str], "quality_weights": dict[str, int]}`.
- **`regeneration_threshold` (`float`, default `80.0`)**: Pipeline configuration parameter passed by the parent pipeline at invocation time. If the final total score falls below this threshold, the feedback node is obligated to produce a non-null `FeedbackState` with `should_regenerate = true`. Above the threshold, `FeedbackState` is still computed but `should_regenerate` is set to `false`. The orchestrator always has the final say regardless of this flag.
- **`diagram_accuracy_threshold` (`float`, default `14.0`)**: Pipeline configuration parameter. If `score_diagrams.points_awarded` falls below this value independently of the total score, the feedback node treats diagram-level issues as sufficient to recommend regeneration even if the total score is above `regeneration_threshold`. This allows targeted re-rendering to be triggered by diagram failures alone.

### Input Type Reference

| Type | Source | Fields Used by SA |
|------|--------|-------------------|
| `C4JsonModel` | RAA output (received through AGA boundary; type defined in AGA §1) | `systems`, `containers`, `components`, `persons`, `external_systems`, `diagram_manifest`, `patterns`, `open_questions`, `confidence_metadata` |
| `AGAOutput` | AGA output | `completed_diagrams` (list of `CompletedDiagram`), `failed_diagrams` (list of `FailedDiagram`) |
| `CompletedDiagram` | AGA output subtype | `diagram_id`, `diagram_type`, `plantuml_source`, `png_bytes`, `output_path` (SA only reads `diagram_id`, `diagram_type`, `plantuml_source`) |
| `FailedDiagram` | AGA output subtype | `diagram_id`, `diagram_type`, `final_error` (contains `error_type`, `http_status`, `raw_message`), `retry_count`, `last_puml_code` |

### Assumptions
- SA does not modify the architecture or regenerate diagrams. It is a read-only, evaluation-focused agent. Node 6 operates on a deep copy of `arch_model`, never the original.
- Because requirement counts can be in the hundreds, raw requirement strings are **not** dumped directly into LLM prompts. A deterministic prep-step summarizes mappings to protect the context window.
- The workflow is **strictly sequential**. No parallel fan-out/fan-in is used, simplifying state management and making the scoring steps highly observable.
- `completed_diagrams` and `failed_diagrams` arrive as flat lists. SA constructs lookup structures (a set of failed `diagram_id` values and a dict mapping `diagram_id` → `CompletedDiagram`) during Node 1 prep before any scoring node references them.

### Integration Pattern
The SA is implemented as a **standalone LangGraph StateGraph**, invoked by the orchestrator after AGA completes. It is not composed as a subgraph inside the AGA or RAA graph. The SA's LLM instance is passed via LangGraph's `context={}` dict — **never via state channels** — to prevent LLM objects from being serialised into checkpoint state (per Orchestrator Plan §3C). The orchestrator calls:

```python
sa_graph.invoke(
    {
        "arch_model": raa_output_model,
        "aga_output": aga_output,
        "requirements_data": {
            "requirements": original_requirements,
            "asrs": arlo_output["asrs"],
            "non_asr": arlo_output["non_asr"],
            "quality_weights": arlo_output["quality_weights"],
        },
        "regeneration_threshold": 80.0,
        "diagram_accuracy_threshold": 14.0,
    },
    config={"configurable": {"thread_id": computed_thread_id}},
    context={"llm": sa_llm},
)
```

Within the graph, SA nodes access the LLM from the runtime context via `config["context"]["llm"]` rather than from a state channel. This keeps the checkpoint state serialisable and follows the same injection pattern used by all other agents in the pipeline.

This separation keeps the SA independently testable and avoids coupling its state schema with RAA or AGA.

---

## 2) Authoritative Source Register

SA's evaluations are grounded in established architectural standards. All LLM prompts and deterministic checks reference these sources.

### 2A) External Standards

| Source | URL | Governs |
|--------|-----|---------|
| C4 Model — Diagrams | https://c4model.com/diagrams | Element types, hierarchy validation for Axis 3 sub-tree checks |
| C4 Model — Notation | https://c4model.com/diagrams/notation | Alias naming rules (validates AGA §2 alias-equals-ID constraint) |
| SAAM — SEI Technical Report | https://sei.cmu.edu/documents/150/2007_019_001_29297.pdf | Quality attribute evaluation methodology (Axis 2) |
| ISO/IEC 25010 | (internal reference via RAA `Quality_Attributes.md`) | Quality attribute taxonomy for ARLO weight interpretation |

### 2B) Internal Cross-Agent References

| Reference | Source Document | Used By |
|-----------|----------------|---------|
| C4 entity hierarchy constraints | RAA_Plan.md §4, §12 | Node 1 tree traversal, Node 4 sub-tree checks |
| Alias-equals-ID normative constraint | AGA_Plan.md §2 | Node 4 alias verification |
| `diagram_manifest` structure | RAA_Plan.md §16 | Node 4 manifest iteration |
| `open_questions` types (`hierarchy_conflict`, `scope_conflict`) | RAA_Plan.md §10 | Node 4 open question penalties, Node 6 scope correction |
| `confidence_metadata` structure | RAA_Plan.md §13 | Node 4 unverified entity deduction, Node 6 confidence resolution |
| Quality attribute taxonomy | RAA `Skills/RAA/references/Quality_Attributes.md` | Axis 2 quality attribute interpretation |

### 2C) Normative Prompt Constraints

The following constraints are paraphrased from the authoritative sources and embedded in SA's LLM skill prompts:

1. **Depth evaluation (Node 2):** Architectural requirements (e.g., "the system shall process payments") can reasonably trace only to the container level. Data-handling requirements (e.g., "the system shall validate IBAN") must trace to the component level. The LLM must distinguish between these categories when awarding depth points.
2. **QA mitigation (Node 3):** A declared pattern satisfies a quality attribute only if the pattern's documented properties directly address the attribute's stimulus-response scenario as defined by SAAM. Generic pattern-to-attribute mappings without mechanistic justification score zero.
3. **Technology inference (Node 3):** The LLM must not penalise generic technology values (e.g., "Database") when the relevant quality attribute imposes no specific technology constraint. Generic values are penalised only when a quality attribute demands a specific property not provided by a generic choice.
4. **Executive summary (Node 5):** All score claims in the narrative must be traceable to specific sub-rubric scores. The LLM must not invent scores or describe remediation steps that SA does not produce.

### 2D) Retrieval Policy

SA's LLM calls use prompt templates stored in `sa/prompts/`. Each template is scoped to a single node:

| Prompt Template | Node | Loaded At |
|----------------|------|-----------|
| `sa/prompts/functional_depth.md` | Node 2 | Node 2 LLM call |
| `sa/prompts/saam_validation.md` | Node 3 | Node 3 LLM call |
| `sa/prompts/executive_summary.md` | Node 5 | Node 5 LLM call |
| `sa/prompts/tech_annotation.md` | Node 3 | Node 3 LLM call (structured suggestion output) |

The corresponding skill reference files in `Skills/SA/references/` define the methodology and output schemas. The runtime prompt templates in `sa/prompts/` are derived from these reference files but are pre-formatted for direct LLM consumption. The skill files are the normative source; runtime templates are operational artefacts.

---

## 3) Scoring Rubric (100-Point Scale)

The SA evaluates the architecture across three dimensions:

### Axis 1: Functional Traceability & Coverage (40 Points)
Focuses on non-ASR (functional) requirements.
*   **Explicit Mapping (25 pts):** Calculated deterministically. `(Functional Reqs mapped to ≥1 entity / Total Functional Reqs) * 25`.
*   **Depth of Resolution (15 pts):** Evaluated by LLM. Rewards architectures that trace requirements down to granular `C4Component` levels rather than leaving them vaguely mapped at the top `C4System` level. For requirements mapped to entities at multiple levels, the deepest level wins — the depth summary passed to the LLM uses the per-requirement deepest-level distribution.
*   **Penalties:** `-2 pts` for every orphaned functional requirement (max penalty: -15 pts).

### Axis 2: Quality Attribute & ASR Satisfaction (40 Points)
Focuses on ASRs, relying on ARLO's `quality_weights` and RAA's `patterns`/`technology`.
*   **High-Risk QA Mitigation (20 pts):** Evaluated by LLM. Assesses if the explicitly declared `patterns` and `technology` fields strongly defend against the top two most heavily weighted quality attributes from ARLO.
*   **ASR Traceability (15 pts):** Calculated deterministically. `(ASRs mapped to ≥1 entity / Total ASRs) * 15`.
*   **Technology Inference Confidence (5 pts):** Evaluated by LLM. Rewards specific, compatible technologies (e.g., "PostgreSQL") over generic or null values (e.g., "Database").
*   **Penalties:** `-5 pts` for explicitly contradictory technological choices (e.g., synchronous pattern chosen for an ASR demanding asynchronous resilience).

### Axis 3: Diagram Accuracy & Hygiene (20 Points)
Focuses on AGA's render success and adherence to the RAA `diagram_manifest`. Evaluated **per-diagram**, then averaged. The per-diagram maximum is 20 points.

The sensitivity of averaging depends on manifest size. With a large manifest (e.g., 20 diagrams), a single failure reduces the Axis 3 score by approximately 1 point. With a small manifest (e.g., 2 diagrams), a single failure reduces it by 10 points. This scale-dependent sensitivity is an intentional design choice: it penalises failure proportionally to how many deliverables were expected, and a project with fewer diagrams has fewer opportunities to demonstrate diagrammatic rigour. No normalisation factor is applied.

*   **Render Success (10 pts):** Deterministic. Did AGA successfully render this `diagram_id` (present in `completed_diagrams`), or did it fail/timeout?
*   **Sub-tree Inclusion (5 pts):** Deterministic. Checks that the generated PlantUML source contains all expected child entities for the diagram type:
    - **Context diagram (`diagram_type = context`):** verify that all persons and external systems referenced in the focus system's `context_relationships` appear as aliases in the PlantUML source.
    - **Container diagram (`diagram_type = container`):** verify that all containers in the focus system's `containers` list appear as aliases in the PlantUML source.
    - **Component diagram (`diagram_type = component`):** verify that all components in the focus container's `components` list appear as aliases in the PlantUML source.
*   **Hygiene & Confidence (5 pts):** Deterministic deduction. `-1 pt` for each entity in the diagram carrying the `[unverified]` (`reduced_confidence`) flag. `-2 pts` if the `focus_entity_id` is implicated in a `hierarchy_conflict` or `scope_conflict` in RAA's `open_questions`. SA reads `open_questions` from `arch_model` directly (the `C4JsonModel` root), which is the authoritative source — not from `aga_output.open_questions`, which is a pass-through copy.

---

## 4) High-Level Pipeline Overview (Sequential Gauntlet)

1.  **Hierarchical Data Preparation:** Traverse the nested RAA JSON tree to build a flat `traceability_matrix`. Build lookup structures from `aga_output` lists. Determine per-requirement deepest mapping level. Identify orphaned requirements immediately.
2.  **Evaluate Functional Completeness:** Calculate Axis 1 base score (math) + determine resolution depth (LLM).
3.  **Evaluate QA/ASR Satisfaction:** Flatten the tech stack and patterns. Judge mitigation of top ARLO risks (LLM). Additionally, the LLM returns a structured list of `TechnologySuggestion` objects stored in the `technology_suggestions` state channel.
4.  **Evaluate Diagram Accuracy:** Iterate through the `diagram_manifest` and score AGA's PlantUML/PNG outputs against the RAA source of truth (Deterministic).
5.  **Compile Partial Report:** Sum the three axes. Generate a narrative executive summary using an LLM. Build a partial `SARReport` containing all score data and the executive summary but leaving `feedback_summary`, `summary.regeneration_recommended`, and `summary.recommended_action` as placeholders.
6.  **Feedback Generation & Report Finalisation (Deterministic):** Evaluate thresholds. Collect and apply adjustments to a deep copy of `arch_model`. Classify structural gaps. Build `targeted_diagrams`. Produce `FeedbackState`. Finalise the `SARReport` by populating the feedback-dependent fields. Write `scoring_report.json`, `scoring_report.md`, and `feedback_state.json` to the filesystem.

---

## 5) State Schema

Because the graph is sequential, all reducers use default `overwrite` semantics.

| Channel | Type | Reducer | Description |
|---------|------|---------|-------------|
| `arch_model` | `C4JsonModel` | overwrite | Read-only input from RAA. |
| `aga_output` | `AGAOutput` | overwrite | Read-only input from AGA. |
| `requirements_data` | `dict` | overwrite | Packed by the orchestrator before invoking SA. Structure: `{"requirements": dict[str, str], "asrs": list[str], "non_asr": list[str], "quality_weights": dict[str, int]}`. |
| `regeneration_threshold` | `float` | overwrite | Pipeline configuration parameter (default 80.0). |
| `diagram_accuracy_threshold` | `float` | overwrite | Pipeline configuration parameter (default 14.0). |
| `failed_diagram_ids` | `list[str]` | overwrite | Deduplicated lookup list built at start of Node 1: all `diagram_id` values present in `aga_output.failed_diagrams`. Stored as `list` rather than `set` for JSON-safe checkpoint serialisation; membership tests use `in` on the list (manifest sizes are small enough that O(n) lookup is negligible). |
| `completed_diagram_map` | `dict[str, CompletedDiagram]` | overwrite | Lookup dict built at start of Node 1: maps `diagram_id` → `CompletedDiagram` for all successfully rendered diagrams. |
| `traceability_matrix` | `dict` | overwrite | Maps `req_id` → list of `{entity_id, level, deepest_level}` records. `deepest_level` is the deepest C4 level (component > container > system) at which this requirement is traced across all mapped entities. |
| `orphaned_reqs` | `list[str]` | overwrite | List of requirement IDs not mapped to any entity. |
| `score_functional` | `FunctionalAxisScore` | overwrite | Output of Node 2 (Axis 1). |
| `score_qa` | `QAAxisScore` | overwrite | Output of Node 3 (Axis 2). |
| `score_diagrams` | `DiagramAxisScore` | overwrite | Output of Node 4 (Axis 3). |
| `technology_suggestions` | `list[TechnologySuggestion]` | overwrite | Structured technology annotation suggestions produced by Node 3's LLM call. Read by Node 6. |
| `final_report` | `SARReport` | overwrite | The aggregated output structure (partial after Node 5, finalised by Node 6). |
| `feedback_state` | `FeedbackState \| null` | overwrite | The optional feedback output produced by Node 6. Null if score is above threshold and no diagram failures occurred. The orchestrator reads this to decide whether to re-trigger AGA. |

### Supporting Type Definitions

**`FunctionalAxisScore`** (Node 2 output):

| Field | Type | Description |
|-------|------|-------------|
| `awarded` | `float` | Total points awarded for Axis 1 |
| `possible` | `int` | Always 40 |
| `explicit_mapping_awarded` | `float` | Points awarded for the deterministic mapping sub-rubric (max 25) |
| `explicit_mapping_mapped_count` | `int` | Number of functional requirements mapped to ≥1 entity |
| `explicit_mapping_total_count` | `int` | Total functional requirement count |
| `depth_awarded` | `float` | Points awarded by LLM for depth of resolution (max 15) |
| `depth_distribution` | `dict[str, float]` | Percentage of requirements at each deepest mapping level: keys are `system`, `container`, `component`; values are 0.0–1.0 |
| `depth_llm_reasoning` | `str` | LLM reasoning string for the depth sub-rubric |
| `orphan_penalty` | `float` | Total penalty applied (negative float) |
| `orphan_count` | `int` | Number of functional requirements that are orphaned |

**`QAAxisScore`** (Node 3 output):

| Field | Type | Description |
|-------|------|-------------|
| `awarded` | `float` | Total points awarded for Axis 2 |
| `possible` | `int` | Always 40 |
| `asr_traceability_awarded` | `float` | Deterministic traceability sub-rubric score (max 15) |
| `asr_mapped_count` | `int` | Number of ASRs mapped to ≥1 entity |
| `asr_total_count` | `int` | Total ASR count |
| `high_risk_mitigation_awarded` | `float` | LLM sub-rubric score (max 20) |
| `top_risk_attributes` | `list[str]` | The top 2 quality attributes by ARLO weight that drove the mitigation evaluation |
| `mitigation_llm_reasoning` | `str` | LLM reasoning string for the high-risk mitigation sub-rubric |
| `technology_confidence_awarded` | `float` | LLM sub-rubric score (max 5) |
| `technology_confidence_llm_reasoning` | `str` | LLM reasoning string for the technology confidence sub-rubric |
| `contradiction_penalty` | `float` | Total penalty applied (negative float) |
| `contradictions_identified` | `list[str]` | Human-readable descriptions of each identified technology contradiction |

**`DiagramAxisScore`** (Node 4 output):

| Field | Type | Description |
|-------|------|-------------|
| `awarded` | `float` | Average per-diagram score scaled to 20 points maximum |
| `possible` | `int` | Always 20 |
| `per_diagram` | `list[DiagramScore]` | One entry per `DiagramManifestEntry` |

**`DiagramScore`**:

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | The manifest `diagram_id` |
| `diagram_type` | `str` | One of `context`, `container`, `component` |
| `focus_entity_id` | `str` | The focus entity from the manifest |
| `awarded` | `float` | Points awarded for this diagram, 0.0–20.0 |
| `render_success` | `bool` | Whether AGA completed this diagram |
| `sub_tree_complete` | `bool \| null` | Whether all expected child entities appear in the PlantUML source. Null if render failed. |
| `missing_entity_ids` | `list[str]` | Canonical IDs of expected entities absent from PlantUML source. Empty list if complete. |
| `unverified_entity_count` | `int` | Number of `[unverified]` entities in this diagram |
| `unverified_penalty` | `float` | Points deducted for unverified entities |
| `open_question_conflict` | `bool` | Whether this diagram's focus node is implicated in a `hierarchy_conflict` or `scope_conflict` |
| `open_question_penalty` | `float` | Points deducted for open question conflicts |

**`TechnologySuggestion`** (Node 3 LLM structured output):

| Field | Type | Description |
|-------|------|-------------|
| `entity_id` | `str` | Canonical ID of the container or component whose `technology` field needs updating |
| `entity_path` | `str` | Human-readable hierarchy path for debugging (e.g., `payment_system → api_gateway`) |
| `entity_type` | `str` | C4 level of the entity: `container` or `component` |
| `current_value` | `str \| null` | The value currently in the model |
| `suggested_value` | `str` | The specific technology string the LLM recommends |
| `confidence` | `float` | LLM's self-assessed confidence in this suggestion, 0.0–1.0. Node 6 skips suggestions below the confidence threshold defined in `Feedback_Technology_Annotation.md`. |
| `rationale` | `str` | Why this technology better satisfies the relevant quality attribute |
| `quality_attribute` | `str` | The ARLO quality attribute this suggestion addresses |

**`AdjustmentRecord`** (produced by Node 6):

| Field | Type | Description |
|-------|------|-------------|
| `adjustment_id` | `str` | Stable identifier, format `adj-{zero-padded sequence}` (e.g., `adj-001`) |
| `adjustment_type` | `str` | One of: `technology_annotation`, `scope_correction`, `confidence_resolution`, `manifest_refresh` |
| `source_axis` | `str` | Which scoring axis produced this adjustment: `Axis1`, `Axis2`, or `Axis3` |
| `target_entity_id` | `str \| null` | Canonical ID of the entity modified. Null for `manifest_refresh`. |
| `target_diagram_id` | `str \| null` | Manifest `diagram_id` of the diagram affected. Null for entity-level adjustments with no single diagram target. |
| `target_field_path` | `str` | Dot-notation path to the modified field within the entity, relative to the entity root (e.g., `technology`, `component_relationships[2].diagram_scope`, `confidence_metadata.reduced_confidence`) |
| `before` | `any` | The value of `target_field_path` before the adjustment. Serialised as a JSON-compatible type. |
| `after` | `any` | The value of `target_field_path` after the adjustment |
| `rationale` | `str` | Why this change was made, tied to the specific scoring deduction it addresses |
| `estimated_score_delta` | `float \| null` | Estimated improvement to the relevant axis score if this adjustment resolves the deduction. Null if not quantifiable. |

**`FeedbackState`** (Node 6 output):

| Field | Type | Description |
|-------|------|-------------|
| `should_regenerate` | `bool` | Whether the orchestrator is advised to re-trigger AGA |
| `trigger_axes` | `list[str]` | Which threshold conditions fired: zero or more of `total_score`, `diagram_accuracy`, `failed_diagrams` |
| `regeneration_threshold_used` | `float` | The configured threshold value for traceability |
| `modified_arch_model` | `C4JsonModel` | The patched copy of RAA's output, ready to be passed directly to AGA as its new input |
| `targeted_diagrams` | `list[str]` | The minimal set of `diagram_id` values AGA should re-render. If AGA is re-triggered with this model, it should only process manifest entries whose `diagram_id` is in this list |
| `adjustment_log` | `list[AdjustmentRecord]` | Ordered record of every change made to produce `modified_arch_model` |
| `structural_gaps_requiring_raa_rerun` | `list[str]` | Requirement IDs whose deficiencies cannot be resolved by AGA re-rendering and require a RAA re-run |
| `notes` | `str \| null` | Free-text warnings from Node 6 (e.g., unresolvable entity IDs from technology suggestions) |

**Imported Types (defined by AGA, used as-is by SA):**

| Type | Defined In | SA Usage |
|------|-----------|----------|
| `CompletedDiagram` | AGA_Plan.md §4 | Lookup map value in `completed_diagram_map`; SA reads `diagram_id`, `plantuml_source` |
| `FailedDiagram` | AGA_Plan.md §4 | Source of `failed_diagram_ids`; SA reads `diagram_id`, `final_error.error_type`, `retry_count` |
| `AGAOutput` | AGA_Plan.md §13 | Top-level input wrapper containing `completed_diagrams`, `failed_diagrams`, `open_questions` (pass-through from RAA; not consumed by SA — SA reads `open_questions` from `arch_model` directly per Node 4), and `session_report` (not consumed by SA) |
| `PatternSelection` | AGA_Plan.md §1 | SA reads `pattern_name`, `quality_attributes` during Node 3 pattern evaluation |
| `ConfidenceRecord` | AGA_Plan.md §1 | Per-entity confidence data keyed by entity ID in `C4JsonModel.confidence_metadata`. SA reads `reduced_confidence` for Node 4 unverified-entity deductions and Node 6 confidence resolution adjustments |

---

## 6) Node Definitions

### Node 1: Hierarchical Data Preparation (Deterministic Python)
*   **Task:** Uses a recursive function to traverse the `arch_model` (`systems` → `containers` → `components`, plus global `persons`/`external_systems`).
*   **Action:**
    1. Build lookup structures from `aga_output`:
       - `failed_diagram_ids`: set of `diagram_id` strings from `aga_output.failed_diagrams`.
       - `completed_diagram_map`: dict mapping `diagram_id` → `CompletedDiagram` from `aga_output.completed_diagrams`.
    2. Traverse hierarchy. Extract `requirement_ids` from every entity and relationship.
    3. Build the `traceability_matrix` (e.g., `{"R1": [{"entity_id": "api_gateway", "level": "container", "deepest_level": "component"}]}`). For each requirement, record all mapped entities with their C4 level. Compute `deepest_level` per requirement as the deepest level across all entities that requirement maps to (component > container > system), resolving multi-level mappings with deepest-wins semantics.
    4. Cross-reference with `requirements_data` to identify `orphaned_reqs`.
    5. Partition requirements into functional (non-ASR) and ASR lists using the `non_asr` and `asrs` ID lists.

### Node 2: Evaluate Functional Completeness (Axis 1)
*   **Task:** Compute Functional Score out of 40.
*   **Deterministic Step:** Calculate `(Mapped Functional Reqs / Total Functional Reqs) * 25`. Apply penalty for functional orphans.
*   **LLM Step:** Compute the per-requirement deepest-level distribution from `traceability_matrix` (percentage of functional reqs at Component level, Container level, System level). Pass this depth summary (e.g., "60% mapped at Component level, 30% at Container level, 10% at System level") to the LLM via the Functional Depth Evaluation skill. LLM awards up to 15 points based on depth adequacy.
*   **Output:** `score_functional` (`FunctionalAxisScore`).

### Node 3: Evaluate QA & ASR Satisfaction (Axis 2)
*   **Task:** Compute QA Score out of 40.
*   **Deterministic Step:** Calculate `(Mapped ASRs / Total ASRs) * 15`.
*   **Data Prep:** Flatten the hierarchical technology declarations into a list (e.g., `systemX.containerY: Node.js`). Sort ARLO `quality_weights` to find the top 2 concerns. Extract pattern names from `arch_model.patterns` via the `PatternSelection.pattern_name` field (AGA §1), not `ArchPattern.name` (RAA §4) — the model received by SA has passed through the AGA boundary where the field is renamed.
*   **LLM Step:** Pass top concerns, selected patterns (using `pattern_name` per `PatternSelection`), and flattened technology stack to the SAAM Validation skill. The LLM produces a single composite response covering both sub-rubrics: up to 20 points for High-Risk Mitigation and up to 5 points for Tech Inference Confidence. The combined reasoning is captured in `QAAxisScore.mitigation_llm_reasoning` and `QAAxisScore.technology_confidence_llm_reasoning`. Applies contradiction penalties.
*   **Structured Technology Suggestions:** The SAAM Validation skill prompt is updated to additionally require the LLM to return a structured list of technology suggestions alongside its score. Each suggestion names a specific entity ID (container or component), the technology value currently in the model (which may be null or a generic string like "Database"), the LLM's specific suggested replacement (e.g., "PostgreSQL 15"), and a brief rationale tied to the quality attribute being addressed. This structured list is returned as a separate field in the LLM's response, not embedded in the reasoning prose. Node 3 parses this list and stores it in `technology_suggestions`. Node 6 reads this channel when constructing the feedback model. This avoids the fragility of parsing LLM reasoning text later.
*   **Output:** `score_qa` (`QAAxisScore`), `technology_suggestions`.

### Node 4: Evaluate Diagram Accuracy (Axis 3) (Deterministic Python)
*   **Task:** Score AGA's output strictly against the `diagram_manifest` out of 20.
*   **Action:** Loop over every `DiagramManifestEntry` in `arch_model.diagram_manifest`.
    1. If `diagram_id` is in `failed_diagram_ids`, score for this diagram is `0`.
    2. If successful, look up the `CompletedDiagram` from `completed_diagram_map`. Extract `plantuml_source` directly from the `CompletedDiagram` object. Traverse `arch_model` to the `focus_entity_id`.
    3. **Sub-tree Inclusion check — branch on `diagram_type`:**
       - **`context`:** build the expected alias set from all persons and external systems referenced as source or target in the focus system's `context_relationships`. Verify every expected alias appears in `plantuml_source`.
       - **`container`:** build the expected alias set from all `C4Container.id` values in the focus system's `containers` list. Verify every expected alias appears in `plantuml_source`.
       - **`component`:** build the expected alias set from all `C4Component.id` values in the focus container's `components` list. Verify every expected alias appears in `plantuml_source`.
       Deduct points proportionally for missing aliases.
    4. Deduct points for `[unverified]` flags (via `confidence_metadata` lookup) or RAA `open_questions` targeting this node. Read `open_questions` from `arch_model.open_questions` (the authoritative source), not from `aga_output.open_questions`.
*   **Output:** Average the scores across all manifest entries to yield `score_diagrams` (`DiagramAxisScore`, max 20).

### Node 5: Partial Report Compilation (Hybrid)
*   **Deterministic Step:** Sum the `awarded` fields from all three axes. Calculate letter grade (A: 90+, B: 80+, C: 70+, D: 60+, F: <60). Build a **partial** `SARReport` structured JSON object per §9, populating all score-derived fields (`summary.total_score`, `summary.grade`, `axis_scores`, `gap_analysis`, and all count fields). Leave `summary.regeneration_recommended`, `summary.recommended_action`, and `feedback_summary` as sentinel values (respectively `false`, `accept`, and `null`) — these are finalised by Node 6 after feedback generation.
*   **LLM Step:** Provide the scores, reasoning strings, and list of `failed_diagram_ids` / `orphaned_reqs` to an LLM to write a concise, professional Executive Summary in Markdown. The LLM also extracts exactly 3–5 key findings (each ≤ 25 words) for the `ExecutiveSummary.key_findings` field.
*   **No filesystem output.** File writing is deferred to Node 6 so that the report includes feedback-dependent fields.
*   **Output:** `final_report` (partial `SARReport` — feedback fields are sentinels).

### Node 6: Feedback Generation & Report Finalisation (Deterministic Python)

Node 6 runs after Node 5 in the sequential chain. It is always executed — it produces a null `feedback_state` if no regeneration is warranted rather than being conditionally skipped. This keeps the graph structure unconditionally sequential and makes the presence or absence of feedback a data value, not a graph branching decision.

After completing feedback generation (threshold evaluation, adjustment collection, structural gap classification, and targeted diagram identification — all described below), Node 6 **finalises the `SARReport`** by overwriting the sentinel values left by Node 5:

*   `summary.regeneration_recommended` ← `FeedbackState.should_regenerate` (or `false` if `feedback_state` is null).
*   `summary.recommended_action` ← determined from `should_regenerate` and `structural_gaps_requiring_raa_rerun` (see §9 `ReportSummary` for values).
*   `feedback_summary` ← built from the `FeedbackState` (adjustment count, types, targeted diagram count, structural gap count, and `feedback_state_path`).
*   `executive_summary.recommended_action` ← copied from the now-final `summary.recommended_action`.

Node 6 then writes all three output files: `scoring_report.json` (the now-complete `SARReport`), `scoring_report.md` (the executive summary markdown from Node 5), and `feedback_state.json` (the full `FeedbackState`).

#### Threshold Evaluation (Deterministic)

Node 6 first evaluates whether to recommend regeneration. It checks three conditions independently: whether `final_report.total_score` is below `regeneration_threshold`; whether `score_diagrams.awarded` is below `diagram_accuracy_threshold`; and whether `aga_output.failed_diagrams` is non-empty. If any condition is true, `should_regenerate` is set to `true`. The `trigger_axes` list records which conditions fired (values: `total_score`, `diagram_accuracy`, `failed_diagrams`). If none are true, `should_regenerate` is `false`, but the node still completes the full adjustment analysis and produces a `FeedbackState` — the orchestrator may choose to apply improvements even when the threshold is not crossed.

**Threshold Trigger Truth Table:**

| Total < `regeneration_threshold` | Diagrams < `diagram_accuracy_threshold` | `failed_diagrams` non-empty | `should_regenerate` | `trigger_axes` | `recommended_action` |
|---|---|---|---|---|---|
| F | F | F | `false` | `[]` | `accept` |
| F | F | T | `true` | `["failed_diagrams"]` | `regenerate_diagrams` |
| F | T | F | `true` | `["diagram_accuracy"]` | `regenerate_diagrams` |
| F | T | T | `true` | `["diagram_accuracy", "failed_diagrams"]` | `regenerate_diagrams` |
| T | F | F | `true` | `["total_score"]` | `regenerate_diagrams`¹ |
| T | F | T | `true` | `["total_score", "failed_diagrams"]` | `regenerate_diagrams`¹ |
| T | T | F | `true` | `["total_score", "diagram_accuracy"]` | `regenerate_diagrams`¹ |
| T | T | T | `true` | `["total_score", "diagram_accuracy", "failed_diagrams"]` | `regenerate_diagrams`¹ |

> ¹ `recommended_action` escalates to `rerun_raa` when `structural_gaps_requiring_raa_rerun` is non-empty (see Structural Gap Classification below). The truth table shows the base recommendation; the presence of structural gaps overrides it.

#### Adjustment Collection (Deterministic)

Node 6 iterates over all scoring deductions and collects candidate adjustments. It operates on a deep copy of `arch_model`, never on the original. The following adjustment types are defined:

**`technology_annotation`**: For each entry in `technology_suggestions`, Node 6 traverses the `arch_model` copy to locate the entity by `entity_id` and updates its `technology` field to `suggested_value`. Each change produces one `AdjustmentRecord`. If an entity ID from `technology_suggestions` cannot be found in the model (which should not occur in a valid pipeline run but must be handled), the suggestion is skipped and a warning is written to the `FeedbackState`'s notes field.

**`scope_correction`**: For each `OpenQuestion` of type `scope_conflict` in `arch_model.open_questions`, Node 6 applies the authoritative scoping rule from RAA §12 mechanically: it identifies the relationship by `source_id` and `target_id`, determines the correct `diagram_scope` from the endpoint entity types (resolved by traversing the hierarchy), and updates the `diagram_scope` field on the relationship in the appropriate scoped relationship list. Each corrected relationship produces one `AdjustmentRecord` with `before` and `after` capturing the scope value.

**`confidence_resolution`**: For each entity whose `confidence_metadata` entry has `reduced_confidence = true`, Node 6 checks whether that entity's `id` appears in `open_questions` with type `hierarchy_conflict`. If it does not appear (meaning the entity's reduced confidence was due to an incoherent batch in RAA, not an unresolved structural conflict), and if the entity's `requirement_ids` are all present in the `traceability_matrix` with successful mapping, Node 6 removes the `reduced_confidence` flag from `confidence_metadata` for that entity. This instructs AGA not to append `[unverified]` to this entity's description in the regenerated diagram. Each resolved entity produces one `AdjustmentRecord`.

**`manifest_refresh`**: After all entity-level adjustments are applied to the model copy, Node 6 regenerates the `diagram_manifest` by re-traversing the adjusted hierarchy. This ensures the manifest remains consistent with any structural changes (e.g., a scope correction that moves a relationship into a different scoped list changes which entities appear in which diagram). The manifest regeneration follows exactly the same deterministic traversal algorithm defined in RAA §16 — it is not an LLM step. The old manifest is replaced entirely.

#### Structural Gap Classification (Deterministic)

Not all scoring deficiencies can be addressed by patching the model and re-running AGA. Node 6 classifies the remaining gaps:

Orphaned requirements (from `orphaned_reqs`) cannot be resolved by AGA re-rendering — they require new entities to be added to the architecture, which is RAA's responsibility. These are collected into `structural_gaps_requiring_raa_rerun` as a list of requirement IDs. The orchestrator reads this field to determine whether the deficiency warrants a full RAA re-run rather than (or in addition to) an AGA re-run.

Requirements mapped only at the system level when they should reach component level similarly require RAA-level analysis and are also added to `structural_gaps_requiring_raa_rerun`. SA identifies these from the `traceability_matrix` depth distribution but cannot create new containers or components on its own.

#### Targeted Diagram Identification (Deterministic)

Rather than re-rendering all diagrams, the orchestrator should instruct AGA to re-render only the subset affected by the adjustments. Node 6 builds `targeted_diagrams` as a list of `diagram_id` strings by collecting: all `diagram_id` values from `aga_output.failed_diagrams`; all diagram IDs whose focus node contains an entity that received a `technology_annotation` or `confidence_resolution` adjustment (resolved by matching `target_entity_id` to the focus node's sub-tree in the manifest); and all diagram IDs affected by a `scope_correction` (the diagram whose scoped relationship list was modified). Duplicate IDs are deduplicated. The resulting list is the minimal set of diagrams AGA must re-render to reflect all adjustments.

---

## 7) Skills vs. Static Templates

Strict separation ensures that LLM token costs and context windows are optimized, keeping mathematical and structural evaluations strictly deterministic.

### Use Skills (LLM Prompts) For:
All skills reside in `Skills/SA/references/`. The existing `SAAM.md` in this directory is the general SAAM reference document (shared with RAA); the four files below are SA-specific skill prompts that reference it but serve distinct evaluation purposes.
1.  **`Functional_Depth_Evaluation.md`:** Guidelines for judging whether tracing a requirement only to a `C4System` is acceptable (e.g., a vague business requirement) versus tracing it to a `C4Component` (e.g., a specific data parsing requirement).
2.  **`SAAM_Validation.md`:** Guidelines for evaluating if the declared `patterns` (e.g., "Event-Driven") and `technology` fields actually satisfy the top-weighted ARLO quality attributes (e.g., "Reliability", "Security"). Updated to include output schema requirements for the structured `TechnologySuggestion` list, following the same output schema section format used by all skill reference files in the RAA plan. Builds on the general SAAM methodology documented in `SAAM.md` but is scoped to the SA's scoring context.
3.  **`Executive_Summary_Writer.md`:** Formatting constraints for translating JSON scorecards into a readable C-suite level Markdown report.
4.  **`Feedback_Technology_Annotation.md`:** Governs the structured technology suggestion output from the Node 3 LLM call. Defines the output schema for `TechnologySuggestion` objects, the confidence threshold below which a suggestion should not be made (the LLM should return no suggestion rather than a low-confidence guess), and the rule that suggestions must name a specific technology string compatible with the entity's existing `technology` field context and the parent system's other technology choices. Follows the standard seven-section template established in the RAA plan (Purpose, Input, Normative rules, Decision guidelines, Output schema, Error cases, Examples).

### Skill Reference File Template

Each SA skill reference file follows the same 7-section template established in the RAA plan (RAA §14):

1. **Purpose** — what the skill does, when it is invoked.
2. **Input** — what data the skill receives from the SA state, with field-level descriptions.
3. **Normative rules** — hard constraints the LLM must follow. Paraphrased from the authoritative sources in §2C. Violating any normative rule invalidates the LLM's score for that sub-rubric.
4. **Decision guidelines** — heuristics for ambiguous cases. These are guidance, not constraints. The LLM may deviate if it provides explicit reasoning.
5. **Output schema** — what the skill must produce, referencing the SA state types defined in §5. For skills that produce structured data (SAAM_Validation, Feedback_Technology_Annotation), this section includes the full JSON schema the LLM must conform to.
6. **Error cases** — known failure modes and how the LLM should handle each (e.g., empty technology stack, zero ASRs, all diagrams failed).
7. **Examples** — one worked example from the custom requirements dataset, showing the input data, the expected reasoning chain, and the expected output.

### Skill Directory Layout

```
Skills/SA/
├── SKILL.MD                              # SA skill definition (agent-level)
└── references/
    ├── SAAM.md                           # General SAAM reference (shared with RAA)
    ├── Functional_Depth_Evaluation.md    # Depth sub-rubric skill (Node 2 LLM)
    ├── SAAM_Validation.md                # QA validation skill (Node 3 LLM)
    ├── Executive_Summary_Writer.md       # Executive summary skill (Node 5 LLM)
    └── Feedback_Technology_Annotation.md # Tech suggestion skill (Node 3 LLM structured output)
```

The skill reference files in `Skills/SA/references/` define the methodology, constraints, and output schemas. The runtime prompt templates in `sa/prompts/` are derived from these reference files but are pre-formatted for direct LLM consumption with state variables already interpolated. The skill files are the normative source; runtime templates are operational artefacts.

### Use Static Templates (Python Scripts) For:
- Lookup structure construction (`failed_diagram_ids` list, `completed_diagram_map` dict) from AGA's flat output lists.
- Recursive tree traversal (`systems` → `containers` → `components`), including per-requirement deepest-level determination.
- Traceability matrix array cross-referencing.
- Base math calculations for Axis 1 and Axis 2.
- Axis 3 (Diagram Accuracy) in its entirety. Regex/string matching against AGA's PlantUML source (canonical alias matching per AGA §2 alias-equals-ID constraint).
- Final grade summation.
- Node 6 in its entirety (deterministic Python). No LLM is involved in feedback generation. The technology suggestions that Node 6 applies were already produced by the LLM in Node 3 and stored in `technology_suggestions`. This keeps feedback generation fast, reproducible, and free of additional token cost.

---

## 8) Checkpointing

SA has three LLM calls spread across Nodes 2, 3, and 5. For large requirements sets this represents meaningful compute time and cost. SA uses the same checkpointing infrastructure as RAA and AGA: `SqliteSaver` from `langgraph-checkpoint-sqlite`.

### 8A) Checkpointer Configuration

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# db_path is received from the orchestrator at runtime (Orchestrator Plan §6C).
# Example: db_path = "projects/my_project/checkpoints/sa.db"
conn = sqlite3.connect(str(db_path), check_same_thread=False)
checkpointer = SqliteSaver(conn)
```

The checkpoint database path is **received from the orchestrator at runtime** — the orchestrator passes a project-scoped path `projects/{project_name}/checkpoints/sa.db` when calling `compile_for_production(db_path=...)` (see Orchestrator Plan §6C). The SA module's `compile_for_production()` accepts `db_path` as a **required parameter** with no default. The SA module does **not** create the `checkpoints/` directory itself — directory creation is the orchestrator's responsibility.

### 8B) Graph Compilation

```python
sa_graph = sa_builder.compile(checkpointer=checkpointer)
```

No additional instrumentation is required. The checkpointer is the only persistence mechanism — SA does not use separate file-based state dumps or external caches.

### 8C) Thread Identity & Run Configuration

SA derives its own `thread_id` for checkpointing. It does not reuse the RAA `thread_id` directly — RAA and SA are separate graphs with separate checkpoint databases, and reusing the same thread ID would cause collisions if they shared a checkpointer (they don't) and would create ambiguity in pipeline traceability.

```
sa_thread_id = "sa-" + sha256(raa_thread_id + sa_run_timestamp_iso)[:16]
```

Where:
- `raa_thread_id` is the RAA `thread_id` that produced the `arch_model` input (available as `pipeline_run_id` in the state).
- `sa_run_timestamp_iso` is the ISO 8601 UTC timestamp of the SA run start, truncated to second precision.

This derivation ensures:
- Rerunning SA on the same RAA output with the same timestamp produces the same thread ID (idempotent).
- Rerunning SA on the same RAA output at a different time produces a different thread ID (new run, new checkpoint history).
- The `sa-` prefix makes it visually distinct from RAA's `raa-` prefix.
- `pipeline_run_id` in `SARReport` carries the RAA thread ID, preserving traceability back to the architecture generation step.

```python
config = {
    "configurable": {
        "thread_id": f"sa-{hashlib.sha256((raa_thread_id + timestamp).encode()).hexdigest()[:16]}"
    }
}
```

### 8D) Entry Point: Fresh Start vs. Resume

At startup, SA queries the checkpointer for existing state:

```python
existing_state = sa_graph.get_state(config)
if existing_state and existing_state.values:
    # Resume from last completed node
    # The graph state contains all channels with the node's outputs
    # LangGraph's invoke() resumes from the next unexecuted node automatically
    last_node = existing_state.metadata.get("writes", {})
else:
    # Fresh invocation — Node 1 starts from inputs
```

Since the graph is strictly sequential with overwrite semantics throughout, resuming from any completed node is straightforward — the checkpoint contains the full state at the node boundary. LangGraph's built-in resume logic handles determining which node to run next.

### 8E) Checkpoint Granularity & What Is Persisted

SA checkpoints after every node completes (the default LangGraph behaviour with `SqliteSaver`). The following table describes what each channel contributes to checkpoint size and which channels are critical for resume correctness.

| Channel | Approx. Size | Resume-Critical | Notes |
|---------|-------------|-----------------|-------|
| `arch_model` | 50–500 KB | Yes | Read-only input, but must be present for every node to reference |
| `aga_output` | 10–200 KB | Yes | Read-only input; contains all PlantUML sources |
| `requirements_data` | 5–50 KB | Yes | Read-only input |
| `regeneration_threshold` | 8 bytes | No | Constant; can be re-supplied |
| `diagram_accuracy_threshold` | 8 bytes | No | Constant; can be re-supplied |
| `failed_diagram_ids` | <1 KB | Yes | Built by Node 1; needed by Nodes 4, 5, 6 |
| `completed_diagram_map` | 10–200 KB | Yes | Built by Node 1; needed by Node 4 |
| `traceability_matrix` | 10–100 KB | Yes | Built by Node 1; needed by Nodes 2, 3, 4, 6 |
| `orphaned_reqs` | <1 KB | Yes | Built by Node 1; needed by Nodes 2, 5, 6 |
| `score_functional` | 1–5 KB | Yes | Node 2 output; needed by Node 5 |
| `score_qa` | 1–5 KB | Yes | Node 3 output; needed by Nodes 5, 6 |
| `score_diagrams` | 1–10 KB | Yes | Node 4 output; needed by Nodes 5, 6 |
| `technology_suggestions` | 0–10 KB | Yes | Node 3 output; needed by Node 6 |
| `final_report` | 10–100 KB | Yes | Node 5 output; finalised by Node 6 |
| `feedback_state` | 50–500 KB | Yes | Node 6 output; contains full modified model |

Total checkpoint size per node boundary: approximately 150 KB to 1.7 MB, dominated by `arch_model` and `feedback_state.modified_arch_model`.

### 8F) Checkpoint Lifecycle & Cleanup

- **During run:** Checkpoints accumulate in the orchestrator-provided checkpoint database after each node. The database file grows monotonically during the run — SqliteSaver does not compact automatically.
- **On success:** After Node 6 completes and all output files are written, the checkpoint database is retained for 7 days to allow pipeline traceability and debugging, then may be removed. The checkpoint is not needed for downstream consumption — the `SARReport` JSON is the authoritative record.
- **On failure:** The checkpoint database is preserved indefinitely until the run is successfully resumed and completed. This allows the orchestrator to retry the SA graph from the point of failure.
- **On regeneration:** When SA runs as part of a regeneration cycle (second or third SA invocation in the same pipeline), it receives a new `sa_thread_id` (different timestamp) and starts a fresh checkpoint. The previous SA run's checkpoint is retained independently.
- **Cleanup policy:** A periodic cleanup job (orchestrator responsibility, not SA's) removes checkpoint databases older than 7 days for completed runs.

### 8G) Failure Mode Coverage

| Failure | Checkpoint State | Recovery |
|---------|-----------------|----------|
| Process killed mid-LLM-call (Node 2) | Checkpoint at Node 1 boundary exists. `score_functional` is absent. | Resume: LangGraph re-executes Node 2. The LLM call is re-attempted. Idempotent — Node 2 is pure function of state channels that were already computed by Node 1. |
| Process killed mid-LLM-call (Node 3) | Checkpoint at Node 2 boundary exists. `score_functional` present, `score_qa` absent. | Resume: LangGraph re-executes Node 3. Idempotent. |
| Process killed mid-LLM-call (Node 5) | Checkpoint at Node 4 boundary exists. `score_qa`, `score_diagrams` present. `final_report` absent. | Resume: LangGraph re-executes Node 5. Idempotent — LLM executive summary generation may produce different prose but scores are deterministic. |
| Process killed mid-Node 6 | Checkpoint at Node 5 boundary exists. `final_report` partial (sentinel values). `feedback_state` absent. | Resume: LangGraph re-executes Node 6. Idempotent — all Node 6 operations are deterministic given the state from Nodes 1–5. Output files are overwritten. |
| Checkpoint DB file corrupted | `SqliteSaver` raises `sqlite3.DatabaseError` on read or write. | Fatal. The run must restart from scratch with a new thread ID (new timestamp). The corrupted `sa.db` is moved to `sa.db.corrupted.{timestamp}` for forensic analysis. |
| Checkpoint DB disk full | `SqliteSaver` write raises `sqlite3.OperationalError` with `SQLITE_FULL`. | The current node continues in memory — SA does not halt mid-node. The error is caught at the node boundary when the checkpointer attempts to persist. SA raises `SACheckpointError`, which the orchestrator must handle. In-memory state is still accessible via `graph.get_state()` for the current run. |

---

## 9) Standardized JSON Report Schema

The `SARReport` is the top-level JSON object written to `scoring_report.json`. The markdown executive summary is separated from the structured data and written to `scoring_report.md`. All numeric scores are typed as `float`. All counts are typed as `int`. No field carries an untyped `dict` value. The full `FeedbackState` is written separately to `feedback_state.json`.

**`SARReport`** (top-level JSON object):

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | `str` | Schema version string (e.g., `"1.0"`). Incremented on breaking changes to enable consumer version checks. |
| `report_id` | `str` | SHA-256 of the RAA `thread_id` concatenated with the SA run timestamp, truncated to 16 hex chars, prefixed with `sa-`. Stable and reproducible for the same input run. |
| `generated_at` | `str` | ISO 8601 UTC timestamp of report generation. |
| `pipeline_run_id` | `str` | The RAA `thread_id` that produced the `arch_model` input. Provides traceability back to the RAA checkpoint. |
| `summary` | `ReportSummary` | Top-level scorecard, intended for orchestrator consumption and dashboard display. |
| `axis_scores` | `AxisBreakdown` | Full breakdown of all three axes with sub-rubric detail. |
| `gap_analysis` | `GapAnalysis` | All identified deficiencies with enough detail for downstream diagnosis. |
| `executive_summary` | `ExecutiveSummary` | LLM-generated narrative plus machine-parseable key findings. |
| `feedback_summary` | `FeedbackSummary \| null` | Summary of the FeedbackState produced by Node 6. Null if `feedback_state` is null. Full `FeedbackState` is written separately to `feedback_state.json`. |

**`ReportSummary`**:

| Field | Type | Description |
|-------|------|-------------|
| `total_score` | `float` | Aggregated score, 0.0–100.0 |
| `grade` | `str` | One of: `A` (≥90), `B` (≥80), `C` (≥70), `D` (≥60), `F` (<60) |
| `regeneration_recommended` | `bool` | Copied from `FeedbackState.should_regenerate`. False if `feedback_state` is null. Initially set to `false` by Node 5; finalised by Node 6. |
| `recommended_action` | `str` | One of: `accept` (score above threshold, no failures), `regenerate_diagrams` (AGA re-run advised), `rerun_raa` (structural gaps requiring RAA re-run exist). Initially set to `accept` by Node 5; finalised by Node 6 based on `structural_gaps_requiring_raa_rerun` and `should_regenerate`. |
| `diagram_manifest_size` | `int` | Total number of diagrams in the RAA manifest |
| `diagrams_completed` | `int` | Number successfully rendered by AGA |
| `diagrams_failed` | `int` | Number that failed in AGA |
| `requirements_total` | `int` | Total requirement count |
| `requirements_asr` | `int` | Count of ASR requirements |
| `requirements_functional` | `int` | Count of non-ASR (functional) requirements |
| `requirements_orphaned` | `int` | Count of requirements not mapped to any entity |

**`AxisBreakdown`**:

| Field | Type | Description |
|-------|------|-------------|
| `functional` | `FunctionalAxisScore` | Axis 1 detail (see §5 for field definitions) |
| `quality_attributes` | `QAAxisScore` | Axis 2 detail (see §5 for field definitions) |
| `diagram_accuracy` | `DiagramAxisScore` | Axis 3 detail (see §5 for field definitions) |

**`GapAnalysis`**:

| Field | Type | Description |
|-------|------|-------------|
| `orphaned_requirements` | `list[OrphanedRequirement]` | All requirements not mapped to any entity |
| `failed_diagrams` | `list[FailedDiagramRecord]` | All diagrams that AGA could not render |
| `incomplete_diagrams` | `list[IncompleteDiagramRecord]` | Diagrams that rendered but with missing sub-tree entities |
| `open_questions_flagged` | `list[OpenQuestionRecord]` | All RAA open_questions that affected scoring |

**`OrphanedRequirement`**:

| Field | Type | Description |
|-------|------|-------------|
| `req_id` | `str` | Requirement ID |
| `is_asr` | `bool` | Whether this is an ASR or functional requirement |
| `quality_attributes` | `list[str]` | Quality attributes from ARLO (empty for non-ASRs) |
| `text_snippet` | `str` | First 120 characters of the requirement description for quick diagnosis |

**`FailedDiagramRecord`**:

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | The manifest `diagram_id` |
| `diagram_type` | `str` | The diagram level |
| `final_error_type` | `str` | `error_type` from AGA's `FailedDiagram.final_error` |
| `retry_count` | `int` | Number of AGA correction attempts; sourced from `FailedDiagram.retry_count` (top-level field, not nested inside `final_error`) |

**`IncompleteDiagramRecord`**:

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | The manifest `diagram_id` |
| `focus_entity_id` | `str` | The focus node |
| `missing_entity_ids` | `list[str]` | Canonical IDs absent from PlantUML source |

**`OpenQuestionRecord`**:

| Field | Type | Description |
|-------|------|-------------|
| `entity_id` | `str \| null` | Related entity ID from the RAA open question |
| `type` | `str` | One of: `change_risk`, `high_coupling`, `contention`, `tie`, `coverage_gap`, `hierarchy_conflict`, `scope_conflict` |
| `description` | `str` | Human-readable description from the RAA open question |
| `affected_diagram_ids` | `list[str]` | Diagrams whose focus node is implicated by this open question |

**`ExecutiveSummary`**:

| Field | Type | Description |
|-------|------|-------------|
| `markdown` | `str` | Full LLM-generated executive summary as a markdown string. Also written separately to `scoring_report.md`. |
| `key_findings` | `list[str]` | Exactly 3–5 concise bullet-point strings extracted by the LLM, each ≤ 25 words. Machine-parseable; suitable for dashboard display without markdown rendering. |
| `recommended_action` | `str` | Copied from `ReportSummary.recommended_action` for co-location with the narrative |

**`FeedbackSummary`** (included in `SARReport` as a compact indicator; full detail is in `feedback_state.json`):

| Field | Type | Description |
|-------|------|-------------|
| `adjustment_count` | `int` | Total number of `AdjustmentRecord` entries in the full `FeedbackState` |
| `adjustment_types_present` | `list[str]` | Distinct `adjustment_type` values present in the adjustment log |
| `targeted_diagram_count` | `int` | Number of diagrams in `targeted_diagrams` |
| `structural_gap_count` | `int` | Number of requirement IDs in `structural_gaps_requiring_raa_rerun` |
| `feedback_state_path` | `str` | Filesystem path to the separately written `feedback_state.json` |

### Filesystem Output

All filesystem writes are performed by **Node 6** after report finalisation (see §6, Node 6). No files are written by Node 5. The SA writes the following files to the project-scoped output directory at `projects/{project_name}/output/sa/`. The output directory path is **provided by the orchestrator** at invocation time — the SA module does not hardcode or assume a default output path. The orchestrator creates the `output/sa/` directory before SA invocation (per Orchestrator Plan §2C).

Files written:

- **`scoring_report.json`** — the full, finalised `SARReport` object serialised as formatted JSON. Includes the feedback-dependent fields (`regeneration_recommended`, `recommended_action`, `feedback_summary`) populated by Node 6.
- **`scoring_report.md`** — the markdown string from `ExecutiveSummary.markdown`, written as a standalone file.
- **`feedback_state.json`** — the full `FeedbackState` object serialised as formatted JSON. Written regardless of whether `should_regenerate` is true or false, so the orchestrator always has the data. Contains the complete `modified_arch_model` (the full patched `C4JsonModel`) and the complete `adjustment_log`. This file is intentionally separate from `scoring_report.json` because it is large (it includes the full model copy) and is consumed by the orchestrator, not by human reviewers.

### Downstream Handoff

The orchestrator reads `scoring_report.json` for the grade and `feedback_state.json` for the patched model. The `SARReport.summary.recommended_action` field is the orchestrator's primary decision signal. The orchestrator reads `FeedbackState.should_regenerate` and `FeedbackState.structural_gaps_requiring_raa_rerun` to determine the next pipeline step per the orchestrator interface contract (§16).

---

## 10) Failure Modes and Mitigations

| Risk | Mitigation |
|------|------------|
| **Context Window Blowout** | Node 1 (Prep) distills hundreds of requirements into a metadata-rich `traceability_matrix`. LLMs never process raw JSON trees or full requirement dictionaries. |
| **LLM Math Hallucination** | Base scores and final summations are 100% deterministic Python. The LLM is only permitted to output scores for specific subjective sub-rubrics (e.g., Depth out of 15). |
| **Mismatched Aliases in Axis 3** | AGA is strictly prompted (AGA §2) to use the canonical entity `id` as the PlantUML alias — this is a normative constraint, not a suggestion. SA's deterministic regex searches for these canonical IDs in the PlantUML source. The AGA hallucination guard (AGA §14) additionally validates that every alias in generated code matches a canonical entity ID exactly, rejecting abbreviated or invented aliases before encoding. |
| **Zero Diagrams Generated** | If AGA suffered a complete `ServerUnavailableException`, Axis 3 automatically scores a 0/20, resulting in a severe grade penalty without crashing the SA. |
| **Crash Mid-Scoring** | Checkpoint after each node (orchestrator-provided `db_path` via `SqliteSaver`, per Orchestrator Plan §6C). Resume from any completed node boundary without re-executing prior nodes. |
| **Node 6 cannot locate an entity from `technology_suggestions` in `modified_arch_model`** | Entity ID mismatch is logged to `FeedbackState.notes`. The suggestion is skipped; remaining adjustments are still applied. A skipped suggestion does not halt the node or prevent `feedback_state.json` from being written. |
| **`feedback_state.json` write fails (disk full, permissions)** | Node 6 logs the write failure as an error. The in-memory `FeedbackState` is still placed in the graph state channel and returned to the caller. The orchestrator can read it from the graph state directly even if the file is absent. `SARReport.feedback_summary.feedback_state_path` is set to null in this case. |
| **`scoring_report.json` write fails (disk full, permissions)** | Node 6 logs the write failure. The in-memory `SARReport` is still in the graph state (`final_report` channel). The orchestrator can read it directly. A warning is emitted to the orchestrator's run log. |
| **Checkpoint DB file corrupted** | Fatal — run must restart with a new thread ID. Corrupted DB moved to `sa.db.corrupted.{timestamp}`. See §8G for full recovery procedure. |
| **LLM returns unparseable structured output (Node 3 technology suggestions)** | Node 3 wraps the LLM call in a retry with schema validation. If the LLM's `TechnologySuggestion` list fails JSON schema validation after 2 retries, the suggestions list is set to empty (`[]`). The Axis 2 score is unaffected — technology suggestions are an additive output, not a scoring dependency. Node 6 handles an empty list gracefully. |

---

## 11) Performance & Cost Profile

| Operation | Complexity / Cost |
|-----------|-------------------|
| Node 1 (tree traversal + matrix build) | O(E) where E = total entities across all hierarchy levels. No LLM cost. |
| Node 2 (Axis 1) | 1 LLM call. Input size: traceability matrix summary + depth distribution (2–5 KB). |
| Node 3 (Axis 2) | 1 LLM call. Input size: patterns + top-2 quality attributes + flattened tech stack summary (3–8 KB). |
| Node 4 (Axis 3) | O(D × A) where D = diagrams, A = avg aliases per diagram. No LLM cost. |
| Node 5 (report compilation) | 1 LLM call. Input size: score summaries + orphan/failure lists (5–15 KB). |
| Node 6 (feedback) | O(E + D) deterministic. No LLM cost. |
| **Total LLM calls** | **3 per SA run** |
| **Total SA runs per pipeline** | 1 (initial) + up to 2 (regeneration cycles) = max 3 |
| **Total LLM calls per pipeline (max)** | 9 (3 calls × 3 runs) |
| **Wall-clock estimate (single run)** | ~15–60 seconds, dominated by 3 sequential LLM calls. Deterministic nodes are sub-second. |
| **Checkpoint overhead per node** | ~10–200 ms for `SqliteSaver` write, proportional to state size (150 KB–1.7 MB). |
| **Total checkpoint storage per run** | 6 checkpoints × 150 KB–1.7 MB = ~1–10 MB on disk. |

Cost is dominated by the 3 LLM calls. The two evaluation LLM calls (Nodes 2 and 3) each process small, pre-summarised inputs — typically 2–8 KB of prompt context. The executive summary LLM call (Node 5) is the most expensive single call because it receives all three axis scores, reasoning strings, and gap lists; its prompt context is typically 5–15 KB.

---

## 12) Validation and Testing Criteria

### Unit Tests
- **Tree Traversal:** Provide a mocked `arch_model` with 3 levels of depth. Assert that Node 1 correctly builds a `traceability_matrix` containing requirements from systems, containers, and components, with `deepest_level` correctly resolving multi-level mappings (e.g., a requirement mapped to both a container and a component records `deepest_level = "component"`).
- **Lookup Construction:** Provide mocked AGA output with 2 completed and 1 failed diagrams. Assert that Node 1 correctly builds `failed_diagram_ids` (set of 1) and `completed_diagram_map` (dict of 2).
- **Axis 3 Math:** Provide mocked AGA output where 1 diagram succeeded fully, 1 succeeded but dropped a component, and 1 failed. Assert the Axis 3 score accurately calculates the average penalties.
- **Axis 3 Context Sub-tree Inclusion:** Provide a mocked context diagram's `plantuml_source` missing one person alias from `context_relationships`. Assert the sub-tree check correctly identifies the omission (not checking for containers, which are not expected in a context diagram).
- **Node 6 `targeted_diagrams` from failures:** Provide a mocked `score_diagrams` where two diagrams failed. Assert that `FeedbackState.targeted_diagrams` contains exactly those two `diagram_id` values, `should_regenerate` is true, and `trigger_axes` contains `failed_diagrams`.
- **Node 6 `technology_annotation` adjustment:** Provide a `technology_suggestions` list with one entry pointing to a known container in a mocked `arch_model`. Assert that the `modified_arch_model` copy has the `technology` field updated, the original `arch_model` is unchanged (deep copy verification), and the `adjustment_log` contains exactly one record of type `technology_annotation` with correct `before` and `after` values.
- **Node 6 `confidence_resolution` adjustment:** Provide a mocked `arch_model` where one entity has `reduced_confidence = true` in `confidence_metadata` and does not appear in `open_questions`. Assert that the entity's `reduced_confidence` is removed in `modified_arch_model` and an `AdjustmentRecord` of type `confidence_resolution` is produced.
- **`SARReport` serialisation:** Assert that the full report object round-trips through `json.dumps` and `json.loads` without error, that all numeric fields are `float` or `int` (not strings), and that `schema_version` is present.

### Integration Tests
- **End-to-End Pipeline:** Pass a known RAA and AGA output. Assert that the SA correctly identifies explicitly seeded "orphaned requirements" and successfully generates the final JSON and Markdown report.
- **Multi-Diagram Manifest:** Pass a model with 8 manifest entries (2 context + 2 container + 4 component). Assert all 8 are scored and the Axis 3 average is correct.
- **End-to-end with missing entity in PlantUML:** Provide a synthetic RAA model and AGA output where one diagram has a missing entity in its PlantUML source. Assert that the `SARReport` records it in `gap_analysis.incomplete_diagrams`, `DiagramScore.sub_tree_complete` is false for that entry, and `FeedbackState.targeted_diagrams` includes that `diagram_id`.
- **End-to-end diagram threshold trigger:** Provide inputs where total score is above `regeneration_threshold` but `score_diagrams` is below `diagram_accuracy_threshold`. Assert `should_regenerate` is true and `trigger_axes` contains `diagram_accuracy` but not `total_score`.

### Functional Tests
- **Report schema compliance:** `scoring_report.json` round-trips through the `SARReport` Pydantic model (or TypedDict validation) without field type mismatches. `schema_version` is present. All numeric fields are `float` or `int` — no numeric values serialised as strings.
- **Feedback state completeness:** When `should_regenerate` is true, `modified_arch_model` is a valid `C4JsonModel` (passes the same structural integrity checks from RAA §19: every container nested in a system, every component nested in a container, no orphan IDs in relationships).
- **Deep copy isolation:** After Node 6 completes, mutating a field in `feedback_state.modified_arch_model` does not affect `arch_model` in the graph state. Verify by setting a `technology` field in the modified model and asserting the original is unchanged.
- **Axis 3 per-diagram-type correctness:** For each diagram type (context, container, component), the expected alias set is derived from the correct scoped entity list (persons+external for context, containers for container, components for component). No cross-level leakage — a container diagram must not be penalised for missing persons, and a component diagram must not be penalised for missing external systems.
- **Filesystem output presence:** After a complete run, all three files (`scoring_report.json`, `scoring_report.md`, `feedback_state.json`) exist in the output directory and are valid JSON/Markdown respectively.
- **Node 6 truth table coverage:** Parameterised test covering all 8 rows of the threshold trigger truth table (§6, Node 6). For each combination, assert `should_regenerate` and `trigger_axes` match the expected values.
- **Thread ID idempotency:** Two SA runs with the same RAA `thread_id` and the same timestamp produce the same `sa_thread_id`. Two runs with different timestamps produce different `sa_thread_id` values.

---

## 13) Deliverables for Spec Kit

1. **State schema** — specific overwrite channels (`traceability_matrix`, `score_functional`, `score_qa`, `score_diagrams`, `failed_diagram_ids`, `completed_diagram_map`, `technology_suggestions`, `feedback_state`, `regeneration_threshold`, `diagram_accuracy_threshold`, etc.) with full type definitions (§5).
2. **Node implementations** — scripts for the 6 sequential nodes, especially the recursive logic for Node 1 (including lookup construction and deepest-level resolution), the structured suggestion parsing in Node 3, the per-diagram-type branching in Node 4, and the full feedback generation + report finalisation + file writing in Node 6 (including deep copy of `arch_model`, all four adjustment type handlers, `targeted_diagrams` construction, `structural_gaps_requiring_raa_rerun` classification, and SARReport finalisation) (§6).
3. **100-Point Rubric definition** — coded as constants/functions to ensure reproducible grading (§3).
4. **Skill Resource Bundle** — `Skills/SA/` directory with 4 reference prompt templates (`Functional_Depth_Evaluation.md`, `SAAM_Validation.md`, `Executive_Summary_Writer.md`, `Feedback_Technology_Annotation.md`) (§7).
5. **Runtime Prompt Templates** — `sa/prompts/` directory with 4 runtime-ready prompt templates derived from the skill reference files (§2D, §14).
6. **Final Output Formatter** — script to build the `SARReport` JSON object, write `scoring_report.json`, `scoring_report.md`, and `feedback_state.json` (§9).
7. **Checkpointing configuration** — `SqliteSaver` setup with orchestrator-provided `db_path` (project-scoped per Orchestrator Plan §6C), with checkpoint hooks after each node, thread ID derivation, resume logic, and failure mode handling (§8A–§8G).
8. **Project structure** — `sa/` package with `nodes/`, `state/`, `prompts/`, and `utils/` modules (§14).

---

## 14) Project Structure & Directory Layout

### Code & Prompt Template Directory (`sa/`)

```
sa/
├── __init__.py
├── runner.py                # Entry point, checkpointer init, graph compilation
├── graph.py                 # StateGraph definition, edge wiring
├── state/
│   ├── __init__.py
│   └── schema.py            # SAState TypedDict, all supporting types (FunctionalAxisScore, QAAxisScore, DiagramAxisScore, TechnologySuggestion, AdjustmentRecord, SARReport, FeedbackState, etc.)
├── nodes/
│   ├── __init__.py
│   ├── prep.py              # Node 1: Hierarchical Data Prep (lookup construction, tree traversal, traceability matrix, orphan detection)
│   ├── axis_functional.py   # Node 2: Functional Completeness (deterministic mapping calc + LLM depth evaluation)
│   ├── axis_qa.py           # Node 3: QA/ASR Satisfaction (deterministic ASR traceability + LLM mitigation & tech inference + TechnologySuggestion parsing)
│   ├── axis_diagrams.py     # Node 4: Diagram Accuracy (per-diagram scoring with per-type branching: context/container/component)
│   ├── report.py            # Node 5: Partial Report Compilation (score summation, grade calc, partial SARReport, LLM executive summary)
│   └── feedback.py          # Node 6: Feedback & Report Finalisation (threshold eval with truth table, 4 adjustment handlers, structural gap classification, targeted diagram identification, SARReport finalisation, file writing)
├── prompts/
│   ├── functional_depth.md  # Runtime prompt for Node 2 LLM depth evaluation
│   ├── saam_validation.md   # Runtime prompt for Node 3 LLM QA validation
│   ├── executive_summary.md # Runtime prompt for Node 5 LLM executive summary
│   └── tech_annotation.md   # Runtime prompt for Node 3 LLM structured technology suggestions
└── utils/
    ├── __init__.py
    └── traversal.py         # Recursive tree traversal helpers (deepest-level resolution, hierarchy flattening, alias set extraction per diagram type)
```

### Skills Resource Bundle (`Skills/SA/`)

```
Skills/SA/
├── SKILL.MD                              # SA skill definition (agent-level metadata, invocation pattern, required context)
└── references/
    ├── SAAM.md                           # General SAAM reference document (shared with RAA)
    ├── Functional_Depth_Evaluation.md    # Depth sub-rubric skill reference (Node 2)
    ├── SAAM_Validation.md                # QA validation skill reference (Node 3)
    ├── Executive_Summary_Writer.md       # Executive summary skill reference (Node 5)
    └── Feedback_Technology_Annotation.md # Tech suggestion skill reference (Node 3)
```

### Convention

Follows the same structure as `arlo/` and `raa/`: `sa/nodes/` for node scripts, `sa/state/` for schema, `sa/prompts/` for runtime prompt templates, `sa/utils/` for shared traversal helpers. The `Skills/SA/` directory is for skill definitions only — never for runtime code or prompt templates.

### Checkpoint Artifacts

Checkpoint databases are **project-scoped** (per Orchestrator Plan §6C). The orchestrator creates and manages the directory at `projects/{project_name}/checkpoints/` and passes the full path to each agent's `compile_for_production(db_path=...)` call:

```
projects/{project_name}/checkpoints/
├── orchestrator.db           # Orchestrator's own checkpoint
├── ingestion.db              # Ingestion pipeline checkpoints
├── arlo.db                   # ARLO checkpoints
├── raa_graph.db              # RAA checkpoints
├── aga.db                    # AGA checkpoints
├── sa.db                     # SA checkpoints
└── rga.db                    # RGA checkpoints
```

The SA module does **not** create or assume a shared `checkpoints/` directory at the project root. Directory creation is the orchestrator's responsibility.

---

## 15) Required AGA Amendment — Selective Rendering

AGA must be amended in three places to support selective diagram re-rendering, which is the mechanism the orchestrator uses when re-triggering AGA with `FeedbackState.modified_arch_model`.

**AGA §1 (Inputs):** Add an optional input `targeted_diagrams: list[str] | null` (default null). This is passed by the orchestrator when re-triggering AGA after SA. When non-null, it contains the `FeedbackState.targeted_diagrams` list. When null (i.e., on the initial AGA run), behaviour is unchanged.

**AGA §3 (Pipeline Overview), Step 1:** After reading the `diagram_manifest`, if `targeted_diagrams` is non-null, filter the manifest to only the entries whose `diagram_id` is in `targeted_diagrams`. The filtered list becomes the `diagram_queue`. All other manifest entries are treated as if they were previously completed and are not re-rendered. If `targeted_diagrams` is null, all manifest entries are queued as before.

**AGA §4 (State Schema), `diagram_queue`:** Add to the description: "When the AGA is re-triggered by the orchestrator with a `targeted_diagrams` filter, this queue is populated with only the filtered subset of manifest entries. Previously completed diagrams are not re-queued."

No other AGA sections require changes. The ReAct loop, encoding, error handling, and output assembly are all unchanged — they operate on whatever entries are in `diagram_queue` regardless of how that queue was populated.

### Amendment Status

These AGA amendments are **not yet applied** to `AGA_Plan.md`. The SA feedback loop (Node 6 → orchestrator → AGA re-run with `targeted_diagrams`) is inoperable until the amendments are applied. Track as a dependency:

- [ ] AGA §1: Add `targeted_diagrams` optional input
- [ ] AGA §3: Add manifest filtering logic
- [ ] AGA §4: Update `diagram_queue` description

---

## 16) Orchestrator Interface Contract

The orchestrator (to be implemented in a later phase) is the consumer of `FeedbackState`. The SA plan defines the following contract for it, which the orchestrator implementation must honour.

The orchestrator reads `FeedbackState.should_regenerate`. If false, it accepts the AGA output as final and does not re-trigger any agent.

If `structural_gaps_requiring_raa_rerun` is non-empty and `should_regenerate` is true, the orchestrator must decide between two paths: re-running RAA (addressing structural gaps, followed by AGA, followed by SA again) or running AGA with the patched model (accepting that structural gaps remain but improving diagrams). This decision is outside SA's scope — SA provides the data, the orchestrator applies policy. SA's `recommended_action` value of `rerun_raa` advises the RAA-first path.

If `should_regenerate` is true and `structural_gaps_requiring_raa_rerun` is empty, the orchestrator re-triggers AGA with `modified_arch_model` as the `arch_model` input and `targeted_diagrams` as the selective rendering filter. SA then re-runs on the new AGA output, receiving the same `modified_arch_model` as `arch_model` (since RAA was not re-run). The orchestrator is responsible for threading the correct model version through.

To prevent infinite regeneration loops, the orchestrator must track how many SA→AGA cycles have been completed for a given `pipeline_run_id` and enforce a maximum (recommended: 2 regeneration cycles). SA does not enforce this limit — it produces feedback every run. The cycle count is the orchestrator's responsibility.
