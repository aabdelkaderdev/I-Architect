"""
Judge reconciliation node (Story 2.3).

Selects the primary fragment for the current batch via SAAM scoring but
does NOT merge, deduplicate, or advance ``batch_cursor``.
"""
from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig

from raa.judge.scoring import rank_batch_fragments
from raa.state.schemas import RAAState


def select_primary_fragment(
    state: RAAState,
    config: RunnableConfig | None = None,
) -> dict[str, Any]:
    """Score and rank fragments for the current batch, selecting a primary.

    Does NOT:
    - Return ``batch_cursor``
    - Update ``arch_model``
    - Perform deduplication or boundary grouping
    """
    batch_outputs: list[dict] = state.get("batch_outputs") or []
    batch_cursor = state.get("batch_cursor", 0)
    quality_weights: dict[str, int] = state.get("quality_weights") or {}

    # Filter to records for the current batch_cursor only
    current_batch = [
        r for r in batch_outputs
        if isinstance(r, dict) and r.get("batch_index") == batch_cursor
    ]

    result = rank_batch_fragments(current_batch, quality_weights)

    # Store auditable ranking results; key is batch_cursor for later lookup
    existing_rankings = dict(state.get("judge_rankings") or {})
    existing_rankings[batch_cursor] = result

    return {"judge_rankings": existing_rankings}
