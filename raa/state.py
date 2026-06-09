"""LangGraph state definition for RAA graph nodes.

State carries the live entity_registry, current batch index, accumulated
BatchOutput list, and per-batch working state. Only the Judge mutates the
live registry. Subgraphs read via frozen snapshots.

RAAConfigSchema is re-exported for convenience — callers inject runtime
LLM instances and checkpoint config via RunnableConfig.configurable.
"""

from __future__ import annotations

from typing import Annotated, NotRequired, TypedDict

from raa.types import (
    BatchInput,
    BatchOutput,
    EntityProposal,
    RAAConfigSchema,
    RAAOutput,
    RegistryEntry,
)

__all__ = ["RAAConfigSchema", "RAAState"]


def _append_lists(left: list | None, right: list | None) -> list:
    """Append accumulator channel lists without mutating either input."""
    return list(left or []) + list(right or [])


class RAAState(TypedDict):
    """Internal graph state flowing through all RAA nodes.

    Populated by the Orchestrator before first invocation. Mutated by graph nodes
    at defined boundaries: only the Judge writes to entity_registry, subgraphs
    write to per-batch proposal fields.
    """

    # ── Cross-batch persistent state ──

    entity_registry_entries: Annotated[list[RegistryEntry], _append_lists]
    # Accumulated registry entries across all batches. Each batch's Judge appends
    # only its new entries. Converted to dict at read time (keyed by canonical_id).
    # Only the Judge node appends to this channel.

    batches: list[BatchInput]
    # Ordered batch list: concern batches first, Foundation batch last.
    # Set once before the batch loop. Immutable after construction.

    batch_index: int
    # Index into batches for the current iteration. Starts at 0.
    # Incremented by the routing node after each Judge completes.

    batch_outputs: Annotated[list[BatchOutput], _append_lists]
    # Accumulated outputs from completed batches. Concern outputs first,
    # Foundation output last. Used by the Assembler to produce RAAOutput.

    # ── Per-batch ephemeral state (reset each iteration) ──

    asr_proposals: NotRequired[list[EntityProposal]]
    # Proposals from the ASR Subgraph for the current batch.

    non_asr_proposals: NotRequired[list[EntityProposal]]
    # Proposals from the Non-ASR Subgraph for the current batch.

    # ── Pre-computed (carried for potential resume) ──

    group_vectors: NotRequired[dict[str, list[float]]]
    # Pre-computed condition group vectors from the embedding phase.

    # ── Final output (set by Assembler) ──

    raa_output: NotRequired[RAAOutput]
    # Final assembled output. Set by the Assembler node after all batches complete.

    _last_written_batch_id: NotRequired[str]
    # Audit marker for the last batch whose Judge node wrote to the registry.
