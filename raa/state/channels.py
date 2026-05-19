"""
RAA state channels and custom reducers.

Defines RAAState TypedDict with all channels from RAA_Plan.md Section 4
(New State Channels table) plus reused ARLO channels. Multi-writer channels
use Annotated reducers to prevent last-write-wins data loss during parallel
Send API super-steps.
"""
from __future__ import annotations

from operator import add
from typing import Annotated

from typing_extensions import TypedDict

from raa.state.types import (
    ArchFragment,
    ArchModel,
    Batch,
    IncoherentBatchRecord,
    OpenQuestion,
)


def merge_batch_outputs(
    left: dict[int, list[ArchFragment]],
    right: dict[int, list[ArchFragment]],
) -> dict[int, list[ArchFragment]]:
    """Dict-merge reducer for batch_outputs channel.

    Concatenates fragment lists per batch index key. When the same key
    exists in both dicts, the two lists are concatenated. Keys present
    in only one dict are copied as-is.

    Used by parallel RAA subgraphs (A, B, C) writing to batch_outputs
    in the same super-step. Without this reducer, LangGraph's default
    last-write-wins would silently discard two of the three outputs.
    """
    merged = {**left}
    for key, value in right.items():
        if key in merged:
            merged[key] = merged[key] + value
        else:
            merged[key] = list(value)
    return merged


def merge_best_batch_output(
    left: dict[int, ArchFragment],
    right: dict[int, ArchFragment],
) -> dict[int, ArchFragment]:
    """Dict-merge reducer for best_batch_output channel.

    When the same batch index key appears in both dicts (unexpected,
    since only the judge writes per batch), prefers the fragment with
    more total C4 entities as a confidence proxy. Keys present in only
    one dict are copied as-is.
    """
    merged = {**left}
    for key, fragment in right.items():
        if key in merged:
            existing = merged[key]
            existing_count = (
                len(existing.systems)
                + len(existing.containers)
                + len(existing.components)
            )
            candidate_count = (
                len(fragment.systems)
                + len(fragment.containers)
                + len(fragment.components)
            )
            if candidate_count > existing_count:
                merged[key] = fragment
        else:
            merged[key] = fragment
    return merged


class RAAState(TypedDict, total=False):
    """Full RAA graph state.

    Single-writer channels use plain types (default overwrite behaviour).
    Multi-writer channels use Annotated[type, reducer] so concurrent
    writes in the same super-step merge instead of overwriting.

    Reused ARLO channels (asrs, non_asr, condition_groups, quality_weights)
    are provided by the parent pipeline via ARLOOutput and read by RAA
    nodes for batch construction and scoring.
    """

    # --- New State Channels (§4 New State Channels table) ---

    # Single-writer (default overwrite)
    batch_queue: list[Batch]
    batch_cursor: int
    running_arch_model: ArchModel
    bridge_requirements: dict[tuple, list[str]]
    embeddings_ready: bool

    # Multi-writer (append reducers)
    open_questions: Annotated[list[OpenQuestion], add]
    incoherent_batches: Annotated[list[IncoherentBatchRecord], add]

    # Multi-writer (dict-merge reducers)
    batch_outputs: Annotated[dict[int, list[ArchFragment]], merge_batch_outputs]
    best_batch_output: Annotated[dict[int, ArchFragment], merge_best_batch_output]

    # --- Reused ARLO Channels (§4 Existing State Reused from ARLO table) ---
    asrs: list[dict]
    non_asr: list[dict]
    condition_groups: list[dict]
    quality_weights: dict[str, int]
