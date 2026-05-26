# Phase 1: Foundation, Data Prep, and Pipeline Skeleton

## Objective

Establish the LangGraph StateGraph architecture, implement robust data ingestion, and ensure the pipeline can run end-to-end producing a valid (but zero-scored) JSON report.

---

## Scope

### In Scope (Vertical Slice)

- Graph definition and state schemas (`schemas.py`, `models.py`, `graphs/core.py`, `runner.py`).
- **Node 1 (Data Preparation):** Fully implemented. Hierarchy traversal, traceability matrix construction, and entity extraction.
- **Node 5 (Report Compilation — Partial):** Deterministic step only. Calculating the final grade from state and writing the structured `ScoringReport` to `scoring_report.json`.

### Mocks / Extensibility

- Nodes 2, 3, and 4 are implemented as mock passthroughs that inject 0 points and empty reasoning into the state.
- Node 5's LLM executive summary is stubbed with a static Markdown string.

### Estimated OpenSpec Task Count: ~10–12 tasks.

---

## Pipeline Position

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

## Inputs

### Architecture Model

The RAA output JSON (`arch_model_test_result.json` structure). Key contents:

| Field | Description |
|-------|-------------|
| `entities` | Flat list of all C4 entities. Each has `id`, `name`, `c4_type` (system/container/component/person/external_system), `technology`, `parent_system_id`, `parent_container_id`, `requirement_ids`, and `metadata` |
| `relationships` | Flat list of relationships. Each has `source_id`, `target_id`, `description`, `diagram_scope`, and `requirement_ids` |

SA reconstructs the hierarchy from the flat entity list using `parent_system_id` and `parent_container_id` references.

### PlantUML Diagram Strings

The orchestrator provides **exactly three** PlantUML source strings:

| Diagram | `diagram_type` | Content Expected |
|---------|---------------|------------------|
| System Context | `context` | The system under design, all persons, and all external systems from the architecture model |
| Container | `container` | All containers within the primary system, plus external dependencies |
| Component | `component` | All components within a selected container, showing internal structure |

These three strings are the raw PlantUML text that AGA produced. SA parses them to verify diagram correctness.

### Requirements Data

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

## Node 1: Data Preparation (Fully Implemented)

Parses all inputs and builds the structures used by later nodes:

1. Traverses the flat `entities` list and reconstructs the C4 hierarchy (systems → containers → components, plus persons and external systems)
2. Builds a `traceability_matrix`: for each requirement ID, records every entity that references it and the deepest C4 level at which it appears
3. Cross-references the matrix with `non_asr` and `asrs` lists to identify orphaned requirements (requirements not mapped to any entity)
4. Extracts a flattened technology list: entity ID → technology value
5. Extracts declared patterns from entity metadata
6. Sorts `quality_weights` to identify the top-weighted quality attributes

---

## Node 5: Report Compilation (Deterministic Only)

**Deterministic step:** Sums the three axis scores. Computes letter grade (A: 90+, B: 80+, C: 70+, D: 60+, F: <60). Builds the structured `ScoringReport` JSON object.

**LLM step (STUBBED):** Returns a static Markdown string placeholder instead of invoking the executive summary skill.

**Filesystem output:** Writes `scoring_report.json` to the output path provided by the orchestrator.

---

## Mock Nodes (2, 3, 4)

Each mock node:
- Accepts the current state
- Injects an `AxisScore` with `awarded = 0.0`, empty `sub_scores`, `llm_reasoning = null`, and no penalties
- Returns the updated state

This allows the full pipeline to run end-to-end and produce a structurally valid report with zero scores.

---

## Project Structure

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
│   ├── axis_functional.py     # Node 2: MOCK passthrough (0 score)
│   ├── axis_asr.py            # Node 3: MOCK passthrough (0 score)
│   ├── axis_saam.py           # Node 4: MOCK passthrough (0 score)
│   └── report.py              # Node 5: report compilation (deterministic only, LLM stubbed)
├── prompts/                   # Empty — no LLM calls in Phase 1
└── utils/
    ├── __init__.py
    └── traversal.py            # Hierarchy traversal, depth resolution, alias extraction
```

---

## LangGraph Integration

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

## State Schema

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

---

## Scoring Report Schema

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

---

## Design Principles

1. **Simple over complex.** Five sequential nodes. Three LLM calls. No branching, no feedback loops, no regeneration logic.
2. **Deterministic where possible.** Math, parsing, tree traversal, and diagram checks are plain Python. LLM is only for subjective evaluation.
3. **Read-only.** SA never modifies the architecture model. It evaluates and reports.
4. **Orchestrator owns decisions.** SA provides the score and findings. Whether to accept, regenerate, or re-run earlier pipeline stages is the orchestrator's call.
5. **SAAM as the primary axis.** The SAAM evaluation carries the most weight (50%) because it directly measures architectural integrity.
