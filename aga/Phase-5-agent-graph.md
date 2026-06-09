# Phase 5 — ReAct Agent, Graph Wiring & Error Handling

> **Goal:** Build the core processing loop — the ReAct agent node that generates/encodes/fetches/validates PlantUML per diagram, the output assembly node, and the main `aga_graph.py` StateGraph that wires all nodes together with conditional edges.
>
> **Depends on:** Phase 1 (state schemas), Phase 2 (tools: `encode_plantuml`, `fetch_plantuml_png`), Phase 3 (prompts: `agent_instruction.md`, `code_generation.md`, `error_correction.md`, `prompt_loader.py`), Phase 4 (nodes: `server_guard`, `input_parsing`)
> **Produces:** `aga/nodes/diagram_generation.py`, `aga/nodes/output_assembly.py`, `aga/graphs/aga_graph.py`, `aga/graphs/__init__.py`
> **Test fixture:** `arch_model_test_result-1.json`

---

## 7) LangChain-Native Agentic Architecture

### 7A — LangGraph StateGraph

The AGA is built as a **LangGraph StateGraph** using LangChain-native constructs:

- **StateGraph** with `AGAState` as the state schema
- **SqliteSaver** checkpointer (path from orchestrator)
- **LangChain tools** (`@tool` decorated functions) for `encode_plantuml` and `fetch_plantuml_png`
- **ReAct agent** created via `create_react_agent()` or equivalent LangGraph agent builder
- **LLM** passed via `context={}` dict (never in state channels, per Orchestrator Plan §3C)

### 7B — Graph Topology

```
START
  │
  ▼
[server_guard]          ── HEAD check PlantUML server availability
  │
  ▼
[input_parsing]         ── Parse flat JSON → derive diagram queue
  │
  ▼
[diagram_loop_entry]    ── Pop next diagram from queue
  │
  ▼
[react_agent_node]      ── ReAct agent: generate → encode → fetch → validate
  │                        (self-correction loop up to max_retries)
  ├── success ──▶ [record_success] → [advance_queue]
  └── failure ──▶ [record_failure] → [advance_queue]
                                          │
                              ┌───────────┤
                              ▼           ▼
                    [diagram_loop_entry]  [output_assembly]
                    (more diagrams)       (queue exhausted)
                                          │
                                          ▼
                                         END
```

### 7D — Checkpointing Strategy

- **SqliteSaver** with WAL mode, matching the RAA pattern in `execution_loop.py`
- One checkpoint per completed diagram (not per ReAct step)
- Checkpoint DB path received from orchestrator — no default
- On resume, the `diagram_cursor` determines where to continue

---

## 12) Error Handling & Halt Conditions

| Error Type | Source | Agent Response |
|------------|--------|----------------|
| `ServerUnavailableException` | HEAD check failed | **Halt immediately** — no diagrams attempted |
| `BinaryNotExecutableException` | Binary path check failed | **Halt immediately** at startup |
| `encoding_error` | planturl non-zero exit | Agent inspects stderr, rewrites code, retries |
| `syntax_error` | SVG error text detected | Agent reads error, applies minimal fix, retries |
| `http_error` (4xx) | Server returned 4xx | Agent adjusts code, retries encode step |
| `http_error` (5xx) | Server returned 5xx | 2 submission retries with backoff, then skip |
| Retry limit exhausted | 5 failed attempts | Record failure, proceed to next diagram |

---

## Relevant Validation Criteria (from §15)

### Integration Tests
- End-to-end with `arch_model_test_result-1.json`: agent generates all derivable diagrams
- Syntax error injection → agent corrects and renders on retry
- Server unavailability → agent halts with structured failure report
