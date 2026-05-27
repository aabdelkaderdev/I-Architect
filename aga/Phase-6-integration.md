# Phase 6 — Integration, Output Contract & Validation

> **Goal:** Wire the AGA module's public API (`__init__.py` exports), implement configurable output paths, finalize the output contract, handle assumption flag annotations, set up integration points with the orchestrator (and downstream SA/RGA), and create the test scaffolding.
>
> **Depends on:** All previous phases (1–5)
> **Produces:** Updated `aga/__init__.py` (public API), test files, integration documentation
> **Test fixture:** `arch_model_test_result-1.json`

---

## 6) Configurable Output Paths

### 6A — Orchestrator-Provided Paths

All output locations are **configurable by the orchestrator** at invocation time. The AGA never hardcodes output paths. The orchestrator provides paths via the `configurable` dict in `RunnableConfig`:

```python
config = {
    "configurable": {
        "thread_id": f"{run_id}:aga",
        "checkpoint_db_path": f"projects/{project_name}/checkpoints/aga.db",
        "output_dir": f"projects/{project_name}/output/aga/",
        "plantuml_server_url": "http://www.plantuml.com/plantuml",
    }
}
```

### 6B — Output Directory Layout

```
projects/{project_name}/output/aga/
├── ctx-sys1.png                    # Context diagram PNG
├── ctx-sys1.puml                   # Context diagram PlantUML source
├── ctx-sys1_metadata.json          # Context diagram metadata sidecar
├── cnt-sys1.png                    # Container diagram PNG
├── cnt-sys1.puml                   # Container diagram PlantUML source
├── cnt-sys1_metadata.json          # Container diagram metadata sidecar
├── cmp-container2.png              # Component diagram PNG
├── cmp-container2.puml             # Component diagram PlantUML source
├── cmp-container2_metadata.json    # Component diagram metadata sidecar
└── aga_report.json                 # Session report
```

### 6C — Checkpoint Directory

```
projects/{project_name}/checkpoints/
└── aga.db                          # SQLite checkpoint database
```

The orchestrator creates these directories before invoking AGA. The AGA module **must not** create directories — this is the orchestrator's responsibility (per Orchestrator Plan §2C).

---

## 11) Output Contract

### 11A — AGAOutput Schema

| Field | Type | Description |
|-------|------|-------------|
| `completed_diagrams` | `list[CompletedDiagram]` | Successfully rendered diagrams |
| `failed_diagrams` | `list[FailedDiagram]` | Diagrams that exhausted retries |
| `session_report` | `SessionReport` | Full session metadata |

### 11B — CompletedDiagram

| Field | Type | Description |
|-------|------|-------------|
| `diagram_id` | `str` | Canonical ID (e.g., `ctx-sys1`) |
| `diagram_type` | `str` | `context`, `container`, or `component` |
| `png_bytes` | `bytes` | Rendered PNG data |
| `plantuml_source` | `str` | PlantUML source code |
| `output_path` | `str` | Filesystem path where PNG was written |

### 11C — SessionReport

| Field | Type | Description |
|-------|------|-------------|
| `completed_count` | `int` | Number of successful diagrams |
| `failed_count` | `int` | Number of failed diagrams |
| `total_diagrams_expected` | `int` | Total diagrams in queue |
| `planturl_binary` | `str` | Binary path used |
| `detected_os` | `str` | OS/architecture detected |
| `plantuml_server_url` | `str` | Server URL used |
| `wall_clock_seconds` | `float` | Total execution time |

---

## 13) Integration Points

### 13A — Orchestrator → AGA

The orchestrator provides:
- `arch_model` dict via state channel
- LLM instance via `context={"llm": aga_llm}`
- Checkpoint DB path via `configurable["checkpoint_db_path"]`
- Output directory via `configurable["output_dir"]`
- Thread ID via `configurable["thread_id"]` (pattern: `{run_id}:aga`)

### 13B — AGA → Downstream (SA, RGA)

The AGA returns `AGAOutput` to the orchestrator, which threads:
- `completed_diagrams` → SA (for diagram accuracy scoring)
- `completed_diagrams` + `failed_diagrams` + `session_report` → RGA (for PDF report)
- `plantuml_source` in each `CompletedDiagram` → SA (for sub-tree inclusion validation)

### 13C — SA Regeneration Loop

When SA determines diagram regeneration is needed:
- Orchestrator re-invokes AGA with `targeted_diagrams` filter from SA's `FeedbackState`
- AGA only regenerates the specified diagram IDs, skipping already-valid ones

---

## 14) Assumption Flag Handling

Entities listed in `assumption_flags` carry an `assumed: true` marker in their metadata. When generating PlantUML code for these entities, the AGA appends `[assumed]` to the entity description string. This makes assumptions visible to diagram reviewers without breaking rendering.

---

## 15) Validation & Acceptance Criteria

### Unit Tests
- OS detection returns correct binary path for all 5 targets
- `encode_plantuml` produces non-empty URL for valid input
- `fetch_plantuml_png` classifies SVG error responses correctly
- Diagram queue derivation from flat JSON produces correct count and ordering

### Integration Tests
- End-to-end with `arch_model_test_result-1.json`: agent generates all derivable diagrams
- Syntax error injection → agent corrects and renders on retry
- Server unavailability → agent halts with structured failure report

### Functional Tests
- All PNGs are valid (magic bytes check)
- All .puml files round-trip through PlantUML server
- No entity alias in generated code references an ID not in the input model
- Assumed entities appear with `[assumed]` annotation

---

## 16) Open Design Decisions

| # | Question | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Parallel vs sequential diagram generation | Sequential (simpler) vs asyncio.gather (faster) | Sequential for v1, parallel as optimization |
| 2 | PlantUML source persistence | .puml alongside PNG vs embedded in metadata JSON | Both: .puml file + metadata sidecar |
| 3 | Diagram deduplication | Skip diagrams with identical entity sets | Defer — manifest-driven approach prevents most duplicates |
| 4 | Self-hosted PlantUML fallback | Auto-fallback to local Docker instance | Explicit config only — no silent fallback |
