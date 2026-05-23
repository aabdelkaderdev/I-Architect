---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md'
  - '_bmad-output/planning-artifacts/briefs/brief-raa-2026-05-22/brief.md'
  - 'matrix.json'
  - 'raa_module_specification.md'
  - '_bmad-output/brainstorming/brainstorming-session-2026-05-22-170344.md'
authorityOrder:
  - 'PRD + brainstorming sessions (highest — behavioral & design decisions)'
  - 'pyproject.toml (authoritative for all dependency version pins)'
  - 'raa_module_specification.md (reference only — overridden by above on any conflict)'
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-05-22'
project_name: 'raa'
user_name: 'Delatom'
date: '2026-05-22'
---

# Architecture Decision Document — RAA (Requirements Analysis Agent)

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

---

## Project Context Analysis

### Requirements Overview

**Functional Requirements (20 total, 7 feature groups):**
- Phase 1: Input Normalization + SQLite Embedding Cache (FR-1, FR-2)
- Phases 2–3: Centroid-Anchored Batching + Overlap Bridging (FR-3, FR-4)
- Phases 4–5: Coherence Gating + Queue Ordering (FR-5, FR-6)
- Phase 6: Parallel Subgraph Execution (FR-7, FR-8, FR-9)
- Phase 6c: Judge Reconciliation & Deduplication (FR-10, FR-11, FR-12, FR-13)
- Phase 7: Interactive Human Review Gate (FR-14, FR-15, FR-16)
- Phase 8: Final Merge & Residual Pass (FR-17, FR-18, FR-19, FR-20)

**Non-Functional Requirements (derived from PRD + spec):**
- **Reliability**: 100% checkpoint recovery from last completed batch (SM-3), zero silent requirement drops (SM-1)
- **Data Integrity**: Entity deduplication precision < 5% duplicate rate (SM-2), zero CQRS boundary violations (SM-C1)
- **Correctness**: C4 JSON schema validation on every run; strict hierarchy enforcement at all phases
- **Performance**: Embedding computation CPU-only, O(n) per requirement; batch-sized DB queries (not full-corpus)
- **Concurrency**: 3 parallel subgraph writes to SQLite WAL checkpoint without lock contention
- **Determinism**: Merge, deduplication, tree assembly, and manifest generation are deterministic (no LLM involved)

**Scale & Complexity:**
- Primary domain: AI agent pipeline / LangGraph orchestration (pure backend)
- Complexity level: Enterprise — 8 phases, 15 state channels (3 with append-merge reducers), parallel fan-out, interrupt-driven HiL gate
- Estimated architectural components: ~12–15 distinct LangGraph nodes across phases, 3 private subgraphs, 1 orchestrator graph

### Technical Constraints & Dependencies

- **ARLO contract (fixed)**: `non_asr` arrives as `list[str]` (bare IDs) — RAA owns all embedding generation for both ASR and non-ASR requirements
- **FastEmbed model pre-cached**: `mixedbread-ai/mxbai-embed-large-v1` must exist at `../models`; RAA throws explicit exception if absent
- **SQLite WAL mode**: Required for concurrent subgraph writes; checkpointer DB path injected at runtime
- **`matrix.json` (read-only)**: 17 architectural patterns × 8 quality attributes; loaded once at pipeline init, not reloaded mid-run
- **LangGraph channels with append reducers**: `batch_outputs`, `open_questions`, `incoherent_batches` must declare merge reducers to prevent concurrent write data loss
- **No embedding vectors in state**: All 1024-dim vectors stored in SQLite only; state channels remain lean for efficient checkpointing
- **Document authority hierarchy**: PRD + brainstorming sessions override `raa_module_specification.md` on all behavioral/design decisions. `pyproject.toml` overrides spec on all version pins. Known conflict: spec says `review_timeout_seconds = 300 s` auto-resume — **PRD FR-15 wins: interrupt waits indefinitely, no timeout**.
- **Implementation syntax reference**: `docs-langchain` MCP (`mintlify://skills/langchain`) is the canonical reference for LangGraph 1.2.0 / LangChain 1.3.0 API syntax during implementation.

### Cross-Cutting Concerns Identified

1. **Semantic Deduplication** — Cosine similarity thresholds (≥0.80 merge, 0.60–0.80 boundary group) applied identically in Phase 6c (per-batch) and Phase 8 (global pass)
2. **SAAM Scoring** — Used by RAA-A (scenario selection), Judge (fragment ranking), and incoherent batch handling (×0.5 weight multiplier)
3. **C4 Hierarchy Enforcement** — Orphan prevention at subgraph output, Judge merge, and residual pass; violations rerouted to `coverage_gap` open questions
4. **Crash Recovery** — `batch_cursor` advancement must be atomic with Judge's state write; preparation phase skipped if `embeddings_ready = true` in checkpoint
5. **`assumption_flag` Tracking** — Distinguishes human-confirmed (false) from judge-assumed (true) resolutions throughout Phase 7–8; required for audit output
6. **Embedding Cache Validity** — Text-hash check per requirement at every preparation phase; stale hashes trigger selective re-embedding

---

## Starter Template Evaluation

### Primary Technology Domain

Pure Python AI agent pipeline / LangGraph orchestration. RAA is a **module within the I-Architect system** — not a standalone project. It runs in the parent project's shared virtual environment.

### Integration Model

RAA is registered as a discoverable package alongside ARLO in the parent `pyproject.toml`. The `packages.find` entry must include `raa*`:

```toml
[tool.setuptools.packages.find]
include = ["arlo*", "raa*"]
```

No separate venv, no separate dependency file. The parent project at `/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/pyproject.toml` is the single execution environment.

### Selected Starter: Shared Parent `pyproject.toml`

**Rationale:** RAA is a module delivery within a graduation project — single delivery, no ongoing maintenance or compatibility concerns. The parent venv with pinned production-stable versions is the correct and only target environment.

### Authoritative Dependency Versions

All version pins from `/pyproject.toml`. These **override any version references in `raa_module_specification.md`**.

| Package | Pinned Version | RAA Role |
|---|---|---|
| `langgraph` | `==1.2.0` | Core orchestration graph, state channels, interrupt logic |
| `langchain` | `==1.3.0` | LLM wrappers, structured output (`with_structured_output`), chat models |
| `langgraph-checkpoint-sqlite` | `==3.0.3` | WAL-mode SQLite checkpointer for graph state persistence |
| `fastembed` | `==0.8.0` | CPU-only embedding generation (`mxbai-embed-large-v1`, 1024-dim) |
| `pydantic` | `==2.13.0` | Structured LLM output schemas, state channel validation |
| `scikit-learn` | `==1.8.0` | Cosine similarity, nearest-neighbor search, coherence scoring |
| `python-dotenv` | `==1.2.2` | Environment/config loading |
| `chevron` | `==0.14` | Mustache prompt template rendering |
| `pytest` | `>=8.2` | Test runner |
| `pytest-asyncio` | `>=0.25` | Async node/graph unit testing |

> `mip>=1.17` is an ARLO dependency (ILP solver) — not used by RAA.

### Architectural Decisions From Stack

**State Management:** LangGraph `StateGraph` with typed `TypedDict` state channels; concurrent-write channels (`batch_outputs`, `open_questions`, `incoherent_batches`) use `Annotated[list, operator.add]` append-merge reducers.

**Persistence:** `langgraph-checkpoint-sqlite==3.0.3` provides WAL-mode graph state checkpointing. Separate SQLite DBs (managed directly, not via checkpointer) store ASR and non-ASR embedding caches.

**Structured LLM Output:** Pydantic v2 models via `with_structured_output(Model, include_raw=True)` for resilient fallback parsing.

**Subgraph Isolation:** RAA-A, RAA-B, RAA-C implemented as fully encapsulated independent LangGraph instances with private state schemas and separate checkpoint boundaries (Brainstorming Idea #12, #13).

**Testing:** Pytest + `GenericFakeChatModel` (from `langchain_core`) for deterministic, type-safe unit tests. `pytest-asyncio` for async graph invocations.

### Implementation Syntax Reference

The **`docs-langchain` MCP server** (`mintlify://skills/langchain`) is the canonical reference for LangGraph 1.2.0 and LangChain 1.3.0 API syntax. Use this during implementation — it takes priority over web searches or older documentation snippets.

### Project Initialization

No generator or scaffolding step required. First implementation action: add `"raa*"` to `packages.find` in the parent `pyproject.toml` and verify all RAA package imports resolve from the shared venv.

---

## Core Architectural Decisions

### System Boundary Clarification

> **RAA is a subgraph, not a top-level system.** The external Orchestrator (a separate future project) invokes the RAA `StateGraph` as a compiled subgraph, injects ARLO outputs as initial state, and collects `arch_model.json` on completion. The Orchestrator's design is out of scope here — RAA only defines its own graph boundary, inputs, and outputs.

### D1 — Graph & State Schema Design

**Decision:** The main RAA `StateGraph` owns the top-level 15-channel state. RAA-A, RAA-B, and RAA-C are **fully encapsulated, independent `StateGraph` instances** with private `TypedDict` schemas. They receive parent state values mapped into their inputs and return only their `ArchFragment` output — no shared state channels during subgraph execution.

**Pattern (from Brainstorming Idea #12):**
```python
# Each subgraph compiled independently
raa_a_graph = raa_a_builder.compile(checkpointer=raa_a_checkpointer)
raa_b_graph = raa_b_builder.compile(checkpointer=raa_b_checkpointer)
raa_c_graph = raa_c_builder.compile(checkpointer=raa_c_checkpointer)

# Parent maps inputs → subgraph, collects ArchFragment output
```

**Concurrent-write channels** in the parent graph use `Annotated[list, operator.add]` reducers:
- `batch_outputs: Annotated[dict, merge_reducer]`
- `open_questions: Annotated[list, operator.add]`
- `incoherent_batches: Annotated[list, operator.add]`

### D2 — SQLite Embedding DB Layout

**Decision:** Two **separate SQLite files**:
- `asr_embeddings.db` — ASR condition text vectors
- `non_asr_embeddings.db` — Non-ASR description text vectors

Shared schema per file: `(req_id TEXT PRIMARY KEY, embedding BLOB, text_hash TEXT, model_name TEXT)`.
Paths injected by orchestrator at runtime; never hardcoded inside RAA.

### D3 — Embedding DB Access

**Decision:** Abstraction layer — an `EmbeddingCache` class encapsulates all SQLite read/write operations. Nodes never call `sqlite3` directly.

```python
cache = EmbeddingCache(db_path="...", model_name="mixedbread-ai/mxbai-embed-large-v1")
vector = cache.get_or_embed(req_id="R5", text="...")
```

This isolates hash-checking, cache-miss re-embedding, and DB connection management from node logic.

### D4 — LLM Slots

**Decision:** Four independent LLM slots — one per functional role: RAA-A, RAA-B, RAA-C, Judge. No constraints on model identity; the same model may be used for all four or each may differ. LLM assignment is the caller's concern at invocation time, not RAA's.

### D5 — LLM Injection Mechanism

**Decision:** LangGraph standard `RunnableConfig` pattern. LLMs are accessed inside nodes via the `config` parameter:

```python
from langchain_core.runnables import RunnableConfig

def my_node(state: RAAState, config: RunnableConfig) -> dict:
    llm = config["configurable"]["raa_a_llm"]  # injected at graph.invoke() time
    result = llm.with_structured_output(MyModel).invoke(...)
    return {"batch_outputs": ...}
```

Invocation:
```python
graph.invoke(initial_state, config={"configurable": {
    "raa_a_llm": my_llm_a,
    "raa_b_llm": my_llm_b,
    "raa_c_llm": my_llm_c,
    "judge_llm": my_llm_judge,
    "thread_id": run_thread_id
}})
```

### D6 — Parallel Subgraph Dispatch

**Decision:** `asyncio.gather` — the three subgraphs are invoked concurrently as async coroutines:

```python
results = await asyncio.gather(
    raa_a_graph.ainvoke(batch_input_a, config=config_a),
    raa_b_graph.ainvoke(batch_input_b, config=config_b),
    raa_c_graph.ainvoke(batch_input_c, config=config_c),
)
arch_fragment_a, arch_fragment_b, arch_fragment_c = results
```

Each subgraph writes to its own separate SQLite checkpointer (WAL mode), eliminating write contention.

### D7 — Incoherent Batch Fallback Strategy

**Decision:** When `reduced_confidence = True`, only **RAA-A (SAAM-First)** runs — the most conservative strategy, scenario-driven from quality attributes. The 0.5× SAAM weight multiplier is applied by the Judge to all scores from this batch.

### D8 — Human Review Gate Interrupt Mechanism

**Decision:** LangGraph `interrupt()` function (LangGraph 1.x standard API). The interrupt waits **indefinitely** — no timeout, no auto-resume. PRD FR-15 is authoritative; the `review_timeout_seconds` field mentioned in `raa_module_specification.md` is **not implemented**.

```python
from langgraph.types import interrupt

def human_review_gate(state: RAAState) -> dict:
    if state["review_mode"] == "interactive":
        human_answers = interrupt(state["human_review_payload"])  # suspends indefinitely
        return {"human_answers": human_answers}
    return {}  # autonomous pass-through
```

The interrupt payload (surfaced to caller) is the `human_review_payload` channel value.

### D9 — Human Answers Injection (Resume)

**Decision:** Resume via `Command(resume=...)` — the LangGraph 1.x standard pattern confirmed from docs:

```python
from langgraph.types import Command

# Caller resumes the suspended graph:
graph.invoke(
    Command(resume=human_answers_dict),  # becomes the return value of interrupt()
    config={"configurable": {"thread_id": run_thread_id}}
)
```

The value passed to `Command(resume=...)` becomes the return value of `interrupt()` inside the node, eliminating any separate state update step.

---

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**6 conflict areas** identified where AI agents could make different implementation choices. All patterns below are mandatory for any agent working on RAA code.

### Naming Conventions

**Python Code:**
- Modules/packages: `snake_case` (`raa`, `raa.nodes`, `raa.utils`)
- Classes: `PascalCase` (`EmbeddingCache`, `ArchFragment`, `OpenQuestion`)
- Functions/methods: `snake_case` (`get_or_embed`, `build_batch_queue`)
- Constants: `UPPER_SNAKE_CASE` (`DEDUP_MERGE_THRESHOLD = 0.80`)
- Type aliases: `PascalCase` (`RAAState`, `BatchQueue`)

**State channel names:** `snake_case`, matching `TypedDict` field names exactly (`batch_outputs`, `open_questions`, `batch_cursor`)

**LLM config keys:** role-prefixed: `raa_a_llm`, `raa_b_llm`, `raa_c_llm`, `judge_llm`

**Runtime config keys:** `asr_db_path`, `non_asr_db_path`, `checkpoint_db_path`, `output_dir`, `review_mode`

**SQLite files:** `asr_embeddings.db`, `non_asr_embeddings.db`, `raa_checkpoint.db`

**Requirement IDs:** always `str` with `"R"` prefix (e.g., `"R5"`, `"R12"`) — never raw integers inside RAA

### Project Structure (ARLO-Aligned)

*(See the full directory tree in the Project Structure & Boundaries section below)*

**Structural rules:**
- Each node function lives in its own file. No multi-node files.
- `graphs/` returns uncompiled `StateGraph` builders (caller controls checkpointer) — matches ARLO `graphs/core.py` pattern.
- `state/` uses the ARLO three-schema pattern: `schemas.py` (TypedDicts for Input/Output/State), `models.py` (Pydantic BaseModels for LLM outputs), `config.py` (typed dataclass config).

### Prompt Template Standard (Mustache via Chevron)

**Format:** Mustache `.md` files in `prompts/`, rendered at runtime via `chevron.render()`.

**Example:**
```markdown
{{! RAA-A SAAM Analysis Prompt — saam_analysis.md }}
{{! Injected reference excerpts: saam:steps, c4:entity_types }}
Analyze the following batch of requirements using the SAAM five-step evaluation.

**Quality Attributes in scope:**
{{#quality_attributes}}
- **{{name}}**: {{description}} (weight: {{weight}})
{{/quality_attributes}}

**Requirements Batch:**
{{#requirements}}
- [{{id}}] {{description}}
{{/requirements}}

{{#condition_text}}
**Condition context:** {{condition_text}}
{{/condition_text}}

> Output structure is enforced externally via Pydantic structured output.
```

**Loading pattern:**
```python
import chevron
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def load_prompt(template_name: str, context: dict) -> str:
    """Render a mustache prompt template with the given context."""
    template = (PROMPTS_DIR / template_name).read_text()
    return chevron.render(template, context)
```

**Prompt injection policy (spec §7.3):**
- Each LLM node receives **only the reference excerpts relevant to its function** — not the full Skills bundle
- Excerpts are ≤25 words each, paraphrased from `Skills/references/` source documents
- Full source documents are **never** copied into prompts

### Skills Bundle Pattern (Agent Skills Spec)

The `Skills/` directory follows the **LangChain Agent Skills specification**. `SKILL.md` uses YAML frontmatter for progressive disclosure:

```markdown
---
name: raa
description: >-
  Requirements Analysis Agent — analyzes software requirements through
  3 parallel strategies (SAAM-first, Pattern-driven, Entity-driven) to
  generate C4-compliant architecture models with full traceability.
---

# RAA Skill

## Overview
RAA processes batches of requirements through divergent analysis subgraphs
and convergent judge reconciliation to produce a merged C4 architecture model.

## References
The following documents in `references/` provide authoritative domain knowledge:
- `saam.md` — SAAM 5-step evaluation, scoring, tie-breaking, hotspot detection
- `c4.md` — C4 model levels, element types, notation rules, boundary grouping
- `quality_attributes.md` — ISO/IEC 25010 quality attributes
- `entity_extraction.md` — Guidelines for extracting C4 entities
- `relationship_extraction.md` — Guidelines for deriving directed relationships
- `pattern_selection.md` — Guidelines for selecting architectural patterns
- `technology_inference.md` — Guidelines for inferring technology annotations
- `c4_level_mapping.md` — Rules for assigning entities to correct C4 levels
```

`Skills/references/` documents are **design-time authoritative references** (spec §7.2). The `prompts/` files are the **runtime** counterpart containing only the ≤25-word excerpts injected into LLM calls.

### State Schema Pattern (ARLO Three-Schema)

**`state/schemas.py`** — TypedDicts for graph state (matches ARLO `ARLOInput/ARLOOutput/ARLOState`):
```python
from typing import Annotated, Any
from typing_extensions import NotRequired, TypedDict
from operator import add

class RAAInput(TypedDict):
    """Input schema — provided by the orchestrator."""
    requirements: dict[str, str]          # Original requirement ID -> description map
    asrs: list[dict]
    non_asr: list[str]
    condition_groups: list[dict]
    quality_weights: dict[str, int]
    review_mode: str  # "interactive" or "autonomous"

class RAAOutput(TypedDict):
    """Output schema — returned to the orchestrator."""
    arch_model: dict           # Final merged C4 JSON
    open_questions: list[dict] # Unresolved questions
    traceability_manifest: dict

class RAAState(RAAInput, RAAOutput):
    """Full internal state — all intermediate data hidden from callers."""
    # ... all 15 channels including:
    batch_outputs: Annotated[list[dict], add]     # append-merge reducer
    open_questions: Annotated[list[dict], add]     # append-merge reducer
    incoherent_batches: Annotated[list[dict], add] # append-merge reducer
    batch_cursor: int
    embeddings_ready: bool
    # etc.
```

**`state/models.py`** — Pydantic BaseModels for LLM structured output (matches ARLO `models.py`):
```python
from pydantic import BaseModel, Field

class C4Entity(BaseModel):
    """Single C4 entity extracted by a subgraph."""
    id: str
    name: str
    type: str  # "system" | "container" | "component"
    parent_id: str | None = None
    requirement_ids: list[str] = Field(default_factory=list)

class ArchFragment(BaseModel):
    """Output of a single subgraph execution."""
    entities: list[C4Entity]
    relationships: list[dict]
    cross_cutting_candidates: list[dict] = Field(default_factory=list)
    assumption_flags: list[str] = Field(default_factory=list)
```

All Pydantic models use `BaseModel` (not `dataclass`). All LLM calls use `with_structured_output(Model, include_raw=True)`.

**`state/config.py`** — Typed dataclass (matches ARLO `config.py`):
```python
from dataclasses import dataclass

@dataclass
class RAAConfig:
    """Typed representation of runtime configuration."""
    batch_size: int = 10
    coherence_threshold: float = 0.55
    residual_rebatch_pct: float = 0.15
    max_human_retries: int = 3

    @classmethod
    def from_dict(cls, d: dict) -> "RAAConfig":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
```

### Data Format Patterns

**ArchFragment:** always a Pydantic model, flat structure (containers carry `parent_system_id`, components carry `parent_container_id`). Never nested during fragment stage; nesting happens only in the Judge's tree assembly.

**OpenQuestion:** always uses the canonical Pydantic model from `state/models.py`. No ad-hoc dicts.

**Named constants (never magic numbers inline):**
```python
# raa/utils/constants.py
DEDUP_MERGE_THRESHOLD = 0.80
DEDUP_GROUP_THRESHOLD_LOW = 0.60
NON_ASR_SIMILARITY_THRESHOLD = 0.65
COHERENCE_THRESHOLD = 0.55
RESIDUAL_HIGH_THRESHOLD = 0.75
RESIDUAL_MID_LOW = 0.50
RESIDUAL_REBATCH_PCT = 0.15
INFRA_KEYWORDS = ["all", "every", "always", "any"]
MAX_HUMAN_RETRIES = 3
```

### Process Patterns

**Node return type:** always `dict` matching state channel names. Never return the full state.

**Error handling:** Nodes raise exceptions for unrecoverable failures (missing embedding model, corrupt DB). Recoverable structural issues (orphan entities, scope conflicts) produce `OpenQuestion` entries — never exceptions.

**Embedding access:** always via `EmbeddingCache` — never direct `sqlite3` in node code.

**`matrix.json` access:** loaded once at graph construction time by `matrix_loader.py`, passed into subgraph config. Never re-read inside a node.

**LLM structured output:** always `with_structured_output(Model, include_raw=True)` — never parse raw LLM string output manually.

**Testing:** All LLM-dependent nodes tested with `GenericFakeChatModel` returning pre-defined `ArchFragment` JSON. No live LLM calls in unit tests.

### Enforcement Rules

**All AI agents implementing RAA code MUST:**

1. Import shared type definitions from `raa/state/models.py` — never redefine `ArchFragment`, `OpenQuestion`, or `Batch`
2. Use named constants from `raa/utils/constants.py` — never inline similarity floats or threshold values
3. Access LLMs only via `config["configurable"]["<role>_llm"]` — never instantiate LLMs inside nodes
4. Return `dict` from all node functions — never mutate state directly
5. Write tests in `tests/raa/` — never alongside source files
6. Use `chevron.render()` for all prompt templates — never f-string or `.format()` for prompts
7. Follow the three-schema state pattern (`schemas.py` / `models.py` / `config.py`) — never mix TypedDicts with Pydantic in the wrong file
8. Access embeddings only via `EmbeddingCache` — never call `sqlite3` directly in nodes
9. Use `with_structured_output(Model, include_raw=True)` for all LLM calls — never parse raw strings
10. One node function per file in `nodes/` — no multi-node files

### Anti-Patterns

| ❌ Anti-Pattern | ✅ Correct Pattern |
|---|---|
| `similarity > 0.8` inline | `similarity > DEDUP_MERGE_THRESHOLD` |
| `json.loads(llm_response)` | `llm.with_structured_output(Model, include_raw=True)` |
| `sqlite3.connect(...)` in a node | `EmbeddingCache(db_path=...).get_or_embed(...)` |
| `f"Analyze {reqs}..."` prompt | `load_prompt("saam_analysis.md", context)` |
| Pydantic model in `schemas.py` | Pydantic model in `models.py`; TypedDicts in `schemas.py` |
| `return state` from node | `return {"batch_outputs": [...]}` |

---

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
raa/
├── __init__.py
├── graphs/                    # Graph builders (returns uncompiled StateGraph)
│   ├── __init__.py
│   ├── main.py                # build_raa_subgraph() → uncompiled StateGraph
│   └── execution_loop.py      # Batch-level loop with asyncio.gather dispatch
├── nodes/                     # One file per phase node
│   ├── __init__.py
│   ├── preparation.py         # Phase 1: Normalize + embed
│   ├── batch_construction.py  # Phase 2: Centroid-anchored batching
│   ├── overlap_bridging.py    # Phase 3: Bridge items
│   ├── coherence_gate.py      # Phase 4: Coherence scoring
│   ├── batch_queue_ordering.py # Phase 5: Priority queue
│   ├── human_review_gate.py   # Phase 7: interrupt() / pass-through
│   └── final_merge.py         # Phase 8: Tree assembly + residual pass
├── subgraphs/                 # Private subgraph builders
│   ├── __init__.py
│   ├── raa_a.py               # SAAM-First subgraph builder
│   ├── raa_b.py               # Pattern-Driven subgraph builder
│   └── raa_c.py               # Entity-Driven subgraph builder
├── judge/                     # Judge reconciliation logic
│   ├── __init__.py
│   ├── reconcile.py           # Fragment merge + scoring
│   ├── deduplication.py       # Conservative auto-dedup engine
│   └── scoring.py             # SAAM scoring + weight multiplier
├── state/                     # Three-schema pattern (matches ARLO state/)
│   ├── __init__.py
│   ├── schemas.py             # RAAInput, RAAOutput, RAAState TypedDicts
│   ├── models.py              # Pydantic BaseModel for LLM structured outputs
│   └── config.py              # RAAConfig dataclass (typed runtime config)
├── prompts/                   # Runtime prompt templates (mustache .md via chevron)
│   ├── saam_analysis.md       # RAA-A SAAM scenario prompt
│   ├── pattern_matching.md    # RAA-B pattern-driven prompt
│   ├── entity_extraction.md   # RAA-C entity/relationship prompt
│   ├── judge_reconcile.md     # Judge fragment merge prompt
│   ├── judge_residual.md      # Judge residual assessment prompt
│   └── human_review.md        # HiL payload rendering
├── Skills/                    # Design-time skill resource bundle
│   ├── SKILL.md               # Skill definition + metadata frontmatter
│   └── references/            # Authoritative reference documents
│       ├── saam.md            
│       ├── c4.md              
│       ├── quality_attributes.md
│       ├── entity_extraction.md
│       ├── relationship_extraction.md
│       ├── pattern_selection.md
│       ├── technology_inference.md
│       └── c4_level_mapping.md
└── utils/
    ├── __init__.py
    ├── embedding_cache.py     # EmbeddingCache abstraction class
    ├── c4_validator.py        # C4 schema hierarchy enforcement
    ├── matrix_loader.py       # matrix.json loader
    ├── prompt_loader.py       # chevron template renderer
    └── constants.py           # Named thresholds, limits
tests/
└── raa/
    ├── unit/
    └── integration/
```

### Architectural Boundaries

**Graph Boundary (Entry/Exit):**
RAA is a compiled LangGraph subgraph, not a standalone web service. It has no REST API boundaries. Its integration boundary is purely Python function invocation: `graph.invoke(input: RAAInput, config: RunnableConfig) -> RAAOutput`. The external Orchestrator manages the parent workflow.

The Orchestrator must build `RAAInput` explicitly from the original requirements map plus ARLO output channels. `requirements: dict[str, str]` is the authoritative source for requirement descriptions across ASR and Non-ASR records. RAA must not inspect ARLO or parent graph state to recover descriptions; LangGraph subgraph state inspection is a debugging capability with checkpointing/static-discovery constraints, not a runtime data contract.

**Subgraph Boundaries (RAA-A, B, C):**
Strict isolation. Subgraphs do not share state channels with the parent graph. They are passed mapped inputs and they return an `ArchFragment`. They execute concurrently without write-contention.

**Data Boundaries (SQLite):**
RAA is the sole owner of the embedding databases (`asr_embeddings.db`, `non_asr_embeddings.db`) and its checkpointer DB. Paths are injected dynamically via `RunnableConfig` by the orchestrator. The `EmbeddingCache` utility isolates all database read/write logic from the operational nodes.

### Requirements to Structure Mapping

**Core Execution Pipeline (PRD FR-1 to FR-5):**
- FR-1 / FR-2 (Normalization & Embedding): `raa/nodes/preparation.py`
- FR-3 / FR-4 (Centroid Batching & Overlaps): `raa/nodes/batch_construction.py`, `raa/nodes/overlap_bridging.py`
- FR-5 (Execution Loop Routing): `raa/graphs/execution_loop.py`, `raa/nodes/batch_queue_ordering.py`

**Parallel Strategies & Judge (PRD FR-6, FR-7):**
- RAA-A (SAAM-First): `raa/subgraphs/raa_a.py`
- RAA-B (Pattern-Driven): `raa/subgraphs/raa_b.py`
- RAA-C (Entity-Driven): `raa/subgraphs/raa_c.py`
- Judge Reconciliation: `raa/judge/reconcile.py`, `raa/judge/deduplication.py`

**Human Review & Output (PRD FR-14, FR-15, FR-17):**
- FR-14 / FR-15 (Interactive Gate): `raa/nodes/human_review_gate.py`
- FR-17 (Output JSON Merging): `raa/nodes/final_merge.py`

### Integration Points

**Internal Communication:**
Components communicate exclusively via the LangGraph state channels defined in `raa/state/schemas.py`. Concurrent map-reduce outputs (like parallel batch processing) use `Annotated[list, operator.add]` to guarantee thread-safe state accumulation.

**External Dependencies:**
- **LLMs:** Passed dynamically via `RunnableConfig` (e.g. `config["configurable"]["raa_a_llm"]`).
- **Embeddings Computation:** `fastembed` library computes vectors locally via CPU; no external API calls for embeddings.

### File Organization Patterns

**Source Code Organization:**
The structure strictly mirrors the upstream `ARLO` agent format. Separation of concerns is rigidly enforced:
- `state/` handles all I/O definitions.
- `graphs/` handles topological routing and edge definitions.
- `nodes/` handles business logic within a single state transition.
- `prompts/` holds decoupled logic rules.

**Asset Organization:**
All LLM prompts are externalized to `.md` templates in `prompts/` and rendered using `chevron`. All architectural reference rules reside in `Skills/references/` to conform to the LangChain Agent Skills specification for progressive disclosure.
