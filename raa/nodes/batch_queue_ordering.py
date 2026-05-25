"""
Phase 5 node: Risk-first queue ordering (FR-6).

Sorts coherent and reduced-confidence batches into an execution queue
by risk, with support for alternative ordering strategies.
"""
from __future__ import annotations

import logging

from langchain_core.runnables import RunnableConfig

from raa.state.schemas import RAAState

logger = logging.getLogger(__name__)

_SUPPORTED_STRATEGIES = {"risk", "asr_count", "quality_weight_frequency"}


def order_batch_queue(state: RAAState, config: RunnableConfig) -> dict:
    """Order batches into a risk-prioritised execution queue.

    Config keys expected in ``config["configurable"]``:
        ``queue_sort_strategy`` (optional, defaults to ``"risk"``)

    Returns:
        dict with keys ``execution_queue`` and ``unprocessed_requirements``.
    """
    configurable = config.get("configurable") or {}
    strategy = configurable.get("queue_sort_strategy", "risk")

    if strategy not in _SUPPORTED_STRATEGIES:
        raise ValueError(
            f"Unsupported queue sort strategy: {strategy!r}. "
            f"Must be one of: {', '.join(sorted(_SUPPORTED_STRATEGIES))}"
        )

    batches = state.get("batches") or []
    quality_weights = state.get("quality_weights") or {}

    # Build sort key per strategy
    if strategy == "risk":
        ordered = sorted(batches, key=lambda b: _risk_sort_key(b, quality_weights))
    elif strategy == "asr_count":
        ordered = sorted(batches, key=lambda b: _asr_count_sort_key(b, quality_weights))
    else:  # quality_weight_frequency
        ordered = sorted(batches, key=lambda b: _quality_weight_freq_sort_key(b, quality_weights))

    # Collect unprocessed requirements
    assigned_ids: set[str] = set()
    for batch in ordered:
        assigned_ids.update(batch.get("asr_ids", []))
        assigned_ids.update(batch.get("non_asr_ids", []))

    leftovers = [
        rec for rec in state.get("normalized_asrs", []) + state.get("normalized_non_asr", [])
        if rec.get("id") not in assigned_ids
    ]

    return {"execution_queue": ordered, "unprocessed_requirements": leftovers}


# ── Private helpers ─────────────────────────────────────────────────────────


def _has_security_or_reliability(records: list[dict]) -> bool:
    """Check case-insensitively whether any record has security or reliability attributes."""
    for rec in records:
        attrs = rec.get("quality_attributes") or []
        for attr in attrs:
            if isinstance(attr, str) and attr.lower() in ("security", "reliability"):
                return True
    return False


def _quality_attribute_frequencies(records: list[dict], weights: dict[str, int]) -> float:
    """Sum weighted quality attribute frequencies across all records."""
    total = 0.0
    for rec in records:
        attrs = rec.get("quality_attributes") or []
        for attr in attrs:
            if isinstance(attr, str):
                total += weights.get(attr, 1)
    return total


def _asr_count(batch: dict) -> int:
    return len(batch.get("asr_ids", []))


def _risk_sort_key(batch: dict, quality_weights: dict[str, int]) -> tuple:
    """Sort key for default risk ordering.

    Security/reliability first, then descending weighted risk score,
    then descending ASR count, then ascending group_id.
    """
    all_records = batch.get("asr_records", []) + batch.get("non_asr_records", [])
    has_sec_rel = _has_security_or_reliability(all_records)
    risk_score = _quality_attribute_frequencies(all_records, quality_weights)
    return (
        0 if has_sec_rel else 1,   # security/reliability batches first
        -risk_score,                # descending risk
        -_asr_count(batch),         # descending ASR count
        batch.get("group_id", ""),  # ascending group_id
    )


def _asr_count_sort_key(batch: dict, quality_weights: dict[str, int]) -> tuple:
    """Sort key for asr_count strategy: descending ASR count, then default risk tie-breakers."""
    all_records = batch.get("asr_records", []) + batch.get("non_asr_records", [])
    has_sec_rel = _has_security_or_reliability(all_records)
    risk_score = _quality_attribute_frequencies(all_records, quality_weights)
    return (
        -_asr_count(batch),         # descending ASR count
        0 if has_sec_rel else 1,
        -risk_score,
        batch.get("group_id", ""),
    )


def _quality_weight_freq_sort_key(batch: dict, quality_weights: dict[str, int]) -> tuple:
    """Sort key for quality_weight_frequency: descending total weighted freq, then default risk tie-breakers."""
    all_records = batch.get("asr_records", []) + batch.get("non_asr_records", [])
    has_sec_rel = _has_security_or_reliability(all_records)
    risk_score = _quality_attribute_frequencies(all_records, quality_weights)
    freq_score = _quality_attribute_frequencies(all_records, quality_weights)
    return (
        -freq_score,                # descending weighted frequency
        0 if has_sec_rel else 1,
        -risk_score,
        batch.get("group_id", ""),
    )
