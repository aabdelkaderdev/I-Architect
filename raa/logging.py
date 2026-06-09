"""Structured JSON-lines logging for the RAA pipeline.

Per FG-Phase-42: all log output is JSON lines (one JSON object per line), directly
ingestible by LangSmith traces and CLI tools (jq).

Correlation: thread_id scopes all entries. batch_id scopes within a run.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from typing import Any


class _JsonLinesFormatter(logging.Formatter):
    """Emits one JSON object per log line."""

    def format(self, record: logging.LogRecord) -> str:
        base: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra"):
            base.update(record.extra)  # type: ignore[union-attr]
        return json.dumps(base, default=str)


def configure_json_logging(
    level: int = logging.INFO,
    stream=sys.stdout,
) -> None:
    """Install the JSON-lines formatter on the root RAA logger.

    Call once at process start. Does not affect third-party loggers.
    """
    handler = logging.StreamHandler(stream)
    handler.setFormatter(_JsonLinesFormatter())
    handler.setLevel(level)

    root = logging.getLogger("raa")
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)


# ── Boundary-level logging helpers ──


def log_run_entry(
    thread_id: str,
    num_condition_groups: int,
    num_non_asrs: int,
    num_concerns: int,
) -> None:
    """Log run() entry per FG-Phase-42 §4."""
    logger = logging.getLogger("raa")
    logger.info(
        "RAA run started",
        extra={
            "thread_id": thread_id,
            "num_condition_groups": num_condition_groups,
            "num_non_asrs": num_non_asrs,
            "num_concerns": num_concerns,
        },
    )


def log_embedding_complete(
    thread_id: str,
    num_group_vectors: int,
    num_assigned: int,
    num_orphaned: int,
) -> None:
    """Log embedding completion per FG-Phase-42 §4."""
    logger = logging.getLogger("raa")
    logger.info(
        "Embedding complete",
        extra={
            "thread_id": thread_id,
            "num_group_vectors": num_group_vectors,
            "num_non_asrs_assigned": num_assigned,
            "num_non_asrs_orphaned": num_orphaned,
        },
    )


def log_batch_start(
    thread_id: str,
    batch_id: str,
    batch_type: str,
    asr_count: int,
    non_asr_count: int,
) -> None:
    """Log batch start per FG-Phase-42 §4."""
    logger = logging.getLogger("raa")
    logger.info(
        "Batch started",
        extra={
            "thread_id": thread_id,
            "batch_id": batch_id,
            "batch_type": batch_type,
            "asr_count": asr_count,
            "non_asr_count": non_asr_count,
        },
    )


def log_batch_complete(
    thread_id: str,
    batch_id: str,
    batch_type: str,
    asr_proposals: int,
    non_asr_proposals: int,
    surviving_entities: int,
    new_registrations: int,
    enrichments: int,
    coverage_gaps: int,
    conflicts_total: int,
    conflicts_unresolved: int,
    registry_size: int,
) -> None:
    """Log batch completion per FG-Phase-42 §3."""
    logger = logging.getLogger("raa")
    logger.info(
        "Batch complete",
        extra={
            "thread_id": thread_id,
            "batch_id": batch_id,
            "batch_type": batch_type,
            "asr_proposals": asr_proposals,
            "non_asr_proposals": non_asr_proposals,
            "surviving_entities": surviving_entities,
            "new_registrations": new_registrations,
            "enrichments": enrichments,
            "coverage_gaps": coverage_gaps,
            "conflicts_total": conflicts_total,
            "conflicts_unresolved": conflicts_unresolved,
            "registry_size": registry_size,
        },
    )


def log_assembly_complete(
    thread_id: str,
    registry_size: int,
    total_coverage_gaps: int,
    total_unresolved_conflicts: int,
) -> None:
    """Log assembly completion per FG-Phase-42 §4."""
    logger = logging.getLogger("raa")
    logger.info(
        "Assembly complete",
        extra={
            "thread_id": thread_id,
            "final_registry_size": registry_size,
            "total_coverage_gaps": total_coverage_gaps,
            "total_unresolved_conflicts": total_unresolved_conflicts,
        },
    )


def log_run_exit(
    thread_id: str,
    duration_ms: float,
    status: str,
) -> None:
    """Log run() exit per FG-Phase-42 §4."""
    logger = logging.getLogger("raa")
    logger.info(
        "RAA run finished",
        extra={
            "thread_id": thread_id,
            "duration_ms": round(duration_ms, 1),
            "status": status,
        },
    )
