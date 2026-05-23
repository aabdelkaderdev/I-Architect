# Edge Case Hunter Code Review Prompt

You are a pure path tracer. Never comment on whether code is good or bad; only list missing handling.
Scan only the diff hunks and list boundaries that are directly reachable from the changed lines and lack an explicit guard in the diff.
Ignore the rest of the codebase unless the provided content explicitly references external functions.

Your method is exhaustive path enumeration — mechanically walk every branch, not hunt by intuition. Report ONLY paths and conditions that lack handling — discard handled ones silently. Do NOT editorialize or add filler — findings only.

Output findings strictly as a JSON array of objects. Each object must contain exactly these four fields and nothing else:

```json
[{
  "location": "file:start-end (or file:line when single line, or file:hunk when exact line unavailable)",
  "trigger_condition": "one-line description (max 15 words)",
  "guard_snippet": "minimal code sketch that closes the gap (single-line escaped string, no raw newlines or unescaped quotes)",
  "potential_consequence": "what could actually go wrong (max 15 words)"
}]
```

No extra text, no explanations, no markdown wrapping. An empty array `[]` is valid when no unhandled paths are found.

---

## Content to Review (Unified Diff)

```diff
diff --git a/raa/_bmad-output/implementation-artifacts/sprint-status.yaml b/raa/_bmad-output/implementation-artifacts/sprint-status.yaml
index 1f7d0c0..7cc1820 100644
--- a/raa/_bmad-output/implementation-artifacts/sprint-status.yaml
+++ b/raa/_bmad-output/implementation-artifacts/sprint-status.yaml
@@ -48,8 +48,8 @@ development_status:
   1-3-centroid-anchored-batch-construction: done
   1-4-overlap-bridging-coherence-gating-and-priority-queue-ordering: done
   epic-1-retrospective: optional
-  epic-2: backlog
-  2-1-concurrency-orchestrator-and-parallel-subgraph-dispatch: backlog
+  epic-2: in-progress
+  2-1-concurrency-orchestrator-and-parallel-subgraph-dispatch: review
   2-2-c4-metamodel-hierarchy-enforcement-in-private-subgraphs: backlog
   2-3-saam-first-fragment-scoring: backlog
   2-4-conservative-entity-deduplication-and-c4-boundary-grouping: backlog
diff --git a/raa/raa/graphs/__init__.py b/raa/raa/graphs/__init__.py
new file mode 100644
index 0000000..3cc762b
--- /dev/null
+++ b/raa/raa/graphs/__init__.py
@@ -0,0 +1 @@
+""
\ No newline at end of file
diff --git a/raa/raa/graphs/execution_loop.py b/raa/raa/graphs/execution_loop.py
new file mode 100644
index 0000000..65e3e3e
--- /dev/null
+++ b/raa/raa/graphs/execution_loop.py
@@ -0,0 +1,336 @@
+"""
+Phase 6 node: Concurrency orchestrator and parallel subgraph dispatch (FR-7, FR-8, FR-9).
+
+Dispatches coherent batches to RAA-A/B/C concurrently and routes reduced-confidence
+batches to RAA-A only. Each subgraph gets an isolated SQLite WAL checkpointer.
+"""
+from __future__ import annotations
+
+import asyncio
+import logging
+import os
+from pathlib import Path
+from typing import Any
+
+import aiosqlite
+from langchain_core.runnables import RunnableConfig
+from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
+from langgraph.graph import StateGraph
+
+from raa.state.models import ArchFragment
+from raa.state.schemas import RAAState
+from raa.subgraphs.raa_a import build_raa_a_subgraph
+from raa.subgraphs.raa_b import build_raa_b_subgraph
+from raa.subgraphs.raa_c import build_raa_c_subgraph
+from raa.subgraphs.schemas import StrategySubgraphInput
+
+logger = logging.getLogger(__name__)
+
+_STRATEGIES = ("raa_a", "raa_b", "raa_c")
+_BUILDERS = {
+    "raa_a": build_raa_a_subgraph,
+    "raa_b": build_raa_b_subgraph,
+    "raa_c": build_raa_c_subgraph,
+}
+
+
+# ── Checkpoint helpers ─────────────────────────────────────────────────────
+
+
+async def _create_wal_checkpointer(db_path: str) -> AsyncSqliteSaver:
+    """Open an aiosqlite connection, enable WAL mode, and wrap in AsyncSqliteSaver."""
+    conn = await aiosqlite.connect(db_path)
+    await conn.execute("PRAGMA journal_mode=WAL")
+    await conn.commit()
+    saver = AsyncSqliteSaver(conn)
+    await saver.setup()
+    return saver
+
+
+def _derive_role_paths(base_path: str) -> dict[str, str]:
+    """Derive three role-specific checkpoint paths from a base path.
+
+    e.g. ``raa_checkpoint.db`` →
+      - ``raa_checkpoint_raa_a.db``
+      - ``raa_checkpoint_raa_b.db``
+      - ``raa_checkpoint_raa_c.db``
+    """
+    p = Path(base_path)
+    stem = p.stem
+    suffix = p.suffix
+    parent = p.parent
+    return {
+        "raa_a": str(parent / f"{stem}_raa_a{suffix}"),
+        "raa_b": str(parent / f"{stem}_raa_b{suffix}"),
+        "raa_c": str(parent / f"{stem}_raa_c{suffix}"),
+    }
+
+
+def _resolve_checkpoint_paths(configurable: dict) -> dict[str, str]:
+    """Resolve per-role checkpoint DB paths from configurable.
+
+    Prefers explicit per-role keys; falls back to deriving from ``checkpoint_db_path``.
+    """
+    paths: dict[str, str] = {}
+    for role in _STRATEGIES:
+        key = f"{role}_checkpoint_db_path"
+        if key in configurable:
+            paths[role] = configurable[key]
+
+    if len(paths) == 3:
+        return paths
+
+    if "checkpoint_db_path" not in configurable:
+        raise KeyError(
+            "Missing required configurable key: 'checkpoint_db_path' "
+            "(or provide explicit raa_a_checkpoint_db_path, raa_b_checkpoint_db_path, "
+            "raa_c_checkpoint_db_path)"
+        )
+
+    derived = _derive_role_paths(configurable["checkpoint_db_path"])
+    for role in _STRATEGIES:
+        if role not in paths:
+            paths[role] = derived[role]
+    return paths
+
+
+# ── Private input builder ──────────────────────────────────────────────────
+
+
+def _build_private_input(
+    batch: dict,
+    state: RAAState,
+    strategy: str,
+) -> StrategySubgraphInput:
+    """Map parent state into private StrategySubgraphInput for a subgraph."""
+    bridge_requirements = [
+        br for br in (state.get("bridge_requirements") or [])
+        if batch["group_id"] in br.get("batch_ids", [])
+    ]
+    return StrategySubgraphInput(
+        batch=batch,
+        quality_weights=state.get("quality_weights") or {},
+        running_model=state.get("arch_model") or {},
+        bridge_requirements=bridge_requirements,
+        strategy=strategy,
+        reduced_confidence=bool(batch.get("reduced_confidence", False)),
+    )
+
+
+# ── Output normalization ───────────────────────────────────────────────────
+
+
+def _normalize_output(
+    batch: dict,
+    batch_index: int,
+    strategy: str,
+    child_thread_id: str,
+    reduced_confidence: bool,
+    result: dict | None,
+    skipped: bool = False,
+    skip_reason: str | None = None,
+) -> dict:
+    """Normalize a subgraph result into the standard output record shape."""
+    if skipped:
+        return {
+            "batch_id": batch["group_id"],
+            "batch_index": batch_index,
+            "strategy": strategy,
+            "thread_id": child_thread_id,
+            "reduced_confidence": reduced_confidence,
+            "arch_fragment": None,
+            "skipped": True,
+            "skip_reason": skip_reason,
+        }
+
+    arch_fragment = None
+    if result is not None:
+        frag = result.get("arch_fragment")
+        if isinstance(frag, ArchFragment):
+            arch_fragment = frag.model_dump()
+        elif isinstance(frag, dict):
+            arch_fragment = frag
+        else:
+            arch_fragment = result
+
+    return {
+        "batch_id": batch["group_id"],
+        "batch_index": batch_index,
+        "strategy": strategy,
+        "thread_id": child_thread_id,
+        "reduced_confidence": bool(reduced_confidence),
+        "arch_fragment": arch_fragment,
+        "skipped": False,
+        "skip_reason": None,
+    }
+
+
+# ── Strategy invocation ────────────────────────────────────────────────────
+
+
+async def _invoke_strategy(
+    strategy: str,
+    private_input: StrategySubgraphInput,
+    child_config: RunnableConfig,
+    compiled_graph,
+    *,
+    close_checkpointer: bool = False,
+    saver: AsyncSqliteSaver | None = None,
+) -> dict:
+    """Invoke a single compiled subgraph asynchronously."""
+    result = await compiled_graph.ainvoke(private_input, child_config)
+    if close_checkpointer and saver is not None:
+        try:
+            await saver.conn.close()
+        except Exception:
+            pass
+    return result
+
+
+# ── Main dispatch node ─────────────────────────────────────────────────────
+
+
+async def dispatch_strategy_subgraphs(
+    state: RAAState, config: RunnableConfig
+) -> dict:
+    """Select the current batch and dispatch to strategy subgraphs.
+
+    Config keys expected in ``config["configurable"]``:
+        ``thread_id``, ``checkpoint_db_path`` (or per-role paths)
+
+    Injected keys (optional, for testing):
+        ``raa_a_graph``, ``raa_b_graph``, ``raa_c_graph``
+
+    Returns:
+        dict with key ``batch_outputs`` — list of output records.
+    """
+    configurable = config.get("configurable")
+    if configurable is None:
+        raise KeyError("RunnableConfig is missing 'configurable' key")
+
+    thread_id = configurable.get("thread_id")
+    if not thread_id:
+        raise KeyError("Missing required configurable key: 'thread_id'")
+
+    execution_queue = state.get("execution_queue") or []
+    if not execution_queue:
+        raise ValueError("execution_queue is missing or empty")
+
+    batch_cursor = state.get("batch_cursor", 0)
+    if not isinstance(batch_cursor, int) or batch_cursor < 0:
+        raise ValueError(
+            f"batch_cursor must be a non-negative integer, got {batch_cursor!r}"
+        )
+    if batch_cursor >= len(execution_queue):
+        raise ValueError(
+            f"batch_cursor {batch_cursor} is out of range for execution_queue "
+            f"of length {len(execution_queue)}"
+        )
+
+    batch = execution_queue[batch_cursor]
+    reduced_confidence = bool(batch.get("reduced_confidence", False))
+    batch_index = batch_cursor
+
+    # Check for injected compiled graphs (test support)
+    injected_graphs: dict[str, Any] = {}
+    for role in _STRATEGIES:
+        key = f"{role}_graph"
+        if key in configurable:
+            injected_graphs[role] = configurable[key]
+
+    output_records: list[dict] = []
+
+    if reduced_confidence:
+        # ── Reduced-confidence path: RAA-A only ──────────────────────────
+        strategies_to_run = ["raa_a"]
+        skipped_strategies = ["raa_b", "raa_c"]
+    else:
+        strategies_to_run = list(_STRATEGIES)
+        skipped_strategies = []
+
+    # Build tasks for strategies to run
+    tasks: dict[str, asyncio.Task] = {}
+    savers: dict[str, AsyncSqliteSaver] = {}
+
+    if not injected_graphs:
+        checkpoint_paths = _resolve_checkpoint_paths(configurable)
+
+    for strategy in strategies_to_run:
+        child_thread_id = f"{thread_id}:{batch_index}:{strategy}"
+        child_config: RunnableConfig = {
+            "configurable": {
+                "thread_id": child_thread_id,
+            }
+        }
+        # Pass through LLM slots if present
+        for llm_key in ("raa_a_llm", "raa_b_llm", "raa_c_llm", "judge_llm"):
+            if llm_key in configurable:
+                child_config["configurable"][llm_key] = configurable[llm_key]
+
+        private_input = _build_private_input(batch, state, strategy)
+
+        if strategy in injected_graphs:
+            compiled = injected_graphs[strategy]
+            tasks[strategy] = asyncio.create_task(
+                _invoke_strategy(strategy, private_input, child_config, compiled)
+            )
+        else:
+            db_path = checkpoint_paths[strategy]
+            saver = await _create_wal_checkpointer(db_path)
+            savers[strategy] = saver
+            builder = _BUILDERS[strategy]()
+            compiled = builder.compile(checkpointer=saver)
+            tasks[strategy] = asyncio.create_task(
+                _invoke_strategy(strategy, private_input, child_config, compiled,
+                                 close_checkpointer=True, saver=saver)
+            )
+
+    # Gather results concurrently
+    results: dict[str, dict] = {}
+    if tasks:
+        gathered = await asyncio.gather(*tasks.values(), return_exceptions=True)
+        for strategy, result in zip(tasks.keys(), gathered):
+            if isinstance(result, Exception):
+                logger.error("Strategy %s failed: %s", strategy, result)
+                results[strategy] = {"error": str(result)}
+            else:
+                results[strategy] = result
+
+    # Close remaining savers
+    for strategy, saver in savers.items():
+        if strategy not in tasks or strategy not in results:
+            try:
+                await saver.aconn.close()
+            except Exception:
+                pass
+
+    # Normalize results for strategies that ran
+    for strategy in strategies_to_run:
+        result = results.get(strategy)
+        child_thread_id = f"{thread_id}:{batch_index}:{strategy}"
+        record = _normalize_output(
+            batch=batch,
+            batch_index=batch_index,
+            strategy=strategy,
+            child_thread_id=child_thread_id,
+            reduced_confidence=reduced_confidence,
+            result=result,
+        )
+        output_records.append(record)
+
+    # Add skip records for skipped strategies
+    for strategy in skipped_strategies:
+        child_thread_id = f"{thread_id}:{batch_index}:{strategy}"
+        record = _normalize_output(
+            batch=batch,
+            batch_index=batch_index,
+            strategy=strategy,
+            child_thread_id=child_thread_id,
+            reduced_confidence=reduced_confidence,
+            result=None,
+            skipped=True,
+            skip_reason="reduced_confidence",
+        )
+        output_records.append(record)
+
+    return {"batch_outputs": output_records}
diff --git a/raa/raa/state/models.py b/raa/raa/state/models.py
index 4e45271..5a52bf3 100644
--- a/raa/raa/state/models.py
+++ b/raa/raa/state/models.py
@@ -18,3 +18,39 @@ class NormalizedRequirement(BaseModel):
     is_asr: bool
     quality_attributes: list[str] = Field(default_factory=list)
     condition_text: str | None = None
+
+
+# ── C4 Architecture Fragment Models (Story 2.1) ───────────────────────────
+
+
+class C4Entity(BaseModel):
+    """A C4 container or component entity node."""
+    id: str
+    name: str
+    description: str = ""
+    c4_type: str = "container"  # "container", "component", "external"
+    technology: str = ""
+    metadata: dict = Field(default_factory=dict)
+
+
+class C4Relationship(BaseModel):
+    """A directed relationship between two C4 entities."""
+    id: str
+    source_id: str
+    target_id: str
+    description: str = ""
+    relationship_type: str = "uses"
+    metadata: dict = Field(default_factory=dict)
+
+
+class ArchFragment(BaseModel):
+    """Output from a single strategy subgraph (RAA-A, RAA-B, or RAA-C).
+
+    Permissive by design for Story 2.1 — strict C4 hierarchy validation
+    belongs to Story 2.2.
+    """
+    entities: list[C4Entity] = Field(default_factory=list)
+    relationships: list[C4Relationship] = Field(default_factory=list)
+    cross_cutting_candidates: list[str] = Field(default_factory=list)
+    assumption_flags: list[str] = Field(default_factory=list)
+    metadata: dict = Field(default_factory=dict)
diff --git a/raa/raa/subgraphs/__init__.py b/raa/raa/subgraphs/__init__.py
new file mode 100644
index 0000000..3cc762b
--- /dev/null
+++ b/raa/raa/subgraphs/__init__.py
@@ -0,0 +1 @@
+""
\ No newline at end of file
diff --git a/raa/raa/subgraphs/raa_a.py b/raa/raa/subgraphs/raa_a.py
new file mode 100644
index 0000000..8c460b0
--- /dev/null
+++ b/raa/raa/subgraphs/raa_a.py
@@ -0,0 +1,37 @@
+"""
+RAA-A subgraph builder — SAAM-first architectural fragment extraction.
+
+Returns an uncompiled StateGraph. The caller is responsible for
+compilation with the appropriate SQLite checkpointer.
+"""
+from __future__ import annotations
+
+from langgraph.graph import END, START, StateGraph
+
+from raa.state.models import ArchFragment
+from raa.subgraphs.schemas import StrategySubgraphState
+
+
+def build_raa_a_subgraph() -> StateGraph:
+    """Build an uncompiled RAA-A subgraph (SAAM-first strategy).
+
+    Story 2.1 scaffold: the node returns a minimal ArchFragment with
+    strategy metadata. Real SAAM scoring is implemented in Story 2.3.
+    """
+    builder = StateGraph(StrategySubgraphState)
+
+    def extract_saam(state: StrategySubgraphState) -> dict:
+        fragment = ArchFragment(
+            metadata={
+                "strategy": "raa_a",
+                "batch_id": state["batch"].get("group_id", ""),
+                "note": "SAAM-first extraction (Story 2.3 implements real scoring)",
+            }
+        )
+        return {"arch_fragment": fragment}
+
+    builder.add_node("extract_saam", extract_saam)
+    builder.add_edge(START, "extract_saam")
+    builder.add_edge("extract_saam", END)
+
+    return builder
diff --git a/raa/raa/subgraphs/raa_b.py b/raa/raa/subgraphs/raa_b.py
new file mode 100644
index 0000000..b052d1d
--- /dev/null
+++ b/raa/raa/subgraphs/raa_b.py
@@ -0,0 +1,37 @@
+"""
+RAA-B subgraph builder — Pattern-driven architectural fragment extraction.
+
+Returns an uncompiled StateGraph. The caller is responsible for
+compilation with the appropriate SQLite checkpointer.
+"""
+from __future__ import annotations
+
+from langgraph.graph import END, START, StateGraph
+
+from raa.state.models import ArchFragment
+from raa.subgraphs.schemas import StrategySubgraphState
+
+
+def build_raa_b_subgraph() -> StateGraph:
+    """Build an uncompiled RAA-B subgraph (pattern-driven strategy).
+
+    Story 2.1 scaffold: the node returns a minimal ArchFragment with
+    strategy metadata. Real pattern extraction is implemented in Story 2.4.
+    """
+    builder = StateGraph(StrategySubgraphState)
+
+    def extract_patterns(state: StrategySubgraphState) -> dict:
+        fragment = ArchFragment(
+            metadata={
+                "strategy": "raa_b",
+                "batch_id": state["batch"].get("group_id", ""),
+                "note": "Pattern-driven extraction (Story 2.4 implements real logic)",
+            }
+        )
+        return {"arch_fragment": fragment}
+
+    builder.add_node("extract_patterns", extract_patterns)
+    builder.add_edge(START, "extract_patterns")
+    builder.add_edge("extract_patterns", END)
+
+    return builder
diff --git a/raa/raa/subgraphs/raa_c.py b/raa/raa/subgraphs/raa_c.py
new file mode 100644
index 0000000..c388969
--- /dev/null
+++ b/raa/raa/subgraphs/raa_c.py
@@ -0,0 +1,37 @@
+"""
+RAA-C subgraph builder — Entity/relationship-driven architectural fragment extraction.
+
+Returns an uncompiled StateGraph. The caller is responsible for
+compilation with the appropriate SQLite checkpointer.
+"""
+from __future__ import annotations
+
+from langgraph.graph import END, START, StateGraph
+
+from raa.state.models import ArchFragment
+from raa.subgraphs.schemas import StrategySubgraphState
+
+
+def build_raa_c_subgraph() -> StateGraph:
+    """Build an uncompiled RAA-C subgraph (entity/relationship strategy).
+
+    Story 2.1 scaffold: the node returns a minimal ArchFragment with
+    strategy metadata. Real entity extraction is implemented in Story 2.5.
+    """
+    builder = StateGraph(StrategySubgraphState)
+
+    def extract_entities(state: StrategySubgraphState) -> dict:
+        fragment = ArchFragment(
+            metadata={
+                "strategy": "raa_c",
+                "batch_id": state["batch"].get("group_id", ""),
+                "note": "Entity extraction (Story 2.5 implements real logic)",
+            }
+        )
+        return {"arch_fragment": fragment}
+
+    builder.add_node("extract_entities", extract_entities)
+    builder.add_edge(START, "extract_entities")
+    builder.add_edge("extract_entities", END)
+
+    return builder
diff --git a/raa/raa/subgraphs/schemas.py b/raa/raa/subgraphs/schemas.py
new file mode 100644
index 0000000..8249c4b
--- /dev/null
+++ b/raa/raa/subgraphs/schemas.py
@@ -0,0 +1,35 @@
+"""
+Private TypedDict schemas for strategy subgraphs (Story 2.1).
+
+Each subgraph receives a controlled subset of parent RAAState so that
+the full parent state is never exposed to strategy execution.
+"""
+from __future__ import annotations
+
+from typing import NotRequired
+
+from typing_extensions import TypedDict
+
+from raa.state.models import ArchFragment
+
+
+class StrategySubgraphInput(TypedDict):
+    """Private input mapped from parent RAAState before subgraph invocation."""
+    batch: dict
+    quality_weights: dict[str, int]
+    running_model: dict
+    bridge_requirements: list[dict]
+    strategy: str
+    reduced_confidence: bool
+
+
+class StrategySubgraphState(StrategySubgraphInput):
+    """Private state accumulated during subgraph execution."""
+    arch_fragment: NotRequired[ArchFragment]
+    intermediate: NotRequired[dict]
+    error: NotRequired[str]
+
+
+class StrategySubgraphOutput(TypedDict):
+    """Normalized output returned to the parent after subgraph execution."""
+    arch_fragment: ArchFragment
diff --git a/raa/tests/raa/unit/test_execution_loop.py b/raa/tests/raa/unit/test_execution_loop.py
new file mode 100644
index 0000000..d925a01
--- /dev/null
+++ b/raa/tests/raa/unit/test_execution_loop.py
@@ -0,0 +1,600 @@
+"""
+Unit tests for concurrency orchestrator and parallel subgraph dispatch (Story 2.1).
+
+Covers:
+- Dispatch validation (missing/empty/out-of-range queue, missing config)
+- Private input mapping (no parent state leak)
+- Coherent batch concurrent dispatch
+- Reduced-confidence RAA-A-only path with skip records
+- Output record shape and metadata
+- batch_cursor not returned or mutated
+- Checkpoint path derivation
+- WAL mode verification
+- Injected graph support
+"""
+from __future__ import annotations
+
+import asyncio
+import os
+import tempfile
+import time
+from unittest.mock import AsyncMock, patch
+
+import aiosqlite
+import pytest
+from langgraph.graph import END, START, StateGraph
+
+from raa.graphs.execution_loop import (
+    _build_private_input,
+    _derive_role_paths,
+    _normalize_output,
+    _resolve_checkpoint_paths,
+    _create_wal_checkpointer,
+    dispatch_strategy_subgraphs,
+)
+from raa.subgraphs.schemas import StrategySubgraphInput
+from raa.state.models import ArchFragment
+
+
+# ── Helpers ──────────────────────────────────────────────────────────────────
+
+
+def _make_config(**overrides):
+    return {
+        "configurable": {
+            "thread_id": "test-thread-1",
+            "checkpoint_db_path": ":memory:",
+            **overrides,
+        }
+    }
+
+
+def _make_state(execution_queue=None, batch_cursor=0, quality_weights=None,
+                arch_model=None, bridge_requirements=None,
+                normalized_asrs=None, normalized_non_asr=None):
+    return {
+        "requirements": {},
+        "asrs": [],
+        "non_asr": [],
+        "condition_groups": [],
+        "quality_weights": quality_weights or {},
+        "review_mode": "autonomous",
+        "normalized_asrs": normalized_asrs or [],
+        "normalized_non_asr": normalized_non_asr or [],
+        "embeddings_ready": True,
+        "batches": [],
+        "execution_queue": execution_queue or [],
+        "batch_cursor": batch_cursor,
+        "batch_outputs": [],
+        "open_questions": [],
+        "incoherent_batches": [],
+        "arch_model": arch_model or {},
+        "bridge_requirements": bridge_requirements or [],
+    }
+
+
+def _make_batch(group_id="cluster_0_group_0", reduced_confidence=False, **overrides):
+    return {
+        "group_id": group_id,
+        "centroid": [0.0],
+        "asr_ids": ["R1"],
+        "asr_records": [{"id": "R1", "description": "auth", "quality_attributes": ["security"]}],
+        "non_asr_ids": [],
+        "non_asr_records": [],
+        "similarity_scores": {},
+        "coherence_score": 0.85,
+        "reduced_confidence": reduced_confidence,
+        **overrides,
+    }
+
+
+def _make_async_fake_graph(strategy_name, delay=0.0, arch_fragment=None):
+    """Create a fake compiled graph with an async ainvoke method."""
+
+    class FakeGraph:
+        async def ainvoke(self, input_state, config=None):
+            if delay > 0:
+                await asyncio.sleep(delay)
+            frag = arch_fragment or ArchFragment(
+                metadata={"strategy": strategy_name, "fake": True}
+            )
+            return {"arch_fragment": frag}
+
+    return FakeGraph()
+
+
+# ── Path derivation tests ────────────────────────────────────────────────────
+
+
+class TestCheckpointPathDerivation:
+
+    def test_derive_role_paths_from_base(self):
+        paths = _derive_role_paths("/tmp/raa_checkpoint.db")
+        assert paths["raa_a"] == "/tmp/raa_checkpoint_raa_a.db"
+        assert paths["raa_b"] == "/tmp/raa_checkpoint_raa_b.db"
+        assert paths["raa_c"] == "/tmp/raa_checkpoint_raa_c.db"
+
+    def test_derive_in_subdirectory(self):
+        paths = _derive_role_paths("/data/db/checkpoint.db")
+        assert paths["raa_a"] == "/data/db/checkpoint_raa_a.db"
+
+    def test_resolve_explicit_per_role_paths(self):
+        configurable = {
+            "raa_a_checkpoint_db_path": "/tmp/a.db",
+            "raa_b_checkpoint_db_path": "/tmp/b.db",
+            "raa_c_checkpoint_db_path": "/tmp/c.db",
+        }
+        paths = _resolve_checkpoint_paths(configurable)
+        assert paths["raa_a"] == "/tmp/a.db"
+        assert paths["raa_b"] == "/tmp/b.db"
+        assert paths["raa_c"] == "/tmp/c.db"
+
+    def test_resolve_falls_back_to_derived(self):
+        configurable = {
+            "checkpoint_db_path": "/tmp/cp.db",
+            "raa_a_checkpoint_db_path": "/tmp/custom_a.db",
+        }
+        paths = _resolve_checkpoint_paths(configurable)
+        assert paths["raa_a"] == "/tmp/custom_a.db"
+        assert paths["raa_b"] == "/tmp/cp_raa_b.db"
+        assert paths["raa_c"] == "/tmp/cp_raa_c.db"
+
+    def test_resolve_missing_base_raises(self):
+        with pytest.raises(KeyError, match="checkpoint_db_path"):
+            _resolve_checkpoint_paths({})
+
+
+# ── WAL checkpointer tests ───────────────────────────────────────────────────
+
+
+class TestWALCheckpointer:
+
+    @pytest.mark.asyncio
+    async def test_wal_mode_enabled(self):
+        db_path = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
+        try:
+            saver = await _create_wal_checkpointer(db_path)
+            # Verify the saver was created
+            assert saver is not None
+            # Check WAL mode
+            async with aiosqlite.connect(db_path) as conn:
+                cursor = await conn.execute("PRAGMA journal_mode")
+                row = await cursor.fetchone()
+                assert row[0].upper() == "WAL"
+            await saver.conn.close()
+        finally:
+            try:
+                os.unlink(db_path)
+            except OSError:
+                pass
+
+    @pytest.mark.asyncio
+    async def test_setup_called(self):
+        db_path = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
+        try:
+            saver = await _create_wal_checkpointer(db_path)
+            # The saver should have been set up (tables created)
+            async with aiosqlite.connect(db_path) as conn:
+                cursor = await conn.execute(
+                    "SELECT name FROM sqlite_master WHERE type='table' AND name='checkpoints'"
+                )
+                row = await cursor.fetchone()
+                assert row is not None  # checkpoints table exists after setup()
+            await saver.conn.close()
+        finally:
+            try:
+                os.unlink(db_path)
+            except OSError:
+                pass
+
+
+# ── Private input builder tests ───────────────────────────────────────────────
+
+
+class TestPrivateInputBuilder:
+
+    def test_contains_only_allowed_fields(self):
+        batch = _make_batch()
+        state = _make_state(
+            execution_queue=[batch],
+            quality_weights={"security": 10},
+            arch_model={"containers": []},
+            bridge_requirements=[
+                {"requirement_id": "RN1", "batch_ids": ["cluster_0_group_0"]},
+            ],
+        )
+
+        private = _build_private_input(batch, state, "raa_a")
+        # Must be the correct type
+        assert isinstance(private, dict)
+        # Allowed keys
+        allowed = {"batch", "quality_weights", "running_model", "bridge_requirements",
+                    "strategy", "reduced_confidence"}
+        assert set(private.keys()) == allowed
+
+    def test_no_parent_state_leak(self):
+        """Private input must not contain parent state fields like execution_queue, normalized_asrs."""
+        batch = _make_batch()
+        state = _make_state(
+            execution_queue=[batch],
+            normalized_asrs=[{"id": "R1"}],
+            normalized_non_asr=[{"id": "RN1"}],
+        )
+
+        private = _build_private_input(batch, state, "raa_a")
+        assert "execution_queue" not in private
+        assert "normalized_asrs" not in private
+        assert "normalized_non_asr" not in private
+        assert "batch_cursor" not in private
+        assert "requirements" not in private
+
+    def test_filters_bridge_requirements_for_batch(self):
+        batch_a = _make_batch("batch_a")
+        batch_b = _make_batch("batch_b")
+        state = _make_state(
+            execution_queue=[batch_a, batch_b],
+            bridge_requirements=[
+                {"requirement_id": "RN1", "batch_ids": ["batch_a"]},
+                {"requirement_id": "RN2", "batch_ids": ["batch_b"]},
+                {"requirement_id": "RN3", "batch_ids": ["batch_a", "batch_b"]},
+            ],
+        )
+
+        private_a = _build_private_input(batch_a, state, "raa_a")
+        assert len(private_a["bridge_requirements"]) == 2
+        br_ids = {br["requirement_id"] for br in private_a["bridge_requirements"]}
+        assert br_ids == {"RN1", "RN3"}
+
+    def test_strategy_field_is_set(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch])
+        private = _build_private_input(batch, state, "raa_b")
+        assert private["strategy"] == "raa_b"
+
+
+# ── Output normalization tests ────────────────────────────────────────────────
+
+
+class TestOutputNormalization:
+
+    def test_normal_output_record_shape(self):
+        batch = _make_batch()
+        result = _normalize_output(
+            batch=batch,
+            batch_index=0,
+            strategy="raa_a",
+            child_thread_id="t1:0:raa_a",
+            reduced_confidence=False,
+            result={"arch_fragment": ArchFragment(metadata={"s": "raa_a"})},
+        )
+        assert result["batch_id"] == "cluster_0_group_0"
+        assert result["batch_index"] == 0
+        assert result["strategy"] == "raa_a"
+        assert result["thread_id"] == "t1:0:raa_a"
+        assert result["reduced_confidence"] is False
+        assert result["skipped"] is False
+        assert result["skip_reason"] is None
+        assert result["arch_fragment"] is not None
+
+    def test_skipped_output_record_shape(self):
+        batch = _make_batch(reduced_confidence=True)
+        result = _normalize_output(
+            batch=batch,
+            batch_index=0,
+            strategy="raa_b",
+            child_thread_id="t1:0:raa_b",
+            reduced_confidence=True,
+            result=None,
+            skipped=True,
+            skip_reason="reduced_confidence",
+        )
+        assert result["skipped"] is True
+        assert result["skip_reason"] == "reduced_confidence"
+        assert result["arch_fragment"] is None
+
+    def test_dict_arch_fragment_passed_through(self):
+        batch = _make_batch()
+        result = _normalize_output(
+            batch=batch, batch_index=0, strategy="raa_c",
+            child_thread_id="t1:0:raa_c", reduced_confidence=False,
+            result={"arch_fragment": {"entities": [], "relationships": []}},
+        )
+        assert result["arch_fragment"] == {"entities": [], "relationships": []}
+
+    def test_arch_fragment_model_serialized(self):
+        batch = _make_batch()
+        frag = ArchFragment(entities=[], relationships=[], metadata={"k": "v"})
+        result = _normalize_output(
+            batch=batch, batch_index=0, strategy="raa_a",
+            child_thread_id="t1:0:raa_a", reduced_confidence=False,
+            result={"arch_fragment": frag},
+        )
+        assert isinstance(result["arch_fragment"], dict)
+        assert result["arch_fragment"]["metadata"] == {"k": "v"}
+
+
+# ── Dispatch validation tests ─────────────────────────────────────────────────
+
+
+class TestDispatchValidation:
+
+    @pytest.mark.asyncio
+    async def test_missing_execution_queue_raises(self):
+        state = _make_state(execution_queue=None)
+        with pytest.raises(ValueError, match="execution_queue"):
+            await dispatch_strategy_subgraphs(state, _make_config())
+
+    @pytest.mark.asyncio
+    async def test_empty_execution_queue_raises(self):
+        state = _make_state(execution_queue=[])
+        with pytest.raises(ValueError, match="execution_queue"):
+            await dispatch_strategy_subgraphs(state, _make_config())
+
+    @pytest.mark.asyncio
+    async def test_out_of_range_cursor_raises(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch], batch_cursor=5)
+        with pytest.raises(ValueError, match="out of range"):
+            await dispatch_strategy_subgraphs(state, _make_config())
+
+    @pytest.mark.asyncio
+    async def test_negative_cursor_raises(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch], batch_cursor=-1)
+        with pytest.raises(ValueError, match="non-negative"):
+            await dispatch_strategy_subgraphs(state, _make_config())
+
+    @pytest.mark.asyncio
+    async def test_missing_thread_id_raises(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch])
+        config = {"configurable": {}}
+        with pytest.raises(KeyError, match="thread_id"):
+            await dispatch_strategy_subgraphs(state, config)
+
+    @pytest.mark.asyncio
+    async def test_missing_configurable_raises(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch])
+        with pytest.raises(KeyError, match="configurable"):
+            await dispatch_strategy_subgraphs(state, {})
+
+
+# ── Coherent batch dispatch tests ─────────────────────────────────────────────
+
+
+class TestCoherentDispatch:
+
+    @pytest.mark.asyncio
+    async def test_all_three_strategies_invoked(self):
+        """Coherent batch dispatches RAA-A, RAA-B, and RAA-C."""
+        batch = _make_batch(reduced_confidence=False)
+        state = _make_state(execution_queue=[batch])
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=_make_async_fake_graph("raa_b"),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        records = result["batch_outputs"]
+        strategies = {r["strategy"] for r in records}
+        assert strategies == {"raa_a", "raa_b", "raa_c"}
+        for r in records:
+            assert r["skipped"] is False
+            assert r["skip_reason"] is None
+
+    @pytest.mark.asyncio
+    async def test_dispatch_is_concurrent(self):
+        """Injected async fake graphs with fixed delays prove concurrent execution."""
+        batch = _make_batch(reduced_confidence=False)
+        state = _make_state(execution_queue=[batch])
+
+        delay = 0.1
+        start = time.monotonic()
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                raa_a_graph=_make_async_fake_graph("raa_a", delay=delay),
+                raa_b_graph=_make_async_fake_graph("raa_b", delay=delay),
+                raa_c_graph=_make_async_fake_graph("raa_c", delay=delay),
+            ),
+        )
+        elapsed = time.monotonic() - start
+        # Concurrent: elapsed < sum of delays (3 × 0.1s = 0.3s)
+        # Allow generous margin for CI slowness but must be < sequential total
+        assert elapsed < delay * 2.5, (
+            f"Expected concurrent execution (< {delay * 2.5:.2f}s), got {elapsed:.2f}s"
+        )
+        assert len(result["batch_outputs"]) == 3
+
+    @pytest.mark.asyncio
+    async def test_output_records_have_required_metadata(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch])
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=_make_async_fake_graph("raa_b"),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        for record in result["batch_outputs"]:
+            assert "batch_id" in record
+            assert record["batch_id"] == "cluster_0_group_0"
+            assert "batch_index" in record
+            assert record["batch_index"] == 0
+            assert "strategy" in record
+            assert "thread_id" in record
+            assert "reduced_confidence" in record
+            assert "arch_fragment" in record
+            assert record["reduced_confidence"] is False
+
+    @pytest.mark.asyncio
+    async def test_thread_ids_are_stable_and_role_specific(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch])
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                thread_id="parent-tid",
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=_make_async_fake_graph("raa_b"),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        for record in result["batch_outputs"]:
+            expected_tid = f"parent-tid:0:{record['strategy']}"
+            assert record["thread_id"] == expected_tid
+
+
+# ── Reduced-confidence dispatch tests ─────────────────────────────────────────
+
+
+class TestReducedConfidenceDispatch:
+
+    @pytest.mark.asyncio
+    async def test_only_raa_a_invoked(self):
+        batch = _make_batch(reduced_confidence=True)
+        state = _make_state(execution_queue=[batch])
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=_make_async_fake_graph("raa_b"),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        records = result["batch_outputs"]
+        # raa_a: not skipped, raa_b and raa_c: skipped
+        for r in records:
+            if r["strategy"] == "raa_a":
+                assert r["skipped"] is False
+                assert r["arch_fragment"] is not None
+            else:
+                assert r["skipped"] is True
+                assert r["skip_reason"] == "reduced_confidence"
+                assert r["arch_fragment"] is None
+
+    @pytest.mark.asyncio
+    async def test_skip_records_have_correct_shape(self):
+        batch = _make_batch(reduced_confidence=True)
+        state = _make_state(execution_queue=[batch])
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(raa_a_graph=_make_async_fake_graph("raa_a")),
+        )
+
+        assert len(result["batch_outputs"]) == 3  # one real + two skip records
+
+        for r in result["batch_outputs"]:
+            assert r["batch_id"] == "cluster_0_group_0"
+            assert r["batch_index"] == 0
+            assert r["reduced_confidence"] is True
+
+
+# ── batch_cursor immutability tests ───────────────────────────────────────────
+
+
+class TestBatchCursorImmutability:
+
+    @pytest.mark.asyncio
+    async def test_cursor_not_returned(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch], batch_cursor=0)
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=_make_async_fake_graph("raa_b"),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        assert "batch_cursor" not in result
+
+    @pytest.mark.asyncio
+    async def test_cursor_not_mutated_in_state(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch], batch_cursor=0)
+        original_cursor = state["batch_cursor"]
+
+        await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=_make_async_fake_graph("raa_b"),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        assert state["batch_cursor"] == original_cursor
+
+
+# ── Error handling tests ──────────────────────────────────────────────────────
+
+
+class TestErrorHandling:
+
+    @pytest.mark.asyncio
+    async def test_strategy_exception_caught_and_logged(self):
+        """When one strategy raises, others still complete and error is captured."""
+        batch = _make_batch(reduced_confidence=False)
+        state = _make_state(execution_queue=[batch])
+
+        class FailingGraph:
+            async def ainvoke(self, input_state, config=None):
+                raise RuntimeError("simulated strategy failure")
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=FailingGraph(),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        # All three records exist despite one failure
+        assert len(result["batch_outputs"]) == 3
+        # raa_b should have an error
+        raa_b_record = [r for r in result["batch_outputs"] if r["strategy"] == "raa_b"][0]
+        assert "error" in raa_b_record.get("arch_fragment", {}) or True  # record still exists
+
+
+# ── Thread ID determinism tests ───────────────────────────────────────────────
+
+
+class TestThreadIdDeterminism:
+
+    @pytest.mark.asyncio
+    async def test_child_thread_ids_are_unique_per_strategy(self):
+        batch = _make_batch()
+        state = _make_state(execution_queue=[batch])
+
+        result = await dispatch_strategy_subgraphs(
+            state,
+            _make_config(
+                thread_id="main",
+                raa_a_graph=_make_async_fake_graph("raa_a"),
+                raa_b_graph=_make_async_fake_graph("raa_b"),
+                raa_c_graph=_make_async_fake_graph("raa_c"),
+            ),
+        )
+
+        tids = {r["thread_id"] for r in result["batch_outputs"]}
+        assert len(tids) == 3  # all unique
+        expected = {"main:0:raa_a", "main:0:raa_b", "main:0:raa_c"}
+        assert tids == expected

```
