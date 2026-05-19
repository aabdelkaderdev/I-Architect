"""Failure modes register for the RAA pipeline.

Maps risks from Section 18 and Section 22H to their active runtime mitigations.
"""

from __future__ import annotations

import copy
from raa.state.types import FailureRegisterEntry

FAILURE_REGISTER: list[FailureRegisterEntry] = [
    FailureRegisterEntry(
        risk_id="FR-RISK-001",
        description="Process killed mid-pipeline (OOM, crash, operator SIGKILL)",
        mitigation_strategy="SQLite checkpointing (SqliteSaver) saves full state after every super-step. On restart, the runner detects existing state where batch_cursor > 0 and resumes from the last completed batch.",
        section_ref="§22H",
        verified_node="runner.py / run_with_recovery",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-002",
        description="Checkpoint DB unavailable or corrupt at startup",
        mitigation_strategy="Try-except block catches sqlite3.DatabaseError on get_state(). Renames corrupted DB to *.corrupted and executes a clean fresh start.",
        section_ref="§22H",
        verified_node="runner.py / run_with_recovery",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-003",
        description="batch_cursor desync (checkpoint advanced but output not written)",
        mitigation_strategy="The final_merge node checks best_batch_output keys against range(len(batch_queue)). If any key is missing or corrupted, it logs a warning, rolls back batch_cursor to the missing index, and redirects execution for a targeted rerun.",
        section_ref="§22H",
        verified_node="final_merge.py / final_merge",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-004",
        description="Embedding SQLite DB missing at RAA startup",
        mitigation_strategy="Startup validation check in prepare_embeddings node. If asr_embeddings.db is missing/corrupted, raises a blocking RuntimeError. If non_asr_embeddings.db is missing, it is automatically rebuilt.",
        section_ref="§22H",
        verified_node="preparation.py / prepare_embeddings",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-005",
        description="Embedding SQLite DB locked (concurrent access)",
        mitigation_strategy="Open connections with Write-Ahead Logging (PRAGMA journal_mode=WAL;). Downstream nodes use read-only URI connections (mode=ro) to avoid locking during parallel reads.",
        section_ref="§22H",
        verified_node="preparation.py / batch_construction.py",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-006",
        description="Condition group has semantic drift",
        mitigation_strategy="Coherence gate (§10) splits batch into homogeneous sub-batches, or flags with reduced confidence if splitting fails.",
        section_ref="§18",
        verified_node="coherence_gate.py / routing.py",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-007",
        description="No good non-ASR matches for a group",
        mitigation_strategy="Allow empty non-ASR list; batch proceeds with ASRs only, logging an informational warning.",
        section_ref="§18",
        verified_node="batch_construction.py / construct_batches",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-008",
        description="Cross-batch entity naming collisions",
        mitigation_strategy="running_arch_model constraint injection (§15) + entity deduplication and merging in judge node.",
        section_ref="§18",
        verified_node="judge.py / final_merge.py",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-009",
        description="Overlap exceeds 3 bridge requirements",
        mitigation_strategy="Overlap bridging node enforces a hard cap of maximum 3 bridge requirements per adjacent batch pair.",
        section_ref="§18",
        verified_node="overlap_bridging.py / apply_overlap_bridging",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-010",
        description="Judge discards a useful artifact",
        mitigation_strategy="Residual scan is run before fragment discard to carry forward unique elements with scenario coverage.",
        section_ref="§18",
        verified_node="judge.py / evaluate_and_merge",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-011",
        description="Incoherent batch degrades model",
        mitigation_strategy="reduced_confidence flag + 0.5x SAAM weight multiplier applied in judge node scoring.",
        section_ref="§18",
        verified_node="judge.py / evaluate_and_merge",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-012",
        description="Reconciliation LLM introduces new conflicts",
        mitigation_strategy="Reconciliation pass output is validated against C4 schema rules; if violations increase, the reconciliation is rejected and pre-reconciliation model is preserved.",
        section_ref="§18",
        verified_node="final_merge.py / final_merge",
    ),
    FailureRegisterEntry(
        risk_id="FR-RISK-013",
        description="Embedding text hash mismatch (stale requirement text)",
        mitigation_strategy="Preparation node checks computed text hashes against DB hashes, logging a warning and recomputing only the modified entries.",
        section_ref="§18",
        verified_node="preparation.py / _persist_non_asr_embeddings",
    ),
]


def get_failure_register() -> list[FailureRegisterEntry]:
    """Return a deep copy of the failure register constant list."""
    return copy.deepcopy(FAILURE_REGISTER)


__all__ = [
    "FAILURE_REGISTER",
    "get_failure_register",
]
