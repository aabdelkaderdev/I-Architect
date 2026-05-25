"""
Judge reconciliation node (Story 2.3 + 2.4 + 2.5).

Scores and ranks fragments via SAAM, deduplicates and merges the primary
fragment into the running ``arch_model``, promotes cross-cutting concerns,
calibrates per-entity SAAM scores, and advances ``batch_cursor``.
"""
from __future__ import annotations

import os
from typing import Any

from langchain_core.runnables import RunnableConfig

from raa.judge.cross_cutting import promote_all_cross_cutting
from raa.judge.deduplication import deduplicate_and_merge_fragment
from raa.judge.saam_calibration import calibrate_entity_saam_scores
from raa.judge.scoring import rank_batch_fragments
from raa.state.schemas import RAAState
from raa.utils.constants import EMBEDDING_CACHE_DIR, EMBEDDING_MODEL_NAME
from raa.utils.embedding_cache import EmbeddingCache, get_embedding_model


def select_primary_fragment(
    state: RAAState,
    config: RunnableConfig | None = None,
) -> dict[str, Any]:
    """Score, rank, deduplicate, and merge the primary fragment.

    Returns partial state update with ``judge_rankings``, ``arch_model``,
    ``batch_cursor`` (incremented by 1), and any dedup ``open_questions``.
    """
    batch_outputs: list[dict] = state.get("batch_outputs") or []
    batch_cursor = state.get("batch_cursor", 0)
    quality_weights: dict[str, int] = state.get("quality_weights") or {}

    # Filter to records for the current batch_cursor only
    current_batch = [
        r
        for r in batch_outputs
        if isinstance(r, dict) and r.get("batch_index") == batch_cursor
    ]

    result = rank_batch_fragments(current_batch, quality_weights)

    # Store auditable ranking results
    existing_rankings = dict(state.get("judge_rankings") or {})
    existing_rankings[batch_cursor] = result

    # ── Story 2.4: Dedup and merge primary fragment into arch_model ──────
    primary = result.get("primary_fragment")
    open_questions: list[dict] = []
    merge_log: list[dict] = []
    current_model = state.get("arch_model") or {}

    # Capture winning fragment's saam_scenarios and cross_cutting_candidates for
    # downstream cross-cutting promotion (Story 2.5) and SAAM calibration (Story 2.5).
    winning_saam_scenarios: list[dict] = []
    winning_cc_candidates: list[str] = []

    if primary is not None:
        # Locate the winning record
        winning_record = None
        for r in current_batch:
            frag = r.get("arch_fragment") if isinstance(r, dict) else None
            if (
                frag
                and r.get("batch_id") == primary.batch_id
                and r.get("strategy") == primary.strategy
            ):
                winning_record = r
                break

        if winning_record is not None and winning_record.get("arch_fragment"):
            pf = winning_record["arch_fragment"]
            pf_entities = pf.get("entities") or []
            rm_entities = current_model.get("entities") or []

            # Capture fragment-level annotations for downstream processing
            winning_saam_scenarios = pf.get("saam_scenarios") or []
            winning_cc_candidates = pf.get("cross_cutting_candidates") or []

            # Only load the embedding model when both sides have entities to compare.
            # First batch (empty running model) and empty fragments skip the model load.
            if pf_entities and rm_entities:
                cfg = {}
                if config is not None:
                    if isinstance(config, dict):
                        cfg = config.get("configurable") or {}
                    else:
                        cfg = getattr(config, "configurable", None) or {}

                db_path = cfg.get(
                    "non_asr_embeddings_db_path",
                    os.path.join(EMBEDDING_CACHE_DIR, "non_asr_embeddings.db"),
                )
                cache_dir = cfg.get("embedding_cache_dir", EMBEDDING_CACHE_DIR)
                model_name = cfg.get("embedding_model_name", EMBEDDING_MODEL_NAME)

                model = get_embedding_model(cache_dir, model_name)

                with EmbeddingCache(db_path, model_name) as cache:
                    new_arch_model, questions, merge_log = deduplicate_and_merge_fragment(
                        pf,
                        current_model,
                        cache,
                        model,
                    )
                open_questions = questions
            else:
                # No cross-model dedup needed — merge without embedding comparison
                new_arch_model, _, merge_log = deduplicate_and_merge_fragment(
                    pf,
                    current_model,
                    None,  # cache
                    None,  # model
                )
        else:
            new_arch_model = current_model
    else:
        new_arch_model = current_model

    # ── Story 2.5: Cross-cutting promotion ────────────────────────────────
    existing_cc = current_model.get("cross_cutting_candidates") or []
    new_arch_model["cross_cutting_candidates"] = list(
        set(existing_cc) | set(winning_cc_candidates)
    )
    new_arch_model, cc_questions = promote_all_cross_cutting(new_arch_model)
    open_questions.extend(cc_questions)

    # Accumulate merge log in arch_model so penalties persist in subsequent batches
    existing_merge_log = current_model.get("merge_log") or []
    accumulated_merge_log = existing_merge_log + merge_log
    new_arch_model["merge_log"] = accumulated_merge_log

    # Retrieve all winning scenarios across all batches processed so far
    all_winning_scenarios = []
    for b_idx, rank_result in existing_rankings.items():
        primary_info = rank_result.get("primary_fragment")
        if not primary_info:
            continue
        for r in batch_outputs:
            if (
                isinstance(r, dict)
                and r.get("batch_index") == b_idx
                and r.get("batch_id") == primary_info.batch_id
                and r.get("strategy") == primary_info.strategy
            ):
                frag = r.get("arch_fragment")
                if frag:
                    all_winning_scenarios.extend(frag.get("saam_scenarios") or [])

    seen_scenario_ids = set()
    deduped_winning_scenarios = []
    for s in all_winning_scenarios:
        s_id = s.get("id") or s.get("scenario_id") or ""
        if s_id and s_id not in seen_scenario_ids:
            seen_scenario_ids.add(s_id)
            deduped_winning_scenarios.append(s)

    # ── Story 2.5: SAAM score calibration ─────────────────────────────────
    new_arch_model = calibrate_entity_saam_scores(
        new_arch_model,
        saam_scenarios=deduped_winning_scenarios,
        merge_log=accumulated_merge_log,
    )

    return {
        "judge_rankings": existing_rankings,
        "arch_model": new_arch_model,
        "batch_cursor": batch_cursor + 1,
        "open_questions": open_questions,
    }
