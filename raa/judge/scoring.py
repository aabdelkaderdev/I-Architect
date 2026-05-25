"""
Pure SAAM-first fragment scoring and ranking (Story 2.3).

No LLM calls, no SQLite access, no embedding access, no merge, no cursor
advancement. Scoring consumes ``ArchFragment`` records and ``quality_weights``
and produces deterministic ``FragmentScore`` outputs.

``matrix.json`` is *not* consumed in this story. The pattern-to-quality-attribute
matrix maps architectural patterns to quality scores, but the primary SAAM scoring
path uses ``quality_weights`` directly per FR-10. Later stories that add
pattern-based scoring can reference the matrix via ``raa/utils/matrix_loader.py``
(not yet created).
"""
from __future__ import annotations

from raa.state.models import ArchFragment, FragmentScore, SAAMScenario
from raa.utils.constants import (
    SAAM_REDUCED_CONFIDENCE_MULTIPLIER,
    SAAM_SATISFACTION_FACTORS,
    SAAM_STRATEGY_ORDER,
)


def _resolve_arch_fragment(record: dict | ArchFragment) -> ArchFragment | None:
    """Accept either a dict or ArchFragment and return an ArchFragment or None."""
    if isinstance(record, ArchFragment):
        return record
    if isinstance(record, dict):
        frag = record.get("arch_fragment")
        if frag is None:
            return None
        if isinstance(frag, ArchFragment):
            return frag
        if isinstance(frag, dict):
            try:
                return ArchFragment(**frag)
            except Exception:
                return None
    return None


def _extract_strategy(record: dict | ArchFragment) -> str:
    if isinstance(record, dict):
        return record.get("strategy", "")
    return getattr(record, "strategy", "")


def _normalize_quality_keys(quality_weights: dict[str, int]) -> dict[str, int]:
    """Lowercase-normalize quality weight keys for case-insensitive matching.

    Original keys are preserved in output metadata via the quality_weights
    dict passed from the caller, which is never mutated.
    """
    return {k.strip().lower(): v for k, v in quality_weights.items()}


def _satisfaction_factor(satisfaction: str) -> float:
    """Map a satisfaction string to its numeric factor.

    Returns 0.0 for unrecognised values per explicit handling requirement.
    """
    key = str(satisfaction or "").strip().lower()
    return SAAM_SATISFACTION_FACTORS.get(key, 0.0)


def _score_scenario(
    scenario: SAAMScenario,
    normalized_weights: dict[str, int],
) -> float:
    """Score a single SAAM scenario against quality weights.

    Contribution = sum(matching quality weights) * satisfaction factor.
    """
    total_weight = 0
    for attr in scenario.quality_attributes or []:
        attr_str = str(attr or "").strip().lower()
        total_weight += normalized_weights.get(attr_str, 0)
    return total_weight * _satisfaction_factor(scenario.satisfaction)


def _score_by_requirement_coverage(
    fragment: ArchFragment,
    normalized_weights: dict[str, int],
) -> tuple[float, list[dict], str]:
    """Fallback scoring when no SAAM scenarios are present.

    Scores by summing unique requirement IDs from entities (flat weight of 1.0
    per requirement ID). This is a simplified fallback design because the scorer
    runs as a pure function without access to the full requirements database mapping.
    """
    all_req_ids: set[str] = set()
    for entity in fragment.entities:
        for req_id in entity.requirement_ids:
            all_req_ids.add(req_id)

    contributions: list[dict] = []
    raw = 0.0
    for req_id in sorted(all_req_ids):
        # Each requirement gets a base weight of 1; this is a fallback heuristic.
        # Quality weights matching happens when entities declare requirement_ids
        # that trace back to source requirements with known quality attributes.
        raw += 1.0
        contributions.append({
            "requirement_id": req_id,
            "weight": 1.0,
            "satisfaction": "unknown",
            "source": "requirement_coverage_fallback",
        })

    note = "score computed by requirement coverage — no SAAM scenarios present"
    if not contributions:
        note = "score is 0.0 — no SAAM scenarios and no entity requirement coverage"

    return raw, contributions, note


def score_fragment_record(
    record: dict | ArchFragment,
    quality_weights: dict[str, int],
) -> FragmentScore | None:
    """Score a single fragment record deterministically.

    Args:
        record: A ``batch_outputs`` record dict or an ``ArchFragment`` instance.
        quality_weights: ARLO quality attribute → frequency count mapping.

    Returns:
        ``FragmentScore`` if the record is scorable, ``None`` if it should be
        skipped (skipped=True or arch_fragment is None).
    """
    # ── Skip gate ────────────────────────────────────────────────────────
    if isinstance(record, dict):
        if record.get("skipped", False):
            return None
        if record.get("arch_fragment") is None:
            return None

    fragment = _resolve_arch_fragment(record)
    if fragment is None:
        return None

    # ── Extract metadata ─────────────────────────────────────────────────
    if isinstance(record, dict):
        batch_id = record.get("batch_id", "")
        batch_index = record.get("batch_index", 0)
        strategy = record.get("strategy", "")
        thread_id = record.get("thread_id", "")
        reduced_confidence = bool(record.get("reduced_confidence", False))
    else:
        batch_id = ""
        batch_index = 0
        strategy = ""
        thread_id = ""
        reduced_confidence = False

    normalized_weights = _normalize_quality_keys(quality_weights)

    # ── Score scenarios ──────────────────────────────────────────────────
    scenario_contributions: list[dict] = []
    raw_score = 0.0
    score_note = ""

    if fragment.saam_scenarios:
        for scenario in fragment.saam_scenarios:
            contrib = _score_scenario(scenario, normalized_weights)
            scenario_contributions.append({
                "scenario_id": scenario.id,
                "description": scenario.description,
                "quality_attributes": scenario.quality_attributes,
                "satisfaction": scenario.satisfaction,
                "contribution": contrib,
            })
            raw_score += contrib
    else:
        raw_score, scenario_contributions, score_note = _score_by_requirement_coverage(
            fragment, normalized_weights
        )
        if score_note:
            scenario_contributions.append({
                "source": "fallback_note",
                "note": score_note,
            })

    # ── Apply multiplier ─────────────────────────────────────────────────
    multiplier = SAAM_REDUCED_CONFIDENCE_MULTIPLIER if reduced_confidence else 1.0
    final_score = raw_score * multiplier

    return FragmentScore(
        batch_id=batch_id,
        batch_index=batch_index,
        strategy=strategy,
        thread_id=thread_id,
        raw_score=raw_score,
        multiplier=multiplier,
        final_score=final_score,
        scenario_contributions=scenario_contributions,
        is_primary=False,  # set by rank_batch_fragments
    )


def rank_batch_fragments(
    records: list[dict],
    quality_weights: dict[str, int],
) -> dict:
    """Score and rank a list of batch output records.

    Args:
        records: List of ``batch_outputs`` records from the dispatch node.
        quality_weights: ARLO quality attribute → frequency count mapping.

    Returns:
        dict with keys:
        - ``scored_fragments``: list of ``FragmentScore`` sorted by rank
          (highest final_score first, then tie-break by strategy order, then
          thread_id).
        - ``skipped_fragments``: list of skip metadata dicts for records
          that were excluded from scoring.
        - ``primary_fragment``: the highest-ranked ``FragmentScore``, or
          ``None`` if nothing was scored.
    """
    scored: list[FragmentScore] = []
    skipped: list[dict] = []

    for record in records:
        score = score_fragment_record(record, quality_weights)
        if score is None:
            if isinstance(record, dict):
                skipped.append({
                    "batch_id": record.get("batch_id", ""),
                    "batch_index": record.get("batch_index", 0),
                    "strategy": record.get("strategy", ""),
                    "thread_id": record.get("thread_id", ""),
                    "skip_reason": record.get("skip_reason") or "skipped_or_null_fragment",
                })
            continue
        scored.append(score)

    # ── Sort: highest final_score, then strategy tie-break, then thread_id
    _strategy_rank = {s: i for i, s in enumerate(SAAM_STRATEGY_ORDER)}

    def _sort_key(fs: FragmentScore) -> tuple:
        # Negate final_score for descending sort
        return (
            -fs.final_score,
            _strategy_rank.get(fs.strategy, 99),
            fs.thread_id or "",
        )

    scored.sort(key=_sort_key)

    # ── Mark primary ─────────────────────────────────────────────────────
    primary = scored[0] if scored else None
    if primary is not None:
        primary.is_primary = True

    return {
        "scored_fragments": scored,
        "skipped_fragments": skipped,
        "primary_fragment": primary,
    }
