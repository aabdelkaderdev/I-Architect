# Requirements Analysis Agent (RAA) — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/raa_module_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### 1.1 Input Processing & Mode Detection

#### FR-RAA-001: Dynamic Mode Detection
- **Description:** The RAA SHALL determine its execution mode at runtime by inspecting the filesystem for ARLO artifacts. It SHALL NOT rely on explicit UI flags:
  - **Mode A (ARLO-Downstream):** `arlo_output/` exists AND contains valid TOON artifacts → treats ARLO Drivers as hard constraints.
  - **Mode B (Standalone):** `arlo_output/` is missing, empty, or corrupt → operates solely on extracted requirements and RAG context.
  The mode detection log SHALL explicitly state which mode was activated.
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** In a project without ARLO results, RAA logs *"ARLO context missing - defaulting to Standalone Mode"* and uses Mode B logic.

#### FR-RAA-002: ARLO-Downstream Ingestion (Mode A)
- **Description:** In Mode A, the RAA SHALL consume:
  - **Input Alpha:** ARLO's architectural decision categories and selected patterns (mapped to Primary Driver IDs).
  - **Input Beta:** QA sensitivity analysis and AIS Requirement IDs.
  - **Input Gamma:** Full descriptions of ASRs (retrieved by joining ARLO's ASR ID list against the requirements CSV).
  ARLO decisions SHALL be treated as **hard constraints** — the RAA SHALL NOT override or ignore them.
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** If ARLO selected "Microservices" for Deployment, the RAA's TOON IR SHALL decompose the system into separate containers — not a monolith.

#### FR-RAA-003: Standalone Ingestion (Mode B)
- **Description:** In Mode B, the RAA SHALL operate solely on the extracted Requirements CSV and RAG context. It SHALL derive architectural significance via internal heuristics and LLM-driven pattern matching.
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** Without ARLO, the RAA produces a valid TOON IR based on requirements analysis and RAG-retrieved patterns.

#### FR-RAA-004: Parallel Execution Context Parity
- **Description:** In Workflows 2 and 3, all parallel RAA instances (Alpha, Beta, Gamma) SHALL receive **identical** inputs (Requirements + ARLO Output). Variations in output SHALL be driven by distinct LLM models or temperature settings, not different data views. Internal entity deduplication is best-effort; cross-model merging is deferred to the MCP Aggregator.
- **SRS Trace:** §9.1, §9.4
- **Priority:** Must
- **Acceptance Criteria:** Three parallel RAA instances all receive the same input hash; output differences are attributable to model/temperature only.

### 1.2 Architectural Synthesis

#### FR-RAA-005: Entity Extraction & Synthesis
- **Description:** The RAA SHALL parse the TOON schema and requirements to identify actors, systems, sub-systems, containers, databases, and external APIs. It SHALL map each entity to specific Requirement IDs for traceability.
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** The output TOON IR contains at least one entity for every domain referenced in the requirements.

#### FR-RAA-006: Relationship Mapping
- **Description:** The RAA SHALL define data flow and dependencies between extracted entities, specifying: source, target, action, type (Synchronous/Asynchronous), and protocol (HTTPS, gRPC, REST, etc.).
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** Every entity with inferred interactions has at least one relationship in the `flow_logic` block.

#### FR-RAA-007: RAG-Driven Pattern Matching
- **Description:** The RAA SHALL query the ChromaDB vector database (collections: `c4_model_standards`, `eip_patterns`) with k=5 results per query to map requirements to industry-standard architectural patterns (Event-Driven, Microservices, CQRS, etc.).
- **SRS Trace:** §9.4, §10.4
- **Priority:** Must
- **Acceptance Criteria:** A requirement mentioning "real-time notifications" triggers a RAG query that retrieves Event-Driven Architecture patterns.

#### FR-RAA-008: Technology Inference (Creative Liberty)
- **Description:** The RAA persona ("Solutions Architect") SHALL infer standard industry technologies when requirements are vague (e.g., "React" for "Frontend," "PostgreSQL" for "Database"). If technologies are explicitly named in requirements, the RAA SHALL use them exactly. All inferences SHALL be cited in `<thinking>` blocks.
- **SRS Trace:** §9.4, §11.2.2
- **Priority:** Must
- **Acceptance Criteria:** A vague requirement "web store" produces entities with specific technologies (e.g., "React," "Node.js"); an explicit "Must use Go" requirement produces "Go" in the tech field.

#### FR-RAA-009: Framework Standardization
- **Description:** The RAA SHALL apply the user-selected architectural framework (C4 Model or UML) to organize the TOON IR structure. The `target_framework` field SHALL be set to the user's selection from the RAA Page (Page 6).
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** Selecting "C4 Container" in the UI produces a TOON IR with `target_framework: C4_Container` and C4-compliant entity types.

### 1.3 Self-Correction & Validation

#### FR-RAA-010: Self-Correction Node (Architect's Review)
- **Description:** Before finalizing the TOON IR, a Self-Correction Node SHALL validate the output against ARLO's Influential Sets (Mode A). If a Critical Driver is missing (e.g., "High Security" requiring an Auth Service), the agent SHALL attempt to rewrite the JSON. Maximum retries: 5. On exhaustion, a generic component (e.g., `Generic_Security_Module`) is forcefully injected (fail-open strategy).
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** If ARLO's Alpha output includes a Security driver and the initial TOON IR lacks an Auth component, the self-correction loop adds one within 5 retries.

#### FR-RAA-011: TOON Schema Validation
- **Description:** The RAA SHALL validate its TOON output against a Pydantic schema ensuring: no `null` values for `tech` or `protocol` fields, all `Requirement ID` references are valid, and `arlo_reference` is present (Mode A).
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** A TOON IR with a `null` protocol field fails Pydantic validation and triggers self-correction.

### 1.4 Output

#### FR-RAA-012: TOON Intermediate Representation Output
- **Description:** The RAA SHALL output a TOON IR payload containing: `metadata` (target framework, arlo_reference, logic priority, agent mode), `system_boundary`, `entities` (id, type, name, tech, rationale, mapped_requirements), `flow_logic` (from, to, action, type, protocol), and `layout_hints` (grouping, alignment, focus_node).
- **SRS Trace:** §9.4
- **Priority:** Must
- **Acceptance Criteria:** The output validates against the SRS §9.4 TOON IR schema; all sections are non-empty for valid requirements.

#### FR-RAA-013: Reasoning Log Isolation
- **Description:** The RAA SHALL output internal Chain-of-Thought reasoning in `<thinking>` XML blocks BEFORE generating the TOON payload. The backend SHALL strip reasoning logs for storage without breaking the JSON parser. In Mode A, citations of RAG document IDs SHALL be included in `<thinking>` blocks.
- **SRS Trace:** §11.1, §11.2.2
- **Priority:** Must
- **Acceptance Criteria:** The LLM response contains `<thinking>...</thinking>` followed by valid TOON JSON; the parser extracts both cleanly.

---

## 2. Non-Functional Requirements (NFR)

### NFR-RAA-001: ChromaDB Fallback
- **Description:** If ChromaDB is unreachable or returns zero results, the RAA SHALL fallback to 3–5 hardcoded canonical C4 examples embedded in the prompt template.
- **SRS Trace:** §13.3 (R-2)
- **Metric:** RAG fallback activates within 5 seconds of connection failure.

### NFR-RAA-002: Token Budget Compliance
- **Description:** The RAA SHALL respect the `max_input_tokens × 0.85` budget. If exceeded, chunking fallback activates.
- **SRS Trace:** §8.5
- **Metric:** No token overflow errors across 100 test runs with varying input sizes.

### NFR-RAA-003: Parallel Instance Memory Isolation
- **Description:** In Workflows 2/3, each parallel RAA instance SHALL operate within its own memory context. No shared mutable state between instances.
- **SRS Trace:** §9.1
- **Metric:** Three simultaneous instances produce independent outputs without cross-contamination.

---

## 3. Interface Requirements (IR)

### IR-RAA-001: Input Interfaces
| Input | Source | Format |
|:--|:--|:--|
| Project Requirements | `structured_requirements/requirements.csv` | CSV/JSON |
| ARLO Artifacts (Mode A) | `arlo_output/*.toon` | TOON (Alpha, Beta, Gamma blocks) |
| RAG Context | ChromaDB (`c4_model_standards`, `eip_patterns`) | Vector search results (k=5) |
| User Framework Selection | UI (Page 6) | String: "C4_Container" or "UML_Component" |

### IR-RAA-002: Output Interface
- **Target:** `/{project}/raa_output/raa_{llm}_{timestamp}.toon`
- **Downstream Consumer:** AGA (or MCP Aggregator in Workflows 2/3)

---

## 4. Disaster Recovery Requirements (DR)

### DR-RAA-001: TOON Schema Validation Failure (R-1)
- **Failure Mode:** Pydantic `ValidationError` on ARLO output (missing `arlo_reference`, malformed IDs).
- **Recovery Action:** Halt and surface exact schema violation. Do NOT auto-correct upstream data. Log raw payload.
- **User-Facing Message:** 🛑 *"The data from ARLO failed validation: {error_detail}. Please re-run ARLO or contact support."*
- **SRS Trace:** §13.3 (R-1)

### DR-RAA-002: ChromaDB Retrieval Failure (R-2)
- **Failure Mode:** `ConnectionError` to ChromaDB or zero results.
- **Recovery Action:** Fallback to embedded few-shot examples. Log RAG failure.
- **User-Facing Message:** ⚠️ *"The architectural knowledge base is temporarily unavailable. Analysis will proceed using built-in templates."*
- **SRS Trace:** §13.3 (R-2)

### DR-RAA-003: Parallel Agent OOM Kill (R-3)
- **Failure Mode:** Docker container exits with code 137 (SIGKILL).
- **Recovery Action:** Downgrade to sequential execution for the failed instance. Re-run with reduced batch size. If 2 of 3 fail, abort and recommend Workflow 1.
- **User-Facing Message:** ⚠️ *"Parallel analysis instance '{LLM_name}' ran out of memory and was restarted in sequential mode."*
- **SRS Trace:** §13.3 (R-3)

---

*End of RAA Requirements Document*
