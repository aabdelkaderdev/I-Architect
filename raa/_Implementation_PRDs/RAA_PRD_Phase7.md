# RAA PRD — Phase 7: Connections, Interfaces & Data Flow

**Version:** 1.0
**Status:** Draft
**Depends on:** Phase 1-6

---

## 1. Orchestrator → RAA Interface

### 1.1 Signature

```python
async def run(input: RAAInput, config: RunnableConfig) -> RAAOutput:
```

| Parameter | Type | Source |
|-----------|------|--------|
| `input` | `RAAInput` | Orchestrator (Phase 1 §2) |
| `config` | `RunnableConfig` | Orchestrator constructs with `RAAConfigSchema` keys (Phase 3 §2.2) |
| Returns | `RAAOutput` | Phase 2 §9 |

Async because Phase 3 node timeouts require async nodes (`langgraph>=1.2`). The
Orchestrator awaits the result.

### 1.2 Config Contract

Required `config["configurable"]` keys per `RAAConfigSchema` (Phase 3 §2.2):

| Key | Type | Purpose |
|-----|------|---------|
| `asr_llm` | `BaseChatModel` | ASR Subgraph LLM |
| `non_asr_llm` | `BaseChatModel` | Non-ASR Subgraph LLM |
| `judge_llm` | `BaseChatModel` | Judge LLM |
| `thread_id` | `str` | Checkpoint namespace — the Orchestrator's correlation ID |
| `db_path` | `str` | SqliteSaver database path (Phase 3 §7.4) |

Validation is deferred to LangGraph's compile-time config schema check. `run()` does
not pre-validate keys — missing keys cause graph compilation to fail with a clear error.

### 1.3 Error Contract

`run()` raises standard Python exceptions — no custom error hierarchy. LangGraph
checkpoints the last successful superstep before any exception bubbles up (Phase 6 §3.3).
The Orchestrator catches the exception and may resume by re-invoking with the same
`thread_id`. Error categories the Orchestrator should distinguish:

| Exception source | Typical cause | Recovery |
|-----------------|---------------|----------|
| `NodeTimeoutError` | LLM call exceeded 120s (Phase 6 §9) | Resume with same `thread_id` |
| Provider HTTP errors (5xx, 429) | Retries exhausted (Phase 6 §3) | Resume when provider recovers |
| `EmbeddingError` | FastEmbed model missing (Phase 6 §8, §5.3 below) | Fix model cache, re-run |
| `ValidationError` (Pydantic) | Malformed LLM output after all layers (Phase 6 §2) | Should not bubble — caught internally |

---

## 2. RAA → AGA Interface

`RAAOutput` (Phase 2 §9) is passed directly to AGA with no transformation by the
Orchestrator. AGA receives the full structure:

- `l1_description` — structured prose for the system context diagram
- `l2_descriptions` — one per concern, backbone containers merged in by the assembler
- `l3_descriptions` — not pre-grouped; AGA resolves grouping via `parent_container_id`
  and `concern_id`
- `entity_registry` — full `dict[str, RegistryEntry]` for resolving `canonical_id`
  foreign keys in `Relationship.source_id` and `Relationship.target_id`
- `coverage_gaps` — AGA may use to annotate diagrams with gap markers
- `conflicts` — only `resolution = "unresolved"` entries; AGA may use to flag entities

AGA ignores fields it does not consume. The Orchestrator adds no packaging layer.

---

## 3. Internal Data Flow

### 3.1 Node-by-Node Table

| Step | Node | Input | Output | Write? |
|------|------|-------|--------|--------|
| 0 | `embed` | `RAAInput.condition_groups`, `RAAInput.non_asrs` | `dict[int, np.ndarray]` (group vectors), `list[tuple[NonASREntry, batch_id]]` | No |
| 1 | `construct_batches` | Group vectors, assignments, `RAAInput` | `list[BatchInput]` (Phase 2 §7.2) | No |
| 2a | `asr_node` | `BatchInput`, `config` | `list[EntityProposal]` (Phase 2 §4.1) | No |
| 2b | `non_asr_node` | `BatchInput`, `config` | `list[EntityProposal]` (Phase 2 §4.1) | No |
| 3 | `judge_node` | `asr_proposals`, `non_asr_proposals`, batch requirements, `RegistrySnapshot` (Phase 2 §5), `config` | `BatchOutput` (Phase 2 §7.3), updated `entity_registry` | Yes — registry |
| 4 | `assemble` | All `BatchOutput` records, final `entity_registry` | `RAAOutput` (Phase 2 §9) | No |

Steps 2a and 2b run in parallel within the graph via `add_node()` on both with
edges to the Judge. LangGraph waits for both before executing the Judge — no manual
synchronisation needed.

### 3.2 Data Flow Diagram (per batch)

```
BatchInput
  │
  ├─ [asr_node] ──→ asr_proposals: list[EntityProposal]
  │                    (Pydantic-validated, logging: role, tokens, latency)
  │
  └─ [non_asr_node] ──→ non_asr_proposals: list[EntityProposal]
                         (Pydantic-validated, logging: role, tokens, latency)
       │
       └─→ [judge_node]
              │ SAAM Steps 1-5 (Phase 1 §8.4)
              │   Step 3: list[JudgedProposal] (Phase 2 §4.2)
              │   Step 4: list[CoverageGap] (Phase 2 §8)
              │   Step 5: list[ConflictRecord] (Phase 2 §8)
              │
              ├─→ registry.register() / registry.enrich()
              │     └─→ RegistryDelta (Phase 2 §7.1)
              │
              └─→ ConcernBatchOutput or FoundationBatchOutput
                    (Phase 2 §7.3)
```

Between batches: `RegistrySnapshot` frozen from live `entity_registry` via
`deepcopy` (Phase 3 §7.3). Checkpoint written after each Judge completes
(Phase 3 §8.1). Next batch reads the updated registry.

Foundation batch runs last, producing `SystemContextDescription` (L1) and
backbone `ContainerDescription` (L2). The assembler merges backbone containers
into each concern's L2 description (`append_unique` merge, Phase 2 §6.3).

---

## 4. Registry API Surface

Owner: `raa/registry/registry.py` (Phase 5). Wraps `dict[str, RegistryEntry]`
keyed by `canonical_id`. Write methods are imported only by `judge_node.py` —
no runtime caller check (simpler than guard logic).

### 4.1 `snapshot`

```python
def snapshot(self) -> RegistrySnapshot:
```

**Pre:** registry may be empty (first batch).
**Post:** returns a `RegistrySnapshot` (Phase 2 §5) with `entries` as a `deepcopy`
of the live dict and `snapshot_after_batch` set to the last batch_id written.
**Side effects:** none (read-only). `deepcopy` ensures subgraph mutations to the
snapshot do not affect the live registry.

### 4.2 `register`

```python
def register(self, entry: RegistryEntry) -> None:
```

**Pre:** `entry.canonical_id` is a new `ENT-NNN` not present in the registry.
`entry.canonical_name`, `c4_level`, `c4_type`, `authority`, `description` are set.
**Post:** entry inserted into the live dict keyed by `canonical_id`.
**Side effects:** mutates the live registry.
**Errors:** raises `ValueError` if `canonical_id` already exists (duplicate ENT-NNN
check, Phase 6 §7). Write access is Judge-only by convention — the import is scoped
to `judge_node.py`.

### 4.3 `enrich`

```python
def enrich(self, canonical_id: str, updates: RegistryEntry) -> None:
```

**Pre:** `canonical_id` exists in the registry.
**Post:** `source_requirements` appended (Phase 2 §3.3 `append_unique`).
`variants` merged by `batch_id` key (Phase 2 §3.3 `merge_by_key`).
`description` is never overwritten — Phase 1 §7.4 Rule 1.
**Side effects:** mutates the live registry entry in place.
**Errors:** raises `ValueError` if caller attempts to change `canonical_name` or
`authority` (Phase 6 §7). Rejects the write by exception — the Judge catches it per
Phase 6 §7.2.

### 4.4 `lookup`

```python
def lookup(self, canonical_id: str) -> RegistryEntry | None:
```

**Pre:** none.
**Post:** returns the `RegistryEntry` for the given `canonical_id`, or `None`.
O(1) dict access. Primary lookup method — uses the registry's native key.

```python
def lookup_by_name(self, canonical_name: str) -> RegistryEntry | None:
```

**Pre:** none.
**Post:** returns the `RegistryEntry` whose `canonical_name` matches (string equality,
Phase 1 §11), or `None`. O(n) linear scan — used only when `canonical_id` is unknown.

---

## 5. Embedding Service Interface

Owner: `raa/embedding/embedder.py` (Phase 5). Wraps `TextEmbedding` from `fastembed`
(Phase 3 §4.2). Synchronous — CPU-bound local inference with no network I/O.

### 5.1 `assign_non_asrs`

```python
def assign_non_asrs(
    condition_groups: list[dict],
    non_asrs: list[NonASREntry],
    threshold: float,
) -> tuple[dict[int, np.ndarray], list[tuple[NonASREntry, str]]]:
```

**Input:**
- `condition_groups` — groups with `cluster`, `nominal_condition`, `requirements`
  (list of `{id, text}`)
- `non_asrs` — `list[NonASREntry]` (Phase 2 §7.1)
- `threshold` — `SIMILARITY_THRESHOLD` from `raa/config/defaults.py`

**Process (internal):**
1. Phase A — embed per-group ASR texts, compute `np.mean` → group vectors
2. Phase B — batch-embed all non-ASR texts in one `model.embed()` call
3. For each (non_asr, vec), compute cosine similarity against stacked group matrix
4. Assign to best group if above threshold, else to foundation batch

**Output:**
- `group_vectors` — `dict[int, np.ndarray]` keyed by cluster ID
- `assignments` — `list[tuple[NonASREntry, batch_id]]`, exclusive (one batch per
  non-ASR, Phase 1 §6.4)

**Error contract:** raises `EmbeddingError` if FastEmbed initialisation fails
(model missing/corrupt) or `model.embed()` raises at runtime (Phase 6 §8).
The caller (`raa/batch/constructor.py`) does not catch this — it bubbles to
`run()` and blocks the pipeline.

---

## 6. LLM Call Interface

Shared helper invoked by all three nodes. Owner: defined alongside the graph nodes;
no separate module needed (single function, ~15 lines).

### 6.1 `invoke_llm`

```python
async def invoke_llm(
    config: RunnableConfig,
    llm_key: Literal["asr_llm", "non_asr_llm", "judge_llm"],
    output_model: type[BaseModel],
    system_template: str,
    user_template: str,
    template_vars: dict,
) -> BaseModel:
```

**Input:**
- `config` — the node's `RunnableConfig`, passed through from the graph
- `llm_key` — which LLM to resolve from `config["configurable"]`
- `output_model` — a Pydantic `BaseModel` subclass (e.g. the model wrapping
  `list[EntityProposal]`). Each caller binds its own model.
- `system_template`, `user_template` — Mustache template strings loaded from
  `.md` files by `raa/utils/rendering.py`
- `template_vars` — dict of variables to render into the templates

**Process:**
1. Resolve `llm = config["configurable"][llm_key]`
2. `structured_llm = llm.with_structured_output(output_model)`
3. Render system and user prompts via `langchain_core.utils.mustache`
4. `response = await structured_llm.ainvoke([SystemMessage, HumanMessage])`
5. Return the Pydantic-validated response

**Output:** a validated instance of `output_model`. Validation failures from
`with_structured_output` (Phase 3 §6 Layer 1) or from `@field_validator` (Layer 2)
are handled per Phase 6 §2 (reject-and-continue for proposals, log for all).

**Error contract:** provider errors (HTTP 5xx, rate limits) are caught by
LangGraph's `retry_policy` on the calling node (Phase 6 §3). `NodeTimeoutError`
fires at 120s (Phase 6 §9). Deterministic errors (`ValueError`, `TypeError`) are
not retried — they bubble to the error handler or abort the batch.

---

## 7. Logging & Observability

### 7.1 Correlation

The Orchestrator passes `thread_id` in `config["configurable"]`. This is the
correlation ID for the full RAA run — all log entries include it. Within a run,
`batch_id` (e.g. `"concern_batch_2"`) scopes entries to a specific batch.

### 7.2 Per-LLM-Call Logging

Every `invoke_llm()` call emits one structured JSON line at completion (success
or failure):

```json
{
  "thread_id": "...",
  "batch_id": "concern_batch_2",
  "role": "asr",
  "step": null,
  "input_tokens": 1240,
  "output_tokens": 380,
  "latency_ms": 4200,
  "status": "success",
  "attempt": 2
}
```

Judge calls additionally set `"step": "classify"` (or `"evaluate"`, `"interact"`,
`"post_saam"`) to distinguish SAAM stages within the same node.

Failed attempts before retry log `"status": "retrying"` with the attempt number.
Exhausted attempts log `"status": "failed"` with the exception type.

### 7.3 Batch-Completion Log

After each Judge node completes, one summary line is emitted:

```json
{
  "thread_id": "...",
  "batch_id": "concern_batch_2",
  "batch_type": "concern",
  "asr_proposals": 8,
  "non_asr_proposals": 3,
  "surviving_entities": 7,
  "new_registrations": 4,
  "enrichments": 3,
  "coverage_gaps": 2,
  "conflicts_total": 1,
  "conflicts_unresolved": 0,
  "registry_size": 23
}
```

### 7.4 Boundary Logs

| Boundary | Logged |
|----------|--------|
| `run()` entry | `thread_id`, input summary (N condition groups, M non-ASRs, K concerns) |
| Embedding complete | N group vectors computed, M non-ASRs assigned (T orphans) |
| Batch start | `batch_id`, batch_type, ASR count, non-ASR count |
| Batch end | Batch-completion JSON (see §7.3) |
| Assembly complete | Final registry size, total coverage gaps, total unresolved conflicts |
| `run()` exit | `thread_id`, wall-clock duration, status |

### 7.5 Format

All log output is structured JSON lines (one JSON object per line). This format is
directly ingestible by LangSmith traces and command-line JSON tools (`jq`). Log
output destination (stdout, file, LangSmith callback) is configured at deployment
time — not specified here.

---

## 8. Deferred Items

1. **LangSmith callback integration** — wiring log output to LangSmith traces via
   `LangChainTracer` or a custom callback handler.
2. **Metrics export** — per-batch latency histograms, token usage aggregates for
   cost tracking.
3. **Log level configuration** — suppressing per-LLM-call logs in production while
   keeping batch-completion summaries.
4. **Trace sampling** — logging every LLM call in large runs may produce excessive
   output; sampling at the batch level.
5. **Exception trace context** — attaching the full SAAM state to error logs for
   debugging Judge failures.
