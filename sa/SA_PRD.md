# Scoring Agent (SA) — Product Requirements Document

## 1. Purpose

The Scoring Agent (SA) evaluates the quality of a generated software architecture. It takes the architecture model produced by the Requirements Analysis Agent (RAA), the three C4 PlantUML diagram strings rendered by the Architecture Generation Agent (AGA), and the original requirements set. It produces a **100-point grade** across three axes and generates an executive report in both JSON and Markdown.

SA is strictly **read-only**. It does not modify the architecture, trigger regeneration, or make decisions about what happens next. It scores and reports — the orchestrator decides what to do with the results.

---

## 2. Pipeline Position

```
RAA (arch model) + AGA (plantuml strings) → Orchestrator → SA → Score & Report → Orchestrator
```

The orchestrator:
- Collects the RAA output (arch model JSON), AGA output (3 PlantUML strings), and requirements dictionary
- Passes them to SA along with an LLM instance
- Invokes SA
- Receives the score report and decides next steps

The orchestrator module is not yet developed. SA is designed to be invoked by it.

---

## 3. Inputs

### 3.1 Architecture Model

The RAA output JSON (`arch_model_test_result.json` structure). Key contents:

| Field | Description |
|-------|-------------|
| `entities` | Flat list of all C4 entities. Each has `id`, `name`, `c4_type` (system/container/component/person/external_system), `technology`, `parent_system_id`, `parent_container_id`, `requirement_ids`, and `metadata` |
| `relationships` | Flat list of relationships. Each has `source_id`, `target_id`, `description`, `diagram_scope`, and `requirement_ids` |

SA reconstructs the hierarchy from the flat entity list using `parent_system_id` and `parent_container_id` references.

### 3.2 PlantUML Diagram Strings

The orchestrator provides **exactly three** PlantUML source strings:

| Diagram | `diagram_type` | Content Expected |
|---------|---------------|------------------|
| System Context | `context` | The system under design, all persons, and all external systems from the architecture model |
| Container | `container` | All containers within the primary system, plus external dependencies |
| Component | `component` | All components within a selected container, showing internal structure |

These three strings are the raw PlantUML text that AGA produced. SA parses them to verify diagram correctness.

### 3.3 Requirements Data

A dictionary packed by the orchestrator:

```
{
    "requirements": dict[str, str],       # req_id → description
    "asrs": list[str],                     # ASR requirement IDs
    "non_asr": list[str],                  # Functional requirement IDs
    "quality_weights": dict[str, int]      # quality_attribute → weight
}
```

Quality weights come from ARLO and indicate the relative importance of each quality attribute (security, performance, reliability, etc.) to the system.

---

## 4. Scoring Rubric (100 Points)

### Axis 1: Functional Traceability (25 points)

Evaluates whether every functional (non-ASR) requirement is mapped to at least one architecture entity, and whether the mapping reaches adequate depth.

| Sub-rubric | Points | Method |
|------------|--------|--------|
| Mapping coverage | 15 pts | Deterministic: `(mapped functional reqs / total functional reqs) × 15` |
| Depth of resolution | 10 pts | LLM-evaluated: do requirements trace down to appropriate C4 levels? Data-handling requirements should reach the component level; broad business requirements may reasonably stop at the system or container level |
| Orphan penalty | -1 per orphan, max -10 | Deterministic: deduction for each functional requirement mapped to zero entities |

**Depth evaluation rationale:** SA examines the deepest C4 level (component > container > system) at which each requirement is traced. The LLM receives a distribution summary — e.g., "60% at component level, 30% at container level, 10% at system level" — and judges whether the distribution is appropriate for the nature of the requirements.

### Axis 2: ASR Coverage (25 points)

Evaluates whether Architecturally Significant Requirements (ASRs) are properly traced into the architecture.

| Sub-rubric | Points | Method |
|------------|--------|--------|
| ASR mapping coverage | 15 pts | Deterministic: `(mapped ASRs / total ASRs) × 15` |
| Technology specificity | 10 pts | LLM-evaluated: rewards specific, compatible technology choices (e.g., "PostgreSQL 15") over generic placeholders (e.g., "Database"). Generic values are penalised only when the relevant quality attribute demands a specific property |
| Contradiction penalty | -5 pts | Deterministic per contradiction found (e.g., synchronous pattern chosen for an ASR demanding asynchronous resilience) |

### Axis 3: SAAM Evaluation & Diagram Accuracy (50 points)

This is the primary axis. It combines SAAM-based quality attribute evaluation with diagram correctness checks. The SAAM (Software Architecture Analysis Method) methodology evaluates whether the architecture's patterns and technology choices genuinely address the system's most important quality attributes.

#### 3A. SAAM Quality Attribute Evaluation (30 points) — LLM

The LLM receives:
- The top-weighted quality attributes from ARLO
- The patterns declared in the architecture model
- The flattened technology stack (technology values per entity)
- The three PlantUML diagram strings

The LLM evaluates whether:
- Declared patterns directly address the quality attribute's stimulus-response scenarios (per SAAM methodology)
- Technology choices are compatible with the quality attribute requirements
- Pattern-to-attribute mappings have mechanistic justification, not just name association

Generic "pattern name matches quality attribute name" reasoning scores zero. A pattern satisfies a quality attribute only if its documented properties address the specific stimulus-response scenario.

#### 3B. Diagram Correctness (20 points) — Deterministic

SA parses each PlantUML string and checks structural correctness against the architecture model:

| Sub-rubric | Points | Method |
|------------|--------|--------|
| Render completeness | 10 pts | All three expected diagram strings are non-empty. Deduct proportionally per missing/empty diagram |
| Entity inclusion | 5 pts | Each diagram's PlantUML source contains the expected entities: context diagram must include all persons and external systems; container diagram must include all containers of the primary system; component diagram must include all components of the selected container |
| Hierarchy validity | 5 pts | C4 element types are used correctly — no containers appearing in context diagrams as top-level, no components appearing in container diagrams. Deductions per misplaced entity |

Alias matching uses the entity's canonical `id` field — AGA is required to use the entity ID as the PlantUML alias, making verification straightforward string matching.

---

## 5. Processing Flow

SA is implemented as a **sequential LangGraph StateGraph** with five nodes. Each node completes before the next starts. No branching, no parallelism — a simple linear pipeline.

### Node 1: Data Preparation (deterministic)

Parses all inputs and builds the structures used by later nodes:

1. Traverses the flat `entities` list and reconstructs the C4 hierarchy (systems → containers → components, plus persons and external systems)
2. Builds a `traceability_matrix`: for each requirement ID, records every entity that references it and the deepest C4 level at which it appears
3. Cross-references the matrix with `non_asr` and `asrs` lists to identify orphaned requirements (requirements not mapped to any entity)
4. Extracts a flattened technology list: entity ID → technology value
5. Extracts declared patterns from entity metadata
6. Sorts `quality_weights` to identify the top-weighted quality attributes

### Node 2: Functional Traceability Score (Axis 1)

**Deterministic step:** Computes mapping coverage: `(mapped_functional / total_functional) × 15`. Applies orphan penalties.

**LLM step:** Passes the depth distribution summary (percentage of functional requirements at each C4 level) to the functional depth evaluation skill. The LLM returns a score out of 10 and a reasoning string.

### Node 3: ASR Coverage Score (Axis 2)

**Deterministic step:** Computes ASR mapping coverage: `(mapped_asrs / total_asrs) × 15`. Identifies technology contradictions.

**LLM step:** Passes the flattened technology list with the relevant quality attribute context to the technology inference skill. The LLM returns a score out of 10 for technology specificity and a reasoning string.

### Node 4: SAAM & Diagram Score (Axis 3)

**LLM step (SAAM evaluation, 30 pts):** Passes the top quality attributes, patterns, technology stack, and the three PlantUML strings to the SAAM validation skill. The LLM evaluates pattern effectiveness and technology-attribute alignment using SAAM methodology. Returns a score out of 30 and a reasoning string.

**Deterministic step (diagram correctness, 20 pts):**
1. Checks each PlantUML string is non-empty (render completeness)
2. Parses each PlantUML string for entity aliases (canonical IDs)
3. For the context diagram: verifies all persons and external systems appear
4. For the container diagram: verifies all containers of the primary system appear
5. For the component diagram: verifies all components of the selected container appear
6. Checks that entity aliases in each diagram match the expected C4 level (no cross-level leakage)
7. Computes proportional deductions for missing or misplaced entities

### Node 5: Report Compilation

**Deterministic step:** Sums the three axis scores. Computes letter grade (A: 90+, B: 80+, C: 70+, D: 60+, F: <60). Builds the structured `ScoringReport` JSON object.

**LLM step:** Passes all scores, reasoning strings, orphaned requirements, and diagram issues to the executive summary skill. The LLM returns an executive summary in Markdown and exactly 3–5 key findings (each ≤25 words).

**Filesystem output:** Writes `scoring_report.json` and `scoring_report.md` to the output path provided by the orchestrator.

---

## 6. Skills & LLM Calls

SA uses three LLM calls, each guided by a skill reference document. Skills define the methodology, constraints, and output schemas. Runtime prompt templates are derived from skills and are pre-formatted for LLM consumption.

| Skill | Node | Purpose |
|-------|------|---------|
| `Functional_Depth_Evaluation.md` | Node 2 | Guidelines for judging appropriate requirement-to-C4-level mapping depth |
| `SAAM_Validation.md` | Node 4 | SAAM methodology: evaluating whether patterns and technologies satisfy quality attribute stimulus-response scenarios |
| `Executive_Summary_Writer.md` | Node 5 | Formatting constraints for translating score data into a readable executive summary |

### Skill File Format

Each skill follows a standard template:
1. **Purpose** — what the skill evaluates
2. **Input** — data received from SA state
3. **Normative Rules** — hard constraints the LLM must follow (paraphrased from C4 model specification, SAAM methodology, and ISO/IEC 25010)
4. **Decision Guidelines** — heuristics for ambiguous cases
5. **Output Schema** — the JSON structure the LLM must return
6. **Error Cases** — known failure modes and handling
7. **Examples** — worked example with expected reasoning and output

### Deterministic Processing

All math, tree traversal, PlantUML parsing, alias matching, and report assembly are deterministic Python. The LLM is only used for subjective evaluation sub-rubrics (depth adequacy, technology specificity, SAAM pattern effectiveness, and executive summary writing).

---

## 7. Outputs

### 7.1 Scoring Report (JSON)

Written to `scoring_report.json`. A structured machine-parseable report containing all scores, reasoning, and gap analysis.

### 7.2 Executive Summary (Markdown)

Written to `scoring_report.md`. The LLM-generated narrative report suitable for human review. Contains the scores, key findings, and overall grade.

### 7.3 Output Location

The orchestrator provides an output directory path. Both files are written there. If the path is not writeable, SA raises an error — the orchestrator handles creation of the directory.

---

## 8. Project Structure

SA mirrors the module layout used by ARLO and RAA:

```
sa/
├── __init__.py
├── runner.py                 # Graph compilation, entry point
├── graphs/
│   ├── __init__.py
│   └── core.py               # StateGraph definition, node wiring, edge definitions
├── state/
│   ├── __init__.py
│   ├── schemas.py             # SA input/output/state TypedDicts
│   └── models.py              # Supporting types (AxisScore, ScoringReport, etc.)
├── nodes/
│   ├── __init__.py
│   ├── preparation.py         # Node 1: data parsing, hierarchy reconstruction, matrix build
│   ├── axis_functional.py     # Node 2: functional traceability score
│   ├── axis_asr.py            # Node 3: ASR coverage score
│   ├── axis_saam.py           # Node 4: SAAM evaluation + diagram accuracy
│   └── report.py              # Node 5: report compilation, summarisation, file output
├── prompts/
│   ├── functional_depth.md    # Runtime prompt for Node 2 LLM call
│   ├── saam_validation.md     # Runtime prompt for Node 4 LLM call
│   └── executive_summary.md   # Runtime prompt for Node 5 LLM call
└── utils/
    ├── __init__.py
    ├── traversal.py            # Hierarchy traversal, depth resolution, alias extraction
    └── plantuml_parser.py      # PlantUML source parsing, entity alias extraction
```

### Skills Directory

```
Skills/SA/
├── SKILL.MD                               # SA skill metadata (agent-level definition)
└── references/
    ├── SAAM.md                            # General SAAM methodology reference
    ├── Functional_Depth_Evaluation.md     # Depth sub-rubric skill
    ├── SAAM_Validation.md                 # SAAM validation skill
    └── Executive_Summary_Writer.md        # Executive summary skill
```

---

## 9. LangGraph Integration

SA is a standalone LangGraph StateGraph, not a subgraph of any other agent. The orchestrator invokes it:

```python
sa_graph.invoke(
    {
        "arch_model": raa_output,
        "plantuml_context": plantuml_context_str,
        "plantuml_container": plantuml_container_str,
        "plantuml_component": plantuml_component_str,
        "requirements_data": { ... },
    },
    context={"llm": sa_llm},
)
```

The LLM is passed via LangGraph's runtime `context` — never through state channels. This keeps state serialisable and follows the pattern used by ARLO and RAA.

The graph is strictly sequential:
```
Node 1 (Prep) → Node 2 (Functional) → Node 3 (ASR) → Node 4 (SAAM) → Node 5 (Report)
```

All state channels use default `overwrite` semantics — no custom reducers needed.

---

## 10. Design Principles

1. **Simple over complex.** Five sequential nodes. Three LLM calls. No branching, no feedback loops, no regeneration logic.
2. **Deterministic where possible.** Math, parsing, tree traversal, and diagram checks are plain Python. LLM is only for subjective evaluation.
3. **Read-only.** SA never modifies the architecture model. It evaluates and reports.
4. **Orchestrator owns decisions.** SA provides the score and findings. Whether to accept, regenerate, or re-run earlier pipeline stages is the orchestrator's call.
5. **SAAM as the primary axis.** The SAAM evaluation carries the most weight (50%) because it directly measures architectural integrity — whether the architecture's design choices actually solve the quality attribute challenges they claim to address.

---

## Appendix A: Scoring Report Schema

### ScoringReport (top-level)

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | `str` | Schema version, e.g. `"1.0"` |
| `report_id` | `str` | Unique identifier for this report |
| `generated_at` | `str` | ISO 8601 UTC timestamp |
| `pipeline_run_id` | `str` | The RAA thread ID that produced the input arch model |
| `summary` | `ReportSummary` | Top-level scorecard |
| `axis_scores` | `AxisBreakdown` | Full three-axis breakdown |
| `gap_analysis` | `GapAnalysis` | All identified deficiencies |
| `executive_summary` | `ExecutiveSummary` | LLM-generated narrative and key findings |

### ReportSummary

| Field | Type | Description |
|-------|------|-------------|
| `total_score` | `float` | 0.0–100.0 |
| `grade` | `str` | A (≥90), B (≥80), C (≥70), D (≥60), F (<60) |
| `requirements_total` | `int` | Total requirement count |
| `requirements_asr` | `int` | Count of ASRs |
| `requirements_functional` | `int` | Count of functional requirements |
| `requirements_orphaned` | `int` | Requirements mapped to zero entities |
| `diagrams_present` | `int` | Number of non-empty PlantUML strings provided (0–3) |

### AxisBreakdown

| Field | Type | Description |
|-------|------|-------------|
| `functional` | `AxisScore` | Axis 1 detail |
| `asr_coverage` | `AxisScore` | Axis 2 detail |
| `saam_diagrams` | `AxisScore` | Axis 3 detail |

### AxisScore

| Field | Type | Description |
|-------|------|-------------|
| `awarded` | `float` | Points awarded |
| `possible` | `int` | Maximum points for this axis |
| `sub_scores` | `dict[str, float]` | Named sub-rubric scores |
| `llm_reasoning` | `str \| null` | LLM reasoning string (null for purely deterministic axes) |
| `penalties_applied` | `list[Penalty]` | All penalties applied |

### Penalty

| Field | Type | Description |
|-------|------|-------------|
| `reason` | `str` | What triggered the penalty |
| `points` | `float` | Points deducted (negative float) |
| `requirement_id` | `str \| null` | Related requirement, if applicable |

### GapAnalysis

| Field | Type | Description |
|-------|------|-------------|
| `orphaned_requirements` | `list[OrphanedRequirement]` | Requirements not mapped to any entity |
| `diagram_issues` | `list[DiagramIssue]` | Problems found in PlantUML diagrams |

### OrphanedRequirement

| Field | Type | Description |
|-------|------|-------------|
| `req_id` | `str` | Requirement ID |
| `is_asr` | `bool` | Whether ASR or functional |
| `text_snippet` | `str` | First 120 characters of requirement text |

### DiagramIssue

| Field | Type | Description |
|-------|------|-------------|
| `diagram_type` | `str` | context, container, or component |
| `issue_type` | `str` | missing_entity, wrong_level, empty_diagram |
| `entity_id` | `str \| null` | Affected entity ID |
| `description` | `str` | Human-readable description |

### ExecutiveSummary

| Field | Type | Description |
|-------|------|-------------|
| `markdown` | `str` | Full LLM-generated executive summary |
| `key_findings` | `list[str]` | 3–5 concise findings, each ≤25 words |
| `overall_grade` | `str` | Letter grade |

## Appendix B: State Schema

SA's internal LangGraph state:

| Channel | Type | Description |
|---------|------|-------------|
| `arch_model` | `dict` | RAA output (entities, relationships, etc.) |
| `plantuml_context` | `str` | Context diagram PlantUML source |
| `plantuml_container` | `str` | Container diagram PlantUML source |
| `plantuml_component` | `str` | Component diagram PlantUML source |
| `requirements_data` | `dict` | Requirements, ASRs, non-ASRs, quality weights |
| `traceability_matrix` | `dict` | req_id → list of {entity_id, level, deepest_level} |
| `orphaned_reqs` | `list[str]` | Unmapped requirement IDs |
| `score_functional` | `AxisScore` | Node 2 output |
| `score_asr` | `AxisScore` | Node 3 output |
| `score_saam` | `AxisScore` | Node 4 output |
| `final_report` | `ScoringReport` | Node 5 output (full report) |
| `output_path` | `str` | Orchestrator-provided directory for output files |
