"""
Three-schema state pattern for the ARLO subgraph.

- ARLOInput:  What the parent pipeline provides (4 keys).
- ARLOOutput: What the parent pipeline receives (4 keys).
- ARLOState:  Full internal state — all intermediate data hidden from external callers.

Private-state TypedDicts (EquivalenceOutput, GroupBuilderInput) are used for
transient data between adjacent nodes via add_sequence. The mechanism requires
explicit return/parameter type annotations on the node functions:

    def check_condition_equivalence(state: ARLOState) -> EquivalenceOutput: ...
    def build_condition_groups(state: GroupBuilderInput) -> dict: ...
"""
from __future__ import annotations

from operator import add
from typing import Annotated, Any, Dict

from typing_extensions import NotRequired, TypedDict


# ---------------------------------------------------------------------------
# Input Schema — provided by the parent pipeline
# ---------------------------------------------------------------------------
class ARLOInput(TypedDict):
    """Input schema for ARLO subgraph. Provided by the parent pipeline."""
    requirements: Dict[str, str]          # Mapping of Requirement ID → description
    experiment_config: dict               # Includes optimizer, mode, batch_size, etc.
    matrix: dict[str, dict[str, int]]     # Pre-loaded quality–architecture pattern matrix
    llm: NotRequired[Any]  # Dev fallback only. Do not pass when checkpointing.


# ---------------------------------------------------------------------------
# Runtime Context — not checkpointed, passed via context={"llm": llm}
# ---------------------------------------------------------------------------
class ARLOContext(TypedDict, total=False):
    """Runtime-only dependencies that must not be checkpointed.

    - llm: Pre-instantiated LangChain ChatModel (required).
    - progress_callback: Orchestrator-injected callback for batch progress
      reporting (§8D). Signature: (batch: int, total: int) -> None.
    - cancellation_flag: Orchestrator-injected threading.Event for graceful
      cancellation at batch boundaries (§4E).
    """
    llm: Any
    progress_callback: Any   # Callable[[int, int], None] | None
    cancellation_flag: Any   # threading.Event | None


# ---------------------------------------------------------------------------
# Output Schema — returned to the parent pipeline
# ---------------------------------------------------------------------------
class ARLOOutput(TypedDict):
    """Output schema for ARLO subgraph. Returned to the parent pipeline.

    The orchestrator threads these channels to downstream agents (§4B):
    - asrs → RAA.asrs
    - non_asr → RAA.non_asr (via requirements_data packing)
    - condition_groups → RAA.condition_groups
    - quality_weights → RAA.quality_weights (via requirements_data packing)
    - concerns → RGA (for reporting)
    - stats → RGA (for reporting)
    """
    concerns: list[dict]
    stats: dict
    asrs: list[dict]
    non_asr: list[dict]                        # Non-ASR requirement dictionaries
    condition_groups: list[dict]              # Condition groups for RAA
    quality_weights: dict[str, int]


# ---------------------------------------------------------------------------
# Full Internal State
# ---------------------------------------------------------------------------
class ARLOState(ARLOInput, ARLOOutput):
    """Full internal state — all intermediate data hidden from external callers."""

    # Stage 1: Parsing
    asrs: list[dict]
    non_asr: list[dict]                            # Non-ASR requirement dictionaries
    parsing_stats: dict                           # {total, asr_count}

    # Stage 2: Embedding & Clustering
    embeddings: list[list[float]]
    cluster_assignments: list[int]

    # Stage 3: Condition / Satisfiable Grouping
    condition_groups: list[dict]
    satisfiable_groups: list[dict]
    sat_group_response: str                       # Raw LLM response text
    sat_parse_attempts: int
    sat_parse_success: bool

    # Stage 4: Optimization
    quality_weights: dict[str, int]
    decisions: list[dict]

    # Stage 5: Output (reducer for parallel / multi-node contribution)
    # The `add` reducer is essential here — parallel concern_workers append.
    concerns: Annotated[list[dict], add]


# ---------------------------------------------------------------------------
# Worker State — per-instance state slice for Send API fan-out
# ---------------------------------------------------------------------------
class ConcernWorkerState(TypedDict):
    """State slice received by each concern_worker via Send API."""
    satisfiable_group: dict
    matrix: dict[str, dict[str, int]]
    experiment_config: dict
    concerns: Annotated[list[dict], add]   # Writes back to ARLOState via add reducer


# ---------------------------------------------------------------------------
# Private State — transient data between adjacent nodes via add_sequence
# ---------------------------------------------------------------------------
class EquivalenceOutput(TypedDict):
    """Return type for check_condition_equivalence. Private channel."""
    similarity_matrix: list[tuple[int, int, bool]]   # (i, j, is_equivalent)


class GroupBuilderInput(TypedDict):
    """Input type for build_condition_groups. Receives private channel data."""
    similarity_matrix: list[tuple[int, int, bool]]
    cluster_assignments: list[int]
    asrs: list[dict]


# ---------------------------------------------------------------------------
# Overwrite Note
# ---------------------------------------------------------------------------
# The `Overwrite` wrapper bypasses a reducer and directly replaces a state value.
# This is meaningful only for keys that HAVE a reducer (like `concerns` with `add`).
#
# Example: In the VaryingRequirements experiment, if you need to reset the
# accumulated concerns list between removal rounds:
#
#   from langgraph.types import Overwrite
#   return {"concerns": Overwrite([])}  # Reset instead of appending
#
# Do NOT use Overwrite on keys without a reducer (e.g., `asrs`) — the default
# behavior is already overwrite.
