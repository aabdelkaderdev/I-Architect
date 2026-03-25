# Scoring Agent (SA) — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/scoring_agent_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### 1.1 Input Processing

#### FR-SA-001: Multi-Source Input Acceptance
- **Description:** The SA SHALL accept the following inputs:
  1. **AGA Output (The Execution):** Raw `.puml` code string.
  2. **RAA TOON IR (The Blueprint):** JSON-validated TOON with `entities` and `relationships` lists.
  3. **ARLO Payload (The Intent):** Alpha decisions and Beta influential sets (when ARLO is enabled).
  4. **AGA Metadata (Optional):** Validation flags (`is_valid`, `retry_count`) from the AGA node.
  5. **RAG Context (The Rules):** ChromaDB access for C4 standards, PlantUML syntax, and SAAM/ATAM criteria.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** The SA node receives all available inputs and produces a complete evaluation JSON.

### 1.2 Pillar 1: Syntactic & Rendering Validation (20% Weight)

#### FR-SA-002: Syntax Health Check
- **Description:** The SA SHALL parse the `aga_code` to detect catastrophic syntax failures by scanning for error markers injected by the AGA (e.g., `' ERROR: Syntax Error on line X`, `' GENERATION_FAILED: Manual review required`).
  - If error marker found: **Syntax Score = 0%**. Add corresponding fix instruction to `adjustments_needed`.
  - If no error marker: **Syntax Score = 100%**.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** An AGA output containing `' GENERATION_FAILED` scores 0% on syntax health.

### 1.3 Pillar 2: Traceability Audit (20% Weight)

#### FR-SA-003: Requirement ID Traceability Verification
- **Description:** The SA SHALL verify that all unique Requirement IDs and the ARLO reference from the TOON payload are present as comments/metadata in the `.puml` code. Verification is performed via regex extraction of `' @Trace:` comments.
  - **Scoring:** `(Matched IDs / Total Required IDs) × 100`.
  - Missing IDs are appended to both `drawbacks` and `adjustments_needed`.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** If 9 of 10 required Requirement IDs are found in the `.puml`, Traceability Score = 90%.

### 1.4 Pillar 3: Structural Fidelity (30% Weight)

#### FR-SA-004: Entity/Edge Parity Check
- **Description:** The SA SHALL cross-reference the AGA's `.puml` output against the RAA's TOON IR for entity/edge parity using Python-based Fuzzy Matching (Levenshtein distance with threshold ≥ 85% similarity).
  - **Scoring:** `(Matched Entities / Total RAA Entities) × 100`.
  - Missing entities are reported with "Missing Entity: [Name]" in drawbacks.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** "OrderDB" in `.puml` matches "Order_Database" in TOON IR (85% Levenshtein match).

### 1.5 Pillar 4: SAAM/ATAM Alignment (30% Weight)

#### FR-SA-005: Rubric-Based Architectural Evaluation
- **Description:** The SA SHALL evaluate the architecture against quality attributes using a deduction model:
  - Start at 100 points.
  - Deduct 15 points for cyclic dependencies.
  - Deduct 15 points for Security violations (e.g., cleartext passwords).
  - Deduct 10 points for monolithic classes/components (>10 inferred methods).
  - Deduct 5 points for poor naming conventions.
  - Deduct 5 points for undefined relationships.
  The evaluation SHALL use a "Nuanced Reviewer" persona via LLM prompting with rubric constraints.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** An architecture with a cyclic dependency between two containers receives a SAAM Alignment deduction of 15 points.

#### FR-SA-006: ARLO Decision Cross-Reference
- **Description:** When ARLO is enabled, the SA SHALL verify that ARLO's Quality Attributes are architecturally reflected in the `.puml` code. If ARLO dictated "Microservices for Scalability" but the diagram tightly couples two APIs, this SHALL be reported as a high-severity drawback.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** A tight coupling between "Order API" and "Payment API" when ARLO selected "Microservices" produces a high-severity SAAM drawback.

### 1.6 Output Generation

#### FR-SA-007: Actionable Adjustments Generation
- **Description:** The SA SHALL synthesize findings from all 4 pillars into actionable imperative commands in the `adjustments_needed` array (e.g., "Rename class 'Ord' to 'Order'", "Separate 'Order API' and 'Payment API' into distinct C4 Containers"). No truncation — all valid adjustments SHALL be listed.
- **SRS Trace:** §9.6, §11.2.4
- **Priority:** Must
- **Acceptance Criteria:** The `adjustments_needed` array contains specific, actionable instructions for every identified issue.

#### FR-SA-008: Structured JSON Output Schema
- **Description:** The SA SHALL return a JSON object conforming to:
  ```json
  {
    "evaluation_metadata": { "target_framework": "...", "arlo_reference_id": "..." },
    "scores": { "total_percent_correct": float, "syntax_health": float, "traceability_score": float, "structural_fidelity": float, "saam_alignment": float },
    "status": { "is_renderable": bool, "recommend_regeneration": bool },
    "drawbacks": [{ "severity": "...", "category": "...", "description": "...", "affected_entities": [...] }],
    "adjustments_needed": ["..."]
  }
  ```
  The `total_percent_correct` is the weighted average: Syntax (20%) + Traceability (20%) + Fidelity (30%) + SAAM (30%).
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** The output validates against the SRS §9.6 Pydantic schema without errors.

#### FR-SA-009: Regeneration Recommendation Logic
- **Description:** The SA SHALL set `recommend_regeneration: true` if `total_percent_correct < 70%` OR if any individual pillar score is below 50%.
- **SRS Trace:** §9.6
- **Priority:** Should
- **Acceptance Criteria:** A total score of 65% triggers the regeneration recommendation.

### 1.7 Aggregation & Deduplication (Workflow 3)

#### FR-SA-010: Median Voting for Score Aggregation
- **Description:** In Workflow 3, the SA Orchestrator SHALL calculate the **median** of the 3 agents' `total_percent_correct` scores. The Median Instance (the instance whose score is closest to the median) SHALL have its entire JSON payload adopted as the `sa_aggregated.json`.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** Scores [72, 85, 90] produce a median of 85; the Beta instance's full JSON is adopted.

#### FR-SA-011: Divergence Warning
- **Description:** If the maximum score minus minimum score exceeds 30 percentage points on any pillar, the system SHALL append a `divergence_warning` field to the aggregated JSON, listing the outlier LLM and its score. The UI SHALL prominently display this warning.
- **SRS Trace:** §9.6, §1.10
- **Priority:** Must
- **Acceptance Criteria:** SAAM scores [55, 85, 90] (range = 35) trigger a divergence warning identifying the Alpha instance as an outlier.

#### FR-SA-012: Semantic Deduplication of Text Lists
- **Description:** In Workflow 3, text-based outputs (`drawbacks`, `adjustments_needed`) from all 3 instances SHALL be merged via a dedicated LLM call to remove semantic duplicates. If the deduplication LLM fails, the system SHALL default to the lists from the Median Instance.
- **SRS Trace:** §9.6
- **Priority:** Must
- **Acceptance Criteria:** Three lists containing semantically identical entries (different wording) are merged into a single deduplicated list.

### 1.8 Operational Modes

#### FR-SA-013: Mode With ARLO
- **Description:** When ARLO is enabled, the SA SHALL evaluate: ARLO Decisions + RAA TOON IR + AGA `.puml` code. SAAM Alignment SHALL cross-reference ARLO's Quality Attributes.
- **SRS Trace:** §11.2.4
- **Priority:** Must
- **Acceptance Criteria:** With ARLO enabled, the SAAM evaluation includes ARLO decision verification.

#### FR-SA-014: Mode Without ARLO
- **Description:** When ARLO is disabled, the SA SHALL evaluate: RAA TOON IR + AGA `.puml` code only. SAAM evaluation relies solely on RAG-retrieved SAAM/ATAM criteria.
- **SRS Trace:** §11.2.4
- **Priority:** Must
- **Acceptance Criteria:** Without ARLO, the SA produces a valid evaluation without `arlo_reference_id` in the metadata.

#### FR-SA-015: Reasoning Log Isolation
- **Description:** The SA SHALL output CoT reasoning in `<thinking>` XML blocks. Feedback output SHALL be formatted as imperative commands, not questions or observations.
- **SRS Trace:** §11.1, §11.2.4
- **Priority:** Must
- **Acceptance Criteria:** Adjustments are commands like "Encrypt the database connection layer," not "Should the database be encrypted?"

---

## 2. Non-Functional Requirements (NFR)

### NFR-SA-001: Fuzzy Match Performance
- **Description:** The Levenshtein-based Fuzzy Matching logic SHALL execute in < 200ms for diagrams with up to 50 entities.
- **SRS Trace:** §9.6
- **Metric:** P95 fuzzy match time ≤ 200ms for 50-entity diagrams.

### NFR-SA-002: Semantic Deduplication Latency
- **Description:** The Semantic Deduplication LLM call (Workflow 3) SHALL not add more than 3 seconds to total processing time.
- **SRS Trace:** §9.6
- **Metric:** Deduplication call completes within 3 seconds.

### NFR-SA-003: JSON Output Integrity
- **Description:** The SA SHALL guarantee valid JSON output. If the LLM produces malformed JSON, `model_validate` (Pydantic) SHALL trigger a retry. On 2nd failure, a fallback evaluation (all scores = 0.0, `recommend_regeneration: true`) SHALL be returned.
- **SRS Trace:** §13.5 (S-1)
- **Metric:** Zero `KeyError` exceptions in the UI from SA output parsing.

### NFR-SA-004: Fuzzy Match Threshold Tuning
- **Description:** The Levenshtein threshold SHALL default to 85% and be tunable via configuration to avoid false positives (e.g., "User" matching "Use").
- **SRS Trace:** §9.6
- **Metric:** No false-positive entity matches across a test suite of 100 entity name pairs.

---

## 3. Interface Requirements (IR)

### IR-SA-001: Input Interfaces
| Input | Source | Format |
|:--|:--|:--|
| AGA `.puml` Code | `aga_output/*.puml` or `mcp_aggregator/aga_aggregated.puml` | PlantUML text |
| RAA TOON IR | `raa_output/*.toon` or `mcp_aggregator/raa_aggregated.toon` | TOON (JSON) |
| ARLO Payload | `arlo_output/*.toon` | TOON (Alpha, Beta blocks) |
| RAG Context | ChromaDB (`c4_model_standards`, `saam_atam_criteria`, `plantuml_syntax`) | Vector search results |

### IR-SA-002: Output Interface
- **Target:** `/{project}/sa_output/sa_{llm}_{timestamp}.json`
- **Aggregated (Workflow 3):** `/{project}/sa_output/mcp_aggregator/sa_aggregated.json`
- **Downstream Consumers:** SA Page (UI), PDF Report Service (Template B), AGA (regeneration loop)

---

## 4. Disaster Recovery Requirements (DR)

### DR-SA-001: JSON Schema Hallucination (S-1)
- **Failure Mode:** SA outputs undefined JSON key (e.g., `"architecture_score"` instead of `"total_percent_correct"`).
- **Blast Radius:** Streamlit UI crashes on `KeyError`.
- **Recovery Action:** Strict Pydantic parsing with `model_validate`. On `ValidationError`, retry SA LLM call once with schema injected. On 2nd failure, return default "incomplete" JSON with all scores `0.0` and `recommend_regeneration: true`.
- **User-Facing Message:** ⚠️ *"The evaluation output was malformed. A re-evaluation was attempted. Please review the scores carefully."*
- **SRS Trace:** §13.5 (S-1)

### DR-SA-002: Aggregation Disagreement (S-2)
- **Failure Mode:** Three parallel SA scores diverge by > 30 percentage points on any pillar.
- **Blast Radius:** "Average voting" produces misleading consensus.
- **Recovery Action:** Flag the divergent pillar. Report **median** instead of average. Attach `divergence_warning` field listing the outlier LLM and score. Surface to user for arbitration.
- **User-Facing Message:** ⚠️ *"Significant disagreement detected on '{pillar_name}'. Median score used. Please review individual scores."*
- **SRS Trace:** §13.5 (S-2)

---

*End of Scoring Agent Requirements Document*
