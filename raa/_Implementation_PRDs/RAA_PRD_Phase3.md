# RAA PRD — Phase 3: Tech Stack & Infrastructure Choices

**Version:** 1.0
**Status:** Draft
**Scope:** Technology selection and infrastructure decisions for the Requirements Analysis Agent.
Covers LLM configuration, framework selection, embedding strategy, vector similarity,
structured output parsing, state management, serialization, and dependency management.
**Depends on:** RAA PRD Phase 1 (high-level design), RAA PRD Phase 2 (schema definitions).

---

## 1. Overview

This document finalises the technology choices that underpin every implementation decision
in the RAA. Each section states the decision, its rationale, and any constraints it imposes
on implementation. Sections do not cover prompt templates, folder structure, error handling,
or method signatures — those are deferred to the mid-level PRD.

Decisions in Phase 2 supersede Phase 1 where they conflict. All schema names, type literals,
and field names used here are consistent with the TypedDicts established in Phase 2.

---

## 2. LLM Configuration Strategy

### 2.1 Decision

LLM instances for the three roles — ASR Subgraph, Non-ASR Subgraph, and Judge — are passed
at graph invocation time via `RunnableConfig.configurable`. They are never injected into
the graph at construction time and never stored in graph state.

### 2.2 Config Schema

```python
from typing import TypedDict
from langchain_core.language_models import BaseChatModel

class RAAConfigSchema(TypedDict, total=False):
    asr_llm:     BaseChatModel
    non_asr_llm: BaseChatModel
    judge_llm:   BaseChatModel
    thread_id:   str        # LangGraph checkpoint namespace
    db_path:     str        # SqliteSaver path, e.g. "./raa_checkpoint.db"
```

`RAAConfigSchema` is passed to `StateGraph` at construction to expose its shape on the
compiled graph. All fields are `total=False` to allow partial configs and config merging,
consistent with how `RunnableConfig` is designed.

### 2.3 Node Pattern

Every node that calls an LLM accepts `config: RunnableConfig` as its second positional
argument and resolves its designated model from `config["configurable"]`.

Each node binds its LLM to a structured output model via `with_structured_output`, called
inside the node body — not at injection time, keeping the output schema binding co-located
with the node logic that depends on it. The ASR and Non-ASR subgraph nodes bind to a
Pydantic model wrapping `list[EntityProposal]` (Phase 2 §4.1). The Judge node uses
separate models per SAAM step, each consuming `EntityProposal` lists and producing
evaluation records (`JudgedProposal`, Phase 2 §4.2). The model is resolved from
`config["configurable"]` — never stored in graph state and never injected at construction
time.

### 2.4 Invocation Pattern

The caller constructs a `config` dict with `configurable` keys for each LLM instance,
`thread_id`, and `db_path`. Model instances are created by the caller using whichever
provider packages the deployment requires — the RAA graph is model-agnostic and consumes
only the `BaseChatModel` interface. Checkpoint fields (`thread_id`, `db_path`) live in
the same `configurable` dict as the LLMs, since both are out-of-band runtime values.
No separate configuration dataclass is needed. See §7.4 for `thread_id` and `db_path`
defaults.

### 2.5 Rationale

Injecting `BaseChatModel` instances at graph construction time (e.g. via a `@dataclass`)
is an anti-pattern in LangGraph. It couples graph construction to specific LLM instances,
prevents per-invocation model swapping without recompilation, and bypasses LangGraph's
native config propagation to subgraphs. `RunnableConfig.configurable` is the designed
mechanism for this: it is out-of-band, propagated automatically to all nodes and subgraphs,
and supports dynamic routing with no graph changes.

---

## 3. Framework Selection

### 3.1 LangGraph

**Decision:** `StateGraph` from LangGraph is the orchestration layer.

The RAA's batch-sequential processing model — run ASR and Non-ASR Subgraphs, collect
`EntityProposal` lists, pass to Judge, write `RegistryEntry` records, advance to next batch
— maps directly onto a `StateGraph`. The state object carries the current batch slice,
the `RegistrySnapshot`, and the accumulated `list[BatchOutput]` across nodes. Sequential
batch execution (concern batches first, Foundation Batch last, per Phase 1 §6.3) is a
deterministic graph with no branching ambiguity. LangGraph also provides the checkpointing
hooks consumed by §7.

### 3.2 LangChain

**Decision:** `BaseChatModel` from `langchain-core` is the LLM abstraction layer.

Every supported LLM — Anthropic, OpenAI, Google, local Ollama models — implements the same
interface. `with_structured_output` binds any `BaseChatModel` to a Pydantic schema in one
call. The RAA uses no other LangChain primitives: no chains, no retrievers, no agents.

### 3.3 Pydantic v2

**Decision:** Pydantic v2 (`pydantic>=2.13.0`) is used for LLM output validation.

The division of responsibility is: LangGraph handles graph state and node sequencing;
LangChain handles the LLM call; Pydantic validates and coerces the structured response
before it reaches the next node. This boundary is clean and each layer does exactly one
job.

Note on naming: the dependency is `pydantic` (plain Pydantic v2), not `pydantic-ai`.
The RAA uses Pydantic's `BaseModel`, `@model_validator`, and `@field_validator` directly.
The `pydantic-ai` package is not required.

### 3.4 Rationale Summary

| Framework     | Role                                    | Why not the alternative            |
|---------------|-----------------------------------------|------------------------------------|
| LangGraph     | Graph orchestration, state, checkpoints | Raw async adds boilerplate, no checkpointing |
| LangChain     | `BaseChatModel` interface + output binding | Provider packages alone lack the abstraction |
| Pydantic v2   | LLM response validation + business rules | TypedDict has no runtime validation |

---

## 4. Embedding Model

### 4.1 Decision

**Library:** `fastembed>=0.8.0`
**Model:** `mixedbread-ai/mxbai-embed-large-v1` (1024-dimensional output)

### 4.2 Two-Phase Embedding Process

The embedding process runs entirely before the batch loop begins. A single `TextEmbedding`
instance is created at module level — no singleton pattern or lazy initialization is needed
since the underlying library caches model files internally.

**Phase A — Condition group vectors (computed once).**

For every condition group where `cluster != -1`, embed all ASR texts in that group in one
batch call, then compute the element-wise mean to produce one representative group vector:

```
group_vectors: dict[int, np.ndarray] — keyed by cluster ID
For each condition_group where cluster != -1:
    texts = [req.text for req in group.requirements]
    vecs  = [v.tolist() for v in model.embed(texts)]
    group_vectors[cluster] = np.mean(vecs, axis=0)
```

Requirement texts are embedded rather than `nominal_condition` strings because requirement
text carries richer semantic signal (Phase 1 §6.4). Group vectors are computed once,
held in memory for the full run, and never recomputed.

**Phase B — Non-ASR vectors (batched, then assigned individually).**

All non-ASR texts are embedded in a single batch call. Assignment then iterates over the
resulting vectors, comparing each against the pre-computed group matrix:

```
na_vecs = [v.tolist() for v in model.embed([n.text for n in non_asrs])]
group_matrix = np.stack(list(group_vectors.values()))

For each (non_asr, vec) in zip(non_asrs, na_vecs):
    scores = cosine_similarity([vec], group_matrix)
    best_idx, best_score = argmax(scores)
    if best_score > SIMILARITY_THRESHOLD:
        assign to cluster_ids[best_idx]
    else:
        assign to foundation batch
```

Batching all non-ASR embeddings into one call eliminates the per-item embedding loop.
Cosine similarity comparison remains one-to-many per non-ASR (see §5 for the vectorized
implementation), which is negligible at typical non-ASR counts.

### 4.3 Rationale

FastEmbed runs locally with no API call overhead — the embedding pass has no LLM dependency
and must complete before any LLM calls begin, so local synchronous inference is the correct
fit. `mxbai-embed-large-v1` is MTEB-competitive at the sentence-similarity task class that
non-ASR assignment requires: distinguishing semantically related but condition-specific
texts. Its 1024-dimension output provides sufficient representational capacity without the
cost of larger models.

---

## 5. Vector Similarity

### 5.1 Decision

`sklearn.metrics.pairwise.cosine_similarity` for all non-ASR batch assignment comparisons.

### 5.2 Implementation

`cosine_similarity` operates on 2D arrays, enabling all N group scores for a single non-ASR
to be computed in one vectorized call by stacking pre-computed group vectors into a matrix
(see Phase B pseudocode in §4.2). No Python loop over groups is needed. The result is an
`(1, N_groups)` array; `.argmax()` finds the best group and `scores[0, best_idx]` extracts
the score for threshold comparison.

### 5.3 Rationale

The similarity computation is one-to-many: one non-ASR vector against N condition group
vectors, where N is the number of non-`-1` condition groups — typically fewer than 20.
FAISS, Annoy, or any approximate nearest-neighbor structure is entirely unwarranted at this
scale. `sklearn.metrics.pairwise.cosine_similarity` is strictly better than
`scipy.spatial.distance.cosine` for this use case: the scipy function is scalar-only and
requires a Python loop. sklearn is already in the dependency manifest, so no additional
import is needed.

---

## 6. Structured Output Parsing

### 6.1 Decision

A three-layer Pydantic validation strategy enforces TypedDict schemas from LLM responses.

### 6.2 Layer 1 — Schema Binding

Each LLM is bound to its output schema via `llm.with_structured_output(TargetModel)`,
called inside the node. This instructs the LLM to produce JSON conforming to the schema via
function-calling or JSON mode depending on the provider. Missing fields, wrong types, and
structural violations are caught here before Python processes the response.

### 6.3 Layer 2 — Model Validators

RAA-specific business rules that JSON Schema cannot express are enforced as
`@model_validator` and `@field_validator` methods on each Pydantic model.

The mandatory validators for `EntityProposal` are:

- `proposed_name` must be PascalCase (no spaces, hyphens, or underscores).
- For `c4_type` values `service | database | gateway | queue | store | external`,
  `proposed_name` must end with the mandatory suffix from Phase 1 §7.5.
- For `c4_type == "actor"`, only PascalCase is enforced — no suffix is required.
- `source_requirements` must be non-empty (traceability invariant, Phase 1 §5 Rule 4).
- `proposing_subgraph` must be `"asr"` or `"non_asr"` — matching the
  `Literal["asr", "non_asr"]` on `EntityProposal` (Phase 2 §4.1).

### 6.4 Layer 3 — Deterministic Normalization

If a name passes the type check but fails the suffix rule (e.g., the LLM outputs
`"Authentication"` instead of `"AuthenticationService"`), a `@field_validator` attempts
a deterministic suffix append before raising a validation error. This is a pragmatic
concession to LLM imperfection: pure rejection requires a retry loop; deterministic
correction is cheaper and fully auditable in the batch output.

### 6.5 Type Boundary

Pydantic `BaseModel` is used for anything that passes through a validator: subgraph
outputs and Judge outputs. `TypedDict` is used at the graph's public input/output surface:
`RAAInput`, `RAAOutput`, `BatchOutput`, `RegistryEntry`, and all C4 description schemas
from Phase 2. The validation layer is entirely internal to the graph.

---

## 7. State Management

### 7.1 Global Entity Registry

The Global Entity Registry lives in the `StateGraph` state as `dict[str, RegistryEntry]`,
keyed by `canonical_id` (e.g. `"ENT-007"`). It is the only mutable cross-batch structure.

### 7.2 Mutability Rules

- **Subgraph nodes:** read-only access via a frozen `RegistrySnapshot` (see §7.3).
- **Judge node:** the sole writer. Applies Phase 1 §7.4 registration rules after SAAM
  evaluation completes. No other node ever touches the live registry.
- **Sequential execution:** because batches are processed sequentially and the Judge is
  the only writer, there are no race conditions and no locking is required.

### 7.3 Snapshot Mechanics

At the start of each batch, before either subgraph node runs, the live registry is frozen:

```python
snapshot = RegistrySnapshot(
    entries=deepcopy(state["entity_registry"]),
    snapshot_after_batch=state.get("last_batch_id", "none"),
)
```

`RegistrySnapshot` is defined in Phase 2 §5 with two fields: `entries` (the frozen dict
keyed by `canonical_id`) and `snapshot_after_batch` (the batch_id of the last batch that
wrote, for audit trail). This snapshot is injected into both subgraph node inputs. The
live `state["entity_registry"]` is only mutated after the Judge completes its write step.
Subgraphs that query the registry always see the pre-batch state.

### 7.4 Checkpoint Configuration

The checkpoint path and thread ID are resolved from `config["configurable"]` at graph
invocation time (see §2.4). Defaults:

| Key         | Default                  | Purpose                                  |
|-------------|--------------------------|------------------------------------------|
| `thread_id` | `"raa_run_default"`      | Namespaces checkpoint sequences          |
| `db_path`   | `"./raa_checkpoint.db"`  | Path to the SQLite checkpoint database   |

Neither value is hardcoded in the graph. Multiple RAA instances or re-runs from a specific
batch are supported by changing `thread_id` at invocation time.

---

## 8. Serialization & Checkpointing

### 8.1 Decision

**Backend:** `langgraph-checkpoint-sqlite` (`SqliteSaver`)
**Granularity:** one checkpoint per batch, written after each Judge node completes.

### 8.2 Format

`SqliteSaver` serializes graph state as JSON blobs keyed by `(thread_id, checkpoint_id)`.
All Phase 2 schemas — `RegistryEntry`, `EntityVariant`, `BatchOutput`, `CoverageGap`,
`ConflictRecord`, and all C4 description schemas (`SystemContextDescription`, `ContainerDescription`, `ComponentDescription`) — contain only strings,
booleans, lists of strings, and nested dicts of the same. No custom serializer is required.

### 8.3 Disaster Recovery

On restart, the graph checks `db_path` for an existing checkpoint under `thread_id`. If
found, it resumes from the last completed batch. This requires that the batch sequence is
deterministic and reproducible from `RAAInput` — which it is, since batch order follows
condition group ordering (Phase 1 §6.3) and `RAAInput` is immutable.

### 8.4 What Is and Is Not Checkpointed

**Checkpointed after each Judge node:**
- The live `entity_registry` as written by that batch's Judge.
- All `BatchOutput` records accumulated so far.
- The current batch index (resume pointer).

**Not checkpointed:**
- The `RegistrySnapshot` for the current batch — ephemeral, reconstructed from the live
  registry at resume time.
- Pre-computed condition group vectors — reconstructed from `RAAInput` embeddings on resume.

### 8.5 Rationale

Per-batch granularity means a crash loses at most one batch of work. Finer granularity
(per-node) would add overhead without proportionate recovery benefit, since LLM calls are
the dominant cost and the most likely failure point. `SqliteSaver` requires no external
service — it is a local file, making it appropriate for the RAA's local batch workload.

---

## 9. Python Version & Dependency Manifest

### 9.1 Python Version

**Minimum: Python 3.11.**

Three concrete features the RAA directly uses justify rejecting 3.10:

- `TypedDict` with `Required` / `NotRequired` — used throughout Phase 2 schemas
  (`ContainerEntry.technology`, `ComponentEntry.technology`, `EntityVariant.technology`,
  `EntityVariant.description_note`, `Relationship.protocol`, `EntityProposal.concern_technology`).
- `match` / `case` structural pattern matching — clean dispatch on
  `batch_type: Literal["concern", "foundation"]` in `BatchOutput`.
- CPython performance improvements relevant to a batch workload with repeated
  `deepcopy` and embedding operations.

### 9.2 Dependency Management

**Tool:** `uv` with `pyproject.toml`.

`uv` is the correct choice for a new project: faster than pip for resolution and
installation, native virtual environment management, and a `uv.lock` file for
reproducible installs. Poetry adds unnecessary complexity (its own resolver and publish
workflow). Plain pip with `requirements.txt` lacks the lockfile hygiene a multi-library
LLM project requires.

**Version pinning policy:**
- `pyproject.toml [project.dependencies]`: minimum lower bounds (e.g. `langgraph>=1.2.0`).
  Avoids constraining downstream consumers if RAA is ever packaged.
- `uv.lock`: exact pinned versions. Guarantees reproducible installs in CI and production.

### 9.3 Dependency Table

```toml
[project]
requires-python = ">=3.11"

[project.dependencies]
langgraph                    = ">=1.2.0"
langchain                    = ">=1.3.0"
langchain-core               = ">=1.4.0"
langgraph-checkpoint-sqlite  = ">=3.0.3"
fastembed                    = ">=0.8.0"
pydantic                     = ">=2.13.0"
scikit-learn                 = ">=1.8.0"
```

| Package                        | Rationale                                                                 |
|--------------------------------|---------------------------------------------------------------------------|
| `langgraph`                    | `StateGraph` orchestration, batch-sequential execution, checkpoint hooks  |
| `langchain`                    | `BaseChatModel` abstraction, `with_structured_output` binding             |
| `langchain-core`               | Shared interfaces; explicit pin prevents transitive version skew          |
| `langgraph-checkpoint-sqlite`  | `SqliteSaver` for per-batch checkpointing and disaster recovery           |
| `fastembed`                    | Local synchronous embedding inference for non-ASR batch assignment        |
| `pydantic`                     | `@model_validator`, `@field_validator` for LLM output validation          |
| `scikit-learn`                 | `cosine_similarity` for non-ASR vector-to-group assignment                |

Provider packages (`langchain-openai`, `langchain-anthropic`, etc.) are not listed.
The Phase 3 specification is model-agnostic; provider packages are a deployment-time
concern documented separately.
