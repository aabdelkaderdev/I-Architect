"""Public entry point for the RAA module. Only file the Orchestrator imports.

Two public interfaces:
    RAA().run()   — instance method per FG-Phase-43 §1.
    run()         — module-level function for callers that don't want the class.

Signature per FG-Phase-40 §1:
    async def run(input: RAAInput, config: RunnableConfig) -> RAAOutput

Async because Phase 3 node timeouts require async nodes (langgraph>=1.2).

FG-Phase-41 data flow:
    0. embed: RAAInput → group_vectors + non_asr assignments
    1. construct_batches: assignments + RAAInput → list[BatchInput]
    2a. asr_node: BatchInput → list[EntityProposal]  (parallel)
    2b. non_asr_node: BatchInput → list[EntityProposal]  (parallel)
    3. judge_node: proposals + requirements + snapshot → BatchOutput + registry delta
    4. assemble: all BatchOutput + final registry → RAAOutput
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from raa.batch.constructor import BatchConstructor, NonASRAssigner
from raa.config.defaults import DB_PATH, SIMILARITY_THRESHOLD, THREAD_ID
from raa.graph import async_graph_context

if TYPE_CHECKING:
    from langgraph.types import RunnableConfig

    from raa.types import RAAInput, RAAOutput

logger = logging.getLogger(__name__)


class RAA:
    """RAA pipeline runner per FG-Phase-43 §1.

    Single method: async run(). The Orchestrator imports exactly this class.
    """

    async def run(self, input: RAAInput, config: RunnableConfig) -> RAAOutput:
        """Execute a full RAA run — embed, assign, batch, graph evaluation, assemble.

        Pre:
            - `input` is the Orchestrator-produced RAAInput boundary object from
              Phase 1 §2.
            - `config["configurable"]` supplies the RAAConfigSchema keys required
              by FG-Phase-10 §1 and FG-Phase-40 §2: asr_llm, non_asr_llm,
              judge_llm, thread_id, and db_path.
            - The caller awaits this coroutine, preserving FG-Phase-40 §1.

        Post:
            - Returns RAAOutput exactly as defined in FG-Phase-07 §3.
            - Concern batches are processed sequentially, Foundation batch last
              (Phase 1 §6.3).
            - l2_descriptions include Foundation backbone containers merged into
              each concern L2 via FG-Phase-09 §2 append_unique semantics.
            - conflicts contains only unresolved ConflictRecord entries.

        Side effects:
            - Creates or resumes LangGraph checkpoints under thread_id and db_path.
            - Mutates the live in-memory entity registry during Judge steps only.
            - Performs local embedding inference and LLM calls through configured models.
        """
        return await _run_impl(input, config)


async def run(
    input: RAAInput,
    config: RunnableConfig | None = None,
) -> RAAOutput:
    """Module-level convenience — delegates to RAA().run().

    FG-Phase-40 §1 contract:
        - input: RAAInput with condition_groups, concerns, non_asr, quality_weights.
        - config: RunnableConfig with configurable keys for LLM instances,
          thread_id, db_path (RAAConfigSchema, FG-Phase-10 §1).
        - Returns: RAAOutput with L1, L2, L3 descriptions, entity registry,
          coverage gaps, and conflicts.

    Raises standard Python exceptions — no custom error hierarchy (FG-Phase-40 §3).
    LangGraph checkpoints the last successful superstep before any exception bubbles up.
    The Orchestrator may resume by re-invoking with the same thread_id.
    """
    if config is None:
        config = {}
    return await _run_impl(input, config)


async def _run_impl(input: RAAInput, config: RunnableConfig) -> RAAOutput:
    """Shared implementation — called by both RAA().run() and run()."""
    from raa.registry.registry import EntityRegistry

    configurable = config.get("configurable", {})

    # Resolve runtime overrides from configurable, falling back to static defaults
    threshold = float(configurable.get("similarity_threshold", SIMILARITY_THRESHOLD))
    db_path = str(configurable.get("db_path", DB_PATH))
    thread_id = str(configurable.get("thread_id", THREAD_ID))

    start_time = time.monotonic()

    condition_groups = input.get("condition_groups", [])
    non_asrs = input.get("non_asr", [])
    concerns = input.get("concerns", [])

    # Boundary log: run entry
    logger.info(
        "RAA run started",
        extra={
            "thread_id": thread_id,
            "num_condition_groups": len(condition_groups),
            "num_non_asrs": len(non_asrs),
            "num_concerns": len(concerns),
        },
    )

    try:
        # 1. Embedding pass
        assigner = NonASRAssigner()
        non_asr_assignments = assigner.assign(condition_groups, non_asrs, threshold)

        foundation_count = sum(
            1 for _, bid in non_asr_assignments if bid == "foundation_batch"
        )
        logger.info(
            "Embedding complete",
            extra={
                "thread_id": thread_id,
                "num_group_vectors": len(condition_groups),
                "num_non_asrs_assigned": len(non_asr_assignments) - foundation_count,
                "num_non_asrs_orphaned": foundation_count,
            },
        )

        # 2. Build batch list
        registry = EntityRegistry()
        initial_snapshot = registry.snapshot()

        constructor = BatchConstructor()
        batches = constructor.build_batches(input, non_asr_assignments, initial_snapshot)

        # 3. Compile graph and invoke
        initial_state = {
            "entity_registry_entries": [],
            "batches": batches,
            "batch_index": 0,
            "batch_outputs": [],
            "group_vectors": {},
        }

        _full_config = {
            "configurable": {
                **configurable,
                "thread_id": thread_id,
                "db_path": db_path,
            }
        }

        async with async_graph_context(db_path=db_path) as graph:
            final_state = await graph.ainvoke(initial_state, _full_config)

        # 4. Return RAAOutput
        raa_output = final_state.get("raa_output")
        if raa_output is None:
            raise RuntimeError(
                "Graph completed but no RAAOutput was produced. "
                "Check that the assembler node ran successfully."
            )

        duration_ms = (time.monotonic() - start_time) * 1000
        logger.info(
            "RAA run finished",
            extra={
                "thread_id": thread_id,
                "duration_ms": round(duration_ms, 1),
                "status": "success",
            },
        )

        return raa_output

    except Exception:
        duration_ms = (time.monotonic() - start_time) * 1000
        logger.error(
            "RAA run failed",
            extra={
                "thread_id": thread_id,
                "duration_ms": round(duration_ms, 1),
                "status": "failed",
            },
        )
        raise
