"""RAA batch queue ordering node — sort batches by risk, ASR count, or quality weight.

Section 11 of RAA_Plan.md.  Reads the batch queue and reorders it according to
the active ``batch_ordering_strategy`` pipeline parameter:

- ``risk_first`` (default): batches with high-risk quality attributes first.
- ``asr_count``: batches with the most ASR requirements first.
- ``quality_weight``: batches with the highest summed ARLO quality weight first.

Every output batch receives a ``sorting_metadata`` dict.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

DEFAULT_BATCH_ORDERING_STRATEGY = "risk_first"
VALID_BATCH_ORDERING_STRATEGIES: set[str] = {
    "risk_first",
    "asr_count",
    "quality_weight",
}
RISK_PRIORITY: dict[str, int] = {
    "security": 4,
    "reliability": 3,
    "performance": 2,
    "usability": 1,
}


# ---------------------------------------------------------------------------
# Strategy normalisation
# ---------------------------------------------------------------------------
def _normalize_strategy(strategy: object) -> str:
    """Return a valid strategy string, falling back to *risk_first*.

    Logs a warning when the supplied value is missing or unrecognised.
    """
    if not isinstance(strategy, str):
        logger.warning(
            "batch_ordering_strategy %r is not a string — falling back to %r.",
            strategy,
            DEFAULT_BATCH_ORDERING_STRATEGY,
        )
        return DEFAULT_BATCH_ORDERING_STRATEGY

    s = strategy.strip().lower()
    if s not in VALID_BATCH_ORDERING_STRATEGIES:
        logger.warning(
            "Unknown batch_ordering_strategy %r — falling back to %r.",
            strategy,
            DEFAULT_BATCH_ORDERING_STRATEGY,
        )
        return DEFAULT_BATCH_ORDERING_STRATEGY

    return s


# ---------------------------------------------------------------------------
# ID helpers
# ---------------------------------------------------------------------------
def _requirement_id(requirement_or_id: object) -> str | None:
    """Normalise a requirement ID to string form."""
    if isinstance(requirement_or_id, dict):
        rid = requirement_or_id.get("id")
    else:
        rid = requirement_or_id
    return str(rid) if rid is not None else None


def _asr_id_set(asrs: list[dict]) -> set[str]:
    """Build a set of ASR requirement ID strings from the state ASR list."""
    return {
        str(a["id"])
        for a in asrs
        if a.get("id") is not None
    }


# ---------------------------------------------------------------------------
# ASR detection
# ---------------------------------------------------------------------------
def _is_asr_requirement(requirement: dict, asr_ids: set[str]) -> bool:
    """Determine whether a requirement dict is an ASR."""
    if requirement.get("is_asr") is True:
        return True
    if requirement.get("is_architecturally_significant") is True:
        return True
    rid = _requirement_id(requirement)
    if rid and rid in asr_ids:
        return True
    return False


def _quality_attributes(requirement: dict) -> list[str]:
    """Extract quality attribute names from a requirement.

    Prefers the plural ``quality_attributes`` list.  Falls back to the
    singular ``quality_attribute`` string (wrapped in a list).
    """
    qa = requirement.get("quality_attributes")
    if qa and isinstance(qa, list):
        return [str(a) for a in qa]
    sing = requirement.get("quality_attribute")
    if sing:
        return [str(sing)]
    return []


# ---------------------------------------------------------------------------
# Scoring strategies
# ---------------------------------------------------------------------------
def _risk_first_score(batch: dict, asr_ids: set[str]) -> float:
    """Max risk priority across ASR requirements in the batch.

    Security=4, Reliability=3, Performance=2, Usability=1, others=0.
    """
    best = 0
    for req in batch.get("requirements", []):
        if not _is_asr_requirement(req, asr_ids):
            continue
        for attr in _quality_attributes(req):
            priority = RISK_PRIORITY.get(attr.lower(), 0)
            if priority > best:
                best = priority
    return float(best)


def _asr_count_score(batch: dict, asr_ids: set[str]) -> float:
    """Number of ASR requirements in the batch (non-ASR excluded)."""
    return float(
        sum(1 for r in batch.get("requirements", []) if _is_asr_requirement(r, asr_ids))
    )


def _quality_weight_score(
    batch: dict,
    quality_weights: dict[str, int],
    asr_ids: set[str],
) -> float:
    """Sum of case-insensitive quality weights for ASR requirement attributes."""
    total = 0
    for req in batch.get("requirements", []):
        if not _is_asr_requirement(req, asr_ids):
            continue
        for attr in _quality_attributes(req):
            for qk, qv in quality_weights.items():
                if qk.lower() == attr.lower():
                    total += qv
    return float(total)


# ---------------------------------------------------------------------------
# Tie-breaker
# ---------------------------------------------------------------------------
def _batch_tie_breaker(batch: dict) -> str:
    """Lexicographic tie-breaker — *group_id* first, then *batch_id*."""
    gid = batch.get("group_id")
    if gid is not None:
        return str(gid)
    return str(batch.get("batch_id", ""))


# ---------------------------------------------------------------------------
# Score dispatch
# ---------------------------------------------------------------------------
def _calculate_ordering_score(
    batch: dict,
    strategy: str,
    quality_weights: dict[str, int],
    asr_ids: set[str],
) -> float:
    """Dispatch to the correct scoring function based on *strategy*."""
    if strategy == "asr_count":
        return _asr_count_score(batch, asr_ids)
    if strategy == "quality_weight":
        return _quality_weight_score(batch, quality_weights, asr_ids)
    return _risk_first_score(batch, asr_ids)


# ---------------------------------------------------------------------------
# Annotation + ordering
# ---------------------------------------------------------------------------
def _annotate_batch(
    batch: dict,
    score: float,
    strategy: str,
    tie_breaker: str,
) -> dict:
    """Return a shallow copy of *batch* with ``sorting_metadata`` attached."""
    annotated = {**batch}
    annotated["sorting_metadata"] = {
        "score": score,
        "strategy": strategy,
        "tie_breaker": tie_breaker,
    }
    return annotated


def _ordered_batches(
    batches: list[dict],
    strategy: str,
    quality_weights: dict[str, int],
    asr_ids: set[str],
) -> list[dict]:
    """Annotate and sort batches by descending score, ascending tie-breaker."""
    annotated: list[dict] = []
    for b in batches:
        score = _calculate_ordering_score(b, strategy, quality_weights, asr_ids)
        tb = _batch_tie_breaker(b)
        annotated.append(_annotate_batch(b, score, strategy, tb))

    annotated.sort(key=lambda b: (
        -b["sorting_metadata"]["score"],
        b["sorting_metadata"]["tie_breaker"],
    ))
    return annotated


# ---------------------------------------------------------------------------
# Node entry point
# ---------------------------------------------------------------------------
def order_batch_queue(state: dict) -> dict:
    """Node: order the batch execution queue.

    Reads ``batch_queue``, ``batch_ordering_strategy``, ``quality_weights``,
    and ``asrs`` from *state*.  Returns ``{"batch_queue": ordered_batches}``.
    """
    batch_queue: list[dict] = list(state.get("batch_queue", []))
    raw_strategy = state.get("batch_ordering_strategy")
    quality_weights: dict[str, int] = state.get("quality_weights", {})
    asrs: list[dict] = state.get("asrs", [])

    strategy = _normalize_strategy(raw_strategy)
    asr_ids = _asr_id_set(asrs)

    ordered = _ordered_batches(batch_queue, strategy, quality_weights, asr_ids)

    logger.info(
        "Ordered %d batches with strategy %r.", len(ordered), strategy,
    )
    return {"batch_queue": ordered}
