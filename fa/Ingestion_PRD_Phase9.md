# Data Ingestion & Requirement Filtering — Phase 9: LangGraph Wiring & State Schema

## Summary

This phase defines the LangGraph StateGraph that wires all prior phases together: the complete state schema with every channel, the five-node sequential graph with its single conditional branch, how the LLM is injected via runtime context, and the checkpointing setup that enables durable execution and resume-after-crash.

**Depends on:** All prior phases. Every node referenced here is specified in Phases 3–8. Every exception referenced is specified in Phase 1. Every configuration field referenced is specified in Phase 2.

**Required reading before:** Phase 10 (Orchestrator Interface, Directory Layout & Design Principles).

---

## 1. Purpose

The ingestion pipeline is implemented as a standalone LangGraph `StateGraph`. This phase defines the graph's structure — the state channels, nodes, edges, and checkpointing — without repeating the internal behaviour of any node. It is the integration spec.

---

## 2. Graph Topology

The graph is strictly sequential with a single conditional branch after the format router:

```
                         ┌──────────────────────┐
                         │  Node 1: Format       │
                         │  Detection & Routing  │
                         └──────────┬───────────┘
                                    │
                              file_format
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
              ┌──────────┐   ┌──────────┐   ┌──────────┐
              │ PDF      │   │ DOCX     │   │ TXT      │
              │ Extract  │   │ Extract  │   │ Extract  │
              └────┬─────┘   └────┬─────┘   └────┬─────┘
                   │              │              │
                   └──────────────┼──────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
              ┌──────────┐               ┌──────────────┐
              │ JSON     │               │ Node 3:       │
              │ Validate │               │ Normaliser    │
              └────┬─────┘               └──────┬───────┘
                   │                            │
                   │ (compliant:                │
                   │  skip normaliser)          │
                   │                            │
                   └──────────────┬─────────────┘
                                  │
                                  ▼
                         ┌──────────────────────┐
                         │  Node 4: RFA          │
                         │  (Requirement          │
                         │   Filtering Agent)     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Node 5: Output       │
                         │  Assembly             │
                         └──────────────────────┘
```

**Node count:** 5 logical steps, but more physical nodes due to the per-format extractor fan-out (PDF, DOCX, TXT, JSON). The format router uses a conditional edge to route to the correct extractor.

**No branching after the normaliser.** The RFA and Output Assembly are unconditional sequential nodes. No feedback loops, no regeneration, no retry routing.

---

## 3. State Schema

All state channels use default `overwrite` semantics — no custom reducers are needed. Every channel is written once (by the node that owns it) and read by downstream nodes.

### 3.1 State Channels

| Channel | Type | Written By | Read By | Description |
|---------|------|-----------|---------|-------------|
| `raw_file_path` | `str` | Orchestrator | Node 1, all extractors | Absolute path to the uploaded file |
| `file_format` | `str` | Node 1 | Graph conditional edge | Detected format: `"pdf"`, `"docx"`, `"txt"`, or `"json"` |
| `extracted_blocks` | `list[dict]` | PDF/DOCX/TXT extractors | Node 3 (Normaliser) | Raw text blocks. Each dict: `{"text": str, "source_page": int\|null, "source_section": str\|null}` |
| `ingestion_config` | `dict` | Orchestrator | Extractor nodes, Node 3 | Serialised `IngestionConfig` (Phase 2, §3) |
| `filter_config` | `dict` | Orchestrator | Node 4 | Serialised `FilterConfig` (Phase 2, §4) |
| `filter_report` | `dict` or `null` | Node 4 | Orchestrator | Filtering summary report (Phase 8, §7.1). `null` when filtering is bypassed. |
| `extracted_requirements` | `dict[str, str]` | Node 3 (tentative), Node 4 (reduced), or JSON validator (passthrough) | Node 5, Orchestrator | The final clean requirement set. Conforms to the standard format (Phase 1, §5). |

### 3.2 Channels NOT in State

The LLM instance is **not** a state channel. It is passed via LangGraph's runtime `context`:

```python
graph.invoke(input_state, context={"llm": llm_instance})
```

This keeps state serialisable and follows the pattern used by ARLO, RAA, AGA, and SA. The LLM is read from `context` by Node 4 (RFA) only — no other node uses it.

### 3.3 Existing Channels Reused

These channels exist in the broader pipeline state and are passed through by the orchestrator. The ingestion pipeline does not write to them:

| Channel | Purpose |
|---------|---------|
| `requirements` | Target of `extracted_requirements` at the ARLO boundary |
| `experiment_config` | Passed through unchanged |
| `matrix` | Passed through unchanged |

---

## 4. Node Definitions (Summary)

Each node is specified in full in its respective phase. This section provides the wiring reference only.

| Node | Phase | Type | Description |
|------|-------|------|-------------|
| Node 1: Format Detection & Routing | Phase 3 | Deterministic | Validates file, detects format, sets `file_format` |
| Node 2a: PDF Extractor | Phase 4 | Deterministic | Extracts text blocks from PDF |
| Node 2b: DOCX Extractor | Phase 5 | Deterministic | Extracts text blocks from DOCX |
| Node 2c: TXT Extractor | Phase 5 | Deterministic | Extracts text blocks from TXT |
| Node 2d: JSON Validator | Phase 6 | Deterministic | Validates JSON schema; passthrough or error |
| Node 3: Normaliser | Phase 6 | Deterministic | Assigns IDs, deduplicates, filters by length |
| Node 4: RFA | Phase 7, 8 | LLM | Classifies requirements, applies threshold, builds report |
| Node 5: Output Assembly | (this phase) | Deterministic | Validates final output, signals completion |

### Node 5: Output Assembly

Node 5 is the only node specified here rather than in a prior phase. It performs two checks:

1. **Minimum content:** If `extracted_requirements` has zero entries, raise `EmptyRequirementsError`. The pipeline must produce at least one requirement.
2. **Final write:** If the check passes, the `extracted_requirements` value is final. The orchestrator reads this channel and passes it to `ARLOInput.requirements`.

No transformation is performed in this node. It is a validation gate, not a processing step.

---

## 5. Conditional Edge (Format Routing)

After Node 1, a conditional edge reads `file_format` and routes to the correct extractor:

| `file_format` Value | Target Node |
|--------------------|-------------|
| `"pdf"` | PDF Extractor |
| `"docx"` | DOCX Extractor |
| `"txt"` | TXT Extractor |
| `"json"` | JSON Validator |

The conditional edge function is a simple string-to-node mapping — no logic beyond the lookup.

---

## 6. Checkpointing

### 6.1 Purpose

The ingestion pipeline is typically short-lived (seconds for extraction plus LLM calls for filtering). However, for large document sets (~1000+ requirements), the RFA may dispatch many parallel LLM calls. If the process is interrupted mid-filtering, classified batches are lost and the pipeline must restart from scratch. Checkpointing eliminates this cost.

### 6.2 Checkpointer Configuration

The pipeline uses `SqliteSaver` from `langgraph-checkpoint-sqlite`. The checkpoint database path is **provided by the orchestrator at runtime** — the orchestrator passes a project-scoped path when calling the ingestion module's compile function:

```
projects/{project_name}/checkpoints/ingestion.db
```

The ingestion module's compile function accepts `db_path` as a required parameter with no default. This ensures the orchestrator always provides the project-scoped path.

The ingestion module does **not** create or manage the checkpoints directory. Directory creation is the orchestrator's responsibility.

### 6.3 Thread Identity

Each pipeline execution is identified by a `thread_id` derived from the input file path and a timestamp:

```
thread_id = "ing-" + sha256(file_path + timestamp)[:16]
```

The `ing-` prefix distinguishes ingestion checkpoint threads from RAA (`raa-`), AGA, and SA (`sa-`) threads. The thread ID is passed via `{"configurable": {"thread_id": "<computed_id>"}}`.

### 6.4 Resume Semantics

At startup, the graph checks for existing state via `graph.get_state(run_config)`.

- **Snapshot exists and filtering partially completed:** The graph resumes from the last committed checkpoint. LangGraph replays from the last completed node.
- **No snapshot exists:** The graph starts fresh from Node 1.

Extraction and normalisation (Nodes 1–3) are deterministic and cheap to re-run — they are not individually checkpointed beyond the node-level boundary. The RFA (Node 4) is the only expensive step. Each batch classification is wrapped in a LangGraph `@task`-decorated function, which provides finer granularity than node-level checkpointing: if a crash occurs mid-batch within the RFA, completed batches are stored as pending writes and are not re-executed on resume.

### 6.5 Checkpoint Lifecycle

The checkpoint database follows the same retention policy as other agents: retained for 7 days after a completed run, then eligible for cleanup. The orchestrator is responsible for archiving or pruning.

### 6.6 Failure Mode

If the checkpoint database is unavailable at startup (e.g., disk full, permissions error), the pipeline falls back to a fresh start, emits a `WARNING` log, and does not crash. Checkpointing is a durability optimisation, not a correctness requirement.

---

## Phase Complete When...

- The graph topology diagram correctly shows all five logical nodes and the single conditional branch.
- All seven state channels are named, typed, sourced (who writes), and consumed (who reads).
- The LLM injection rule is stated: runtime `context`, never state channels.
- The conditional edge table maps all four `file_format` values to their extractor nodes.
- Node 5 (Output Assembly) is specified with its two validation checks.
- Checkpointing: `SqliteSaver` with orchestrator-provided `db_path` is specified.
- Checkpointing: thread ID derivation formula and `ing-` prefix convention are specified.
- Checkpointing: resume semantics and `@task` granularity for the RFA are specified.
- Checkpointing: the failure mode (DB unavailable → fresh start + warning) is specified.
- No extractor internals, taxonomy criteria, or configuration field definitions are repeated in this file.
