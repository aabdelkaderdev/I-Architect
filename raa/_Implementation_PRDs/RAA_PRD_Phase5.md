# RAA PRD — Phase 5: Project Structure & Module Layout

**Version:** 1.0
**Status:** Draft
**Depends on:** Phase 1 (design), Phase 3 (tech stack), Phase 4 (prompts)

---

## 1. Directory Tree

```
raa/
  __init__.py
  main.py                  # Entry point — Orchestrator calls this
  graph.py                 # StateGraph construction, node wiring, compilation
  state.py                 # RAAState TypedDict + config schema
  batch/
    __init__.py
    constructor.py         # Batch list builder, non-ASR assigner
    input_types.py         # ConcernBatchInput, FoundationBatchInput (Phase 2 §7.2)
  subgraphs/
    __init__.py
    asr_node.py            # ASR Subgraph node — LLM call + structured output
    non_asr_node.py        # Non-ASR Subgraph node — LLM call + structured output
    judge_node.py          # Judge node — SAAM steps, registry write, C4 assembly
  registry/
    __init__.py
    registry.py            # Live registry dict + snapshot(), register(), enrich()
    delta.py               # RegistryDelta construction and validation
  schemas/                 # Phase 2 TypedDicts, re-exported for internal use
    __init__.py
    core.py                # C4Level, C4Type, Relationship, EntityVariant, RegistryEntry
    proposals.py           # EntityProposal, JudgedProposal
    c4_descriptions.py     # ActorEntry .. ComponentDescription (L1/L2/L3 schemas)
    batch_io.py            # ASREntry, NonASREntry, DecisionEntry, BatchInput, BatchOutput
    output.py              # CoverageGap, ConflictRecord, RegistrySnapshot, RAAOutput
  prompts/
    asr_subgraph_system.md
    asr_subgraph_user.md
    non_asr_subgraph_system.md
    non_asr_subgraph_user.md
    judge_system.md
    judge_user.md
    naming_convention.md
    examples/
      asr_direct.md
      asr_indirect.md
      non_asr_external.md
      non_asr_user_type.md
      judge_chain.md
  embedding/
    __init__.py
    embedder.py            # FastEmbed wrapper — group vectors + non-ASR assignment
  config/
    __init__.py
    defaults.py            # SIMILARITY_THRESHOLD, checkpoint path, token limits
  utils/
    __init__.py
    naming.py              # PascalCase + suffix validators (Phase 3 §6.3 Layer 2)
    rendering.py           # Mustache template loader + renderer
tests/
  __init__.py
  conftest.py              # Shared fixtures: empty registry, sample ASRs, mock LLM
  test_batch/
    test_constructor.py
    test_input_types.py
  test_subgraphs/
    test_asr_node.py
    test_non_asr_node.py
    test_judge_node.py
  test_registry/
    test_registry.py
    test_delta.py
  test_embedding/
    test_embedder.py
  test_utils/
    test_naming.py
    test_rendering.py
pyproject.toml             # Dependencies + build config (Phase 3 §9.2-9.3)
uv.lock                    # Exact pinned versions
```

### 1.1 Directory Rationale

| Directory | Why it exists |
|-----------|--------------|
| `raa/` | Single Python package — no namespace packages, no `src/` layout. The RAA is a library called by the Orchestrator, not a standalone application. |
| `raa/batch/` | Batch construction is a distinct pre-processing concern. Isolating it prevents the graph and subgraph modules from importing each other circularly. |
| `raa/subgraphs/` | One file per node. Each node is a pure function — no shared mutable state between them beyond the graph state. |
| `raa/registry/` | Registry logic (snapshot, register, enrich) is shared by the Judge and batch constructor. Pulled into its own module to avoid duplication. |
| `raa/schemas/` | Phase 2 TypedDicts in one place. Every other module imports from here. No schema is defined outside this directory. |
| `raa/prompts/` | Mustache `.md` files live on disk, not in Python strings. Separating prompts from code lets non-engineers review and edit them. |
| `raa/embedding/` | Embedding is a pre-batch step with its own dependency (FastEmbed). Isolated to keep the `fastembed` import out of the graph modules. |
| `raa/config/` | Single source of truth for all hardcoded values. No magic numbers in node bodies. |
| `raa/utils/` | Stateless helper functions with no graph or LLM dependency. Pure logic. |
| `tests/` | Mirrors `raa/` one-to-one. `conftest.py` provides shared fixtures so test files don't duplicate setup. |

---

## 2. Module Responsibilities

### `raa/main.py`
Public entry point. Exposes a single function that the Orchestrator calls. Accepts
`RAAInput` (Phase 1 §2) and a `RunnableConfig` with LLM instances (Phase 3 §2.2),
constructs the compiled graph from `raa.graph`, invokes it, and returns `RAAOutput`
(Phase 2 §9). This is the only file the Orchestrator imports.

### `raa/graph.py`
Constructs the `StateGraph` — adds the embedding pre-processing node, the batch loop
(subgraphs + judge), and the assembly node. Registers `RAAConfigSchema` (Phase 3 §2.2)
as the config schema. Compiles with `SqliteSaver` (Phase 3 §8.1). Owns the node wiring
and edge definitions.

### `raa/state.py`
Defines `RAAState` — the internal TypedDict that flows between nodes. This is the
graph's private state, distinct from the Phase 2 I/O schemas which define what crosses
the Orchestrator boundary. Fields include the live `entity_registry`, the current batch
index, accumulated `list[BatchOutput]`, and per-batch working state (`asr_proposals`,
`non_asr_proposals`). Also re-exports `RAAConfigSchema` (Phase 3 §2.2).

### `raa/batch/constructor.py`
Implements the batch construction logic from Phase 1 §6.2-6.4. Calls the embedder to
assign non-ASRs, then builds the ordered batch list: concern batches first, Foundation
Batch last. Produces `list[ConcernBatchInput | FoundationBatchInput]` (Phase 2 §7.2).

### `raa/batch/input_types.py`
Re-exports `ConcernBatchInput`, `FoundationBatchInput`, and the `BatchInput` union type
from the schema definitions (Phase 2 §7.2). Separated from `constructor.py` so tests
can import types without importing the embedder.

### `raa/subgraphs/asr_node.py`
A single LangGraph node function. Renders `asr_subgraph_system.md` and
`asr_subgraph_user.md` Mustache templates (Phase 4 §2), resolves the ASR LLM from
`config["configurable"]` (Phase 3 §2.3), binds it to a Pydantic model wrapping
`list[EntityProposal]` (Phase 2 §4.1), invokes the LLM, and returns the validated
proposals. No registry access beyond reading the snapshot.

### `raa/subgraphs/non_asr_node.py`
Same pattern as `asr_node.py`, but renders the Non-ASR templates (Phase 4 §3), uses
`config["configurable"]["non_asr_llm"]`, and sets `proposing_subgraph = "non_asr"`.
No QA weights or decisions in scope.

### `raa/subgraphs/judge_node.py`
The most complex node. Renders `judge_system.md` and `judge_user.md` (Phase 4 §4),
resolves `config["configurable"]["judge_llm"]`, and executes SAAM steps 1-5 (Phase 1
§8.4). Each SAAM step uses a different `with_structured_output` binding — classification
produces `list[JudgedProposal]` (Phase 2 §4.2), coverage evaluation produces
`list[CoverageGap]` (Phase 2 §8), interaction detection produces `list[ConflictRecord]`
(Phase 2 §8). Post-SAAM: deduplicates, derives relationships with natural keys (Phase 2
§3.1), calls `registry.register()` and `registry.enrich()`, builds `RegistryDelta`
(Phase 2 §7.1), and assembles partial C4 descriptions. Returns the `BatchOutput`
(Phase 2 §7.3) and the updated live registry.

### `raa/registry/registry.py`
Wraps a `dict[str, RegistryEntry]` (keyed by `canonical_id`). Provides `snapshot()`
→ `RegistrySnapshot` (Phase 2 §5, with `deepcopy` per Phase 3 §7.3), `register()`
for new entries (assigns `ENT-NNN`, enforces immutability), `enrich()` for appending
`source_requirements` and merging `variants` (Phase 1 §7.4), and `lookup()` by
`canonical_name`.

### `raa/registry/delta.py`
Constructs and validates `RegistryDelta` records (Phase 2 §7.1). Enforces the
non-overlap constraint: `new_entries` and `enriched_ids` must be disjoint.

### `raa/schemas/`
Five files, each grouping related Phase 2 TypedDicts. No logic — pure type definitions.
Imported by every other module. The split into five files prevents any single file from
becoming a 300-line wall of types.

### `raa/embedding/embedder.py`
Wraps `TextEmbedding` from `fastembed` (Phase 3 §4.2). Exposes `compute_group_vectors()`
and `assign_non_asrs()`. Called once before the batch loop. Returns group vectors as
`dict[int, np.ndarray]` and the non-ASR-to-batch assignment mapping. No graph dependency.

### `raa/config/defaults.py`
Module-level constants: `SIMILARITY_THRESHOLD` (Phase 1 §6.4), default `DB_PATH`
(Phase 3 §7.4), default `THREAD_ID`, token limits per prompt. Values here are
overridable via `configurable` at invocation time — this file holds the fallbacks.

### `raa/utils/naming.py`
Stateless validators: `is_pascal_case()`, `has_correct_suffix(name, c4_type)`,
`normalize_name()` (Phase 3 §6.3 Layer 2 + Layer 3). Used by Pydantic validators
on the output models and optionally as pre-write checks in the registry.

### `raa/utils/rendering.py`
Loads Mustache `.md` files from `raa/prompts/`, renders them with a variables dict
via `langchain_core.utils.mustache` (Phase 4). Caches loaded templates in memory
to avoid repeated disk reads across batches.

---

## 3. Configuration Files

Configuration follows a layered strategy consistent with the config injection pattern
in Phase 3 §2: static defaults live in `raa/config/defaults.py`, overridable runtime
values arrive via `config["configurable"]`.

| Layer | Location | Examples |
|-------|----------|---------|
| Static defaults | `raa/config/defaults.py` | `SIMILARITY_THRESHOLD = 0.65`, `DB_PATH = "./raa_checkpoint.db"` |
| pyproject metadata | `pyproject.toml` | Package name, version, dependency lower bounds (Phase 3 §9.3) |
| Runtime config | `config["configurable"]` | `thread_id`, `db_path`, LLM instances (Phase 3 §2.2) |

No YAML, TOML, or `.env` files beyond `pyproject.toml`. The RAA is a library, not a
deployed service — the Orchestrator owns deployment configuration. Adding a separate
config file would create a second source of truth that the Orchestrator must
coordinate with.

---

## 4. Prompt File Organization

Prompts are stored as Mustache `.md` files under `raa/prompts/` — the exact layout
defined in Phase 4 §8.1. Format is Markdown because Mustache is a superset of plain
text; `.md` extension gives syntax highlighting and preview in editors.

No `.jinja2`, no `.py` string constants, no `.txt`. Rationale:

- **Not `.py`:** prompts in Python strings require escaping quotes and newlines;
  editing them means modifying code. Separating them into `.md` files lets
  non-engineers review and propose prompt changes via PR.
- **Not `.jinja2`:** Mustache is already rendered by `langchain_core.utils.mustache`;
  introducing a second templating engine adds a dependency with no benefit.
- **Not `.txt`:** Markdown gives structure (headings, lists, code blocks) that
  matches how prompts are already formatted in Phase 4 — headings for sections,
  bullets for requirement lists, backtick blocks for output format specs.

The `raa/utils/rendering.py` module loads `.md` files from this directory, caches them,
and renders them with variable dicts. Template files are never imported as Python modules.

---

## 5. Test Structure

```
tests/
  conftest.py
  test_batch/
    test_constructor.py
    test_input_types.py
  test_subgraphs/
    test_asr_node.py
    test_non_asr_node.py
    test_judge_node.py
  test_registry/
    test_registry.py
    test_delta.py
  test_embedding/
    test_embedder.py
  test_utils/
    test_naming.py
    test_rendering.py
```

Tests mirror `raa/` one-to-one. `conftest.py` provides shared fixtures:

- `empty_registry()` — a `RegistrySnapshot` with zero entries (first batch scenario)
- `sample_asrs()` — 3-5 ASREntry dicts with realistic QA labels
- `sample_non_asrs()` — 3-5 NonASREntry dicts
- `sample_proposals()` — a mix of ASR and Non-ASR `EntityProposal` objects
- `mock_llm()` — a `BaseChatModel` fake that returns pre-defined structured output

Naming convention: `test_<module>.py` with `test_<function>()` methods. No `unittest`
classes — pytest functions with fixtures. No integration tests at this level; those
belong in a separate `tests/integration/` directory (deferred to Phase 8).

---

## 6. Entry Point

The Orchestrator imports exactly one function:

```python
from raa.main import run

result = run(input=raa_input, config=config)
# raa_input: RAAInput (Phase 1 §2)
# config: RunnableConfig with configurable keys (Phase 3 §2.2)
# result: RAAOutput (Phase 2 §9)
```

`run()` is the only public API. It:
1. Calls `raa.embedding.embedder` to compute group vectors and assign non-ASRs
2. Calls `raa.batch.constructor` to build the batch list
3. Compiles the graph from `raa.graph` with `SqliteSaver(config["configurable"]["db_path"])`
4. Invokes the graph with the batch list as initial state
5. Returns the `RAAOutput` from the final graph state

No other function or class is imported by the Orchestrator. Internal modules are free
to change signatures as long as `run()` keeps its contract.

---

## 7. Deferred Items

1. **`pyproject.toml` exact contents** — dependency lower bounds are specified in
   Phase 3 §9.3; the full `[project]` metadata (authors, description, license) is
   a project-admin concern, not an RAA design concern.
2. **Integration test directory** — `tests/integration/` for end-to-end batch runs
   with real FastEmbed and a real LLM. Location and scope deferred to Phase 8.
3. **Package publishing config** — whether the RAA is published to PyPI or consumed
   as a git dependency. The `pyproject.toml` structure supports either.
4. **CI pipeline** — linting, type-checking, and test commands. Deferred to
   implementation.
5. **Logging configuration** — where log output goes, format, and level. Phase 7
   covers observability hooks but not the logging framework setup.
