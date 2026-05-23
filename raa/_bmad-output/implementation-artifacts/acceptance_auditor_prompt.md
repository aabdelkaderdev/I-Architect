# Acceptance Auditor Code Review Prompt

You are an Acceptance Auditor. Review the provided diff against the spec and context docs below. Check for:
1. Violations of acceptance criteria.
2. Deviations from spec intent.
3. Missing implementation of specified behavior.
4. Contradictions between spec constraints and actual code.

Output findings as a Markdown list. Each finding must contain:
- A one-line title
- Which AC/constraint it violates
- Evidence from the diff

## Spec Document

```markdown
# Story 3.1: Open Question Classification and Human Review Payload Generation

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want the RAA Orchestrator to classify open questions and build a detailed human review payload,
so that interactive and autonomous execution steps have clear contexts and pre-computed solutions.

## Acceptance Criteria

1. **Question Categorization**: Given a list of open questions accumulated in the `open_questions` channel from Phase 6, when question classification is executed, it must categorize each question:
   - `change_risk`, `high_coupling`, and `coverage_gap` must be classified as `human_preferred`.
   - `contention`, `tie`, `hierarchy_conflict`, and `scope_conflict` must be classified as `judge_resolvable`.
2. **Pre-computed suggested resolutions**: The node must auto-generate a pre-computed suggested answer for each `judge_resolvable` question.
3. **Payload Construction**: It must construct a `human_review_payload` dictionary containing:
   - `open_questions`: The list of categorized questions (with their type, description, classification, and suggestion if applicable).
   - `conflicting_elements`: Details of the conflicting C4 elements (from the merged model).
   - `model_statistics`: A summary of model statistics (system count, container count, component count, and relationship count).
   - `pre_computed_resolutions`: A dictionary mapping question IDs to the pre-computed suggested resolutions.

## Tasks / Subtasks

- [x] Task 1: Define `OpenQuestion` Pydantic model in `raa/state/models.py` (AC: #1)
  - [x] 1.1 Add `class OpenQuestion(BaseModel)` to `raa/state/models.py` with fields:
    - `id: str`
    - `question_type: str`
    - `description: str`
    - `context: dict = Field(default_factory=dict)`
    - `resolution_owner: str = "human_preferred"`  # "human_preferred" or "judge_resolvable"
    - `resolution: str | None = None`
    - `assumption_flag: bool = False`
    - `metadata: dict = Field(default_factory=dict)`
  - [x] 1.2 Export `OpenQuestion` in `raa/state/models.py` and ensure it's imported in the `raa/state/__init__.py`.

- [x] Task 2: Implement Classification & Payload Generation Node in `raa/nodes/human_review_gate.py` (AC: #1, #2, #3)
  - [x] 2.1 Create the file `raa/nodes/human_review_gate.py` if it does not exist.
  - [x] 2.2 Implement `prepare_human_review_payload(state: RAAState) -> dict`:
    - Read `open_questions` from state. If empty, proceed with generating statistics and empty lists.
    - Normalize any legacy keys (e.g., if a question has `type` instead of `question_type`, map it).
    - Map each question to a deterministic ID (e.g., `q_{index}` or based on its content) and instantiate an `OpenQuestion` model.
    - Apply categorization logic:
      - `change_risk`, `high_coupling`, `coverage_gap` -> `resolution_owner = "human_preferred"`.
      - `contention`, `tie`, `hierarchy_conflict`, `scope_conflict` -> `resolution_owner = "judge_resolvable"`.
    - Generate `suggested_resolution` for `judge_resolvable` questions:
      - `hierarchy_conflict`: "Use parent hierarchy from canonical entity."
      - `scope_conflict`: "Apply fallback constraints to adjust relationship scope."
      - `tie`: "Resolve tie by selecting the proposal from primary strategy (RAA-A SAAM-First)."
      - `contention`: "Consolidate entities using the primary strategy's structure as the ground truth."
    - Gather details for `conflicting_elements`: Scan the `arch_model` for entities referenced in the open questions (using `entity_a_id`, `entity_b_id`, `entity_id`, or `promoted_component_id` inside the question context) and collect their details.
    - Calculate `model_statistics`: Count system, container, and component entities, and count relationship arrows in the `arch_model`.
    - Build `human_review_payload` dict containing: `open_questions`, `conflicting_elements`, `model_statistics`, and `pre_computed_resolutions` (mapping question IDs to suggestions).
    - Return `{"human_review_payload": payload_dict}`.

- [x] Task 3: Author comprehensive unit tests in `tests/raa/unit/test_human_review_gate.py` (AC: #1, #2, #3)
  - [x] 3.1 Create `tests/raa/unit/test_human_review_gate.py`.
  - [x] 3.2 Add test cases validating that questions are classified correctly.
  - [x] 3.3 Add test cases verifying pre-computed suggested resolutions.
  - [x] 3.4 Add test cases checking that conflicting elements are fetched correctly from `arch_model`.
  - [x] 3.5 Add test cases verifying statistics logic (systems, containers, components, relationships).
  - [x] 3.6 Run the test suite:
    ```bash
    python3 -m pytest tests/raa/unit/test_human_review_gate.py -q
    ```

## Dev Notes

- **Pydantic Validation**: Use `model_validate` for Pydantic v2 coercion when converting state dictionaries to models.
- **State Immutability**: Ensure `prepare_human_review_payload` is a pure function that does not mutate the inputs.

### Project Structure Notes

- New node function in `raa/nodes/human_review_gate.py`.
- New Pydantic model in `raa/state/models.py`.
- New unit tests in `tests/raa/unit/test_human_review_gate.py`.

### References

- [Source: `_bmad-output/planning-artifacts/epics.md#Story 3.1: Open Question Classification and Human Review Payload Generation`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#D8 — Human Review Gate Interrupt Mechanism`]
- [Source: `raa/state/schemas.py` — `RAAState` definition]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

No debug logs — all 448 tests passed on first implementation pass.

### Completion Notes List

- **Task 1**: Added `OpenQuestion` Pydantic model to `raa/state/models.py` with fields: `id`, `question_type`, `description`, `context`, `resolution_owner` (default `"human_preferred"`), `resolution`, `assumption_flag`, `metadata`.
- **Task 2**: Created `raa/nodes/human_review_gate.py` with `prepare_human_review_payload(state: RAAState) -> dict`. Classification maps `change_risk`/`high_coupling`/`coverage_gap` → `human_preferred`, `contention`/`tie`/`hierarchy_conflict`/`scope_conflict` → `judge_resolvable`. Auto-generates suggested resolutions for judge-resolvable types. Gathers conflicting C4 elements from `arch_model` by scanning `entity_a_id`, `entity_b_id`, `entity_id`, `promoted_component_id` keys. Computes model statistics (system/container/component counts, relationship count). Handles legacy `type` key normalization.
- **Task 3**: Created `tests/raa/unit/test_human_review_gate.py` with 29 tests covering classification, legacy key normalization, suggested resolutions, conflicting elements, model statistics, pre-computed resolutions, payload structure, edge cases, and determinism.

### File List

- `raa/state/models.py` — Added `OpenQuestion` model
- `raa/nodes/human_review_gate.py` — **NEW**: Classification and payload generation node
- `tests/raa/unit/test_human_review_gate.py` — **NEW**: 29 unit tests

```

## Context Document (raa/state/schemas.py)

```python
"""
Three-schema state pattern for the RAA subgraph.

- RAAInput:  What the orchestrator provides (6 keys).
- RAAOutput: What the orchestrator receives (3 keys).
- RAAState:  Full internal state — all intermediate data hidden from external callers.

Private-state TypedDicts are used for transient data between adjacent nodes via
add_sequence. The mechanism requires explicit return/parameter type annotations
on the node functions.
"""
from __future__ import annotations

from operator import add
from typing import Annotated, Any

from typing_extensions import NotRequired, TypedDict


# ---------------------------------------------------------------------------
# Input Schema — provided by the orchestrator
# ---------------------------------------------------------------------------
class RAAInput(TypedDict):
    """Input schema for RAA subgraph. Provided by the orchestrator.

    The orchestrator threads ARLO output channels into these fields:
    - asrs → from ARLO.asrs
    - non_asr → from ARLO.non_asr
    - condition_groups → from ARLO.condition_groups
    - quality_weights → from ARLO.quality_weights
    """
    requirements: dict[str, str]          # Mapping of Requirement ID → description text
    asrs: list[dict]                      # ARLO ASR output: {id, quality_attributes, condition_text}
    non_asr: list[str]                    # ARLO non-ASR bare requirement ID strings
    condition_groups: list[dict]          # K-Means clusters of ASRs from ARLO
    quality_weights: dict[str, int]       # Quality attribute frequency counts
    review_mode: str                      # "interactive" or "autonomous"


# ---------------------------------------------------------------------------
# Output Schema — returned to the orchestrator
# ---------------------------------------------------------------------------
class RAAOutput(TypedDict):
    """Output schema for RAA subgraph. Returned to the orchestrator.

    The orchestrator threads these channels to downstream agents:
    - arch_model → AGA
    - open_questions → audit trail
    - traceability_manifest → AGA
    """
    arch_model: NotRequired[dict]           # Final merged C4 JSON
    open_questions: NotRequired[list[dict]] # Unresolved questions for audit
    traceability_manifest: NotRequired[dict]


# ---------------------------------------------------------------------------
# Full Internal State
# ---------------------------------------------------------------------------
class RAAState(RAAInput, RAAOutput):
    """Full internal state — all intermediate data hidden from external callers.

    The `Annotated[list, add]` reducer is essential for concurrent-write channels —
    parallel subgraph outputs are appended rather than overwritten.
    """

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

    # Phase 6: Parallel execution — append-merge reducers for concurrent writes
    batch_outputs: Annotated[list[dict], add]
    open_questions: Annotated[list[dict], add]
    incoherent_batches: Annotated[list[dict], add]
    batch_cursor: int

    # Phase 7-8: Review and finalize
    human_review_payload: NotRequired[dict]
    human_answers: NotRequired[dict]

    # Judge scoring channel (Story 2.3)
    # Maps batch_cursor → ranking result dict. Not an append reducer because
    # each batch is scored exactly once by the Judge node; the node reads the
    # current cursor, scores matching records, and writes the full dict.
    judge_rankings: NotRequired[dict[int, dict]]

```

## Diff to Review

```diff
diff --git a/raa/raa/state/models.py b/raa/raa/state/models.py
index 9ea73c7..b28da22 100644
--- a/raa/raa/state/models.py
+++ b/raa/raa/state/models.py
@@ -100,3 +100,22 @@ class FragmentScore(BaseModel):
     final_score: float
     scenario_contributions: list[dict] = Field(default_factory=list)
     is_primary: bool = False
+
+
+# ── Human Review Models (Story 3.1) ──────────────────────────────────────────
+
+
+class OpenQuestion(BaseModel):
+    """A classified open question for human review payload generation.
+
+    Questions are categorized as ``human_preferred`` (requires human judgment)
+    or ``judge_resolvable`` (can be auto-resolved by the Judge).
+    """
+    id: str
+    question_type: str
+    description: str
+    context: dict = Field(default_factory=dict)
+    resolution_owner: str = "human_preferred"
+    resolution: str | None = None
+    assumption_flag: bool = False
+    metadata: dict = Field(default_factory=dict)

diff --git a/raa/nodes/human_review_gate.py b/raa/nodes/human_review_gate.py
new file mode 100644
index 0000000..6724a25
--- /dev/null
+++ b/raa/nodes/human_review_gate.py
@@ -0,0 +1,164 @@
+"""
+Human review gate node (Story 3.1).
+
+Classifies open questions and builds a detailed human review payload
+with categorized questions, conflicting elements, model statistics,
+and pre-computed suggested resolutions for judge-resolvable questions.
+"""
+from __future__ import annotations
+
+from raa.state.models import OpenQuestion
+from raa.state.schemas import RAAState
+
+# ── Classification mapping ──────────────────────────────────────────────────
+
+_HUMAN_PREFERRED_TYPES = frozenset({"change_risk", "high_coupling", "coverage_gap"})
+_JUDGE_RESOLVABLE_TYPES = frozenset({"contention", "tie", "hierarchy_conflict", "scope_conflict"})
+
+# ── Suggested resolutions for judge-resolvable question types ───────────────
+
+_SUGGESTED_RESOLUTIONS: dict[str, str] = {
+    "hierarchy_conflict": "Use parent hierarchy from canonical entity.",
+    "scope_conflict": "Apply fallback constraints to adjust relationship scope.",
+    "tie": "Resolve tie by selecting the proposal from primary strategy (RAA-A SAAM-First).",
+    "contention": "Consolidate entities using the primary strategy's structure as the ground truth.",
+}
+
+
+def _classify_question_type(question_type: str) -> str:
+    """Map a raw question_type to its resolution_owner category.
+
+    Returns:
+        ``"human_preferred"`` or ``"judge_resolvable"``.
+    """
+    if question_type in _HUMAN_PREFERRED_TYPES:
+        return "human_preferred"
+    if question_type in _JUDGE_RESOLVABLE_TYPES:
+        return "judge_resolvable"
+    # Default: unknown types go to human review
+    return "human_preferred"
+
+
+def _generate_deterministic_id(index: int, question: dict) -> str:
+    """Generate a deterministic question ID from its index and content."""
+    q_type = question.get("question_type", question.get("type", ""))
+    return f"q_{index}_{q_type}"
+
+
+def _normalize_question(raw: dict, index: int) -> OpenQuestion:
+    """Normalize a raw question dict into an OpenQuestion model.
+
+    Handles legacy keys (``type`` → ``question_type``).
+    """
+    question_type = raw.get("question_type") or raw.get("type") or "unknown"
+    resolution_owner = _classify_question_type(question_type)
+
+    suggested: str | None = None
+    if resolution_owner == "judge_resolvable":
+        suggested = _SUGGESTED_RESOLUTIONS.get(question_type)
+
+    return OpenQuestion(
+        id=_generate_deterministic_id(index, raw),
+        question_type=question_type,
+        description=raw.get("description") or raw.get("summary") or "",
+        context={
+            k: v
+            for k, v in raw.items()
+            if k not in ("question_type", "type", "description", "summary")
+        },
+        resolution_owner=resolution_owner,
+        resolution=suggested,
+        assumption_flag=False,
+        metadata=raw.get("metadata", {}),
+    )
+
+
+def _gather_conflicting_elements(
+    open_questions: list[dict],
+    arch_model: dict,
+) -> list[dict]:
+    """Collect entity details from arch_model for entities referenced in open questions.
+
+    Scans entity IDs from keys: ``entity_a_id``, ``entity_b_id``, ``entity_id``,
+    and ``promoted_component_id``.
+    """
+    entity_map: dict[str, dict] = {}
+    for entity in arch_model.get("entities") or []:
+        eid = entity.get("id", "")
+        if eid:
+            entity_map[eid] = entity
+
+    referenced_ids: set[str] = set()
+    id_keys = ("entity_a_id", "entity_b_id", "entity_id", "promoted_component_id")
+
+    for q in open_questions:
+        for key in id_keys:
+            val = q.get(key)
+            if val and isinstance(val, str):
+                referenced_ids.add(val)
+
+    conflicting: list[dict] = []
+    for eid in sorted(referenced_ids):
+        if eid in entity_map:
+            conflicting.append(entity_map[eid])
+
+    return conflicting
+
+
+def _calculate_model_statistics(arch_model: dict) -> dict:
+    """Count entities by C4 type and count relationships."""
+    entities: list[dict] = arch_model.get("entities") or []
+    relationships: list[dict] = arch_model.get("relationships") or []
+
+    type_counts: dict[str, int] = {}
+    for e in entities:
+        c4_type = e.get("c4_type", "unknown")
+        type_counts[c4_type] = type_counts.get(c4_type, 0) + 1
+
+    return {
+        "system_count": type_counts.get("system", 0),
+        "container_count": type_counts.get("container", 0),
+        "component_count": type_counts.get("component", 0),
+        "relationship_count": len(relationships),
+        "total_entities": len(entities),
+    }
+
+
+def prepare_human_review_payload(state: RAAState) -> dict:
+    """Classify open questions and build a human review payload.
+
+    Reads ``open_questions`` from state, normalizes and classifies each question,
+    auto-generates suggested resolutions for judge-resolvable types, gathers
+    conflicting C4 elements from ``arch_model``, and computes model statistics.
+
+    Args:
+        state: Full RAA state with ``open_questions`` and ``arch_model`` channels.
+
+    Returns:
+        dict with key ``human_review_payload`` containing categorized questions,
+        conflicting elements, model statistics, and pre-computed resolutions.
+    """
+    raw_questions: list[dict] = list(state.get("open_questions") or [])
+    arch_model: dict = state.get("arch_model") or {}
+
+    classified: list[OpenQuestion] = []
+    for i, raw in enumerate(raw_questions):
+        classified.append(_normalize_question(raw, i))
+
+    # Build pre-computed resolutions map
+    pre_computed_resolutions: dict[str, str] = {}
+    for q in classified:
+        if q.resolution_owner == "judge_resolvable" and q.resolution is not None:
+            pre_computed_resolutions[q.id] = q.resolution
+
+    conflicting_elements = _gather_conflicting_elements(raw_questions, arch_model)
+    model_statistics = _calculate_model_statistics(arch_model)
+
+    payload = {
+        "open_questions": [q.model_dump() for q in classified],
+        "conflicting_elements": conflicting_elements,
+        "model_statistics": model_statistics,
+        "pre_computed_resolutions": pre_computed_resolutions,
+    }
+
+    return {"human_review_payload": payload}

diff --git a/tests/raa/unit/test_human_review_gate.py b/tests/raa/unit/test_human_review_gate.py
new file mode 100644
index 0000000..c7e2874
--- /dev/null
+++ b/tests/raa/unit/test_human_review_gate.py
@@ -0,0 +1,388 @@
+"""
+Unit tests for human review gate node (Story 3.1).
+"""
+from __future__ import annotations
+
+import pytest
+
+from raa.nodes.human_review_gate import prepare_human_review_payload
+from raa.state.models import OpenQuestion
+
+
+# ── Helpers ─────────────────────────────────────────────────────────────────
+
+
+def _make_state(open_questions=None, arch_model=None):
+    return {
+        "batch_cursor": 0,
+        "quality_weights": {},
+        "requirements": {},
+        "asrs": [],
+        "non_asr": [],
+        "condition_groups": [],
+        "review_mode": "autonomous",
+        "normalized_asrs": [],
+        "normalized_non_asr": [],
+        "embeddings_ready": False,
+        "batch_outputs": [],
+        "open_questions": open_questions or [],
+        "incoherent_batches": [],
+        "arch_model": arch_model or {},
+        "judge_rankings": {},
+    }
+
+
+# ── Classification ──────────────────────────────────────────────────────────
+
+
+class TestClassification:
+    def test_change_risk_classified_as_human_preferred(self):
+        state = _make_state(open_questions=[
+            {"question_type": "change_risk", "description": "Risk of merging entities"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "human_preferred"
+
+    def test_high_coupling_classified_as_human_preferred(self):
+        state = _make_state(open_questions=[
+            {"question_type": "high_coupling", "description": "High coupling detected"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "human_preferred"
+
+    def test_coverage_gap_classified_as_human_preferred(self):
+        state = _make_state(open_questions=[
+            {"question_type": "coverage_gap", "description": "Coverage gap"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "human_preferred"
+
+    def test_contention_classified_as_judge_resolvable(self):
+        state = _make_state(open_questions=[
+            {"question_type": "contention", "description": "Strategy contention"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "judge_resolvable"
+
+    def test_tie_classified_as_judge_resolvable(self):
+        state = _make_state(open_questions=[
+            {"question_type": "tie", "description": "Tie between strategies"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "judge_resolvable"
+
+    def test_hierarchy_conflict_classified_as_judge_resolvable(self):
+        state = _make_state(open_questions=[
+            {"question_type": "hierarchy_conflict", "description": "Parent mismatch"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "judge_resolvable"
+
+    def test_scope_conflict_classified_as_judge_resolvable(self):
+        state = _make_state(open_questions=[
+            {"question_type": "scope_conflict", "description": "Scope conflict"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "judge_resolvable"
+
+    def test_unknown_type_defaults_to_human_preferred(self):
+        state = _make_state(open_questions=[
+            {"question_type": "unknown_thing", "description": "Something weird"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution_owner"] == "human_preferred"
+
+
+# ── Legacy Key Normalization ────────────────────────────────────────────────
+
+
+class TestLegacyKeyNormalization:
+    def test_maps_type_to_question_type(self):
+        state = _make_state(open_questions=[
+            {"type": "change_risk", "description": "Old format"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["question_type"] == "change_risk"
+
+    def test_question_type_takes_precedence_over_type(self):
+        state = _make_state(open_questions=[
+            {"question_type": "tie", "type": "change_risk", "description": "Has both"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["question_type"] == "tie"
+
+    def test_missing_both_defaults_to_unknown(self):
+        state = _make_state(open_questions=[
+            {"description": "No type at all"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["question_type"] == "unknown"
+        assert q["resolution_owner"] == "human_preferred"
+
+
+# ── Suggested Resolutions ───────────────────────────────────────────────────
+
+
+class TestSuggestedResolutions:
+    def test_hierarchy_conflict_suggestion(self):
+        state = _make_state(open_questions=[
+            {"question_type": "hierarchy_conflict", "description": "Mismatch"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution"] == "Use parent hierarchy from canonical entity."
+
+    def test_scope_conflict_suggestion(self):
+        state = _make_state(open_questions=[
+            {"question_type": "scope_conflict", "description": "Scope issue"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution"] == "Apply fallback constraints to adjust relationship scope."
+
+    def test_tie_suggestion(self):
+        state = _make_state(open_questions=[
+            {"question_type": "tie", "description": "Tiebreaker needed"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution"] == "Resolve tie by selecting the proposal from primary strategy (RAA-A SAAM-First)."
+
+    def test_contention_suggestion(self):
+        state = _make_state(open_questions=[
+            {"question_type": "contention", "description": "Contention detected"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution"] == "Consolidate entities using the primary strategy's structure as the ground truth."
+
+    def test_human_preferred_has_no_suggestion(self):
+        state = _make_state(open_questions=[
+            {"question_type": "change_risk", "description": "Risk"},
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["resolution"] is None
+
+
+# ── Conflicting Elements ────────────────────────────────────────────────────
+
+
+class TestConflictingElements:
+    def test_gathers_entity_a_id_and_entity_b_id(self):
+        state = _make_state(
+            open_questions=[
+                {
+                    "question_type": "change_risk",
+                    "description": "Risk",
+                    "entity_a_id": "svc-a",
+                    "entity_b_id": "svc-b",
+                },
+            ],
+            arch_model={
+                "entities": [
+                    {"id": "svc-a", "name": "Service A", "c4_type": "container"},
+                    {"id": "svc-b", "name": "Service B", "c4_type": "container"},
+                ],
+            },
+        )
+        result = prepare_human_review_payload(state)
+        elements = result["human_review_payload"]["conflicting_elements"]
+        assert len(elements) == 2
+        names = {e["name"] for e in elements}
+        assert names == {"Service A", "Service B"}
+
+    def test_gathers_promoted_component_id(self):
+        state = _make_state(
+            open_questions=[
+                {
+                    "question_type": "change_risk",
+                    "description": "No parent container",
+                    "promoted_component_id": "cc_security",
+                    "source": "cross_cutting_promotion",
+                },
+            ],
+            arch_model={
+                "entities": [
+                    {"id": "cc_security", "name": "Security (Cross-Cutting)", "c4_type": "component"},
+                ],
+            },
+        )
+        result = prepare_human_review_payload(state)
+        elements = result["human_review_payload"]["conflicting_elements"]
+        assert len(elements) == 1
+        assert elements[0]["name"] == "Security (Cross-Cutting)"
+
+    def test_entity_not_in_model_is_skipped(self):
+        state = _make_state(
+            open_questions=[
+                {"question_type": "change_risk", "description": "Risk", "entity_a_id": "nonexistent"},
+            ],
+            arch_model={"entities": []},
+        )
+        result = prepare_human_review_payload(state)
+        elements = result["human_review_payload"]["conflicting_elements"]
+        assert elements == []
+
+    def test_deduplicates_referenced_ids(self):
+        state = _make_state(
+            open_questions=[
+                {"question_type": "change_risk", "description": "Risk 1", "entity_a_id": "svc-1"},
+                {"question_type": "change_risk", "description": "Risk 2", "entity_a_id": "svc-1"},
+            ],
+            arch_model={
+                "entities": [{"id": "svc-1", "name": "Service 1", "c4_type": "container"}],
+            },
+        )
+        result = prepare_human_review_payload(state)
+        elements = result["human_review_payload"]["conflicting_elements"]
+        assert len(elements) == 1
+
+
+# ── Model Statistics ────────────────────────────────────────────────────────
+
+
+class TestModelStatistics:
+    def test_counts_entity_types(self):
+        state = _make_state(
+            arch_model={
+                "entities": [
+                    {"id": "s1", "name": "System", "c4_type": "system"},
+                    {"id": "s2", "name": "External", "c4_type": "external_system"},
+                    {"id": "c1", "name": "Container 1", "c4_type": "container"},
+                    {"id": "c2", "name": "Container 2", "c4_type": "container"},
+                    {"id": "c3", "name": "Container 3", "c4_type": "container"},
+                    {"id": "comp1", "name": "Component", "c4_type": "component"},
+                ],
+                "relationships": [
+                    {"id": "r1", "source_id": "c1", "target_id": "c2"},
+                    {"id": "r2", "source_id": "c1", "target_id": "c3"},
+                ],
+            },
+        )
+        result = prepare_human_review_payload(state)
+        stats = result["human_review_payload"]["model_statistics"]
+        assert stats["system_count"] == 1
+        assert stats["container_count"] == 3
+        assert stats["component_count"] == 1
+        assert stats["relationship_count"] == 2
+        assert stats["total_entities"] == 6
+
+    def test_empty_model_returns_zeros(self):
+        state = _make_state(arch_model={})
+        result = prepare_human_review_payload(state)
+        stats = result["human_review_payload"]["model_statistics"]
+        assert stats["system_count"] == 0
+        assert stats["container_count"] == 0
+        assert stats["component_count"] == 0
+        assert stats["relationship_count"] == 0
+        assert stats["total_entities"] == 0
+
+
+# ── Pre-computed Resolutions ────────────────────────────────────────────────
+
+
+class TestPreComputedResolutions:
+    def test_maps_question_ids_to_suggestions(self):
+        state = _make_state(open_questions=[
+            {"question_type": "tie", "description": "Tie"},
+            {"question_type": "hierarchy_conflict", "description": "Conflict"},
+            {"question_type": "change_risk", "description": "Risk"},
+        ])
+        result = prepare_human_review_payload(state)
+        resolutions = result["human_review_payload"]["pre_computed_resolutions"]
+        assert len(resolutions) == 2  # only judge_resolvable
+        assert "q_0_tie" in resolutions
+        assert "q_1_hierarchy_conflict" in resolutions
+        assert "q_2_change_risk" not in resolutions
+
+
+# ── Payload Structure ───────────────────────────────────────────────────────
+
+
+class TestPayloadStructure:
+    def test_payload_has_all_required_keys(self):
+        state = _make_state(open_questions=[
+            {"question_type": "change_risk", "description": "Test"},
+        ])
+        result = prepare_human_review_payload(state)
+        payload = result["human_review_payload"]
+        assert "open_questions" in payload
+        assert "conflicting_elements" in payload
+        assert "model_statistics" in payload
+        assert "pre_computed_resolutions" in payload
+
+    def test_returns_dict_with_human_review_payload_key(self):
+        state = _make_state()
+        result = prepare_human_review_payload(state)
+        assert isinstance(result, dict)
+        assert "human_review_payload" in result
+        assert isinstance(result["human_review_payload"], dict)
+
+
+# ── Empty/Edge Cases ────────────────────────────────────────────────────────
+
+
+class TestEdgeCases:
+    def test_empty_open_questions_produces_empty_list(self):
+        state = _make_state(open_questions=[])
+        result = prepare_human_review_payload(state)
+        payload = result["human_review_payload"]
+        assert payload["open_questions"] == []
+        assert payload["pre_computed_resolutions"] == {}
+        assert payload["conflicting_elements"] == []
+
+    def test_preserves_question_context(self):
+        state = _make_state(open_questions=[
+            {
+                "question_type": "change_risk",
+                "description": "Risk",
+                "entity_a_id": "svc-1",
+                "severity": "high",
+                "source": "deduplication",
+            },
+        ])
+        result = prepare_human_review_payload(state)
+        q = result["human_review_payload"]["open_questions"][0]
+        assert q["context"]["entity_a_id"] == "svc-1"
+        assert q["context"]["severity"] == "high"
+        assert q["context"]["source"] == "deduplication"
+
+    def test_multiple_questions_get_deterministic_ids(self):
+        state = _make_state(open_questions=[
+            {"question_type": "change_risk", "description": "Risk"},
+            {"question_type": "tie", "description": "Tie"},
+            {"question_type": "contention", "description": "Contention"},
+        ])
+        result = prepare_human_review_payload(state)
+        ids = [q["id"] for q in result["human_review_payload"]["open_questions"]]
+        assert ids == ["q_0_change_risk", "q_1_tie", "q_2_contention"]
+
+    def test_deterministic_same_input_same_output(self):
+        state = _make_state(
+            open_questions=[
+                {"question_type": "tie", "description": "Tie", "entity_a_id": "a", "entity_b_id": "b"},
+                {"question_type": "change_risk", "description": "Risk", "entity_a_id": "c"},
+            ],
+            arch_model={
+                "entities": [
+                    {"id": "a", "name": "A", "c4_type": "system"},
+                    {"id": "b", "name": "B", "c4_type": "container"},
+                    {"id": "c", "name": "C", "c4_type": "component"},
+                ],
+            },
+        )
+        r1 = prepare_human_review_payload(state)
+        r2 = prepare_human_review_payload(state)
+        assert r1 == r2

```
