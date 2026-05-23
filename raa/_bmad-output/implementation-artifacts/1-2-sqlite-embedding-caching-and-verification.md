# Story 1.2: SQLite Embedding Caching and Verification

Status: done

## Story

As a Pipeline Engineer,
I want to cache dense vector embeddings for requirements in external SQLite databases,
So that we prevent redundant vector computation and keep LangGraph checkpoints lean.

## Acceptance Criteria

1. **Model existence check fails fast**: Given a runtime-configured `cache_dir` path (`../models` resolving to `/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/models`), when the embedding node initializes FastEmbed for `mixedbread-ai/mxbai-embed-large-v1`, then it must verify the model files exist on disk before attempting embedding computation, and raise `ModelNonExistentException` immediately if they are absent.

2. **ASR embedding cache with text-hash dedup**: Given normalized ASR records with `condition_text` values, when the embedding node processes them, then it must compute a SHA-256 hash of each requirement's text, check the `asr_embeddings.db` SQLite database for a matching `(req_id, text_hash)` entry, skip embedding generation when an up-to-date cached vector exists, and only call FastEmbed for new or modified text.

3. **Non-ASR embedding cache with text-hash dedup**: Given normalized Non-ASR records with `description` text, when the embedding node processes them, then it must apply the same hash-check-skip logic against `non_asr_embeddings.db`.

4. **Vectors stored as binary blobs outside state**: Given newly computed 1024-dimensional embeddings, when the embedding node persists them, then it must store them as binary blobs (`struct.pack` of 1024 float32 values) in the external SQLite databases (`asr_embeddings.db`, `non_asr_embeddings.db`) and must NOT place embedding vectors into any LangGraph state channel.

5. **Embeddings-ready gate set**: When all ASR and Non-ASR embeddings are verified or generated, then the node must set the state channel `embeddings_ready` to `True`, gating downstream batch construction nodes.

6. **DB paths injected at runtime**: Given the orchestrator-provided `RunnableConfig`, when the embedding node initializes, then it must read `asr_db_path` and `non_asr_db_path` from `config["configurable"]` and must never hardcode database file paths.

## Tasks / Subtasks

- [x] Task 1: Create `EmbeddingCache` class (AC: #2, #3, #4)
  - [x] 1.1 Create `raa/utils/embedding_cache.py` with `EmbeddingCache` class
  - [x] 1.2 Implement `__init__(self, db_path: str, model_name: str)` — creates/opens SQLite DB, runs `CREATE TABLE IF NOT EXISTS` with schema `(req_id TEXT PRIMARY KEY, embedding BLOB, text_hash TEXT, model_name TEXT)`
  - [x] 1.3 Implement `get_cached_vector(req_id: str, text_hash: str) -> list[float] | None` — returns deserialized vector if `(req_id, text_hash)` matches, `None` otherwise
  - [x] 1.4 Implement `store_vector(req_id: str, text_hash: str, vector: list[float]) -> None` — serializes 1024 float32 values via `struct.pack('<1024f', *vector)` and upserts into SQLite
  - [x] 1.5 Implement `text_hash(text: str) -> str` static method — returns SHA-256 hex digest

- [x] Task 2: Create `ModelNonExistentException` and model loader (AC: #1)
  - [x] 2.1 Define `ModelNonExistentException(Exception)` — include `cache_dir` and `model_name` in the message
  - [x] 2.2 Decide placement: co-locate in `raa/utils/embedding_cache.py` or separate `raa/utils/exceptions.py`
  - [x] 2.3 Create `_get_embedding_model(cache_dir: str, model_name: str) -> TextEmbedding` function — verifies `cache_dir / "models--mixedbread-ai--mxbai-embed-large-v1"` directory exists, raises `ModelNonExistentException` if absent, initializes `TextEmbedding(model_name=..., cache_dir=...)` with lazy singleton pattern matching ARLO's `arlo/nodes/embedding.py`

- [x] Task 3: Implement `verify_embeddings` node (AC: #1, #2, #3, #4, #5, #6)
  - [x] 3.1 Add `verify_embeddings(state: RAAState, config: RunnableConfig) -> dict` to `raa/nodes/preparation.py`
  - [x] 3.2 Read `asr_db_path`, `non_asr_db_path`, `cache_dir` from `config["configurable"]`
  - [x] 3.3 Initialize two `EmbeddingCache` instances (one per DB) and the shared `TextEmbedding` model
  - [x] 3.4 For each ASR: compute SHA-256 of `condition_text`, check cache, embed on miss, store result
  - [x] 3.5 For each Non-ASR: compute SHA-256 of `description`, check cache, embed on miss, store result
  - [x] 3.6 Return `{"embeddings_ready": True}`

- [x] Task 4: Write unit tests (AC: all)
  - [x] 4.1 Create `tests/raa/unit/test_embedding_cache.py` — test EmbeddingCache in isolation with tempfile SQLite DBs
  - [x] 4.2 Test `text_hash()` determinism and uniqueness for different inputs
  - [x] 4.3 Test `store_vector` + `get_cached_vector` roundtrip (exact float preservation tolerance 1e-6)
  - [x] 4.4 Test `get_cached_vector` returns `None` for missing req_id
  - [x] 4.5 Test `get_cached_vector` returns `None` for mismatched text_hash
  - [x] 4.6 Test upsert behavior (storing same req_id twice updates the row, does not create duplicate)
  - [x] 4.7 Test `ModelNonExistentException` raised when `cache_dir` has no model files
  - [x] 4.8 Test `verify_embeddings` returns `embeddings_ready: True` with empty input lists (no-op case)
  - [x] 4.9 Test `verify_embeddings` with pre-cached vectors (all ASRs and Non-ASRs already in DB → zero FastEmbed calls)
  - [x] 4.10 Test `verify_embeddings` with partial cache (some reqs cached, some new → only new ones embedded)
  - [x] 4.11 Test `verify_embeddings` with all-new requirements (all reqs embedded, all stored)
  - [x] 4.12 Test `verify_embeddings` with stale cache (text_hash mismatch → re-embed)
  - [x] 4.13 Test `verify_embeddings` reads DB paths from `config["configurable"]`

- [x] Task 5: Add embedding-specific constants to `raa/utils/constants.py`
  - [x] 5.1 Add `EMBEDDING_DIM = 1024`
  - [x] 5.2 Add `EMBEDDING_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"`
  - [x] 5.3 Add `EMBEDDING_CACHE_DIR = str(Path(__file__).parent.parent.parent / "models")` as module-level path resolution or document that `cache_dir` comes from config

### Review Findings

- [x] [Review][Patch] _get_embedding_model argument mismatch bug [raa/utils/embedding_cache.py:89]
- [x] [Review][Patch] Context manager support for EmbeddingCache [raa/utils/embedding_cache.py:110]
- [x] [Review][Patch] Dimensionality validation in store_vector [raa/utils/embedding_cache.py:151]
- [x] [Review][Patch] BLOB length validation in get_cached_vector [raa/utils/embedding_cache.py:138]
- [x] [Review][Patch] _get_embedding_model thread-safety [raa/utils/embedding_cache.py:89]
- [x] [Review][Patch] Abstraction boundary crossing in verify_embeddings [raa/nodes/preparation.py:412]
- [x] [Review][Patch] Warn/log on non-string quality attributes [raa/nodes/preparation.py:339]
- [x] [Review][Patch] Test isolation leakage from singleton mutation [tests/raa/unit/test_embedding_cache.py:695]
- [x] [Review][Patch] Tempfile leakage in _temp_db_paths helper [tests/raa/unit/test_embedding_cache.py:542]
- [x] [Review][Patch] sqlite3.connect operational errors [raa/utils/embedding_cache.py:119]
- [x] [Review][Patch] Connection leak on init failure in EmbeddingCache [raa/utils/embedding_cache.py:119]
- [x] [Review][Patch] Locked/full disk transaction rollback on write [raa/utils/embedding_cache.py:151]
- [x] [Review][Patch] Robust config input validation in verify_embeddings [raa/nodes/preparation.py:406]
- [x] [Review][Patch] Connection leak in verify_embeddings when second cache instantiation raises [raa/nodes/preparation.py:413]
- [x] [Review][Patch] Missing check for empty/missing id on records in verify_embeddings [raa/nodes/preparation.py:448]
- [x] [Review][Patch] Incorrect test patch target path in test_empty_inputs_returns_embeddings_ready [tests/raa/unit/test_embedding_cache.py:716]
- [x] [Review][Patch] Spec discrepancy: static method name is compute_hash instead of text_hash [raa/utils/embedding_cache.py:133]
- [x] [Review][Patch] Spec discrepancy: missing EMBEDDING_CACHE_DIR constant [raa/utils/constants.py]
- [x] [Review][Patch] Spec discrepancy: missing verifiable DB storage assertions in unit tests [tests/raa/unit/test_embedding_cache.py:722]
- [x] [Review][Patch] Vacuous test assertion in test_exception_attributes [tests/raa/unit/test_embedding_cache.py:682]

## Dev Notes

### Architecture Compliance (Mandatory)

1. **EmbeddingCache abstraction** — All SQLite read/write for embeddings must go through `EmbeddingCache`. Nodes never call `sqlite3` directly. This matches architecture decision D3.

2. **DB schema** — Both `asr_embeddings.db` and `non_asr_embeddings.db` use identical schema:
   ```sql
   CREATE TABLE IF NOT EXISTS embeddings (
       req_id TEXT PRIMARY KEY,
       embedding BLOB NOT NULL,
       text_hash TEXT NOT NULL,
       model_name TEXT NOT NULL
   );
   ```

3. **Vector serialization** — 1024 float32 values packed via `struct.pack('<1024f', *vector)`. Deserialize with `struct.unpack('<1024f', blob)`. Never store as JSON strings — BLOB only.

4. **Text to embed**:
   - ASR: embed `condition_text` (may be `None` — treat as empty string `""`)
   - Non-ASR: embed `description` (may be `""` — embed the empty string; empty string is a valid text to embed)

5. **Node return type** — Always `dict` matching state channel keys. `verify_embeddings` returns `{"embeddings_ready": True}`.

6. **LLM injection** — Not needed for this story (no LLM calls in embedding), but node must accept `config: RunnableConfig` parameter for forward compatibility.

7. **Named constants** — Import from `raa/utils/constants.py`. Never inline `1024`, `"mixedbread-ai/mxbai-embed-large-v1"`, or the model directory path.

8. **One node per file** — Architecture maps FR-1/FR-2 both to `raa/nodes/preparation.py`. `verify_embeddings` joins `normalize_requirements` in this file. Both are Phase 1 nodes sharing the same preparation domain. All other phases get their own files.

### Model Directory Path

The model files live at the **parent project level**, not inside `raa/`:

```
/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/
├── models/                                          ← model cache (parent level)
│   └── models--mixedbread-ai--mxbai-embed-large-v1/
│       ├── blobs/
│       ├── refs/
│       └── snapshots/
├── raa/                                             ← current project
│   └── raa/utils/embedding_cache.py
└── pyproject.toml
```

From within `raa/raa/utils/embedding_cache.py`, the models directory resolves as:
```python
from pathlib import Path
_MODELS_DIR = Path(__file__).parent.parent.parent / "models"
# raa/raa/utils/embedding_cache.py
#   └── parent = raa/raa/utils/
#       └── parent = raa/raa/
#           └── parent = raa/          ← project root
#               └── / "models"         ← project_root/models = parent-level models
```

Wait — that resolves to `raa/models/`, not the parent-level `models/`. Correct resolution for the parent-level models directory:

```python
# From raa/raa/utils/embedding_cache.py:
# Path(__file__) = raa/raa/utils/embedding_cache.py
# .parent = raa/raa/utils/
# .parent.parent = raa/raa/
# .parent.parent.parent = raa/           ← RAA project root
# .parent.parent.parent.parent = I-Architect/  ← PARENT project root (where models/ lives)
_MODELS_DIR = Path(__file__).parent.parent.parent.parent / "models"
```

Or equivalently, resolve from the `raa` package root:
```python
# raa/__init__.py or computed dynamically:
# The models dir is sibling to raa/, not child of raa/
# raa/../models = parent_of_raa/models
```

**However**, the architecture and ARLO precedent use `Path(__file__).parent.parent.parent / "models"` — in ARLO this works because ARLO's structure is `arlo/nodes/embedding.py` (3 levels to project root = `arlo/../models`). But RAA's `raa/utils/embedding_cache.py` is 4 levels from the parent project root (raa → raa → raa → I-Architect). Count carefully:

```
raa/raa/utils/embedding_cache.py
^   ^   ^     ^
|   |   |     file
|   |   raa/utils/
|   raa/raa/ (package)
raa/ (project dir, sibling to models/)
```

Actually the raa project structure under the working directory is:
```
/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/raa/
└── raa/
    └── utils/
        └── embedding_cache.py
```

So `Path(__file__).parent` = `raa/raa/utils/`, `.parent.parent` = `raa/raa/`, `.parent.parent.parent` = `raa/` (the project dir).

The models dir is at `raa/../models/` = parent of the raa project dir. So:
```python
_MODELS_DIR = Path(__file__).parent.parent.parent.parent / "models"
# 4 levels up from the file
```

BUT — the architecture says "RAA initializes FastEmbed using `cache_dir = '../models'` (resolved as `/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/models`)." The `../` is relative to the raa project directory. Since nodes may be run from different working directories, always resolve from `__file__`, never from `os.getcwd()`.

The safest approach: inject `cache_dir` via `config["configurable"]`, matching the runtime injection pattern. BUT the architecture also shows ARLO using a module-level `_CACHE_DIR = Path(__file__).parent.parent.parent / "models"`. In ARLO's case this is `arlo/nodes/embedding.py` → 3 levels up = `arlo/../models` = parent project models/. For RAA, the embedding_cache.py is 4 levels deep.

**Decision for this story**: The `cache_dir` must come from `config["configurable"]["cache_dir"]`. This is consistent with architecture decision D2: "Paths injected by orchestrator at runtime; never hardcoded inside RAA." The `EmbeddingCache` class itself doesn't need the model directory — only the model loader function does. The node reads `cache_dir` from config and passes it to the model loader.

For unit tests: tests inject a temp dir as `cache_dir` (with a mock model directory structure) or mock the `_get_embedding_model` function entirely.

### FastEmbed API (0.8.0)

```python
from fastembed import TextEmbedding

model = TextEmbedding(
    model_name="mixedbread-ai/mxbai-embed-large-v1",
    cache_dir="/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/models",
)

# embed() returns a generator of lists of floats
vectors = list(model.embed(["text one", "text two"]))
# vectors[0] → list of 1024 floats
# vectors[1] → list of 1024 floats
```

Model existence verification: check that `Path(cache_dir) / "models--mixedbread-ai--mxbai-embed-large-v1"` is an existing directory. This is the directory created by FastEmbed when it downloads the model. If it doesn't exist, raise `ModelNonExistentException` immediately — do not let FastEmbed attempt to download.

### ARLO Embedding Pattern (Reference)

`arlo/nodes/embedding.py` demonstrates the pattern to follow:
- Module-level `_embedding_model: TextEmbedding | None = None` singleton
- `_get_model()` function that lazy-initializes on first call
- `_CACHE_DIR` computed from `Path(__file__).parent.parent.parent / "models"`
- `model.embed(texts)` called with full text list, results converted via `.tolist()`

RAA differs from ARLO: RAA stores vectors in SQLite with hash-based dedup. ARLO embeds the full corpus every run. RAA adds the caching layer that ARLO doesn't have.

### EmbeddingCache API Contract

```python
class EmbeddingCache:
    def __init__(self, db_path: str, model_name: str) -> None:
        """Open (or create) the SQLite DB and ensure the schema exists."""

    @staticmethod
    def compute_hash(text: str) -> str:
        """SHA-256 hex digest of `text.encode('utf-8')`."""

    def get_cached_vector(self, req_id: str, text_hash: str) -> list[float] | None:
        """Return deserialized 1024-dim vector if (req_id, text_hash) matches, else None."""

    def store_vector(self, req_id: str, text_hash: str, vector: list[float]) -> None:
        """Serialize vector to BLOB and INSERT OR REPLACE into the DB."""
```

### `verify_embeddings` Node Logic

```python
def verify_embeddings(state: RAAState, config: RunnableConfig) -> dict:
    configurable = config["configurable"]
    asr_db_path = configurable["asr_db_path"]
    non_asr_db_path = configurable["non_asr_db_path"]
    cache_dir = configurable["cache_dir"]
    model_name = configurable.get("embedding_model_name", EMBEDDING_MODEL_NAME)

    model = _get_embedding_model(cache_dir, model_name)
    asr_cache = EmbeddingCache(asr_db_path, model_name)
    non_asr_cache = EmbeddingCache(non_asr_db_path, model_name)

    # Process ASRs
    for asr in state["normalized_asrs"]:
        text = asr.get("condition_text") or ""
        h = EmbeddingCache.compute_hash(text)
        vec = asr_cache.get_cached_vector(asr["id"], h)
        if vec is None:
            vec = list(model.embed([text]))[0].tolist()
            asr_cache.store_vector(asr["id"], h, vec)

    # Process Non-ASRs
    for req in state["normalized_non_asr"]:
        text = req["description"]
        h = EmbeddingCache.compute_hash(text)
        vec = non_asr_cache.get_cached_vector(req["id"], h)
        if vec is None:
            vec = list(model.embed([text]))[0].tolist()
            non_asr_cache.store_vector(req["id"], h, vec)

    return {"embeddings_ready": True}
```

### Files to Create

| File | Purpose |
|------|---------|
| `raa/utils/embedding_cache.py` | `EmbeddingCache` class + `ModelNonExistentException` + `_get_embedding_model()` |
| `tests/raa/unit/test_embedding_cache.py` | Unit tests for embedding cache and verification node |

### Files to Modify

| File | Change |
|------|--------|
| `raa/nodes/preparation.py` | Add `verify_embeddings` node function |
| `raa/utils/constants.py` | Add `EMBEDDING_DIM`, `EMBEDDING_MODEL_NAME` constants |

### Testing Standards

- Framework: `pytest` (≥8.2)
- No live LLM calls — not applicable (no LLMs in this story)
- No live FastEmbed calls in unit tests for `EmbeddingCache` (SQLite-only tests use tempfile)
- For `verify_embeddings` node tests: mock `_get_embedding_model` to return a fake embedder that produces deterministic vectors (e.g., `[float(i) for i in range(1024)]`)
- Test file locations: `tests/raa/unit/test_embedding_cache.py`
- Run with: `python -m pytest tests/raa/unit/test_embedding_cache.py -v`
- Existing `tests/raa/unit/test_preparation.py` must continue to pass (28 tests)

### Previous Story Intelligence (Story 1.1)

**Established patterns to follow:**
- `_make_state()` and `_make_config()` test helpers — replicate this pattern for embedding tests
- Node functions accept `(state: RAAState, config: RunnableConfig) -> dict`
- Private helper functions prefixed with `_` are co-located with their sole consumer
- State channels already defined: `normalized_asrs`, `normalized_non_asr`, `embeddings_ready`
- `normalize_requirements` returns `embeddings_ready: False` — `verify_embeddings` is the node that flips it to `True`
- Constants live in `raa/utils/constants.py`, imported by name (never inline)

**Review findings applicable to this story:**
- Description text may be empty string `""` — embed it anyway (empty string is valid input)
- Canonical ID format is `"R{id}"` — `req_id` values stored in SQLite match this format
- Edge cases matter: empty input lists, whitespace-only text (though for ASR, `condition_text` may be `None`)

**State channels consumed by this node:**
- `state["normalized_asrs"]` — list of dicts with keys `id`, `description`, `is_asr`, `quality_attributes`, `condition_text`
- `state["normalized_non_asr"]` — list of dicts with keys `id`, `description`, `is_asr`, `quality_attributes`, `condition_text`

**State channels written by this node:**
- `embeddings_ready: True`

### Project Structure Reference

```
raa/
├── nodes/
│   └── preparation.py        ← ADD verify_embeddings() here
├── utils/
│   ├── constants.py           ← MODIFY: add EMBEDDING_DIM, EMBEDDING_MODEL_NAME
│   └── embedding_cache.py     ← CREATE: EmbeddingCache + ModelNonExistentException
└── state/
    └── schemas.py             ← UNCHANGED (embeddings_ready already defined)
tests/
└── raa/
    └── unit/
        ├── test_preparation.py         ← UNCHANGED (28 tests must still pass)
        └── test_embedding_cache.py     ← CREATE: 13 tests
```

### References

- Source: `_bmad-output/planning-artifacts/epics.md` — Epic 1, Story 1.2 (FR2)
- Source: `_bmad-output/planning-artifacts/architecture.md` — D2 (SQLite Embedding DB Layout), D3 (Embedding DB Access), Embedding Cache Abstraction (AR4)
- Source: `arlo/nodes/embedding.py` — FastEmbed singleton pattern to mirror
- Source: `raa/nodes/preparation.py` — existing Phase 1 node, normalize_requirements output shape
- Source: `raa/state/schemas.py` — RAAState channels (normalized_asrs, normalized_non_asr, embeddings_ready)
- Source: `raa/utils/constants.py` — existing named constants pattern
- Source: `pyproject.toml` — fastembed==0.8.0 pinned
- FastEmbed 0.8.0 API: `TextEmbedding(model_name, cache_dir)` → `.embed(list[str])` returns generator of `list[float]`
- Model files at: `/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/models/models--mixedbread-ai--mxbai-embed-large-v1/`

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

### Completion Notes List

- Task 1: Created `raa/utils/embedding_cache.py` with `EmbeddingCache` class. SQLite schema: `(req_id TEXT PRIMARY KEY, embedding BLOB, text_hash TEXT, model_name TEXT)`. Vector serialization via `struct.pack('<1024f', *vector)`. WAL mode enabled.
- Task 2: Created `ModelNonExistentException(Exception)` with `cache_dir` and `model_name` attributes. `_get_embedding_model(cache_dir, model_name)` lazy-singleton loader verifies model directory exists before initializing `TextEmbedding`.
- Task 3: Added `verify_embeddings(state, config)` node to `raa/nodes/preparation.py`. Reads `asr_db_path`, `non_asr_db_path`, `cache_dir`, `embedding_model_name` from `config["configurable"]`. Shared `_embed_requirements()` helper processes both ASR (condition_text) and Non-ASR (description) with hash-check-skip logic. Returns `{"embeddings_ready": True}`.
- Task 4: 22 unit tests covering EmbeddingCache (roundtrip, upsert, persistence, hash determinism), ModelNonExistentException (message, attributes, happy path), and verify_embeddings node (empty inputs, new, cached, partial cache, stale re-embed, null text, config path injection, combined ASR+Non-ASR). All 56 tests pass (22 new + 34 existing).
- Task 5: Added `EMBEDDING_DIM = 1024` and `EMBEDDING_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"` to `raa/utils/constants.py`. `cache_dir` injected via config per architecture D2 — not a module-level constant.

### File List

- `raa/utils/embedding_cache.py` (new)
- `raa/utils/constants.py` (modified — added EMBEDDING_DIM, EMBEDDING_MODEL_NAME)
- `raa/nodes/preparation.py` (modified — added verify_embeddings node + _embed_requirements helper)
- `tests/raa/unit/test_embedding_cache.py` (new)
