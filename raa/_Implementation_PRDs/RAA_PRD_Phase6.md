# RAA PRD — Phase 6: Error Handling, Edge Cases & Fallbacks

**Version:** 1.0
**Status:** Draft
**Depends on:** Phase 1 (architecture, SAAM, registry rules), Phase 2 (schemas),
Phase 3 (tech stack, fault tolerance), Phase 4 (prompts, output binding)

---

## 1. Overview

This PRD defines the RAA's error handling policy across eight categories. Each section
states the detection mechanism, the fallback behaviour, and the rationale. LangGraph
provides three composable fault-tolerance primitives — `retry_policy`, `timeout`, and
`error_handler` — applied per-node via `add_node()` or globally via `set_node_defaults()`
(LangGraph fault-tolerance docs, `langgraph>=1.2` in Phase 3 §9.3). The RAA uses all
three, layered as follows:

```
Node attempt → timeout fires? → retry? → retries exhausted? → error_handler? → abort
```

Per-node configuration chosen over graph-wide defaults because the ASR, Non-ASR, and
Judge nodes have meaningfully different failure postures.

---

## 2. LLM Output Validation Failures

### 2.1 Detection

Pydantic validation runs in three layers (Phase 3 §6). Layer 1 (`with_structured_output`)
catches schema mismatches. Layer 2 (`@field_validator`, `@model_validator`) catches
business rule violations: non-PascalCase names (Phase 1 §7.5), missing type suffix,
empty `source_requirements` (Phase 2 §4.1 [VALIDATE]). Layer 3 attempts deterministic
suffix normalisation before Layer 2 rejects.

### 2.2 Policy: Reject and Continue

A proposal that fails validation after all three layers is stripped from the output
list. The remaining valid proposals proceed normally. The failure is logged with the
proposal's `proposed_name`, the validation error message, and the `source_requirements`
it would have addressed. The batch continues — a single bad proposal does not block
the subgraph or the batch.

### 2.3 Rationale

Validation failures are deterministic, not transient. Retrying the LLM call with the
same input would produce the same output (no new information). Feeding the error back
to the LLM as a correction prompt is a future enhancement (deferred to §9). Stripping
the invalid proposal and continuing matches the "simplicity over engineering" principle
(Phase 1 §5 Rule 1): the Judge already handles missing proposals via coverage gaps.

---

## 3. Retry & Fallback Strategy

### 3.1 Detection

Transient failures are detected by exception type at the node boundary. LangGraph's
`default_retry_on` excludes `ValueError`, `TypeError`, and other deterministic errors,
retrying only on network errors, rate limits (429), server errors (5xx), and
`NodeTimeoutError`.

### 3.2 Policy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Max attempts | 5 | Higher than LangGraph default (3) because LLM calls are the dominant cost and transient provider errors (rate limits, 5xx) are the most common failure mode. |
| Backoff factor | 2.0 | Standard exponential backoff. |
| Initial interval | 0.5s | Quick first retry for transient network blips. |
| Max interval | 128s | Cap growth for long provider outages. |
| Jitter | True | Prevent thundering herd on provider recovery. |
| Per-node | Yes | ASR and Non-ASR run in parallel — one's retry loop does not block the other. Judge has its own policy. |
| Configurable at build | Yes | The Orchestrator passes `max_retries` when calling the graph builder. Not in `configurable` at invoke time (LangGraph `RetryPolicy` is set at `add_node()`). Defaults live in `raa/config/defaults.py`. |

### 3.3 Exhaustion Behaviour

When all retries are exhausted, the node's `error_handler` fires. If no handler is
registered, the exception bubbles up. The RAA does not register per-node error handlers
for the subgraph nodes — exhaustion means the provider is unreachable, and there is no
meaningful degraded output an ASR or Non-ASR node could produce without an LLM. The
exception aborts the batch. LangGraph checkpoints the last successful superstep
automatically; the Orchestrator catches the exception and resumes with the same
`thread_id` when the provider is available again.

### 3.4 Rationale

Five retries with exponential backoff gives providers a ~30-second recovery window
before the batch is abandoned. Per-node configuration means a failing ASR node does
not stall the parallel Non-ASR node. Aborting on exhaustion rather than producing
degraded output keeps the registry consistent — a batch that cannot complete SAAM
evaluation must not write partial entities.

---

## 4. Coverage Gap Handling

### 4.1 Detection

SAAM Step 4 (Phase 1 §8.4): the Judge identifies requirements with zero satisfying
entity proposals. A proposal satisfies a requirement if its `responsibilities` and
`description` address the concern in the requirement text (semantic match, not keyword
match). Requirements with no match produce `CoverageGap` records (Phase 2 §8).

### 4.2 Policy: Log and Continue

All coverage gaps — regardless of `scenario_classification` (direct or indirect) — are
recorded and the batch continues to SAAM Step 5. No re-prompting, no escalation within
the batch. Gaps accumulate in `BatchOutput.coverage_gaps` and propagate to
`RAAOutput.coverage_gaps` (Phase 2 §9). The Orchestrator or a post-processing step
may surface gaps for human review.

### 4.3 Rationale

A coverage gap means no existing proposal addresses a requirement. Re-prompting the
subgraph with targeted instruction ("requirement X has no entity, propose one") risks
an infinite loop if the requirement is genuinely unaddressable by the LLM. Recording
the gap and continuing is safe, deterministic, and preserves complete traceability for
post-run review.

---

## 5. Genuine Conflict Escalation

### 5.1 Detection

SAAM Step 5 (Phase 1 §8.4): two or more requirements demand mutually exclusive
behaviours from the same entity. The Judge produces a `ConflictRecord` with
`resolution = "unresolved"` (Phase 2 §8).

### 5.2 Policy: Non-Blocking, Entity Always Survives

**Scenario A — conflict on a new entity.** The entity is registered with a note in its
`description` field flagging the conflicting demands. The `ConflictRecord` is emitted
alongside. Both requirements keep the entity as their satisfying proposal; the conflict
is documented, not resolved.

**Scenario B — conflict on an existing registry entry.** The entity is enriched per
normal merge rules (Phase 1 §7.4 Rule 1, Phase 2 §3.3 merge strategies). A new
`ConflictRecord` is emitted for this batch, referencing the same `entity_name` but
with the new batch's `requirement_ids`.

In both scenarios, `ConflictRecord` entries with `resolution = "unresolved"` propagate
to `RAAOutput.conflicts` (Phase 2 §9). Resolved conflicts (`"asr_wins"`, `"merged"`)
do not propagate — they are recorded in `BatchOutput` but filtered at assembly.

### 5.3 Rationale

Conflicts are informational for human reviewers, not blocking for the pipeline. The
registry is the source of truth for entity identity — refusing to register an entity
because two requirements disagree about its behaviour would lose the entity entirely
and create coverage gaps for both requirements. Registering with a note preserves
traceability and lets human reviewers reconcile the conflict with full context.

---

## 6. Empty Batch Handling

### 6.1 Detection

Three scenarios produce near-empty or fully empty input/output:

| Scenario | Detection |
|----------|-----------|
| Concern batch with zero assigned non-ASRs | `non_asrs` list is empty in `ConcernBatchInput` |
| Foundation batch with no orphan non-ASRs | `non_asrs` list is empty in `FoundationBatchInput` |
| Zero proposals survive SAAM | Judge produces empty `RegistryDelta` and empty C4 descriptions |

### 6.2 Policy: Run Normally

All three scenarios are valid operational states.

- **Zero non-ASRs:** the Non-ASR node receives an empty list, renders the Mustache
  inverted section `{{^non_asrs}}...{{/non_asrs}}` (Phase 4 §3.3), and returns an
  empty proposal list. The batch proceeds with ASR proposals only.
- **Zero orphans:** same behaviour as above. The Foundation Batch still processes
  conditionless ASRs and produces the L1 system context.
- **Zero surviving proposals after SAAM:** the Judge produces a `BatchOutput` with
  empty C4 descriptions, an empty `RegistryDelta` (`new_entries=[]`,
  `enriched_ids=[]`), and any `CoverageGap` or `ConflictRecord` entries that arose
  during evaluation. This is a valid outcome — the registry already contained all
  relevant entities from prior batches.

No batch is skipped. Skipping would require pre-evaluating whether a batch will
produce output, which requires running the LLM — defeating the purpose of skipping.

### 6.3 Rationale

Empty batches are a natural consequence of exclusive non-ASR assignment (Phase 1 §6.4)
and cumulative registry growth. They carry no correctness risk: an empty proposal list
fed to the Judge produces empty output deterministically. The cost is one Judge LLM
call per empty batch — acceptable and simpler than adding skip logic.

---

## 7. Registry Consistency Guards

### 7.1 Detection

The registry module (`raa/registry/registry.py`, Phase 5) enforces invariants on every
write. Three violations are detectable:

| Violation | Rule | Detection point |
|-----------|------|-----------------|
| Overwrite `canonical_name` | Phase 1 §7.4 Rule 1 | `enrich()`: caller attempts to change `canonical_name` on an existing `RegistryEntry` |
| Overwrite `authority` | Phase 1 §7.4 Rule 1 | `enrich()`: caller attempts to change `authority` on an existing `RegistryEntry` |
| Duplicate `ENT-NNN` | Phase 2 §3.3 [MERGE: never] | `register()`: generated `canonical_id` collides with an existing entry |

### 7.2 Policy: Reject Write, Log, Continue

The offending write is rejected — the registry entry is not modified. The violation is
logged with the entity's `canonical_name`, the field that would have been overwritten,
and the batch that attempted the write. The batch continues; other valid writes from
the same Judge invocation proceed normally. The rejected write is recorded in
`BatchOutput` as metadata so the Orchestrator can surface it.

### 7.3 Rationale

These violations indicate a Judge logic error, not bad LLM output — the Judge produces
deterministic registry operations after SAAM completes. Raising an exception would
abort the batch and lose all valid writes alongside the invalid one. Rejecting the
offending write and continuing preserves the registry's integrity while keeping valid
work. The log entry provides an audit trail for debugging the Judge.

---

## 8. Embedding Failures

### 8.1 Detection

FastEmbed (Phase 3 §4) runs before the batch loop. Two failure modes:

- **Model missing or corrupt:** `TextEmbedding(model_name=...)` raises an exception at
  initialisation if the model file is absent, corrupt, or the cache directory is
  unwritable.
- **Runtime embedding failure:** `model.embed(texts)` raises an exception mid-batch
  (unlikely — model is loaded into memory after init — but possible on OOM or
  hardware error).

### 8.2 Policy: Block the Pipeline

The embedding phase is a prerequisite for batch construction. Without group vectors,
non-ASR assignment has no similarity target. The exception is raised immediately —
no fallback heuristic, no default assignment, no retry. The Orchestrator receives the
exception and decides whether to re-run (after fixing the model cache) or abort.

There is no fallback-to-foundation assignment because that would silently degrade the
output quality: all non-ASRs would land in the Foundation Batch, concern batches would
lose their functional context, and the resulting C4 descriptions would be
architecturally incomplete. The Orchestrator must know that the embedding phase failed.

### 8.3 Rationale

FastEmbed is a local, CPU-only library with no network dependency. Model file corruption
is a deployment error, not a transient runtime condition — retrying won't fix it.
Blocking immediately surfaces the problem to the operator rather than producing
degraded output that looks valid but is semantically wrong.

---

## 9. Timeout & Resource Limits

### 9.1 Detection

Per-node timeouts via LangGraph's `timeout=TimeoutPolicy(run_timeout=120)` on each
subgraph and Judge node (`langgraph>=1.2`, Phase 3 §9.3). `NodeTimeoutError` is raised
when the wall-clock limit is exceeded. `NodeTimeoutError` is retryable by default in
LangGraph's `default_retry_on`.

### 9.2 Policy

| Parameter | Value | Scope |
|-----------|-------|-------|
| `run_timeout` | 120 seconds | Per node (ASR, Non-ASR, Judge) |
| `idle_timeout` | Not set | LLM streaming produces continuous progress signals; idle timeout would only catch hung connections after streaming stops, which `run_timeout` already covers |
| Token cap | None | If the rendered Mustache prompt exceeds the model's context window, the LLM call fails with a context-length error. This is a batch-sizing configuration problem, not a runtime error — the Orchestrator must ensure batches fit within the chosen model's context window |
| Pipeline timeout | Orchestrator responsibility | The RAA graph has no global deadline. The Orchestrator may wrap `graph.invoke()` in a caller-side timeout |

On `NodeTimeoutError`: the node's retry policy applies (criterion 3). If all 5 retries
are exhausted, the batch aborts with a checkpoint saved. The 120-second cap resets on
each retry attempt.

### 9.3 Rationale

120 seconds covers typical structured-output LLM calls with headroom for large batches.
A hung LLM connection that survives 5 retries × 120 seconds (10 minutes total) is a
provider outage, not a transient issue — aborting is correct. No token cap keeps the
RAA provider-agnostic: each model has a different context window, and the Orchestrator
controls batch sizing.

---

## 10. Deferred Items

1. **Correction re-prompting** — feeding validation errors back to the LLM for targeted
   correction (alternative to reject-and-continue in §2). Requires per-provider
   re-prompt strategies.
2. **Coverage gap re-prompting** — re-invoking subgraphs with targeted instruction when
   SAAM Step 4 finds a gap. Risk of infinite loops requires a max-re-prompt limit.
3. **Provider fallback chain** — if the primary LLM provider for a role is exhausted,
   automatically trying a secondary provider. Requires multi-model config injection.
4. **Conflict severity levels** — tagging `ConflictRecord` entries with severity
   (blocking vs. informational) so the Orchestrator can prioritise human review.
5. **Per-node idle timeout** — enabling `idle_timeout` once baseline latency data is
   collected from real runs.
6. **Pipeline-level timeout** — a global deadline enforced by the RAA graph itself
   rather than the Orchestrator. Requires a wrapper node or `RunControl` drain.
7. **Token budgeting** — calculating max tokens per batch based on the configured
   model's context window and the expected output size, with truncation strategy for
   oversized registry snapshots.
