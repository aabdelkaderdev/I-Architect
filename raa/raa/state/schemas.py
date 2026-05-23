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
