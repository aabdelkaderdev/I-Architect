"""
Batched requirement parsing with durable @task execution.

Each batch is an LLM call wrapped in @task so that completed batches
survive crashes and are not re-executed on resume.
"""
from __future__ import annotations

import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.func import task  # Compliance fix: explicit import
from langgraph.runtime import Runtime

from arlo.llm import render_template
from arlo.nodes.runtime import get_llm, get_progress_callback, is_cancelled
from arlo.state.config import ExperimentConfig
from arlo.state.models import ParsedBatch
from arlo.state.schemas import ARLOContext, ARLOState
from arlo.utils.text_processing import batch_requirements

logger = logging.getLogger(__name__)

_CONDITIONLESS = "under any circumstances"

_QUALITY_ATTRIBUTES = [
    {"name": "Performance Efficiency", "description": "Achieving high performance under economic resource utilization."},
    {"name": "Compatibility", "description": "Interoperability and co-existence."},
    {"name": "Usability", "description": "A user-friendly app with straightforward and elegant UX and UI."},
    {"name": "Reliability", "description": "Stability under different conditions."},
    {"name": "Security", "description": "Protecting data, preventing breaches."},
    {"name": "Maintainability", "description": "Easy to modify and improve."},
    {"name": "Portability", "description": "Adaptable to different environments."},
    {"name": "Cost Efficiency", "description": "Keep the overall cost (including development, operations, and maintenance) as low as possible."},
]


class ARLOCancelled(Exception):
    """Raised when the orchestrator requests graceful cancellation mid-batch."""


def _normalize_condition_text(condition_text: str | None) -> str:
    """Normalize conditionless outputs to the grouping sentinel."""
    condition = (condition_text or "").strip()
    if not condition or condition.upper() == "N/A":
        return _CONDITIONLESS
    return condition


@task
def _parse_batch(
    batch: list[dict[str, str]],
    system_instructions: str,
    llm,
) -> list[dict]:
    """Parse a single batch of requirements via LLM.

    This is a @task — its result is checkpointed. If the pipeline crashes
    after this batch completes, it will not be re-executed on resume.
    """
    item_id_to_req_id = {
        item_id: requirement["id"]
        for item_id, requirement in enumerate(batch, start=1)
    }
    batch_text = (
        "Return each object's `id` as the numeric Item ID shown below.\n\n"
        + "\n\n".join(
            f"Item ID: {item_id}\n"
            f"Original requirement ID: {requirement['id']}\n"
            f"Description: {requirement['description']}"
            for item_id, requirement in enumerate(batch, start=1)
        )
    )
    result = llm.with_structured_output(ParsedBatch).invoke([
        SystemMessage(content=system_instructions),
        HumanMessage(content=batch_text),
    ])

    parsed_requirements: list[dict] = []
    for parsed_requirement in result.requirements:
        parsed = parsed_requirement.model_dump()
        original_id = item_id_to_req_id.get(parsed_requirement.id)
        if original_id is None:
            raise ValueError(f"Parsed item ID {parsed_requirement.id!r} is not in the current batch.")
        parsed["id"] = original_id
        parsed["condition_text"] = _normalize_condition_text(parsed.get("condition_text"))
        parsed_requirements.append(parsed)

    return parsed_requirements


def parse_requirements(
    state: ARLOState,
    runtime: Runtime[ARLOContext] | None = None,
) -> dict:
    """Node: Parse all requirements into ASRs via batched LLM calls.

    Reads: requirements, experiment_config, llm
    Writes: asrs, non_asr, parsing_stats

    Orchestrator integration:
    - Calls progress_callback(batch, total) after each batch (§8D).
    - Checks cancellation_flag before each batch (§4E). If set, persists
      the checkpoint and raises ARLOCancelled for the orchestrator to handle.
    """
    llm = get_llm(state, runtime)
    config = ExperimentConfig.from_dict(state["experiment_config"])
    progress_callback = get_progress_callback(runtime)

    system_instructions = render_template("asr_classification", {
        "stringent": config.mode == "stringent",
        "quality_attributes": _QUALITY_ATTRIBUTES,
    })

    # Batch and dispatch
    batches = batch_requirements(state["requirements"], config.batch_size)
    total_batches = len(batches)
    futures = []

    for batch_idx, batch in enumerate(batches):
        # §4E: Check cancellation at batch boundaries
        if is_cancelled(runtime):
            logger.info(
                "Cancellation requested at batch %d/%d — persisting checkpoint.",
                batch_idx + 1, total_batches,
            )
            raise ARLOCancelled(
                f"ARLO parsing cancelled at batch {batch_idx + 1}/{total_batches}"
            )

        futures.append(_parse_batch(batch, system_instructions, llm))

        # §8D: Report progress after dispatching each batch
        if progress_callback:
            progress_callback(batch_idx + 1, total_batches)

    all_parsed = [item for f in futures for item in f.result()]

    # Separate architecturally significant vs non-ASR requirements
    asrs = [r for r in all_parsed if r["is_architecturally_significant"]]
    non_asr = [
        r for r in all_parsed
        if not r["is_architecturally_significant"]
    ]

    return {
        "asrs": asrs,
        "non_asr": non_asr,
        "parsing_stats": {"total": len(all_parsed), "asr_count": len(asrs)},
    }
