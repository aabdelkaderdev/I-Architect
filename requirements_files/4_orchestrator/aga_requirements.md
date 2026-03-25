# Architecture Generation Agent (AGA) — Functional & Non-Functional Requirements

> **Version:** 1.0
> **Source Plan:** `requirements_planning/4_orchestrator/aga_module_plan.md`
> **SRS Reference:** I-Architect SRS v2.3
> **Date:** 2026-03-24

---

## 1. Functional Requirements (FR)

### 1.1 Input Processing

#### FR-AGA-001: Composite Input State Acceptance
- **Description:** The AGA SHALL accept a composite input state containing:
  - **Primary:** `raa_output.toon` — the structural blueprint (TOON IR from RAA).
  - **Context:** `arlo_decisions.json` — ARLO decisions for consistency reference.
  - **Refinement (Optional):** `user_manual_edits.puml` — user-modified code from the UI editor.
  - **Feedback (Optional):** `sa_adjustments.json` — list of issues from the Scoring Agent.
  - **User Notes (Optional):** Freeform notes from the ARLO Page "Notes for AGA" textarea.
- **SRS Trace:** §9.5
- **Priority:** Must
- **Acceptance Criteria:** The AGA node receives all available inputs from the LangGraph state and processes them without errors.

#### FR-AGA-002: Generation Mode vs. Regeneration Mode
- **Description:** The AGA SHALL operate in two modes:
  1. **Generation Mode:** Converts RAA TOON IR into initial `.puml` files.
  2. **Regeneration Mode:** When triggered from the SA Page ("↺ Regenerate Diagram"), applies `sa_adjustments` to the baseline (user edits if present, else original output). User notes from the ARLO Page are also included in the regeneration prompt.
- **SRS Trace:** §9.5, §1.10
- **Priority:** Must
- **Acceptance Criteria:** In Regeneration Mode, the AGA applies SA-reported adjustments to user-modified code without reverting user changes.

### 1.2 Code Generation

#### FR-AGA-003: Strict Translator Persona
- **Description:** The AGA persona SHALL be a "Strict Translator" that outputs ONLY valid PlantUML code — no conversational text, explanations, or markdown wrappers. The agent SHALL prioritize syntactic correctness and traceability over creative interpretation.
- **SRS Trace:** §9.5, §11.2.3
- **Priority:** Must
- **Acceptance Criteria:** The LLM output contains only PlantUML code (starting with `@startuml`, ending with `@enduml`) with no surrounding prose.

#### FR-AGA-004: Traceability Comment Injection
- **Description:** Every architectural entity (Component, Container, Database) generated in the `.puml` output SHALL be preceded by a traceability comment in the format: `' @Trace: [REQ-ID-1], [REQ-ID-2]`. The `arlo_reference` SHALL also be included as a global comment. This allows the SA's regex parser to deterministically map code blocks to requirements.
- **SRS Trace:** §9.5
- **Priority:** Must
- **Acceptance Criteria:** The rendered `.puml` file contains `' @Trace:` comments above every entity definition; the SA can extract all mapped requirement IDs via regex.

#### FR-AGA-005: Framework-Specific Code Generation
- **Description:** When `target_framework: C4_Container`, the AGA SHALL use C4-PlantUML stdlib macros (`!include`, `Container()`, `ContainerDb()`, `System_Ext()`, `System_Boundary()`, etc.). When `target_framework: UML_Component`, the AGA SHALL use standard UML component diagram syntax.
- **SRS Trace:** §9.5
- **Priority:** Must
- **Acceptance Criteria:** A C4 Container diagram includes correct `!include` directives and C4 macros; a UML diagram uses `component` and `interface` keywords.

#### FR-AGA-006: RAG-Driven Syntax Retrieval
- **Description:** The AGA SHALL query ChroamDB's `plantuml_syntax` collection for precise PlantUML C4 macros or standard UML syntax examples relevant to the current diagram type.
- **SRS Trace:** §9.5, §10.4
- **Priority:** Must
- **Acceptance Criteria:** A C4 Container diagram generation triggers a RAG query that retrieves C4 macro examples and include statements.

#### FR-AGA-007: Layout Hints Interpretation
- **Description:** The AGA SHALL interpret `layout_hints` from the RAA's TOON IR and apply corresponding PlantUML layout directives (e.g., `LAYOUT_LEFT_RIGHT()`, `LAYOUT_TOP_DOWN()`, `System_Boundary()` for groupings).
- **SRS Trace:** §9.5
- **Priority:** Should
- **Acceptance Criteria:** A `layout_hints.alignment: Left-to-Right` results in `LAYOUT_LEFT_RIGHT()` in the output `.puml`.

### 1.3 Syntax Validation & Self-Correction

#### FR-AGA-008: Compilation Validation Loop
- **Description:** After generating `.puml` code, the AGA node SHALL validate it by sending an HTTP POST to the PlantUML server (`plantuml-server:8080/svg/`):
  1. **Success (200 OK):** Save the `.puml` and proceed.
  2. **Failure (400 Bad Request):** Capture the syntax error message.
  3. **Self-Correction:** Feed the original code + error message back to the LLM with prompt: *"The previous code failed to compile. Error: {error}. Fix the syntax while preserving the architecture."*
  4. **Retry Limit:** Maximum 5 attempts total.
  5. **Fallback:** If 5 attempts fail, save the last broken version with marker comment `' GENERATION_FAILED: Manual review required` and proceed.
- **SRS Trace:** §9.5, §13.4
- **Priority:** Must
- **Acceptance Criteria:** A syntax error in the initial output triggers the correction loop; the corrected output compiles successfully within 5 retries.

#### FR-AGA-009: Validation Request Timeout
- **Description:** Individual syntax validation requests to the PlantUML server SHALL timeout after 5 seconds to prevent hanging during the correction loop.
- **SRS Trace:** §9.5
- **Priority:** Should
- **Acceptance Criteria:** A hanging PlantUML server does not block the AGA indefinitely; timeout triggers after 5 seconds.

### 1.4 Parallel Aggregation (Workflow 3)

#### FR-AGA-010: LLM-Based Parallel Code Merge
- **Description:** In Workflow 3, the AGA SHALL merge outputs from three parallel instances (Alpha, Beta, Gamma) using an LLM-based synthesis approach:
  1. Read `alpha.puml`, `beta.puml`, `gamma.puml`.
  2. The LLM assigned to AGA Alpha acts as "Lead Architect" with prompt: *"Analyze these three architectural variants. Synthesize a single, unified PlantUML file that incorporates the strongest structural elements of all three. Ensure no duplicate IDs exist."*
  3. Save as `mcp_aggregator/aga_aggregated.puml`.
- **SRS Trace:** §9.5, §4.3
- **Priority:** Must
- **Acceptance Criteria:** The aggregated `.puml` contains entities from all three variants without ID conflicts.

### 1.5 User Edit Handling

#### FR-AGA-011: User Manual Edit Baseline
- **Description:** When `user_manual_edits.puml` exists in the LangGraph state, the AGA SHALL use it as the baseline (overriding the original LLM output). In Regeneration Mode, SA adjustments SHALL be applied to the user-edited version, preserving user modifications.
- **SRS Trace:** §9.5, §1.9
- **Priority:** Must
- **Acceptance Criteria:** A user rename ("Db" → "Postgres") is preserved when SA feedback triggers regeneration.

### 1.6 Large Context Strategy

#### FR-AGA-012: Semantic Partitioning for Large Diagrams
- **Description:** If the RAA TOON input size suggests the output `.puml` will exceed the LLM's output token limit, the AGA SHALL:
  1. Split RAA entities by Container or Subsystem.
  2. Generate separate `.puml` partials (e.g., `defs_container_a.puml`, `defs_container_b.puml`, `rels.puml`).
  3. Concatenate into a master file using `!include` or raw text merging.
- **SRS Trace:** §9.5
- **Priority:** Should
- **Acceptance Criteria:** A large architecture with 50+ entities is split into sub-diagrams and reassembled without syntax errors.

### 1.7 Reasoning & Prompt Engineering

#### FR-AGA-013: Reasoning Log Isolation
- **Description:** The AGA SHALL output CoT reasoning in `<thinking>` XML blocks before generating the `.puml` code. The backend strips reasoning for storage. Citation in `<thinking>` blocks is NOT required (per §11.2.3).
- **SRS Trace:** §11.1, §11.2.3
- **Priority:** Must
- **Acceptance Criteria:** The response contains `<thinking>...</thinking>` followed by clean `.puml` code.

#### FR-AGA-014: Reactive Hallucination Permission
- **Description:** The AGA is allowed to invent a relationship ONLY if required to fix a specific "orphan node" syntax warning generated by the compiler. It SHALL NOT proactively hallucinate entities or relationships.
- **SRS Trace:** §9.5
- **Priority:** Must
- **Acceptance Criteria:** An orphan node warning triggers a minimal relationship addition; no unprompted entities are created.

---

## 2. Non-Functional Requirements (NFR)

### NFR-AGA-001: File Naming Convention
- **Description:** Output files SHALL follow: `aga_{LLM_Name}_{Timestamp}.puml`.
- **SRS Trace:** §3
- **Metric:** All AGA output files match the naming pattern.

### NFR-AGA-002: Token Budget Compliance
- **Description:** The AGA SHALL respect the `max_input_tokens × 0.85` budget. If exceeded, semantic partitioning (FR-AGA-012) activates.
- **SRS Trace:** §8.5
- **Metric:** No token overflow errors across test runs.

### NFR-AGA-003: Code Style
- **Description:** No specific aesthetic enforcement is applied to generated PlantUML code. The focus is strictly on syntax validity and structural correctness.
- **SRS Trace:** §11.2.3
- **Metric:** All generated `.puml` files compile successfully via the PlantUML server.

---

## 3. Interface Requirements (IR)

### IR-AGA-001: Input Interfaces
| Input | Source | Format |
|:--|:--|:--|
| RAA TOON IR | `raa_output/*.toon` or `mcp_aggregator/raa_aggregated.toon` | TOON (JSON) |
| ARLO Decisions | `arlo_output/*.toon` | TOON (context only) |
| User Edits | LangGraph state (`user_manual_edits.puml`) | PlantUML text |
| SA Feedback | LangGraph state (`sa_adjustments.json`) | JSON array |
| RAG Context | ChromaDB (`plantuml_syntax`) | Vector search results |

### IR-AGA-002: Output Interface
- **Target:** `/{project}/aga_output/aga_{llm}_{timestamp}.puml`
- **Aggregated (Workflow 3):** `/{project}/aga_output/mcp_aggregator/aga_aggregated.puml`
- **Downstream Consumer:** Scoring Agent, PlantUML Rendering Service, PDF Report Service

### IR-AGA-003: PlantUML Validation Interface
- **Target:** `http://plantuml-server:8080/svg/`
- **Method:** POST with raw `.puml` text
- **Purpose:** Syntax validation during the self-correction loop

---

## 4. Disaster Recovery Requirements (DR)

### DR-AGA-001: PlantUML Syntax Error (G-1)
- **Failure Mode:** Self-correction regex detects missing `@startuml`/`@enduml`, unclosed brackets, or invalid macros.
- **Recovery Action:** Re-invoke AGA with syntax error as correction prompt (up to 5 total attempts including initial). On exhaustion, output minimal valid stub with `' GENERATION_FAILED: Manual review required`.
- **User-Facing Message:** ⚠️ *"The diagram could not be generated correctly after multiple attempts. A placeholder has been saved."*
- **SRS Trace:** §13.4 (G-1)

### DR-AGA-002: Entity Hallucination (G-2)
- **Failure Mode:** AGA introduces Container/Component not present in RAA's TOON IR.
- **Recovery Action:** Post-generation diff check: compare entity names in `.puml` against TOON IR `entities[].name` list. Remove unmatched entities and log them.
- **User-Facing Message:** ℹ️ *"The diagram generator added {N} component(s) not in the specification. They have been automatically removed."*
- **SRS Trace:** §13.4 (G-2)

---

*End of AGA Requirements Document*
