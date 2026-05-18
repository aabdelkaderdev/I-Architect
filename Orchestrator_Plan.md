# Orchestrator Specification

## 0) Goal of this Portion

Define the **central orchestrator** that manages the I-Architect pipeline end-to-end: project lifecycle, LLM instance registry, pipeline execution sequencing, state threading between subgraphs, timing measurement, progress estimation, checkpoint management, pre-flight dependency validation, and error propagation. The orchestrator is the **backend brain** — it receives signals from the UI layer, executes pipeline logic, and emits state updates back to the UI. It never imports PySide6 widget classes.

The orchestrator is implemented as a **LangGraph StateGraph** so that its own state (current stage, timing records, LLM assignments) benefits from the same checkpointing infrastructure used by all subgraphs.

> **Pipeline position note:** The orchestrator is the outermost graph. It is not a subgraph — it is the root LangGraph StateGraph that invokes all subgraphs (Ingestion, ARLO, RAA, AGA, SA, RGA) in sequence. It produces no analytical output of its own; its sole products are timing metadata, progress signals, and the final assembled `PipelineMetadata` for RGA.

> **Boundary:** UI layer owns visual rendering, widget state, and user interaction. Orchestrator owns pipeline execution, LLM management, file/project management, timing, progress estimation, and state threading. See UX&UI_Plan.md for the UI-side signal/slot contracts.

---

## 1) Architecture Overview

The orchestrator is the central controller in a hub-and-spoke architecture:

```
┌──────────────────────────────────────────────────────────────────────┐
│                        UI Layer (PySide6)                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────┐  │
│  │Projects │ │LLM/Work │ │Ingestion│ │  ARLO   │ │ RAA/AGA/SA   │  │
│  │  View   │ │  flow   │ │  View   │ │  View   │ │   Views      │  │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └──────┬───────┘  │
│       │           │           │           │               │          │
│       └───────────┴───────────┴───────────┴───────────────┘          │
│                           │ Qt Signals/Slots                         │
└───────────────────────────┼──────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────────┐
│                   Orchestrator (LangGraph StateGraph)                 │
│                           │                                          │
│  ┌────────────────────────┼───────────────────────────────────────┐  │
│  │  Project Registry │ LLM Registry │ Pipeline Engine │ Progress │  │
│  └────────────────────────┼───────────────────────────────────────┘  │
│                           │                                          │
│     ┌─────────────────────┼─────────────────────────────────┐        │
│     │  Ingestion → ARLO → RAA → AGA → SA → RGA             │        │
│     └───────────────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────────────┘
```

**Key design decisions (from Segregate.md §Key Design Decisions):**

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | Orchestrator form | LangGraph StateGraph | Enables checkpointing of orchestrator's own state; consistent with existing patterns |
| 2 | Project registry format | SQLite | Consistent with checkpoint storage; survives partial writes; supports concurrent reads |
| 3 | Checkpoint isolation | Per-project `projects/{name}/checkpoints/` | Prevents cross-project collisions; clean deletion |
| 4 | LLM object passing | `context={}` dict | Follows ARLO's existing pattern (`context={"llm": llm}`); prevents LLM serialization into checkpoints |
| 5 | Progress callback | Context-injected callbacks for batch subgraphs; event streaming for others | Best granularity where it matters; simpler where it doesn't |
| 6 | User overrides storage | Orchestrator state channel | Keeps override history in checkpoints; enables resume after crash |
| 7 | API key encryption | AES for production; plain JSON for development | Spec defines interface; implementation chooses |

---

## 2) Project & File Management

### 2A — Project Directory Structure

Each project is an isolated directory on disk:

```
projects/
├── registry.db                    # SQLite project registry
└── {project_name}/
    ├── input/                     # Uploaded requirement document
    ├── output/
    │   ├── arlo/                  # ARLO output artifacts
    │   ├── raa/                   # RAA output (C4JsonModel JSON)
    │   ├── aga/                   # AGA PNGs + metadata sidecars + aga_report.json
    │   ├── sa/                    # scoring_report.json, scoring_report.md, feedback_state.json
    │   └── rga/                   # Final PDF report
    ├── checkpoints/
    │   ├── orchestrator.db        # Orchestrator's own checkpoint
    │   ├── ingestion.db           # Ingestion pipeline checkpoint
    │   ├── arlo.db                # ARLO checkpoint
    │   ├── raa_graph.db           # RAA checkpoint
    │   ├── aga.db                 # AGA checkpoint
    │   ├── sa.db                  # SA checkpoint
    │   └── rga.db                 # RGA checkpoint
    └── logs/                      # Structured per-run logs
```

### 2B — Project Registry

A SQLite database at `projects/registry.db` tracks all projects.

**`projects` table schema:**

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `id` | `TEXT` | `PRIMARY KEY` | UUID identifying the project |
| `name` | `TEXT` | `UNIQUE NOT NULL` | User-provided folder name |
| `created_at` | `TEXT` | `NOT NULL` | ISO 8601 UTC timestamp |
| `status` | `TEXT` | `NOT NULL` | One of: `active`, `archived`, `error` |
| `last_run_id` | `TEXT` | FK → `pipeline_runs.run_id` | Most recent pipeline run |
| `document_path` | `TEXT` | — | Path to uploaded requirement document |
| `document_format` | `TEXT` | — | One of: `pdf`, `docx`, `txt`, `json` |
| `metadata_json` | `TEXT` | — | Arbitrary extensible metadata (JSON string) |

**`pipeline_runs` table schema:**

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `run_id` | `TEXT` | `PRIMARY KEY` | Run identifier, pattern `run-{sha256[:16]}` |
| `project_id` | `TEXT` | `NOT NULL`, FK → `projects.id` | Owning project |
| `started_at` | `TEXT` | `NOT NULL` | ISO 8601 UTC start timestamp |
| `completed_at` | `TEXT` | — | ISO 8601 UTC completion timestamp (null if running) |
| `status` | `TEXT` | `NOT NULL` | One of: `running`, `completed`, `failed`, `cancelled` |
| `current_stage` | `TEXT` | — | Which subgraph is executing |
| `overall_progress` | `REAL` | — | 0.0–1.0 progress fraction |
| `llm_assignments_json` | `TEXT` | — | JSON map of `{agent_role: instance_name}` |

### 2C — Artifact Organization

Every subgraph output is written to a project-scoped directory. The orchestrator creates `output/{agent}/` before each subgraph invocation.

| Subgraph | Output Directory | Key Artifacts |
|----------|-----------------|---------------|
| Ingestion | `output/ingestion/` | `extracted_requirements.json`, `filter_report.json` |
| ARLO | `output/arlo/` | `arlo_output.json` (asrs, non_asr, condition_groups, quality_weights, concerns, stats) |
| RAA | `output/raa/` | `arch_model.json` (C4JsonModel), `open_questions.json` |
| AGA | `output/aga/` | `{diagram_id}.png`, `{diagram_id}_metadata.json`, `aga_report.json` |
| SA | `output/sa/` | `scoring_report.json`, `scoring_report.md`, `feedback_state.json` |
| RGA | `output/rga/` | `i-architect-report-{run_id}.pdf` |

### 2D — File Upload Handling

- Single document per project (enforced by project registry `document_path` field).
- On upload signal from UI, the orchestrator copies the file to `projects/{name}/input/` and records the path in the registry.
- Re-uploading replaces the existing document; previous document is archived with a `.bak` suffix.

### 2E — Log Management

Structured JSON-line logs per project at `projects/{name}/logs/{run_id}.jsonl`. Each log entry:

```json
{"timestamp": "2026-05-18T14:30:45.123Z", "level": "INFO", "stage": "arlo", "event": "batch_complete", "batch": 3, "total": 12, "duration_ms": 2340}
```

The "Download Logs" UI button triggers the orchestrator to bundle `projects/{name}/logs/` into a `.tar.gz` and present a save dialog path.

### 2F — Authoritative Source Register

**Purpose:** Ensure all orchestrator behaviours are anchored to authoritative API contracts for LangGraph checkpointing, LangChain ChatModel interfaces, PySide6 signal/slot threading, and SQLite persistence. Explicit normative constraints derived from each source.

#### Source Register Table

| Source | URL | Retrieval Date | Governs |
|--------|-----|----------------|---------|
| LangGraph — Checkpointing | https://langchain-ai.github.io/langgraph/reference/checkpoints/ | (set on retrieval) | SqliteSaver API, `get_state()`, `get_state_history()`, thread ID semantics, checkpoint granularity |
| LangGraph — StateGraph | https://langchain-ai.github.io/langgraph/reference/graphs/ | (set on retrieval) | `add_node`, `add_edge`, `add_conditional_edges`, `compile`, `invoke` signatures |
| LangGraph — Send API | https://langchain-ai.github.io/langgraph/how-tos/branching/ | (set on retrieval) | Fan-out semantics, parallel execution in super-step, reducer requirements for multi-writer channels |
| LangChain — BaseChatModel | https://python.langchain.com/api_reference/core/language_models/langchain_core.language_models.chat_models.BaseChatModel.html | (set on retrieval) | `invoke`, `ainvoke`, `bind_tools`, `with_structured_output` signatures |
| PySide6 — Signals & Slots | https://doc.qt.io/qtforpython-6/PySide6/QtCore/Signal.html | (set on retrieval) | `Signal(dict)` declaration, `emit`, `connect`, QThread affinity, `Qt.QueuedConnection` |
| SQLite — WAL Mode | https://www.sqlite.org/wal.html | (set on retrieval) | Concurrent read/write behaviour, checkpointing, WAL file management |

#### Normative Constraints (Derived from Sources)

**LangGraph constraints:**
- State channels written by multiple nodes in the same super-step must use an append or dict-merge reducer. Without a reducer, LangGraph applies last-write-wins.
- LLM objects must never be stored in state channels — they are not serialisable by `JsonPlusSerializer` and would bloat checkpoints.
- `thread_id` is the sole key for checkpoint retrieval. The orchestrator must use project-scoped, deterministic thread IDs.
- `SqliteSaver` connections must be opened in the same process that invokes the graph. Cross-process sharing is not supported.

**PySide6 constraints:**
- Signals crossing thread boundaries (UI thread ↔ QThread worker) require `Signal(dict)` or `Signal(object)` type declarations. Bare `Signal()` rejects arguments.
- `Qt.AutoConnection` resolves to `Qt.QueuedConnection` when sender and receiver are in different threads — safe for orchestrator-to-UI communication.
- QThread workers must not import or touch widget classes. Only signal payloads (dicts) cross the boundary.

**SQLite constraints:**
- WAL mode must be enabled for checkpoint databases accessed concurrently by the orchestrator and subgraph graphs.
- Directory creation (`checkpoints/`, `output/`) is the orchestrator's responsibility — subgraph modules must not create directories.

---

## 3) LLM Instance Management

> **UI reference:** UX&UI_Plan.md §1.3 (LLM Configuration Dashboard) defines the widget layout. The orchestrator implements the backend logic described there.

### 3A — Global Registry Schema

LLM instances are stored in a project-agnostic SQLite database at `llm_registry.db` in the project root.

**`llm_instances` table schema:**

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `name` | `TEXT` | `PRIMARY KEY` | User-defined unique label |
| `provider` | `TEXT` | `NOT NULL` | One of: `OpenRouter`, `ChatGPT`, `Anthropic`, `DeepSeek`, `Ollama` |
| `model_name` | `TEXT` | `NOT NULL` | e.g., `gpt-4o`, `claude-sonnet-4-6` |
| `api_key_encrypted` | `TEXT` | — | AES-encrypted key (NULL for Ollama) |
| `base_url` | `TEXT` | — | NULL = provider default |
| `temperature` | `REAL` | `NOT NULL` | 0.0–1.0 |
| `created_at` | `TEXT` | `NOT NULL` | ISO 8601 UTC |
| `updated_at` | `TEXT` | `NOT NULL` | ISO 8601 UTC |

**`project_llm_assignments` table schema:**

| Column | Type | Constraint | Description |
|--------|------|-----------|-------------|
| `project_id` | `TEXT` | `NOT NULL`, FK → `projects.id` | Owning project |
| `agent_role` | `TEXT` | `NOT NULL` | One of the canonical agent role keys |
| `instance_name` | `TEXT` | `NOT NULL`, FK → `llm_instances.name` | Assigned LLM instance |
| **Primary Key** | — | `(project_id, agent_role)` | One instance per role per project |

**Agent role key space:**

| Role Key | Agent | Required LLM Count |
|----------|-------|--------------------|
| `rfa` | Requirement Filtering Agent | 1 |
| `arlo` | ARLO | 1 |
| `raa_a` | RAA-A (SAAM-first) | 1 |
| `raa_b` | RAA-B (Pattern-driven) | 1 |
| `raa_c` | RAA-C (Entity-driven) | 1 |
| `raa_judge` | RAA Judge | 1 |
| `aga` | AGA | 1 |
| `sa` | SA | 1 |

### 3B — Provider-to-LangChain Mapping

| Provider | LangChain Class | API Key Header | Default Base URL |
|----------|----------------|----------------|------------------|
| OpenRouter | `ChatOpenAI` | `Authorization: Bearer {key}` | `https://openrouter.ai/api/v1` |
| ChatGPT | `ChatOpenAI` | `Authorization: Bearer {key}` | `https://api.openai.com/v1` |
| Anthropic | `ChatAnthropic` | `x-api-key: {key}` | `https://api.anthropic.com/v1` |
| DeepSeek | `ChatDeepSeek` | `Authorization: Bearer {key}` | `https://api.deepseek.com/v1` |
| Ollama | `ChatOllama` | None | `http://localhost:11434` |

### 3C — Instance Instantiation

The orchestrator resolves each `LLMInstanceConfig` to a `BaseChatModel` by matching `instance.provider` against the provider-to-class mapping (§3B). Provider-specific defaults (`base_url`) are applied when not overridden. API keys are decrypted at instantiation time and never persisted in plaintext. The resulting `BaseChatModel` is passed to subgraphs via LangGraph's `context={}` dict — never via state channels — to prevent LLM objects from being serialised into checkpoints.

> **Context-only passing rationale:** LLM objects contain non-serialisable internal state (HTTP clients, connection pools, token counters). Storing them in LangGraph state channels would cause checkpoint serialisation failures and massively inflate checkpoint database sizes. The `context={}` dict is LangGraph's designated mechanism for runtime dependencies that should not be checkpointed.

For RAA (4 LLM instances), all are passed via context:

```python
# Orchestrator invokes RAA with all 4 LLMs in context
context = {
    "llm_raa_a": raa_a_instance,
    "llm_raa_b": raa_b_instance,
    "llm_raa_c": raa_c_instance,
    "llm_judge": raa_judge_instance,
}
```

### 3D — Model List Fetch

When the UI emits `llm_fetch_models_requested`, the orchestrator queries the provider's `/models` endpoint:

| Provider | Endpoint | Auth Header |
|----------|----------|-------------|
| OpenRouter | `{base_url}/models` | `Authorization: Bearer {api_key}` |
| ChatGPT | `{base_url}/models` | `Authorization: Bearer {api_key}` |
| Anthropic | `{base_url}/models` | `x-api-key: {api_key}` |
| DeepSeek | `{base_url}/models` | `Authorization: Bearer {api_key}` |
| Ollama | `{base_url}/api/tags` | None |

Returns `list[str]` of model IDs. Emitted back to UI via `llm_models_fetched` signal.

### 3E — Pre-flight Health Check

Before any pipeline run, the orchestrator pings every LLM instance assigned to the current pipeline. Each instance is checked by sending a minimal chat completion request with `max_tokens=1`.

Per-instance result: `{instance_name: str, reachable: bool, error_message: str | null}`.

If any instance is unreachable, the pipeline is blocked. The full result set is emitted to the UI via `preflight_result` signal. The UI displays a blocking `MessageBox` (see UX&UI_Plan.md §1.3.3 for dialog text).

### 3F — API Key Security

- Keys are encrypted at rest using AES-256-GCM with a key derived from the machine's unique identifier.
- Keys are never logged, never included in checkpoint state, never exposed in error messages.
- LLM objects are passed via LangGraph `context={}` (not state) — see §3C.
- The `api_key_encrypted` field in `llm_registry.db` is NULL for Ollama instances.

---

## 4) Pipeline Execution Engine

### 4A — Execution Sequencing

The orchestrator LangGraph StateGraph executes subgraphs in strict order:

```
START → Ingestion → ARLO → RAA → AGA → SA → RGA → END
```

Each stage is a node in the orchestrator graph. Each node invokes the corresponding subgraph via `subgraph.invoke()` or `subgraph.ainvoke()`.

> **Sync invocation rationale:** Pipeline stages are inherently sequential — each stage consumes the previous stage's output. Synchronous `graph.invoke()` calls within QThread workers keep the code simple. The QThread isolation already prevents UI blocking. See §17 (Open Design Decisions) for the sync-vs-async tradeoff discussion.

**Regeneration loop:** After SA, the orchestrator reads `FeedbackState.should_regenerate` and conditionally re-invokes stages (see §4F).

### 4B — State Threading Map

The orchestrator maps output channels of one subgraph to input channels of the next:

| From | Channel | To | Channel |
|------|---------|----|---------|
| Ingestion | `extracted_requirements` | ARLO | `requirements` |
| Orchestrator | (assembled from UI) | ARLO | `experiment_config` |
| Orchestrator | (loaded from `data/matrix.json`) | ARLO | `matrix` |
| ARLO | `asrs` | RAA | `asrs` |
| ARLO | `non_asr` | RAA | `non_asr` |
| ARLO | `condition_groups` | RAA | `condition_groups` |
| ARLO | `quality_weights` | RAA | `quality_weights` |
| Parent pipeline | `requirements` (original) | RAA | `requirements` |
| Orchestrator | (resolved ChatModel) | RAA | `llm_raa_a/b/c`, `llm_judge` (via context) |
| RAA | `arch_model` (C4JsonModel) | AGA | `arch_model` |
| Orchestrator | (resolved ChatModel) | AGA | LLM (via context) |
| RAA | `arch_model` | SA | `arch_model` |
| AGA | `aga_output` (AGAOutput) | SA | `aga_output` |
| Orchestrator | `requirements_data` (packed dict) | SA | `requirements_data` |
| Orchestrator | `regeneration_threshold` | SA | `regeneration_threshold` |
| Orchestrator | `diagram_accuracy_threshold` | SA | `diagram_accuracy_threshold` |
| SA | `FeedbackState.modified_arch_model` | AGA (on regeneration) | `arch_model` |
| SA | `FeedbackState.targeted_diagrams` | AGA (on regeneration) | `targeted_diagrams` |
| All upstream | All outputs | RGA | All inputs |
| Orchestrator | `pipeline_metadata` | RGA | `pipeline_metadata` |
| Orchestrator | `report_config` | RGA | `report_config` |

**`requirements_data` packing (for SA):** The orchestrator packs a dict containing four keys:
- `requirements` — the original `dict[str, str]` requirement set
- `asrs` — `list[str]` of ASR IDs from ARLO output
- `non_asr` — `list[str]` of non-ASR IDs from ARLO output
- `quality_weights` — `dict[str, int]` from ARLO output

### 4C — Subgraph Invocation Pattern

Each subgraph follows the invocation pattern established by ARLO (`arlo/runner.py`): the orchestrator calls `graph.invoke(state_payload, {"configurable": {"thread_id": thread_id}}, context=context)` with a project-scoped thread ID and context-injected LLM instances.

**Resume detection:** At each stage node, the orchestrator checks for existing state via `graph.get_state(config)`. If a checkpoint exists, it resumes from the last committed node. If not, it starts fresh.

**Wrapper pattern:** Each subgraph stage uses a wrapper function following `arlo/pipeline_wrapper.py`'s pattern: transform orchestrator state to subgraph input schema, invoke, map output back to orchestrator state.

### 4D — Single Active Run Enforcement

The orchestrator tracks active runs in its own state channel `active_run_id`. When a pipeline start is requested:

1. Check `active_run_id`. If non-null, reject with `PipelineAlreadyRunningError`.
2. Set `active_run_id` to the new run ID.
3. Clear `active_run_id` on completion, failure, or cancellation.

The UI's Pipeline Progress Overlay (UX&UI_Plan.md §1.11.3) is the visual enforcement — no interactive widgets remain accessible during execution.

### 4E — Graceful Cancellation Protocol

When the UI emits `pipeline_cancel_requested`:

1. The orchestrator sets a `cancellation_flag` in its context.
2. Subgraph nodes that support cancellation check the flag at batch boundaries (Ingestion RFA batches, ARLO batches, RAA batches).
3. On cancel, the current subgraph persists its checkpoint and returns partial state.
4. The orchestrator skips remaining stages and emits `pipeline_cancelled` to the UI.
5. The UI restores the underlying step view from the overlay.

### 4F — Regeneration Loop

After SA completes, the orchestrator evaluates the `FeedbackState` returned by the scoring agent to determine whether a regeneration cycle is required:

1. Read `should_regenerate` from the SA output's `FeedbackState`.
2. If `structural_gaps_requiring_raa_rerun` is true, re-invoke the pipeline from RAA onwards (RAA → AGA → SA) with the `modified_arch_model` and increment `regeneration_count`.
3. If `structural_gaps_requiring_raa_rerun` is false but `should_regenerate` is true, re-invoke AGA with `targeted_diagrams` from `FeedbackState`, then re-invoke SA, and increment `regeneration_count`.
4. If `regeneration_count` exceeds `MAX_REGENERATION_CYCLES` (2, per SA §16), the orchestrator accepts the current output and logs a warning. No further regeneration is attempted.

> **Cycle cap rationale:** The 2-cycle maximum prevents infinite feedback loops when the scoring agent and architecture generation agent cannot converge on a satisfactory result. The limit is defined in SA §16 and enforced by the orchestrator.

---

## 5) State Schema

### State Channels

| Channel | Type | Reducer | Description |
|---------|------|---------|-------------|
| `project_id` | `str` | overwrite | Active project UUID |
| `project_name` | `str` | overwrite | Active project name |
| `run_id` | `str` | overwrite | Current pipeline run ID. Pattern: `run-{sha256(project_name + utc_timestamp)[:16]}`. |
| `current_stage` | `str` | overwrite | Canonical stage key: `ingestion`, `arlo`, `raa`, `aga`, `sa`, or `rga` |
| `stage_order` | `list[str]` | overwrite | Fixed ordered list: `["ingestion", "arlo", "raa", "aga", "sa", "rga"]` |
| `stage_cursor` | `int` | overwrite | Index into `stage_order`. Advanced by the orchestrator after each stage completes. |
| `llm_assignments` | `dict[str, str]` | overwrite | Map of `{agent_role: instance_name}`. Resolved to `ChatModel` objects at invocation time, never serialised into checkpoints. |
| `extracted_requirements` | `dict[str, str]` | overwrite | From Ingestion → ARLO. Original requirement set keyed by ID. |
| `filter_report` | `dict \| None` | overwrite | From Ingestion → RGA. Filtering metadata and statistics. |
| `arlo_output` | `dict` | overwrite | ARLOOutput: `{asrs, non_asr, condition_groups, quality_weights, concerns, stats}` |
| `raa_output` | `dict` | overwrite | ArchModel / C4JsonModel serialised as dict |
| `aga_output` | `dict` | overwrite | AGAOutput serialised as dict |
| `sa_report` | `dict` | overwrite | SARReport serialised as dict |
| `feedback_state` | `dict \| None` | overwrite | FeedbackState from SA. Evaluated by the regeneration loop (§4F). |
| `user_overrides` | `dict[str, bool]` | overwrite | `{req_id: user_override}` from Requirement Editing UI |
| `stage_timings` | `dict[str, float]` | overwrite | `{stage: wall_clock_seconds}`. Populated as each stage completes. |
| `batch_timings` | `dict[str, list[float]]` | overwrite | `{stage: [last_5_batch_durations]}`. Sliding window for ETA calculation. |
| `active_run_id` | `str \| None` | overwrite | Currently executing run ID. Null = idle. Gates against concurrent starts (§4D). |
| `cancellation_requested` | `bool` | overwrite | Set by cancel signal handler (§4E). Checked by subgraph nodes at batch boundaries. |
| `regeneration_count` | `int` | overwrite | Current regeneration cycle count. Capped at `MAX_REGENERATION_CYCLES` (2, per SA §16). |
| `last_error` | `PipelineError \| None` | overwrite | Most recent pipeline error. See PipelineError type definition below. |
| `preflight_results` | `list[dict]` | overwrite | `[{name, passed, message}]` from pre-flight validation (§9). |

> **LLM injection note:** LLM instances are **not stored in state channels**. They are passed to subgraphs via LangGraph's `context={}` dict at invocation time (see §3C). This follows the mandate that LLM objects must never be serialised into checkpoint state.

> **Reducer note:** All channels in the orchestrator StateGraph use the default `overwrite` reducer. Since each stage node is a single writer in its super-step (no parallel fan-out within the orchestrator graph itself), no append or dict-merge reducers are required. The orchestrator invokes subgraphs sequentially, not in parallel.

### State Channel Type Definitions

**`PipelineError`** — error signal payload emitted to UI on pipeline faults.

| Field | Type | Description |
|-------|------|-------------|
| `severity` | `str` | One of: `warning`, `error`, `fatal` |
| `source_agent` | `str` | Which agent produced the error: `ingestion`, `arlo`, `raa`, `aga`, `sa`, `rga`, `orchestrator` |
| `error_type` | `str` | Exception class name |
| `message` | `str` | Human-readable description |
| `recoverable` | `bool` | Can the pipeline continue from this error? |

**`ProjectConfig`** — configuration for a single project entry.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | User-provided project name |
| `created_at` | `str` | ISO 8601 UTC creation timestamp |
| `document_path` | `str \| None` | Path to uploaded requirement document |
| `document_format` | `str \| None` | One of: `pdf`, `docx`, `txt`, `json` |
| `status` | `str` | One of: `active`, `archived`, `error` |

**`PipelineRunConfig`** — configuration for a single pipeline execution.

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | `str` | Unique run identifier (see §7A) |
| `project_id` | `str` | Owning project UUID |
| `llm_assignments` | `dict[str, str]` | `{agent_role: instance_name}` for this run |
| `filter_config` | `dict \| None` | FilterConfig serialised |
| `experiment_config` | `dict` | ARLO ExperimentConfig serialised |
| `batch_ordering_strategy` | `str` | One of: `risk_first`, `asr_count`, `quality_weight` |
| `aga_config` | `dict` | `{max_retries, plantuml_server_url}` |
| `regeneration_threshold` | `float` | SA regeneration threshold (default 80.0) |
| `diagram_accuracy_threshold` | `float` | SA diagram accuracy threshold (default 14.0) |
| `report_config` | `dict` | ReportConfig serialised |

**`LLMInstanceConfig`** — configuration for a single registered LLM instance.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | User-defined unique label |
| `provider` | `str` | One of: `OpenRouter`, `ChatGPT`, `Anthropic`, `DeepSeek`, `Ollama` |
| `model_name` | `str` | e.g., `gpt-4o`, `claude-sonnet-4-6` |
| `api_key_encrypted` | `str \| None` | AES-encrypted key (None for Ollama) |
| `base_url` | `str \| None` | None = provider default |
| `temperature` | `float` | 0.0–1.0 |
| `created_at` | `str` | ISO 8601 UTC |
| `updated_at` | `str` | ISO 8601 UTC |

**`PipelineMetadata`** — assembled after all stages complete; passed to RGA for the final PDF report (see PDF_Reporting.md §4).

| Field | Type | Description |
|-------|------|-------------|
| `pipeline_run_id` | `str` | Run identifier |
| `run_timestamp` | `str` | ISO 8601 UTC start time |
| `pipeline_version` | `str` | Semantic version of the pipeline (e.g., `1.0.0`) |
| `total_wall_clock_seconds` | `float` | Sum of all `stage_timings` values |
| `subgraph_llms` | `dict[str, str]` | `{stage: model_name}` for each stage. RAA combines all 4 models with `/` separator. RGA uses `"N/A (no LLM)"`. |
| `subgraph_timings` | `dict[str, float]` | Per-stage wall-clock durations in seconds |

---

## 6) Timing & Progress

### 6A — Wall-Clock Timing Per Subgraph

The orchestrator records `time.perf_counter()` deltas around each `graph.invoke()` call. Per-stage wall-clock durations are stored in the `stage_timings` state channel.

### 6B — Batch-Level Timing

For batch-oriented subgraphs, progress callbacks report per-batch timing. The orchestrator records the last 5 batch durations in a sliding window stored in `batch_timings`.

### 6C — Rolling ETA Algorithm

```
ETA = remaining_batches × avg(last_5_batch_durations)
```

If fewer than 5 batches completed, use the average of all completed batches. Emitted to UI via stage-specific progress signals after each batch.

### 6D — Progress Percentage Calculation Per Agent

| Agent | Formula |
|-------|---------|
| Ingestion RFA | `completed_batches / total_batches × 100` |
| ARLO | `completed_batches / total_batches × 100` |
| RAA | `(batch_cursor + 1) / len(batch_queue) × 100` |
| AGA | `completed_diagrams / len(diagram_queue) × 100` |
| SA | `completed_nodes / 6 × 100` |
| RGA | Phase-weighted: Validating=10%, Assembling=40%, Rendering=40%, Writing=10% |

### 6E — Overall Pipeline Progress

Weighted progress across all stages. Default weights (calibrated from expected relative durations):

| Stage | Weight |
|-------|--------|
| Ingestion | 0.10 |
| ARLO | 0.20 |
| RAA | 0.35 |
| AGA | 0.15 |
| SA | 0.15 |
| RGA | 0.05 |

Weighted overall progress = `Σ(stage_progress × stage_weight)` for completed stages + `current_stage_progress × current_stage_weight`.

### 6F — PipelineMetadata Assembly for RGA

After all stages complete (or the pipeline halts), the orchestrator assembles a `PipelineMetadata` instance (type definition in §5). The `subgraph_llms` field records model names used per stage — for RAA, all four models are concatenated with `/` separators. The `subgraph_timings` field records per-stage wall-clock seconds. RGA receives this metadata for inclusion in the final PDF report.

---

## 7) Thread ID & Checkpoint Management

### 7A — Pipeline Run ID Generation

Run IDs follow the pattern `run-{sha256(project_name + utc_timestamp)[:16]}`. The hash input concatenates the project name with the current UTC ISO 8601 timestamp, ensuring uniqueness across projects and runs.

### 7B — Per-Subgraph Thread ID Derivation

Each subgraph receives a thread ID derived from the pipeline run ID. This follows the convention in `arlo/pipeline_wrapper.py`: `f"{parent_thread_id}:{stage}"`.

| Subgraph | Thread ID Pattern |
|----------|-------------------|
| Orchestrator | `{run_id}:orchestrator` |
| Ingestion | `{run_id}:ingestion` |
| ARLO | `{run_id}:arlo` |
| RAA | `{run_id}:raa` |
| AGA | `{run_id}:aga` |
| SA | `{run_id}:sa` |
| RGA | `{run_id}:rga` |

> **Collision guarantee:** Because the run ID includes a high-resolution UTC timestamp and is unique per run, and each subgraph appends its stage name, thread ID collisions are impossible across runs.

### 7C — Checkpoint DB Path Convention

All checkpoint databases are project-scoped: `projects/{project_name}/checkpoints/{agent}.db`.

This overrides the agent plans' assumption of a shared `checkpoints/` directory at the project root. The orchestrator passes the project-scoped path when calling each subgraph's `compile_for_production()`. The subgraph module accepts `db_path` as a required parameter with no default, ensuring the orchestrator always provides the correct path.

### 7D — Resume Detection & Offer

At pipeline start, the orchestrator checks `orchestrator_state = orchestrator_graph.get_state(run_config)`. If a snapshot exists and `current_stage` is not `None`:

1. Emit `pipeline_resume_available` signal to UI with the stage name.
2. UI displays a `MessageBox`: *"A partially completed pipeline run was found at stage '{stage}'. Resume from checkpoint?"*
3. If user confirms, invoke the orchestrator graph — LangGraph replays from the last checkpoint.
4. If user declines, generate a new `run_id` and start fresh.

> **Always-ask rationale:** The user may want to restart with different LLM assignments or configuration. Auto-resuming without confirmation risks executing a pipeline with stale settings. The safer default is to always present the choice. See §18 (Open Design Decisions) for the alternative.

### 7E — Checkpoint Lifecycle & Cleanup

- **7-day retention:** Completed run checkpoints are retained for 7 days, then eligible for cleanup.
- **Cleanup job:** A background task in the orchestrator removes expired checkpoint DBs on startup and periodically (every 6 hours).
- **Archive:** Critical runs can be archived to `projects/{name}/checkpoints/archive/{run_id}/` before cleanup.
- **Failed runs:** Checkpoints for incomplete/failed runs are retained indefinitely until the run is completed or explicitly discarded.

---

## 8) SQLite Checkpointing & Crash Recovery

### Purpose

The orchestrator manages long-running pipeline executions spanning multiple subgraphs. If the process is interrupted — kernel OOM kill, power loss, operator error — all in-progress state is lost and the pipeline must restart from scratch. SQLite checkpointing eliminates this cost by persisting the full LangGraph state after every super-step, enabling resumption from the last committed checkpoint.

---

### 8A — Checkpointer Configuration

Use `SqliteSaver` from the `langgraph-checkpoint-sqlite` package. The checkpoint database path follows the project-scoped convention `projects/{project_name}/checkpoints/orchestrator.db`.

Initialize `SqliteSaver` by passing it a `sqlite3` connection. The orchestrator is responsible for creating the `checkpoints/` directory before graph compilation — subgraph modules must not create directories themselves.

---

### 8B — Graph Compilation

Pass the checkpointer at compile time so LangGraph automatically persists state at every super-step boundary. No further instrumentation is required. LangGraph writes a checkpoint after each super-step completes; the checkpoint captures the full `OrchestratorState` channel snapshot at that moment.

---

### 8C — Thread Identity & Run Configuration

Each pipeline execution is identified by a `thread_id`. The thread ID is the key used to retrieve and resume a specific run. The orchestrator uses the thread ID derivation scheme defined in §7B. The thread ID is passed via the `configurable` dict: `{"configurable": {"thread_id": thread_id}}`.

---

### 8D — Entry Point: Fresh Start vs Resume

At process startup, query the checkpointer for an existing state snapshot using `graph.get_state(run_config)` before invoking the graph. If a snapshot exists and its `current_stage` is not `None`, the pipeline resumes from that point — LangGraph replays from the last committed checkpoint, skipping all completed stages. If no snapshot exists or `current_stage` is `None`, the pipeline starts fresh with the initial state.

**Invariant:** `stage_cursor` is the authoritative resume marker. It is advanced by the orchestrator after each stage completes. Because the checkpoint is written after each stage node's super-step commits, a resume will never re-execute an already-completed stage.

---

### 8E — Checkpoint Granularity & What Is Persisted

LangGraph creates a checkpoint at each **super-step boundary**. The orchestrator's critical state channels persisted at each checkpoint are:

| State Channel | Checkpoint Significance |
|---|---|
| `stage_cursor` | Primary resume marker; determines which stage to start from next |
| `current_stage` | Human-readable stage label; used for resume confirmation dialog (§7D) |
| `stage_order` | Fixed ordered list; loaded from checkpoint, not reconstructed |
| `run_id` | Pipeline run identity; must be consistent across resumes |
| `llm_assignments` | `{agent_role: instance_name}` map; preserved so resume uses same models |
| `extracted_requirements` | Ingestion output; downstream stages depend on this |
| `arlo_output` | ARLO output; RAA and SA depend on this |
| `raa_output` | RAA output; AGA, SA, and RGA depend on this |
| `aga_output` | AGA output; SA and RGA depend on this |
| `sa_report` | SA output; RGA depends on this |
| `feedback_state` | Regeneration loop state; determines whether re-invocation is needed |
| `stage_timings` | Cumulative timing data; preserved across resumes |
| `regeneration_count` | Current regeneration cycle count; must not reset on resume |
| `user_overrides` | Requirement editing overrides; must survive crash |
| `last_error` | Most recent error; preserved for post-mortem analysis |
| `preflight_results` | Pre-flight validation results; not re-run on resume |

All channels in `OrchestratorState` are serialised by LangGraph's default serialiser (`JsonPlusSerializer`). Nested dicts (`arlo_output`, `raa_output`, etc.) are handled natively — no custom serialisation annotation is required.

---

### 8F — Checkpoint Lifecycle & Cleanup

**Retention policy:** Completed run checkpoints are retained for 7 days, then eligible for cleanup. A background task in the orchestrator removes expired checkpoint DBs on startup and periodically (every 6 hours).

**Archive:** Critical runs can be archived to `projects/{name}/checkpoints/archive/{run_id}/` before cleanup. The archive operation must occur only after the pipeline has completed and all output artifacts have been written to disk.

**Failed runs:** Checkpoints for incomplete or failed runs are retained indefinitely until the run is completed or explicitly discarded by the operator.

---

### 8G — Failure Mode Coverage

| Failure Mode | Checkpointing Behaviour |
|---|---|
| Process killed mid-stage (inside a subgraph invocation) | The interrupted super-step has not committed a full orchestrator checkpoint. The subgraph's own checkpoint (separate `SqliteSaver` instance at the subgraph level) records its internal progress independently. On resume, the orchestrator replays the current stage node, which checks the subgraph's checkpoint and resumes from the subgraph's last committed state. |
| Process killed after stage completes, before orchestrator checkpoint commits | LangGraph commits the orchestrator checkpoint atomically at the super-step boundary. A kill after the subgraph `invoke()` returns but before the orchestrator node function returns will have the pending write preserved. On resume, the stage is re-invoked; if the subgraph detects its own completed checkpoint, it returns immediately. |
| Process killed during regeneration loop | `regeneration_count` is checkpointed. On resume, the loop continues from the correct cycle count. |
| Checkpoint DB corrupted | LangGraph raises on `get_state`; the orchestrator catches this and falls back to a fresh start with a warning. The corrupt checkpoint is moved to `{path}.corrupt.{timestamp}` for forensic inspection. Never silently discards a corrupt checkpoint without operator acknowledgement. |
| Subgraph checkpoint DB missing but orchestrator checkpoint exists | The orchestrator treats the subgraph checkpoint as absent and invokes the subgraph from scratch. The subgraph's output replaces the missing state channel data. |

---

### 8H — Integration with §13 Failure Modes Register

The checkpointing behaviour directly mitigates the following failure modes in §13:

| Failure Mode (§13) | Mitigation |
|---|---|
| Subgraph invoke hangs indefinitely | Configurable per-stage timeout. On timeout, orchestrator sets cancellation flag. Existing checkpoint preserved for resume. |
| Subgraph returns partial/corrupt output | Output schema validated at each stage boundary. On failure, `PipelineError` emitted; checkpoint not advanced past the failing stage. |
| Checkpoint write fails (disk full) | Catch `sqlite3.OperationalError` at node boundary. Emit `pipeline_error(fatal)`. In-memory state preserved for current run. |
| Process killed mid-pipeline (OOM, timeout, SIGKILL) | SQLite checkpoint persists state after every super-step; resume skips completed stages. |
| `stage_cursor` desync (checkpoint advanced but output not written) | Stage output validation before advancing cursor; if output missing, re-run the stage. |

---

## 9) Pre-flight Checks & Dependency Validation

### 9A — Check Registry Table

| # | Check | Failure Action |
|---|-------|---------------|
| 1 | LLM connectivity | Block pipeline; show per-instance status in UI (UX&UI_Plan.md §1.3.3) |
| 2 | Embedding model exists at `arlo/models/` | Show download dialog (UX&UI_Plan.md §1.11.4) |
| 3 | `planturl` binary exists and is executable | Block pipeline; `BinaryNotExecutableException` (AGA_Plan.md §7) |
| 4 | PlantUML server reachable (HEAD request) | Block pipeline; `ServerUnavailableException` (AGA_Plan.md §11) |
| 5 | WeasyPrint importable and backend functional | Block PDF generation; show install guide (UX&UI_Plan.md §1.11.5) |
| 6 | `data/matrix.json` exists and is valid JSON | Block pipeline; show file-missing error |

### 9B — Embedding Model Check & Download

- ARLO uses FastEmbed with `mixedbread-ai/mxbai-embed-large-v1` (~670 MB).
- Check: verify `arlo/models/` contains the expected model files.
- If missing: emit `embedding_download_needed` signal to UI. UI shows the download dialog (UX&UI_Plan.md §1.11.4).
- If user confirms: run the download (FastEmbed auto-downloads on first use). Emit `embedding_download_complete` on success.
- Pre-download scripts (`download_model.sh`, `download_model.bat`) are provided for offline setup.

### 9C — planturl Binary Check

Verify `tools/planturl/Bin/{os_target}/planturl` exists and is executable. OS detection per AGA_Plan.md §7.

### 9D — PlantUML Server Check

HEAD request to configured PlantUML server URL with 3-second timeout. If unreachable, emit `preflight_result` with failure detail.

### 9E — WeasyPrint System Library Check

Attempt `import weasyprint`. If import fails due to missing system libraries, the error is surfaced when the user triggers PDF generation (not at pipeline start). See UX&UI_Plan.md §1.11.5 for the user-facing dialog.

### 9F — matrix.json Validation

Verify `data/matrix.json` exists, is valid JSON, and has the expected structure (`dict[str, dict[str, int]]`). Load once at orchestrator startup and cache in memory.

---

## 10) UI Communication Contract

### 10A — Signal/Slot Architecture (QThread Workers)

The orchestrator runs pipeline execution on `QThread` workers to keep the UI responsive. Qt signals cross the thread boundary safely: `Qt.AutoConnection` resolves to `Qt.QueuedConnection` when sender and receiver are in different threads.

All orchestrator signals are declared as `Signal(dict)` on a shared `QObject` subclass. `Signal(dict)` is preferred over `Signal(object)` for clarity. The signal payload is always a flat dict with string keys and JSON-serialisable values. No widget references, no LLM objects, no file handles cross the boundary.

```
UI Thread (main)                    Worker Thread (QThread)
================                    ======================
 [User clicks "Run ARLO"]
        │
        ▼
 emit arlo_run_requested ──────────▶ OrchestratorWorker.run_arlo()
                                        │
                                        ├─ Pre-flight checks
                                        ├─ Instantiate LLM
                                        ├─ graph.invoke(...)
                                        │   ├─ per-batch callback → emit arlo_progress
                                        │   └─ ...
                                        ├─ Record timing
                                        └─ emit arlo_complete ──────▶ UI updates ARLO view
```

### 10B — Signals Received from UI

| Signal | Payload | Triggered By |
|--------|---------|-------------|
| `project_create_requested` | `{name: str}` | "New Project" button |
| `project_selected` | `{project_id: str}` | Project card click |
| `llm_instance_saved` | `{instance_config: dict}` | LLM dialog "Save" |
| `llm_instance_deleted` | `{instance_name: str}` | LLM dialog delete button |
| `llm_fetch_models_requested` | `{provider, api_key, base_url}` | "Fetch Models" button |
| `llm_check_connectivity_requested` | `{}` | "Check Connectivity" button |
| `file_uploaded` | `{file_path: str}` | File dialog selection |
| `extraction_requested` | `{filter_config: dict}` | "Extract" button |
| `requirement_overrides_submitted` | `{overrides: list[{req_id, user_override}]}` | Requirement Editing save |
| `arlo_run_requested` | `{experiment_config: dict}` | "Run ARLO" button |
| `raa_run_requested` | `{batch_ordering: str}` | "Run RAA" button |
| `aga_run_requested` | `{aga_config: dict}` | "Run AGA" button |
| `sa_export_requested` | `{export_dir: str}` | "Export SA Artifacts" button |
| `pdf_report_requested` | `{report_config: dict}` | "Save Full PDF Report" button |
| `regenerate_diagrams_requested` | `{}` | "Regenerate Affected Diagrams" button |
| `rerun_raa_requested` | `{}` | "Re-run RAA" button |
| `pipeline_cancel_requested` | `{}` | "Cancel Run" button |
| `download_logs_requested` | `{}` | "Download Logs" button |
| `embedding_download_confirmed` | `{}` | Download dialog "Download & Continue" |

### 10C — Signals Emitted to UI

| Signal | Payload | UI Action |
|--------|---------|-----------|
| `project_created` | `{project_id, name, path}` | Add card to Projects View |
| `project_list_loaded` | `{projects: list[dict]}` | Populate project card list |
| `llm_models_fetched` | `{models: list[str]}` | Populate Model Name ComboBox |
| `llm_connectivity_result` | `{instance_name: str, reachable: bool}` | Update status badge per row |
| `extraction_progress` | `{stage: str, batch: int, total: int, eta_seconds: float}` | Update extraction ProgressBar + label |
| `extraction_complete` | `{filter_report: dict, requirements: dict}` | Populate Requirement Editing TableWidget |
| `arlo_progress` | `{batch: int, total: int, eta_seconds: float}` | Update ARLO ProgressBar |
| `arlo_complete` | `{asrs, quality_weights, concerns, stats}` | Populate ARLO Results Summary |
| `raa_progress` | `{batch: int, total: int, phase: str}` | Update RAA ProgressBar + phase label |
| `raa_complete` | `{model_stats: dict, open_questions: list}` | Populate RAA Results Summary |
| `aga_progress` | `{diagram: int, total: int, current_label: str}` | Update AGA ProgressBar |
| `aga_complete` | `{completed: list, failed: list, session_report: dict}` | Populate Diagram Gallery |
| `sa_progress` | `{node: int, total: int, node_name: str}` | Update SA ProgressBar |
| `sa_complete` | `{sa_report: dict, feedback_state: dict}` | Populate SA Results Display |
| `rga_progress` | `{phase: str}` | Update PDF generation IndeterminateProgressBar + label |
| `rga_complete` | `{pdf_path, page_count, size_bytes, diagrams_embedded}` | Show success InfoBar |
| `pipeline_progress` | `{overall_pct: float, current_agent: str, eta_seconds: float}` | Update Pipeline Progress Overlay |
| `pipeline_error` | `{severity, source_agent, error_type, message, recoverable}` | Show MessageBox (blocking) or InfoBar |
| `pipeline_cancelled` | `{}` | Restore underlying view from overlay |
| `preflight_result` | `{checks: list[{name, passed, message}]}` | Show blocking MessageBox if any check failed |
| `embedding_download_needed` | `{size_mb: int}` | Show embedding download MessageBox |
| `embedding_download_complete` | `{}` | Show success InfoBar, continue pipeline |
| `pipeline_resume_available` | `{stage: str, run_id: str}` | Show resume confirmation dialog |

### 10D — Progress Callback Mechanism

| Subgraph Type | Mechanism | Detail |
|---------------|-----------|--------|
| Batch (Ingestion RFA, ARLO, RAA) | Context-injected callback | Orchestrator injects `progress_callback(batch, total)` via context dict. Each subgraph's batch-processing node calls it after each batch completes. The callback emits the appropriate stage-specific progress signal with ETA computed from the rolling average (§6C). |
| Non-batch (AGA, SA) | LangGraph event streaming | Orchestrator uses `graph.astream_events()` (version `v3`) to intercept node completion events. Each `on_chain_end` event maps to a progress increment. Emitted to UI via stage-specific progress signals. |
| RGA | Phase milestones | RGA emits phase labels (`Validating`, `Assembling`, `Rendering`, `Writing`) at phase boundaries. The orchestrator maps these to the phase-weighted progress formula (§6D). |

> **astream_events v3 note:** Event types in v3 include lifecycle events (`started`, `running`, `completed`, `failed`, `interrupted`). The exact key path for node-completion events must be verified against the installed `langgraph` version.

### 10E — Error Signal Format

Error signals use the `PipelineError` structure (type definition in §5). Severity determines the UI widget:

| Severity | UI Widget | Blocking? |
|----------|-----------|-----------|
| `fatal` | `MessageBox` (customized with `InfoBarIcon.ERROR` in `viewLayout`, "Retry" button text) | Yes |
| `error` | `MessageBox` with `yesButton.setText("Retry")` + cancel button | Yes |
| `warning` | `InfoBar.warning()` | No |

Per UX&UI_Plan.md §1.11.1: all `[WARNING]` and `[STOP]` messages use modal dialogs exclusively. `InfoBar` is reserved for success and informational confirmations.

---

## 11) Error Handling & Propagation

### 11A — Exception Taxonomy (per subgraph)

| Subgraph | Exception | Source | Severity |
|----------|-----------|--------|----------|
| Ingestion | `EmptyFileError` | §7H | error |
| Ingestion | `ExtractionError` | §7H | error |
| Ingestion | `NonStandardJSONError` | §7E | error |
| Ingestion | `FormatMismatchError` | §7H | error |
| Ingestion | `UnsupportedFormatError` | §7H | error |
| Ingestion | `EmptyRequirementsError` | §7H | error |
| AGA | `BinaryNotExecutableException` | §7 | fatal |
| AGA | `ServerUnavailableException` | §11 | fatal |
| AGA | `EncodingException` | §8 | error |
| RGA | `ReportInputError` | §6 Node 1 | error |
| SA | `SACheckpointError` | §8G | fatal |
| All | Checkpoint DB corruption | — | fatal |

### 11B — Fatal vs Recoverable Classification

| Classification | Meaning | Orchestrator Response |
|---------------|---------|----------------------|
| `fatal` | Pipeline cannot continue. Requires operator intervention. | Halt all stages. Emit `pipeline_error`. Persist checkpoint for resume. |
| `error` | Current stage failed but pipeline may be recoverable. | Emit `pipeline_error`. UI shows MessageBox with retry/cancel options. |
| `warning` | Non-blocking issue. | Emit `pipeline_error` as non-blocking `InfoBar.warning()`. Pipeline continues. |

**Recoverable errors (auto-retry within subgraph, invisible to orchestrator):**
- LLM structured output parse failure (retry up to 2 times)
- Transient network error during LLM call (retry with backoff)
- Transient PlantUML server 5xx (retry up to 2 times — AGA §9)

### 11C — Error-to-UI Mapping

| Error | UI Widget | Blocking? |
|-------|-----------|-----------|
| `fatal` severity | `MessageBox` (customized with `InfoBarIcon.ERROR` in `viewLayout`, "Retry" button text) | Yes |
| `error` severity | `MessageBox` with `yesButton.setText("Retry")` + cancel button | Yes |
| `warning` severity | `InfoBar.warning()` | No |
| `error` (non-blocking) | `InfoBar.error()` | No |
| Success / info | `InfoBar.success()` / `InfoBar.info()` | No |

> **MessageBox customization note:** `MessageBox(title, content, parent)` has no built-in severity icon parameter. To add an icon, subclass `MessageBoxBase` and insert an `InfoBarIcon` widget into `viewLayout`. Default button labels are "Yes"/"Cancel" — override via `box.yesButton.setText("Retry")`.

---

## 12) Performance & Cost Profile

| Operation | Complexity | LLM Cost |
|-----------|-----------|----------|
| Project creation | O(1) — directory + registry insert | None |
| LLM instance CRUD | O(1) — registry insert/update/delete | None |
| Model list fetch | O(1) HTTP request per provider | None |
| Pre-flight LLM ping | O(N) where N = assigned instances | 1 token per ping |
| Pipeline stage handoff | O(1) — state dict copy | None |
| Checkpoint write | O(S) where S = state size (~50–500 KB) | None |
| Total orchestrator LLM calls | **0** | **$0** |

All LLM cost is incurred by subgraphs. The orchestrator itself makes zero LLM calls.

---

## 13) Failure Modes & Mitigations

| Risk | Mitigation |
|------|------------|
| Subgraph invoke hangs indefinitely | Configurable per-stage timeout (default: 30 min). On timeout, set cancellation flag and wait for batch boundary. Force-kill QThread if unresponsive. |
| Subgraph returns partial/corrupt output | Validate output schema at each stage boundary. Missing required fields → `PipelineError(error, recoverable=true)`. |
| Checkpoint write fails (disk full) | Catch `sqlite3.OperationalError` at node boundary. Emit `pipeline_error(fatal)`. In-memory state preserved for current run. |
| LLM registry DB corrupted | Fall back to backup (`llm_registry.db.bak`). If both corrupted, start with empty registry and warn user. |
| Project registry DB corrupted | Rebuild from filesystem scan of `projects/` directories. |
| Two pipeline starts requested simultaneously | `active_run_id` gate rejects the second request. |
| Subgraph thread_id collision | Thread IDs include the run ID (unique per run). Collision impossible within a single run. |
| Embedding model download fails (network) | Block pipeline. Emit error. User retries or uses pre-download script. |
| `matrix.json` missing or malformed | Block pipeline at startup. Emit `preflight_result` with failure detail. |
| Process killed mid-pipeline (OOM, timeout, SIGKILL) | SQLite checkpoint (§8) persists state after every super-step; resume skips completed stages. |
| Checkpoint DB unavailable at startup | Fall back to fresh start; emit a `WARNING` log; do not crash. |
| `stage_cursor` desync (checkpoint advanced but output not written) | Stage output validated before advancing cursor; if output missing, re-run the stage. |

---

## 14) Validation & Testing Criteria

### Unit Tests
- `instantiate_llm()` returns correct LangChain class for each provider.
- Thread ID derivation produces stable, deterministic IDs from the same inputs.
- State threading map correctly transforms ARLO output keys to RAA input keys.
- Rolling ETA calculation: 5 durations of [2, 3, 2, 3, 2] → average 2.4s.
- Overall progress: 50% through RAA (weight 0.35) with ARLO done (0.20) = `0.20 + 0.50 × 0.35 = 0.375`.
- Pre-flight check correctly categorizes each dependency (llm, embedding, planturl, plantuml, weasyprint, matrix).
- `requirements_data` packing correctly separates ASR and non-ASR IDs.

### Integration Tests
- End-to-end: create project → assign LLMs → run ingestion → output flows to ARLO input correctly.
- Resume from checkpoint: simulate crash mid-RAA; verify orchestrator resumes from RAA checkpoint.
- Cancel mid-pipeline: verify cancellation flag propagates to batch boundary, partial state persisted.
- Regeneration loop: SA returns `regenerate_diagrams` → AGA re-runs with `targeted_diagrams` → SA re-runs.

### Functional Tests
- Single active run: concurrent start requests rejected.
- Per-project checkpoint isolation: project A's checkpoints never collide with project B's.
- LLM instance deletion with active assignments triggers confirmation and cascading unassignment.
- Pipeline metadata assembly includes all subgraph timings and LLM model names.

---

## 15) Deliverables for Spec Kit

1. **State schema** — all channels, types, reducers, and ownership (§5)
2. **Project registry module** — SQLite schema, CRUD operations, directory lifecycle (§2)
3. **LLM registry module** — instance CRUD, provider mapping, encryption, instantiation (§3)
4. **Pipeline execution engine** — stage sequencing, state threading, subgraph invocation wrappers (§4A–C)
5. **Regeneration loop** — feedback evaluation, conditional re-invocation, cycle cap (§4F)
6. **Timing & progress module** — per-stage timing, batch-level ETA, overall weighted progress (§6)
7. **Checkpoint management** — checkpointer config, resume detection, lifecycle, crash recovery (§7, §8)
8. **Pre-flight validation** — dependency check registry, health checks, user-facing error dialogs (§9)
9. **Signal/slot contracts** — all UI-bound signals with payload schemas (§10)
10. **Error propagation** — exception taxonomy, severity classification, UI mapping (§11)

---

## 16) Project Directory Layout & Resource Bundles

### 16A — Orchestrator Code (`orchestrator/`)

```
orchestrator/
├── __init__.py
├── runner.py                  # Entry point, checkpointer init, graph compilation
├── graph.py                   # Orchestrator StateGraph definition, stage nodes, edge wiring
├── state/
│   ├── __init__.py
│   └── schema.py              # OrchestratorState TypedDict, PipelineError, all config dataclasses
├── nodes/
│   ├── __init__.py
│   ├── ingestion_stage.py     # Ingestion subgraph invocation wrapper
│   ├── arlo_stage.py          # ARLO subgraph invocation wrapper
│   ├── raa_stage.py           # RAA subgraph invocation wrapper
│   ├── aga_stage.py           # AGA subgraph invocation wrapper
│   ├── sa_stage.py            # SA subgraph invocation wrapper
│   └── rga_stage.py           # RGA subgraph invocation wrapper
├── management/
│   ├── __init__.py
│   ├── projects.py            # Project registry (SQLite), directory creation, artifact paths
│   ├── llm_registry.py        # LLM instance CRUD, encryption, instantiation
│   ├── preflight.py           # Pre-flight check orchestration
│   └── logs.py                # Structured logging, log bundling for download
├── signals/
│   ├── __init__.py
│   └── contracts.py           # Signal/slot contract definitions (Qt signal classes)
├── progress/
│   ├── __init__.py
│   ├── eta.py                 # Rolling ETA calculator
│   ├── callbacks.py           # Context-injected progress callbacks per subgraph
│   └── weights.py             # Stage weight configuration for overall progress
└── utils/
    ├── __init__.py
    ├── threading.py           # State key mapping functions (§4B)
    ├── run_id.py              # Run ID and thread ID generators
    └── encryption.py          # AES key encryption/decryption for API keys
```

### 16B — Project Data Layout

```
projects/
├── registry.db
└── {project_name}/
    ├── input/
    ├── output/
    │   ├── ingestion/
    │   ├── arlo/
    │   ├── raa/
    │   ├── aga/
    │   ├── sa/
    │   └── rga/
    ├── checkpoints/
    │   ├── orchestrator.db
    │   ├── ingestion.db
    │   ├── arlo.db
    │   ├── raa_graph.db
    │   ├── aga.db
    │   ├── sa.db
    │   └── rga.db
    └── logs/
```

### 16C — Shared Resources

```
data/
└── matrix.json                # Quality-architecture pattern matrix (loaded by orchestrator, passed to ARLO)

tools/
└── planturl/
    └── Bin/                   # planturl binaries per OS (see AGA_Plan.md §7)

llm_registry.db                # Global LLM instance registry (project-agnostic)
```

### 16D — Authority Direction

```
Orchestrator Spec (this doc) → orchestrator/ code → subgraph invocations
                                    ↑
                        Agent Plans (RAA, AGA, SA, etc.) define subgraph contracts
```

---

## 17) Dependencies

| Package | Purpose | Version Constraint |
|---------|---------|-------------------|
| `langgraph` | Orchestrator StateGraph, checkpoint persistence, Send API | Already in project |
| `langgraph-checkpoint-sqlite` | `SqliteSaver` for checkpoint persistence (`from langgraph.checkpoint.sqlite import SqliteSaver`) | Already in project |
| `langchain-core` | `BaseChatModel` interface, `RunnableConfig` | Already in project |
| `langchain-openai` | `ChatOpenAI` for OpenRouter and ChatGPT providers | Already in project |
| `langchain-anthropic` | `ChatAnthropic` for Anthropic provider | Required |
| `langchain-deepseek` | `ChatDeepSeek` for DeepSeek provider | Required |
| `langchain-ollama` | `ChatOllama` for Ollama provider | Required |
| `pydantic` | Configuration dataclasses | Already in project |
| `cryptography` | AES-256-GCM encryption for API keys | Required |
| `PySide6` | Qt signal/slot types (Signal, QObject, QThread) for UI communication | Required (UI dependency) |

> **Import scope note:** The orchestrator imports `PySide6` only for `QObject`, `Signal`, and `QThread` — it never imports widget classes. The UI layer link is through signal/slot contracts only.

---

## 18) Open Design Decisions

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Should pipeline stage execution be synchronous or async? | (a) Sync `graph.invoke()`, (b) Async `graph.ainvoke()` | **(a) Sync** — simpler; QThread workers handle UI thread isolation. |
| 2 | Should the orchestrator support partial pipeline runs (e.g., ARLO-only for debugging)? | (a) Full pipeline only, (b) Configurable start/end stages | **(b) Configurable** — useful for development and debugging. |
| 3 | Should the orchestrator auto-resume on restart without user prompt? | (a) Always ask, (b) Auto-resume for non-fatal interruptions, (c) Configurable | **(a) Always ask** — safer default; user may want to restart with different config. |
