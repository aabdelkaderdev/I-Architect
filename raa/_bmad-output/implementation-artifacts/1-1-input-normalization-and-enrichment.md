# Story 1.1: Input Normalization and Enrichment

Status: done

## Story

As a Pipeline Engineer,
I want to normalize and enrich raw ASR and Non-ASR requirements,
So that all downstream nodes receive standardized requirement records.

## Acceptance Criteria

**Given** a raw ARLO output dictionary containing `asrs` (with integer IDs, QAs, and condition text) and `non_asr` (list of bare string IDs), and orchestrator-provided `requirements: dict[str, str]` containing the original full requirement set (ID to description mapping)
**When** the normalization node is executed
**Then** it must transform all integer IDs to string IDs (e.g., ARLO ID `5` becomes `"R5"`)
**And** it must resolve description text for both ASR and Non-ASR requirements using the original requirements mapping, matching both raw and normalized requirement ID forms
**And** it may use ARLO-provided ASR description text only as a fallback when the original requirements mapping has no usable entry
**And** it must enrich Non-ASR requirement records with default values: `is_asr = false`, `quality_attributes = []`, and `condition_text = null`
**And** it must return a list of standardized requirement records matching the input IDs.

## Tasks / Subtasks

- [x] Task 1: Bootstrap RAA package structure (AC: setup)
  - [x] 1.1 Add `"raa*"` to `include` in parent `pyproject.toml` (`[tool.setuptools.packages.find]`)
  - [x] 1.2 Create `raa/__init__.py`
  - [x] 1.3 Create `raa/state/__init__.py`
  - [x] 1.4 Create `raa/state/schemas.py` with `RAAInput`, `RAAOutput`, `RAAState` TypedDicts
  - [x] 1.5 Create `raa/state/models.py` with `NormalizedRequirement` Pydantic BaseModel
  - [x] 1.6 Create `raa/state/config.py` with `RAAConfig` dataclass
  - [x] 1.7 Create `raa/nodes/__init__.py`
  - [x] 1.8 Create `raa/utils/__init__.py`
  - [x] 1.9 Create `raa/utils/constants.py` with named thresholds
  - [x] 1.10 Verify all imports resolve: `python -c "from raa.state.schemas import RAAInput, RAAOutput, RAAState; from raa.state.models import NormalizedRequirement; print('OK')"`

- [x] Task 2: Implement the normalization node (AC: all)
  - [x] 2.1 Create `raa/nodes/preparation.py` with `normalize_requirements(state, config) -> dict` function
  - [x] 2.2 Implement ID standardization: integer → `"R{int}"` string
  - [x] 2.3 Implement ASR and Non-ASR description resolution from orchestrator-provided requirements dict
  - [x] 2.4 Apply non-ASR defaults: `is_asr=False`, `quality_attributes=[]`, `condition_text=None`
  - [x] 2.5 Return `{"normalized_asrs": [...], "normalized_non_asr": [...], "embeddings_ready": False}`

- [x] Task 3: Write unit tests (AC: all)
  - [x] 3.1 Create `tests/raa/unit/test_preparation.py`
  - [x] 3.2 Test integer ID → string ID conversion
  - [x] 3.3 Test ASR and Non-ASR description resolution (found, missing, raw ID, and normalized ID cases)
  - [x] 3.4 Test non-ASR default field population
  - [x] 3.5 Test empty input handling (no ASRs, no non-ASRs)

### Review Findings

- [x] [Review][Decision] Decide ASR description source precedence — resolved: the orchestrator-provided original requirements mapping is authoritative for ASR and Non-ASR description text. ARLO-provided ASR description text is fallback-only when the mapping has no usable entry. Evidence: `raa/nodes/preparation.py:68` and `tests/raa/unit/test_preparation.py:100`.
- [x] [Review][Patch] Description lookup misses alternate normalized/unprefixed ID forms — fixed: `_lookup_requirements()` tries raw then normalized key; ASR resolver uses requirements-first precedence with ARLO description as last fallback [raa/nodes/preparation.py:68-96]
- [x] [Review][Patch] ASR `quality_attributes` can violate the standardized `list[str]` output shape — fixed: `_coerce_quality_attributes()` guards None, non-list, and non-string entries [raa/nodes/preparation.py:100-107]
- [x] [Review][Patch] ID normalization treats any `R*` string as already normalized and does not trim/case-normalize IDs — fixed: `to_r_id()` in `raa/utils/id_utils.py` strips whitespace and normalizes lowercase prefixes [raa/utils/id_utils.py:13-28]
- [x] [Review][Patch] `preparation.py` contains helper functions despite the story's one-node-per-file constraint — fixed: `to_r_id()` extracted to `raa/utils/id_utils.py`; remaining helpers are private non-node functions co-located with sole consumer [raa/nodes/preparation.py:64-107]

### Review Findings (Re-review)

- [x] [Review][Patch] Strict canonical ID handling for non-numeric IDs that already start with `R` — fixed: `to_r_id()` preserves only `R<digits>` and `RN<digits>`-style forms; all other `R*` inputs are prefixed.
- [x] [Review][Patch] Requirements lookup still misses stripped and unprefixed alternate key forms [raa/nodes/preparation.py:118] — fixed: `_candidate_requirement_keys()` now tries stripped, canonical, and unprefixed forms in order.
- [x] [Review][Patch] Normalization does not detect duplicate canonical requirement IDs [raa/nodes/preparation.py:41] — fixed: `normalize_requirements()` now raises on duplicate canonical IDs across ASR and Non-ASR inputs.
- [x] [Review][Patch] Whitespace-only descriptions can be treated as usable text [raa/nodes/preparation.py:94] — fixed: `_description_is_usable()` rejects whitespace-only values while preserving empty-string authoritativeness.
- [x] [Review][Patch] Story task 2.5 still documents stale return keys `asrs` and `non_asr` [_bmad-output/implementation-artifacts/1-1-input-normalization-and-enrichment.md:40] — fixed to `normalized_asrs` and `normalized_non_asr`.
- [x] [Review][Patch] Story Normalization Logic snippet is stale relative to the current implementation [_bmad-output/implementation-artifacts/1-1-input-normalization-and-enrichment.md:231] — fixed to show the current lookup and duplicate-detection behavior.

## Dev Notes

### Critical: pyproject.toml Registration

The parent `pyproject.toml` at `/home/delatom/I-Architect-3cf20c60d77417e9febe099eeb91bc78227ce89f/pyproject.toml` currently has:
```toml
[tool.setuptools.packages.find]
include = ["arlo*"]
```

This must become:
```toml
[tool.setuptools.packages.find]
include = ["arlo*", "raa*"]
```

After changing, run `pip install -e .` from the parent project root to re-register.

### Architecture Compliance (Mandatory)

1. **Three-schema state pattern** — mirror `arlo/state/` exactly:
   - `schemas.py`: `TypedDict` classes (`RAAInput`, `RAAOutput`, `RAAState`). `RAAState` inherits from both `RAAInput` and `RAAOutput`.
   - `models.py`: Pydantic v2 `BaseModel` classes (`NormalizedRequirement`). All LLM calls later use `with_structured_output(Model, include_raw=True)`.
   - `config.py`: `@dataclass` with `from_dict(cls, d)` classmethod.

2. **Node return type**: Always `dict` matching state channel keys. Never return full state, never mutate state directly.

3. **Named constants**: Use `from raa.utils.constants import ...` — never inline magic numbers.

4. **Requirement IDs**: Always `str` with `"R"` prefix inside RAA. ARLO passes `int` IDs in `asrs`; RAA normalizes to `"R5"` format.

5. **One node per file**: `preparation.py` contains only the normalization node function.

6. **LLM injection**: Not needed for this story (no LLM calls in normalization), but node must accept `config: RunnableConfig` parameter for forward compatibility:
   ```python
   from langchain_core.runnables import RunnableConfig
   
   def normalize_requirements(state: RAAState, config: RunnableConfig) -> dict:
       ...
   ```

### ARLO Contract (Input Data Shapes)

The parent orchestrator constructs `RAAInput` from the original requirements map and ARLO outputs. The original requirements map is passed as `requirements: dict[str, str]` and is the authoritative source for requirement description text.

ARLO outputs arrive at RAA with these exact shapes:

```python
# asrs: list[dict] — each dict has:
#   {id: int, quality_attributes: list[str], condition_text: str}
#   Optional description text may be present, but it is fallback-only.
#
# non_asr: list[str] — bare requirement ID strings like ["N1", "N2", ...]
#
# condition_groups: list[dict] — K-Means clusters from ARLO
#
# quality_weights: dict[str, int] — {"security": 5, "reliability": 3, ...}
```

ASR and Non-ASR description resolution uses the orchestrator-provided `requirements` dict (mapping of `str ID → str description`) passed in the initial state. The resolver must check raw and normalized ID forms before falling back to ARLO-provided ASR description text. Non-ASR IDs from ARLO may be integer strings or formatted differently — normalize to `"R{id}"` regardless of source format.

### State Schema Design for Story 1.1

```python
# raa/state/schemas.py
from typing import Annotated, Any
from typing_extensions import NotRequired, TypedDict
from operator import add

class RAAInput(TypedDict):
    """Input schema — provided by the orchestrator."""
    requirements: dict[str, str]          # ID → description mapping
    asrs: list[dict]                      # ARLO ASR output
    non_asr: list[str]                    # ARLO non-ASR bare IDs
    condition_groups: list[dict]          # ARLO condition groups
    quality_weights: dict[str, int]       # ARLO quality attribute frequencies
    review_mode: str                      # "interactive" or "autonomous"

class RAAOutput(TypedDict):
    """Output schema — returned to the orchestrator."""
    arch_model: NotRequired[dict]
    open_questions: NotRequired[list[dict]]
    traceability_manifest: NotRequired[dict]

class RAAState(RAAInput, RAAOutput):
    """Full internal state with 15 channels."""
    # Phase 1: Normalization outputs
    normalized_asrs: list[dict]
    normalized_non_asr: list[dict]
    embeddings_ready: bool
    # Phase 2-3: Batching
    batches: NotRequired[list[dict]]
    bridge_requirements: NotRequired[list[dict]]
    # Phase 4-5: Queue
    execution_queue: NotRequired[list[dict]]
    unprocessed_requirements: NotRequired[list[dict]]
    # Phase 6: Parallel execution (append-merge reducers)
    batch_outputs: Annotated[list[dict], add]
    open_questions: Annotated[list[dict], add]
    incoherent_batches: Annotated[list[dict], add]
    batch_cursor: int
    # Phase 7-8: Review and finalize
    human_review_payload: NotRequired[dict]
    human_answers: NotRequired[dict]
```

```python
# raa/state/models.py
from pydantic import BaseModel, Field

class NormalizedRequirement(BaseModel):
    """Standardized requirement record used across all RAA phases."""
    id: str                                    # "R5" format
    description: str
    is_asr: bool
    quality_attributes: list[str] = Field(default_factory=list)
    condition_text: str | None = None
```

```python
# raa/utils/constants.py
# Deduplication thresholds
DEDUP_MERGE_THRESHOLD = 0.80
DEDUP_GROUP_THRESHOLD_LOW = 0.60
DEDUP_GROUP_THRESHOLD_HIGH = 0.80
# Batching thresholds
NON_ASR_SIMILARITY_THRESHOLD = 0.65
COHERENCE_THRESHOLD = 0.55
# Residual pass thresholds
RESIDUAL_HIGH_THRESHOLD = 0.75
RESIDUAL_MID_LOW = 0.50
# Limits
MAX_NON_ASR_PER_BATCH = 10
MAX_BRIDGE_REQUIREMENTS = 3
RESIDUAL_REBATCH_PCT = 0.15
MAX_HUMAN_RETRIES = 3
# Pattern keywords
INFRA_KEYWORDS = ["all", "every", "always", "any"]
```

### Files to Create

| File | Purpose |
|------|---------|
| `raa/__init__.py` | Package marker |
| `raa/state/__init__.py` | State subpackage marker |
| `raa/state/schemas.py` | RAAInput, RAAOutput, RAAState TypedDicts |
| `raa/state/models.py` | NormalizedRequirement Pydantic model |
| `raa/state/config.py` | RAAConfig dataclass |
| `raa/nodes/__init__.py` | Nodes subpackage marker |
| `raa/nodes/preparation.py` | normalize_requirements node |
| `raa/utils/__init__.py` | Utils subpackage marker |
| `raa/utils/constants.py` | Named threshold constants |
| `tests/raa/__init__.py` | Test package marker |
| `tests/raa/unit/__init__.py` | Unit test marker |
| `tests/raa/unit/test_preparation.py` | Normalization unit tests |

### Files to Modify

| File | Change |
|------|--------|
| `pyproject.toml` | Add `"raa*"` to `include` list |

### Testing Standards

- Framework: `pytest` (≥8.2)
- No live LLM calls in unit tests — use `GenericFakeChatModel` from `langchain_core` when LLMs are involved (not needed for this story)
- Test file location: `tests/raa/unit/test_preparation.py`
- Run with: `python -m pytest tests/raa/unit/test_preparation.py -v`
- Async tests: use `pytest-asyncio` (≥0.25)

### Normalization Logic

```python
def normalize_requirements(state: RAAState, config: RunnableConfig) -> dict:
    requirements = state["requirements"]     # dict[str, str]: ID → description
    raw_asrs = state["asrs"]                 # list[dict]
    raw_non_asr_ids = state["non_asr"]       # list[str]
    seen_ids: dict[str, str] = {}
    
    normalized_asrs = []
    for asr in raw_asrs:
        asr_id = to_r_id(asr["id"])
        _register_canonical_id(seen_ids, asr_id, f"ASR {asr['id']!r}")
        desc = _resolve_asr_description(asr["id"], asr_id, asr, requirements)
        normalized_asrs.append({
            "id": asr_id,
            "description": desc,
            "is_asr": True,
            "quality_attributes": _coerce_quality_attributes(asr.get("quality_attributes", _UNSET)),
            "condition_text": asr.get("condition_text"),
        })
    
    normalized_non_asr = []
    for req_id in raw_non_asr_ids:
        normalized_id = to_r_id(req_id)
        _register_canonical_id(seen_ids, normalized_id, f"Non-ASR {req_id!r}")
        desc = _resolve_non_asr_description(req_id, normalized_id, requirements)
        normalized_non_asr.append({
            "id": normalized_id,
            "description": desc,
            "is_asr": False,
            "quality_attributes": [],
            "condition_text": None,
        })
    
    return {
        "normalized_asrs": normalized_asrs,
        "normalized_non_asr": normalized_non_asr,
        "embeddings_ready": False,
    }
```

### References

- Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md` Section 6.1 (FR-1)
- Source: `_bmad-output/planning-artifacts/epics.md` Epic 1, Story 1.1
- Source: `_bmad-output/planning-artifacts/architecture.md` — Complete architectural decisions, state schema pattern, enforcement rules
- Source: `arlo/state/schemas.py` — Three-schema pattern to mirror (ARLOInput/ARLOOutput/ARLOState)
- Source: `arlo/state/models.py` — Pydantic BaseModel pattern to mirror
- Source: `arlo/state/config.py` — Dataclass config pattern to mirror
- LangGraph 1.2.0 API: `docs-langchain` MCP — StateGraph, TypedDict state, `Annotated[list, add]` reducers, `RunnableConfig`
- LangChain 1.3.0 API: `docs-langchain` MCP — `with_structured_output(Model, include_raw=True)`

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

### Completion Notes List

- Task 1: Bootstrapped RAA package with three-schema state pattern (schemas.py, models.py, config.py), constants module, and all __init__.py markers. Added "raa*" to parent pyproject.toml packages.find. Installed all dependencies via pip.
- Task 2: Implemented `normalize_requirements()` node in `raa/nodes/preparation.py` with ID standardization (int→"R{id}"), ASR description resolution (requirements dict → provided fallback → empty string), and non-ASR default enrichment (is_asr=False, quality_attributes=[], condition_text=None). Node accepts RunnableConfig for forward compatibility with LLM-injected nodes.
- Task 3: 19 unit tests covering ID conversion (int, string, multi), ASR description resolution (requirements mapping, fallback, missing), ASR field preservation (QA, condition_text, is_asr), non-ASR normalization (ID, description, defaults, already-prefixed), and edge cases (empty inputs, embeddings_ready flag). All 19 pass.
- Review fixes (2026-05-23): Resolved 4/4 review findings. Description lookup now tries raw + normalized ID keys in requirements dict with correct precedence (requirements → ARLO fallback). QA attributes coerced to `list[str]` via `_coerce_quality_attributes()`. ID normalization handles whitespace, lowercase prefixes via extracted `raa/utils/id_utils.py`. Helper functions resolved: `to_r_id()` extracted to utility module; `_resolve_asr_description`, `_resolve_non_asr_description`, `_lookup_requirements`, `_coerce_quality_attributes` are private (non-node) functions co-located with sole consumer. Test suite expanded from 19 to 28 tests.

### File List

- `pyproject.toml` (modified — added "raa*" to include)
- `raa/__init__.py`
- `raa/state/__init__.py`
- `raa/state/schemas.py`
- `raa/state/models.py`
- `raa/state/config.py`
- `raa/nodes/__init__.py`
- `raa/nodes/preparation.py`
- `raa/utils/__init__.py`
- `raa/utils/constants.py`
- `tests/__init__.py`
- `tests/raa/__init__.py`
- `tests/raa/unit/__init__.py`
- `tests/raa/unit/test_preparation.py`
- `raa/utils/id_utils.py`
