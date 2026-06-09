"""Batch list construction and non-ASR-to-batch assignment.

One concern maps to exactly one CCG, one condition group, and one batch (1:1:1:1).
The Foundation Batch is the sole exception — it maps to the conditionless group (cluster == -1).

Processing order: Concern Batch 1 → 2 → ... → N → Foundation Batch.
Sequential over parallel: entities proposed by an earlier concern batch should not be
re-proposed by a later one. Sequential processing lets each judge consult a progressively
richer registry.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from raa.embedding.embedder import assign_non_asrs as _assign_embed

if TYPE_CHECKING:
    from raa.types import BatchInput, NonASREntry, RegistrySnapshot


logger = logging.getLogger(__name__)


def _dedupe_decisions(decisions: list) -> list:
    """Preserve decision order while removing duplicate selected patterns."""
    deduped = []
    seen: set[str] = set()
    for decision in decisions:
        if isinstance(decision, dict):
            key = str(decision.get("selected_pattern", decision))
        else:
            key = str(decision)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(decision)
    return deduped


class NonASRAssigner:
    """Wraps the Phase 17 embedding-based non-ASR assignment process."""

    def assign(
        self,
        condition_groups: list[dict[str, object]],
        non_asrs: list[NonASREntry],
        threshold: float,
    ) -> list[tuple[NonASREntry, str]]:
        """Pre:
            - `condition_groups` contains the Orchestrator boundary shape:
              cluster, nominal_condition, and ASR requirements.
            - `non_asrs` contains enriched functional requirements.
            - `threshold` is the similarity cutoff.

        Post:
            - Returns one tuple per non-ASR: (non_asr, batch_id).
            - batch_id is the best matching concern batch when score > threshold;
              otherwise it is "foundation_batch".
            - Assignment is exclusive and deterministic for identical embeddings.

        Side effects:
            - Performs local FastEmbed inference (delegates to Phase 17 utilities).
            - Does not call LLMs and does not mutate registry or graph state.
        """
        _, assignments = _assign_embed(condition_groups, non_asrs, threshold)
        return assignments


class BatchConstructor:
    """Builds ordered BatchInput list from RAAInput and non-ASR assignments."""

    def build_batches(
        self,
        input: dict,
        non_asr_assignments: list[tuple[NonASREntry, str]],
        registry_snapshot: RegistrySnapshot,
    ) -> list[BatchInput]:
        """Pre:
            - input contains condition_groups, concerns, non_asr, and quality_weights.
            - non_asr_assignments is exclusive: each NonASREntry appears in exactly
              one tuple, assigned to a concern batch id or "foundation_batch".
            - registry_snapshot is a frozen snapshot from EntityRegistry.snapshot().

        Post:
            - Returns ordered BatchInput records: all ConcernBatchInput values first
              (one per condition group where cluster != -1), then one FoundationBatchInput.
            - Each concern batch carries its ASRs, assigned non-ASRs, ARLO decisions,
              global quality weights, condition text, and supplied registry snapshot.
            - The Foundation batch carries conditionless ASRs, orphan non-ASRs,
              global quality weights, and supplied registry snapshot.

        Side effects: None. Constructs data only; does not read or write the live registry.
        """
        condition_groups: list[dict] = input.get("condition_groups", [])
        quality_weights: dict[str, int] = input.get("quality_weights", {})
        concerns: list[dict] = input.get("concerns", [])

        # Index non-ASR assignments by batch_id
        assigned_non_asrs: dict[str, list[NonASREntry]] = {}
        for non_asr, batch_id in non_asr_assignments:
            assigned_non_asrs.setdefault(batch_id, []).append(non_asr)

        batches: list[BatchInput] = []

        # Build concern batches (one per non-foundation group, ordered by cluster ascending)
        non_foundation_groups = [
            g for g in condition_groups if int(g.get("cluster", -1)) != -1
        ]
        non_foundation_groups.sort(key=lambda g: int(g["cluster"]))

        decisions_by_cluster: dict[int, list] = {}
        for concern in concerns:
            ccg_id = concern.get("ccg_id")
            if ccg_id is None:
                continue
            decisions_by_cluster.setdefault(int(ccg_id), []).extend(
                concern.get("decisions", [])
            )

        for ordinal, group in enumerate(non_foundation_groups, start=1):
            cluster = int(group["cluster"])
            batch_id = f"concern_batch_{ordinal}"

            asrs = [
                {"id": req.get("id", ""), "text": req.get("text", ""), "quality_attributes": req.get("quality_attributes", [])}
                for req in group.get("requirements", [])
                if isinstance(req, dict)
            ]

            concern_non_asrs = assigned_non_asrs.get(batch_id, [])

            if cluster in decisions_by_cluster:
                decisions = _dedupe_decisions(decisions_by_cluster[cluster])
            elif len(concerns) == len(non_foundation_groups):
                decisions = concerns[ordinal - 1].get("decisions", [])
            else:
                decisions = []
                if concerns:
                    logger.warning(
                        "No concern decisions mapped to %s (cluster %s); "
                        "leaving decisions empty.",
                        batch_id,
                        cluster,
                    )

            condition = str(group.get("nominal_condition", ""))

            batch: BatchInput = {
                "batch_id": batch_id,
                "batch_type": "concern",
                "asrs": asrs,
                "non_asrs": list(concern_non_asrs),
                "quality_weights": quality_weights,
                "registry_snapshot": registry_snapshot,
                "decisions": [{"selected_pattern": d.get("selected_pattern", d) if isinstance(d, dict) else str(d)} for d in decisions],
                "condition": condition,
            }
            batches.append(batch)

        # Build foundation batch (processed last)
        foundation_group = next(
            (g for g in condition_groups if int(g.get("cluster", -1)) == -1),
            None,
        )

        foundation_asrs = []
        if foundation_group is not None:
            foundation_asrs = [
                {"id": req.get("id", ""), "text": req.get("text", ""), "quality_attributes": req.get("quality_attributes", [])}
                for req in foundation_group.get("requirements", [])
                if isinstance(req, dict)
            ]

        foundation_non_asrs = assigned_non_asrs.get("foundation_batch", [])
        # Also include any non-ASRs that weren't matched to a batch_id pattern
        all_unmatched = [
            na for na, bid in non_asr_assignments
            if bid == "foundation_batch"
        ]
        foundation_non_asrs = list(foundation_non_asrs) if foundation_non_asrs else all_unmatched

        foundation_batch: BatchInput = {
            "batch_id": "foundation_batch",
            "batch_type": "foundation",
            "asrs": foundation_asrs,
            "non_asrs": list(foundation_non_asrs),
            "quality_weights": quality_weights,
            "registry_snapshot": registry_snapshot,
        }
        batches.append(foundation_batch)

        return batches
