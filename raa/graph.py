"""StateGraph construction, node wiring, edge definitions, and compilation.

Implements the processing architecture from Phase 1 §8.1:
- ASR and Non-ASR subgraph nodes run in parallel per batch.
- Judge node is the sole writer to the entity_registry.
- Concern batches process sequentially, Foundation batch runs last.
- Assembler merges backbone containers into concern L2 descriptions and produces RAAOutput.

Framework rationale (FG-Phase-32):
- LangGraph: StateGraph orchestration with built-in checkpointing.
- LangChain: BaseChatModel abstraction for provider-agnostic LLM calls.
- Pydantic v2: LLM response validation via with_structured_output.

Retry and timeout policies per FG-Phase-36 §2.2 and FG-Phase-39 §2.2.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from raa.config.defaults import (
    DB_PATH,
    NODE_RUN_TIMEOUT,
    RETRY_BACKOFF_FACTOR,
    RETRY_INITIAL_INTERVAL,
    RETRY_JITTER,
    RETRY_MAX_ATTEMPTS,
    RETRY_MAX_INTERVAL,
)

if TYPE_CHECKING:
    from langgraph.graph import StateGraph


def build_graph(
    db_path: str = DB_PATH,
    max_retries: int = RETRY_MAX_ATTEMPTS,
    checkpointer: Any | None = None,
) -> StateGraph:
    """Construct and compile the RAA StateGraph.

    Nodes:
        - snapshot_registry: freezes the live registry before each batch.
        - asr_node: ASR Subgraph — LLM call, structured output, validated proposals.
        - non_asr_node: Non-ASR Subgraph — functional proposals, same pattern.
        - judge_node: SAAM Steps 1-5, deduplication, relationships, registry write,
          partial C4 assembly.
        - next_batch: increments batch_index or routes to END.
        - assemble_output: merges backbone containers, constructs RAAOutput.

    Edges:
        START → snapshot_registry
        snapshot_registry → asr_node
        snapshot_registry → non_asr_node     (parallel)
        asr_node → judge_node
        non_asr_node → judge_node            (converge)
        judge_node → next_batch
        next_batch → snapshot_registry       (loop back for next batch)
        next_batch → assemble_output         (exit when all batches done)
        assemble_output → END

    Retry policy (FG-Phase-36 §2.2):
        max_attempts=5, backoff_factor=2.0, initial_interval=0.5s,
        max_interval=128s, jitter=True.
        Applied per-node: ASR, Non-ASR, and Judge have independent retry loops.

    Timeout (FG-Phase-39 §2.2):
        run_timeout=120s per LLM-calling node.

    Compilation:
        Uses the supplied checkpointer when provided. Otherwise, compiles with
        a synchronous SqliteSaver for sync graph operations such as rendering.
    """
    from langgraph.graph import END, START, StateGraph
    from langgraph.types import RetryPolicy, RunnableConfig, TimeoutPolicy

    from raa.state import RAAState

    graph = StateGraph(RAAState)

    # ── Node registrations ──

    retry_policy = RetryPolicy(
        max_attempts=max_retries,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        initial_interval=RETRY_INITIAL_INTERVAL,
        max_interval=RETRY_MAX_INTERVAL,
        jitter=RETRY_JITTER,
    )
    timeout_policy = TimeoutPolicy(run_timeout=NODE_RUN_TIMEOUT)

    # snapshot_registry: deterministic — no retry/timeout needed
    graph.add_node("snapshot_registry", _snapshot_registry)

    # asr_node: LLM-calling — retry + timeout
    graph.add_node(
        "asr_node",
        _asr_node,
        retry_policy=retry_policy,
        timeout=timeout_policy,
    )

    # non_asr_node: LLM-calling — retry + timeout
    graph.add_node(
        "non_asr_node",
        _non_asr_node,
        retry_policy=retry_policy,
        timeout=timeout_policy,
    )

    # judge_node: LLM-calling (Steps 3-5) — retry + timeout
    graph.add_node(
        "judge_node",
        _judge_node,
        retry_policy=retry_policy,
        timeout=timeout_policy,
    )

    # next_batch: deterministic routing
    graph.add_node("next_batch", _next_batch)

    # assemble_output: deterministic assembly
    graph.add_node("assemble_output", _assemble_output)

    # ── Edge wiring ──

    graph.add_edge(START, "snapshot_registry")

    # Parallel ASR / Non-ASR
    graph.add_edge("snapshot_registry", "asr_node")
    graph.add_edge("snapshot_registry", "non_asr_node")

    # Converge at Judge
    graph.add_edge("asr_node", "judge_node")
    graph.add_edge("non_asr_node", "judge_node")

    # Route after Judge
    graph.add_conditional_edges(
        "judge_node",
        _route_after_judge,
        {
            "next_batch": "next_batch",
            "assemble": "assemble_output",
        },
    )

    # Loop back or exit
    graph.add_conditional_edges(
        "next_batch",
        _route_after_next_batch,
        {
            "snapshot": "snapshot_registry",
            "assemble": "assemble_output",
        },
    )

    graph.add_edge("assemble_output", END)

    # ── Compile with checkpointing ──
    if checkpointer is None:
        import sqlite3

        from langgraph.checkpoint.sqlite import SqliteSaver

        conn = sqlite3.connect(db_path, check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        checkpointer.setup()

    return graph.compile(checkpointer=checkpointer)


@asynccontextmanager
async def async_graph_context(
    db_path: str = DB_PATH,
    max_retries: int = RETRY_MAX_ATTEMPTS,
):
    """Yield a compiled graph with an async SQLite checkpointer.

    LangGraph async invocation calls async checkpoint methods, so it must use
    AsyncSqliteSaver rather than the synchronous SqliteSaver.
    """
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

    async with AsyncSqliteSaver.from_conn_string(db_path) as checkpointer:
        yield build_graph(
            db_path=db_path,
            max_retries=max_retries,
            checkpointer=checkpointer,
        )


# ═══════════════════════════════════════════════════════════════════════
# Node implementations
# ═══════════════════════════════════════════════════════════════════════

async def _snapshot_registry(state: dict, config: RunnableConfig) -> dict:
    """Freeze the live registry before each batch. Deterministic — no LLM.

    Produces a RegistrySnapshot injected into both subgraph node inputs.
    per FG-Phase-34 §2 mechanics.
    """
    from copy import deepcopy

    entity_registry_entries = state.get("entity_registry_entries", [])
    entity_registry = {e["canonical_id"]: e for e in entity_registry_entries}
    batches: list = state.get("batches", [])
    batch_index: int = state.get("batch_index", 0)

    if batch_index >= len(batches):
        return {}

    updated_batches = list(batches)
    current_batch = dict(updated_batches[batch_index])

    # Freeze the registry as a snapshot
    snapshot = {
        "entries": deepcopy(entity_registry),
        "snapshot_after_batch": state.get("_last_written_batch_id", "none"),
    }

    # Inject snapshot into the current batch's registry_snapshot field
    current_batch["registry_snapshot"] = snapshot
    updated_batches[batch_index] = current_batch

    return {"batches": updated_batches}


async def _asr_node(state: dict, config: RunnableConfig) -> dict:
    """ASR Subgraph node — LLM call, structured output, validated proposals.

    Resolves asr_llm from config["configurable"]. Skips when batch has no ASRs.
    Empty batch is valid — returns empty proposals (FG-Phase-38 §1.2).
    """
    from raa.state import RAAState
    from raa.subgraphs.asr_node import ASRSubgraph

    batches: list = state.get("batches", [])
    batch_index: int = state.get("batch_index", 0)

    if batch_index >= len(batches):
        return {}

    batch = batches[batch_index]
    asr = ASRSubgraph()
    proposals = await asr.build_proposals(batch, config)

    return {"asr_proposals": proposals}


async def _non_asr_node(state: dict, config: RunnableConfig) -> dict:
    """Non-ASR Subgraph node — LLM call, functional proposals.

    Resolves non_asr_llm from config["configurable"].
    Empty non_asrs list is valid — returns empty proposals (FG-Phase-38 §1.2).
    """
    from raa.state import RAAState
    from raa.subgraphs.non_asr_node import NonASRSubgraph

    batches: list = state.get("batches", [])
    batch_index: int = state.get("batch_index", 0)

    if batch_index >= len(batches):
        return {}

    batch = batches[batch_index]
    non_asr = NonASRSubgraph()
    proposals = await non_asr.build_proposals(batch, config)

    return {"non_asr_proposals": proposals}


async def _judge_node(state: dict, config: RunnableConfig) -> dict:
    """Judge node — SAAM Steps 1-5, deduplication, relationships, registry write.

    Sole writer to entity_registry. Resolves judge_llm from config["configurable"].
    Empty proposal lists produce empty output deterministically (FG-Phase-38 §1.2).
    """
    from raa.subgraphs.judge_node import Judge

    batches: list = state.get("batches", [])
    batch_index: int = state.get("batch_index", 0)

    if batch_index >= len(batches):
        return {}

    batch = batches[batch_index]
    entity_registry_entries: list = state.get("entity_registry_entries", [])
    entity_registry = {e["canonical_id"]: e for e in entity_registry_entries}
    asr_proposals: list = state.get("asr_proposals", [])
    non_asr_proposals: list = state.get("non_asr_proposals", [])

    from copy import deepcopy

    from raa.registry.registry import EntityRegistry

    registry = EntityRegistry()
    registry._entries = deepcopy(entity_registry)
    registry._name_index = {
        entry["canonical_name"]: cid
        for cid, entry in registry._entries.items()
    }

    judge = Judge(registry=registry)

    # SAAM Step 1: Scenario Development (deterministic)
    scenarios = judge.develop_scenarios(batch)

    # SAAM Step 2: Architecture Description (deterministic)
    all_proposals = judge.describe_architecture(asr_proposals, non_asr_proposals)

    # SAAM Step 3: Scenario Classification (LLM)
    judged = await judge.classify_scenarios(batch, all_proposals, config)

    # SAAM Step 4: Individual Scenario Evaluation (LLM)
    judged, coverage_gaps = await judge.evaluate_coverage(batch, judged, config)

    # SAAM Step 5: Scenario Interaction (LLM)
    judged, conflicts = await judge.detect_interactions(batch, judged, config)

    # Coverage invariant: if batch has requirements but zero judged + zero gaps → impossible
    all_reqs = list(batch.get("asrs", [])) + list(batch.get("non_asrs", []))
    if all_reqs and not judged and not coverage_gaps:
        import logging
        logging.getLogger(__name__).warning(
            "Batch %s: %d requirements, zero judged proposals, zero coverage gaps — "
            "generating synthetic gaps.",
            batch["batch_id"],
            len(all_reqs),
        )
        coverage_gaps = [
            {
                "requirement_id": r.get("id", ""),
                "requirement_text": r.get("text", ""),
                "batch_id": batch["batch_id"],
                "gap_reason": "No judged proposal remained after Judge evaluation.",
            }
            for r in all_reqs
        ]

    # Post-SAAM: deduplicate, registry write, derive relationships
    surviving = judge.deduplicate(judged, conflicts)
    registry_delta = judge.resolve_and_register(batch, judged, conflicts)

    if surviving and not registry_delta.get("new_entries") and not registry_delta.get("enriched_ids"):
        raise RuntimeError(
            f"Batch {batch['batch_id']} had {len(surviving)} surviving proposals, "
            "but the registry rejected every write. Check Judge proposal provenance "
            "and registry validation logs."
        )

    relationships = judge.derive_relationships(
        batch, surviving, batch.get("registry_snapshot", {})
    )

    # Assemble partial C4 descriptions
    batch_output = judge.assemble_descriptions(
        batch, surviving, relationships,
        registry_delta, coverage_gaps, conflicts,
    )

    # Collect changed entries: new + enriched
    changed_entries: list = list(registry_delta.get("new_entries", []))
    for cid in registry_delta.get("enriched_ids", []):
        entry = registry._entries.get(cid)
        if entry is not None:
            changed_entries.append(entry)

    return {
        "entity_registry_entries": changed_entries,
        "batch_outputs": [batch_output],
        "asr_proposals": [],
        "non_asr_proposals": [],
        "_last_written_batch_id": batch["batch_id"],
    }


def _route_after_judge(state: dict) -> str:
    """Route from Judge: always go to next_batch for index increment."""
    return "next_batch"


async def _next_batch(state: dict, config: RunnableConfig) -> dict:
    """Increment batch_index to advance to the next batch."""
    batch_index: int = state.get("batch_index", 0)
    return {"batch_index": batch_index + 1}


def _route_after_next_batch(state: dict) -> str:
    """Route after increment: loop back for more batches, or assemble if done."""
    batches: list = state.get("batches", [])
    batch_index: int = state.get("batch_index", 0)

    if batch_index < len(batches):
        return "snapshot"
    return "assemble"


async def _assemble_output(state: dict, config: RunnableConfig) -> dict:
    """Assemble final RAAOutput from all batch outputs and the final registry.

    Merges backbone containers into each concern L2 description.
    Filters conflicts to unresolved only (append_filtered merge).
    """
    from raa.validators import validate_raa_output

    batch_outputs: list = state.get("batch_outputs", [])
    entity_registry_entries: list = state.get("entity_registry_entries", [])
    entity_registry: dict = {e["canonical_id"]: e for e in entity_registry_entries}

    # Separate foundation output from concern outputs
    foundation_output = None
    concern_outputs = []

    for bo in batch_outputs:
        if bo["batch_type"] == "foundation":
            foundation_output = bo
        else:
            concern_outputs.append(bo)

    # Collect L1 description
    raw_l1 = foundation_output.get("system_context_description") if foundation_output else {
        "system_name": "",
        "system_description": "",
        "system_boundary_description": "",
        "actors": [],
        "external_systems": [],
        "relationships": [],
        "source_requirements": [],
    }
    l1 = {
        **raw_l1,
        "actors": list(raw_l1.get("actors", [])),
        "external_systems": list(raw_l1.get("external_systems", [])),
        "relationships": list(raw_l1.get("relationships", [])),
        "source_requirements": list(raw_l1.get("source_requirements", [])),
    }

    # Merge backbone containers into each concern L2 description
    backbone_containers = []
    if foundation_output and "backbone_description" in foundation_output:
        backbone_containers = foundation_output["backbone_description"].get("containers", [])

    def _entry_source_reqs(entry: dict) -> list[str]:
        return list(entry.get("source_requirements", []))

    def _dedupe_by_canonical_id(entries: list[dict]) -> list[dict]:
        seen: set[str] = set()
        result: list[dict] = []
        for entry in entries:
            canonical_id = entry.get("canonical_id", "")
            key = canonical_id or f"__idx_{len(result)}"
            if key in seen:
                continue
            seen.add(key)
            result.append(entry)
        return result

    def _relationship_key(relationship: dict) -> tuple[str, str, str]:
        return (
            relationship.get("source_id", ""),
            relationship.get("target_id", ""),
            relationship.get("label", ""),
        )

    def _append_relationship_once(relationships: list[dict], relationship: dict) -> None:
        existing = {_relationship_key(rel) for rel in relationships}
        if _relationship_key(relationship) not in existing:
            relationships.append(relationship)

    actor_ids = {actor.get("canonical_id", "") for actor in l1.get("actors", [])}
    external_ids = {
        external.get("canonical_id", "")
        for external in l1.get("external_systems", [])
    }
    for cid, entry in sorted(entity_registry.items()):
        if entry.get("c4_type") == "actor" and cid not in actor_ids:
            l1.setdefault("actors", []).append({
                "canonical_id": cid,
                "name": entry.get("canonical_name", ""),
                "description": entry.get("description", ""),
                "source_requirements": _entry_source_reqs(entry),
            })
            actor_ids.add(cid)
        elif entry.get("c4_type") == "external" and cid not in external_ids:
            l1.setdefault("external_systems", []).append({
                "canonical_id": cid,
                "name": entry.get("canonical_name", ""),
                "description": entry.get("description", ""),
                "source_requirements": _entry_source_reqs(entry),
            })
            external_ids.add(cid)

    internal_entries = [
        entry for _, entry in sorted(entity_registry.items())
        if (
            entry.get("c4_level") == "container"
            and entry.get("c4_type") not in {"actor", "external"}
        )
    ]
    if internal_entries:
        system_entry = internal_entries[0]
        system_id = system_entry["canonical_id"]
        system_name = system_entry.get("canonical_name", "System")
        for actor in l1.get("actors", []):
            actor_id = actor.get("canonical_id", "")
            if not actor_id:
                continue
            _append_relationship_once(l1["relationships"], {
                "source_id": actor_id,
                "target_id": system_id,
                "label": "uses",
                "description": (
                    f"{actor.get('name', 'Actor')} uses {system_name}."
                ),
            })
        for external in l1.get("external_systems", []):
            external_id = external.get("canonical_id", "")
            if not external_id:
                continue
            _append_relationship_once(l1["relationships"], {
                "source_id": system_id,
                "target_id": external_id,
                "label": "calls",
                "description": (
                    f"{system_name} calls {external.get('name', 'External system')}."
                ),
            })

    l1["source_requirements"] = sorted(set(
        req_id
        for actor in l1.get("actors", [])
        for req_id in actor.get("source_requirements", [])
    ) | set(
        req_id
        for external in l1.get("external_systems", [])
        for req_id in external.get("source_requirements", [])
    ))

    l2_descriptions = []
    for co in concern_outputs:
        raw_cd = co.get("container_description")
        cd = {
            **raw_cd,
            "containers": list(raw_cd.get("containers", [])),
            "relationships": list(raw_cd.get("relationships", [])),
            "source_requirements": list(raw_cd.get("source_requirements", [])),
        } if raw_cd else None
        if cd and backbone_containers:
            cd["containers"] = _dedupe_by_canonical_id(
                list(backbone_containers) + cd.get("containers", [])
            )
        if cd:
            cd["source_requirements"] = sorted({
                req_id
                for container in cd.get("containers", [])
                for req_id in container.get("source_requirements", [])
            })
        if cd:
            l2_descriptions.append(cd)

    # Collect L3 descriptions
    l3_descriptions = []
    for co in concern_outputs:
        l3_descriptions.extend(co.get("component_descriptions", []))

    # Collect coverage gaps and conflicts (append_filtered for unresolved only)
    coverage_gaps = []
    for bo in batch_outputs:
        coverage_gaps.extend(bo.get("coverage_gaps", []))

    conflicts = []
    for bo in batch_outputs:
        for c in bo.get("conflicts", []):
            if c.get("resolution") == "unresolved":
                conflicts.append(c)

    raa_output = {
        "l1_description": l1,
        "l2_descriptions": l2_descriptions,
        "l3_descriptions": l3_descriptions,
        "entity_registry": entity_registry,
        "coverage_gaps": coverage_gaps,
        "conflicts": conflicts,
    }

    try:
        validate_raa_output(raa_output)
    except ValueError as exc:
        import logging
        logging.getLogger(__name__).warning("RAAOutput validation: %s", exc)

    return {"raa_output": raa_output}


# ── Module-level cached compiled graph ──

_compiled_graphs: dict[tuple[str, int], StateGraph] = {}


def get_graph(
    db_path: str = DB_PATH,
    max_retries: int = RETRY_MAX_ATTEMPTS,
):
    """Return a sync-checkpointed compiled graph, cached by checkpoint settings."""
    key = (db_path, max_retries)
    if key not in _compiled_graphs:
        _compiled_graphs[key] = build_graph(db_path=db_path, max_retries=max_retries)
    return _compiled_graphs[key]
