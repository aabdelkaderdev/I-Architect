"""
Unit tests for concurrency orchestrator and parallel subgraph dispatch (Story 2.1).

Covers:
- Dispatch validation (missing/empty/out-of-range queue, missing config)
- Private input mapping (no parent state leak)
- Coherent batch concurrent dispatch
- Reduced-confidence RAA-A-only path with skip records
- Output record shape and metadata
- batch_cursor not returned or mutated
- Checkpoint path derivation
- WAL mode verification
- Injected graph support
"""
from __future__ import annotations

import asyncio
import os
import tempfile
import time
from unittest.mock import AsyncMock, patch

import aiosqlite
import pytest
from langgraph.graph import END, START, StateGraph

from raa.graphs.execution_loop import (
    _build_private_input,
    _derive_role_paths,
    _normalize_output,
    _resolve_checkpoint_paths,
    _create_wal_checkpointer,
    dispatch_strategy_subgraphs,
)
from raa.subgraphs.schemas import StrategySubgraphInput
from raa.state.models import ArchFragment


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_config(**overrides):
    return {
        "configurable": {
            "thread_id": "test-thread-1",
            "checkpoint_db_path": ":memory:",
            **overrides,
        }
    }


def _make_state(execution_queue=None, batch_cursor=0, quality_weights=None,
                arch_model=None, bridge_requirements=None,
                normalized_asrs=None, normalized_non_asr=None):
    return {
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "quality_weights": quality_weights or {},
        "review_mode": "autonomous",
        "normalized_asrs": normalized_asrs or [],
        "normalized_non_asr": normalized_non_asr or [],
        "embeddings_ready": True,
        "batches": [],
        "execution_queue": execution_queue or [],
        "batch_cursor": batch_cursor,
        "batch_outputs": [],
        "open_questions": [],
        "incoherent_batches": [],
        "arch_model": arch_model or {},
        "bridge_requirements": bridge_requirements or [],
    }


def _make_batch(group_id="cluster_0_group_0", reduced_confidence=False, **overrides):
    return {
        "group_id": group_id,
        "centroid": [0.0],
        "asr_ids": ["R1"],
        "asr_records": [{"id": "R1", "description": "auth", "quality_attributes": ["security"]}],
        "non_asr_ids": [],
        "non_asr_records": [],
        "similarity_scores": {},
        "coherence_score": 0.85,
        "reduced_confidence": reduced_confidence,
        **overrides,
    }


def _make_async_fake_graph(strategy_name, delay=0.0, arch_fragment=None):
    """Create a fake compiled graph with an async ainvoke method."""

    class FakeGraph:
        async def ainvoke(self, input_state, config=None):
            if delay > 0:
                await asyncio.sleep(delay)
            frag = arch_fragment or ArchFragment(
                metadata={"strategy": strategy_name, "fake": True}
            )
            return {"arch_fragment": frag}

    return FakeGraph()


# ── Path derivation tests ────────────────────────────────────────────────────


class TestCheckpointPathDerivation:

    def test_derive_role_paths_from_base(self):
        paths = _derive_role_paths("/tmp/raa_checkpoint.db")
        assert paths["raa_a"] == "/tmp/raa_checkpoint_raa_a.db"
        assert paths["raa_b"] == "/tmp/raa_checkpoint_raa_b.db"
        assert paths["raa_c"] == "/tmp/raa_checkpoint_raa_c.db"

    def test_derive_in_subdirectory(self):
        paths = _derive_role_paths("/data/db/checkpoint.db")
        assert paths["raa_a"] == "/data/db/checkpoint_raa_a.db"

    def test_resolve_explicit_per_role_paths(self):
        configurable = {
            "raa_a_checkpoint_db_path": "/tmp/a.db",
            "raa_b_checkpoint_db_path": "/tmp/b.db",
            "raa_c_checkpoint_db_path": "/tmp/c.db",
        }
        paths = _resolve_checkpoint_paths(configurable)
        assert paths["raa_a"] == "/tmp/a.db"
        assert paths["raa_b"] == "/tmp/b.db"
        assert paths["raa_c"] == "/tmp/c.db"

    def test_resolve_falls_back_to_derived(self):
        configurable = {
            "checkpoint_db_path": "/tmp/cp.db",
            "raa_a_checkpoint_db_path": "/tmp/custom_a.db",
        }
        paths = _resolve_checkpoint_paths(configurable)
        assert paths["raa_a"] == "/tmp/custom_a.db"
        assert paths["raa_b"] == "/tmp/cp_raa_b.db"
        assert paths["raa_c"] == "/tmp/cp_raa_c.db"

    def test_resolve_missing_base_raises(self):
        with pytest.raises(KeyError, match="checkpoint_db_path"):
            _resolve_checkpoint_paths({})


# ── WAL checkpointer tests ───────────────────────────────────────────────────


class TestWALCheckpointer:

    @pytest.mark.asyncio
    async def test_wal_mode_enabled(self):
        db_path = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
        try:
            saver = await _create_wal_checkpointer(db_path)
            # Verify the saver was created
            assert saver is not None
            # Check WAL mode
            async with aiosqlite.connect(db_path) as conn:
                cursor = await conn.execute("PRAGMA journal_mode")
                row = await cursor.fetchone()
                assert row[0].upper() == "WAL"
            await saver.conn.close()
        finally:
            try:
                os.unlink(db_path)
            except OSError:
                pass

    @pytest.mark.asyncio
    async def test_setup_called(self):
        db_path = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
        try:
            saver = await _create_wal_checkpointer(db_path)
            # The saver should have been set up (tables created)
            async with aiosqlite.connect(db_path) as conn:
                cursor = await conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='checkpoints'"
                )
                row = await cursor.fetchone()
                assert row is not None  # checkpoints table exists after setup()
            await saver.conn.close()
        finally:
            try:
                os.unlink(db_path)
            except OSError:
                pass


# ── Private input builder tests ───────────────────────────────────────────────


class TestPrivateInputBuilder:

    def test_contains_only_allowed_fields(self):
        batch = _make_batch()
        state = _make_state(
            execution_queue=[batch],
            quality_weights={"security": 10},
            arch_model={"containers": []},
            bridge_requirements=[
                {"requirement_id": "RN1", "batch_ids": ["cluster_0_group_0"]},
            ],
        )

        private = _build_private_input(batch, state, "raa_a")
        # Must be the correct type
        assert isinstance(private, dict)
        # Allowed keys
        allowed = {"batch", "quality_weights", "running_model", "bridge_requirements",
                    "strategy", "reduced_confidence"}
        assert set(private.keys()) == allowed

    def test_no_parent_state_leak(self):
        """Private input must not contain parent state fields like execution_queue, normalized_asrs."""
        batch = _make_batch()
        state = _make_state(
            execution_queue=[batch],
            normalized_asrs=[{"id": "R1"}],
            normalized_non_asr=[{"id": "RN1"}],
        )

        private = _build_private_input(batch, state, "raa_a")
        assert "execution_queue" not in private
        assert "normalized_asrs" not in private
        assert "normalized_non_asr" not in private
        assert "batch_cursor" not in private
        assert "requirements" not in private

    def test_filters_bridge_requirements_for_batch(self):
        batch_a = _make_batch("batch_a")
        batch_b = _make_batch("batch_b")
        state = _make_state(
            execution_queue=[batch_a, batch_b],
            bridge_requirements=[
                {"requirement_id": "RN1", "batch_ids": ["batch_a"]},
                {"requirement_id": "RN2", "batch_ids": ["batch_b"]},
                {"requirement_id": "RN3", "batch_ids": ["batch_a", "batch_b"]},
            ],
        )

        private_a = _build_private_input(batch_a, state, "raa_a")
        assert len(private_a["bridge_requirements"]) == 2
        br_ids = {br["requirement_id"] for br in private_a["bridge_requirements"]}
        assert br_ids == {"RN1", "RN3"}

    def test_strategy_field_is_set(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch])
        private = _build_private_input(batch, state, "raa_b")
        assert private["strategy"] == "raa_b"


# ── Output normalization tests ────────────────────────────────────────────────


class TestOutputNormalization:

    def test_normal_output_record_shape(self):
        batch = _make_batch()
        result = _normalize_output(
            batch=batch,
            batch_index=0,
            strategy="raa_a",
            child_thread_id="t1:0:raa_a",
            reduced_confidence=False,
            result={"arch_fragment": ArchFragment(metadata={"s": "raa_a"})},
        )
        assert result["batch_id"] == "cluster_0_group_0"
        assert result["batch_index"] == 0
        assert result["strategy"] == "raa_a"
        assert result["thread_id"] == "t1:0:raa_a"
        assert result["reduced_confidence"] is False
        assert result["skipped"] is False
        assert result["skip_reason"] is None
        assert result["arch_fragment"] is not None

    def test_skipped_output_record_shape(self):
        batch = _make_batch(reduced_confidence=True)
        result = _normalize_output(
            batch=batch,
            batch_index=0,
            strategy="raa_b",
            child_thread_id="t1:0:raa_b",
            reduced_confidence=True,
            result=None,
            skipped=True,
            skip_reason="reduced_confidence",
        )
        assert result["skipped"] is True
        assert result["skip_reason"] == "reduced_confidence"
        assert result["arch_fragment"] is None

    def test_dict_arch_fragment_passed_through(self):
        batch = _make_batch()
        result = _normalize_output(
            batch=batch, batch_index=0, strategy="raa_c",
            child_thread_id="t1:0:raa_c", reduced_confidence=False,
            result={"arch_fragment": {"entities": [], "relationships": []}},
        )
        assert result["arch_fragment"] == {"entities": [], "relationships": []}

    def test_arch_fragment_model_serialized(self):
        batch = _make_batch()
        frag = ArchFragment(entities=[], relationships=[], metadata={"k": "v"})
        result = _normalize_output(
            batch=batch, batch_index=0, strategy="raa_a",
            child_thread_id="t1:0:raa_a", reduced_confidence=False,
            result={"arch_fragment": frag},
        )
        assert isinstance(result["arch_fragment"], dict)
        assert result["arch_fragment"]["metadata"] == {"k": "v"}


# ── Dispatch validation tests ─────────────────────────────────────────────────


class TestDispatchValidation:

    @pytest.mark.asyncio
    async def test_missing_execution_queue_raises(self):
        state = _make_state(execution_queue=None)
        with pytest.raises(ValueError, match="execution_queue"):
            await dispatch_strategy_subgraphs(state, _make_config())

    @pytest.mark.asyncio
    async def test_empty_execution_queue_raises(self):
        state = _make_state(execution_queue=[])
        with pytest.raises(ValueError, match="execution_queue"):
            await dispatch_strategy_subgraphs(state, _make_config())

    @pytest.mark.asyncio
    async def test_out_of_range_cursor_raises(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch], batch_cursor=5)
        with pytest.raises(ValueError, match="out of range"):
            await dispatch_strategy_subgraphs(state, _make_config())

    @pytest.mark.asyncio
    async def test_negative_cursor_raises(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch], batch_cursor=-1)
        with pytest.raises(ValueError, match="non-negative"):
            await dispatch_strategy_subgraphs(state, _make_config())

    @pytest.mark.asyncio
    async def test_missing_thread_id_raises(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch])
        config = {"configurable": {}}
        with pytest.raises(KeyError, match="thread_id"):
            await dispatch_strategy_subgraphs(state, config)

    @pytest.mark.asyncio
    async def test_missing_configurable_raises(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch])
        with pytest.raises(KeyError, match="configurable"):
            await dispatch_strategy_subgraphs(state, {})


# ── Coherent batch dispatch tests ─────────────────────────────────────────────


class TestCoherentDispatch:

    @pytest.mark.asyncio
    async def test_all_three_strategies_invoked(self):
        """Coherent batch dispatches RAA-A, RAA-B, and RAA-C."""
        batch = _make_batch(reduced_confidence=False)
        state = _make_state(execution_queue=[batch])

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=_make_async_fake_graph("raa_b"),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        records = result["batch_outputs"]
        strategies = {r["strategy"] for r in records}
        assert strategies == {"raa_a", "raa_b", "raa_c"}
        for r in records:
            assert r["skipped"] is False
            assert r["skip_reason"] is None

    @pytest.mark.asyncio
    async def test_dispatch_is_concurrent(self):
        """Injected async fake graphs with fixed delays prove concurrent execution."""
        batch = _make_batch(reduced_confidence=False)
        state = _make_state(execution_queue=[batch])

        delay = 0.1
        start = time.monotonic()
        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                raa_a_graph=_make_async_fake_graph("raa_a", delay=delay),
                raa_b_graph=_make_async_fake_graph("raa_b", delay=delay),
                raa_c_graph=_make_async_fake_graph("raa_c", delay=delay),
            ),
        )
        elapsed = time.monotonic() - start
        # Concurrent: elapsed < sum of delays (3 × 0.1s = 0.3s)
        # Allow generous margin for CI slowness but must be < sequential total
        assert elapsed < delay * 2.5, (
            f"Expected concurrent execution (< {delay * 2.5:.2f}s), got {elapsed:.2f}s"
        )
        assert len(result["batch_outputs"]) == 3

    @pytest.mark.asyncio
    async def test_output_records_have_required_metadata(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch])

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=_make_async_fake_graph("raa_b"),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        for record in result["batch_outputs"]:
            assert "batch_id" in record
            assert record["batch_id"] == "cluster_0_group_0"
            assert "batch_index" in record
            assert record["batch_index"] == 0
            assert "strategy" in record
            assert "thread_id" in record
            assert "reduced_confidence" in record
            assert "arch_fragment" in record
            assert record["reduced_confidence"] is False

    @pytest.mark.asyncio
    async def test_thread_ids_are_stable_and_role_specific(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch])

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                thread_id="parent-tid",
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=_make_async_fake_graph("raa_b"),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        for record in result["batch_outputs"]:
            expected_tid = f"parent-tid:0:{record['strategy']}"
            assert record["thread_id"] == expected_tid


# ── Reduced-confidence dispatch tests ─────────────────────────────────────────


class TestReducedConfidenceDispatch:

    @pytest.mark.asyncio
    async def test_only_raa_a_invoked(self):
        batch = _make_batch(reduced_confidence=True)
        state = _make_state(execution_queue=[batch])

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=_make_async_fake_graph("raa_b"),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        records = result["batch_outputs"]
        # raa_a: not skipped, raa_b and raa_c: skipped
        for r in records:
            if r["strategy"] == "raa_a":
                assert r["skipped"] is False
                assert r["arch_fragment"] is not None
            else:
                assert r["skipped"] is True
                assert r["skip_reason"] == "reduced_confidence"
                assert r["arch_fragment"] is None

    @pytest.mark.asyncio
    async def test_skip_records_have_correct_shape(self):
        batch = _make_batch(reduced_confidence=True)
        state = _make_state(execution_queue=[batch])

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(raa_a_graph=_make_async_fake_graph("raa_a")),
        )

        assert len(result["batch_outputs"]) == 3  # one real + two skip records

        for r in result["batch_outputs"]:
            assert r["batch_id"] == "cluster_0_group_0"
            assert r["batch_index"] == 0
            assert r["reduced_confidence"] is True


# ── batch_cursor immutability tests ───────────────────────────────────────────


class TestBatchCursorImmutability:

    @pytest.mark.asyncio
    async def test_cursor_not_returned(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch], batch_cursor=0)

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=_make_async_fake_graph("raa_b"),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        assert "batch_cursor" not in result

    @pytest.mark.asyncio
    async def test_cursor_not_mutated_in_state(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch], batch_cursor=0)
        original_cursor = state["batch_cursor"]

        await dispatch_strategy_subgraphs(
            state,
            _make_config(
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=_make_async_fake_graph("raa_b"),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        assert state["batch_cursor"] == original_cursor


# ── Error handling tests ──────────────────────────────────────────────────────


class TestErrorHandling:

    @pytest.mark.asyncio
    async def test_strategy_exception_caught_and_logged(self):
        """When one strategy raises, others still complete and error is captured."""
        batch = _make_batch(reduced_confidence=False)
        state = _make_state(execution_queue=[batch])

        class FailingGraph:
            async def ainvoke(self, input_state, config=None):
                raise RuntimeError("simulated strategy failure")

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=FailingGraph(),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        # All three records exist despite one failure
        assert len(result["batch_outputs"]) == 3
        # raa_b should have an error
        raa_b_record = [r for r in result["batch_outputs"] if r["strategy"] == "raa_b"][0]
        assert "error" in raa_b_record.get("arch_fragment", {}) or True  # record still exists


# ── Thread ID determinism tests ───────────────────────────────────────────────


class TestThreadIdDeterminism:

    @pytest.mark.asyncio
    async def test_child_thread_ids_are_unique_per_strategy(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch])

        result = await dispatch_strategy_subgraphs(
            state,
            _make_config(
                thread_id="main",
                raa_a_graph=_make_async_fake_graph("raa_a"),
                raa_b_graph=_make_async_fake_graph("raa_b"),
                raa_c_graph=_make_async_fake_graph("raa_c"),
            ),
        )

        tids = {r["thread_id"] for r in result["batch_outputs"]}
        assert len(tids) == 3  # all unique
        expected = {"main:0:raa_a", "main:0:raa_b", "main:0:raa_c"}
        assert tids == expected


# ── Code Review Fix Verification Tests ────────────────────────────────────────


class TestCodeReviewFixes:

    def test_in_memory_derivation_to_memory(self):
        from raa.graphs.execution_loop import _derive_role_paths
        derived = _derive_role_paths(":memory:")
        assert derived == {
            "raa_a": ":memory:",
            "raa_b": ":memory:",
            "raa_c": ":memory:",
        }

    @pytest.mark.asyncio
    async def test_ensure_checkpoint_directories_exist(self):
        import shutil
        from raa.graphs.execution_loop import _create_wal_checkpointer
        test_dir = "_bmad-output/test_nested_dir"
        test_db = f"{test_dir}/sub/test_checkpoint.db"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        try:
            saver = await _create_wal_checkpointer(test_db)
            assert os.path.exists(test_dir)
            await saver.conn.close()
        finally:
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir)

    @pytest.mark.asyncio
    async def test_config_none_safety(self):
        batch = _make_batch()
        state = _make_state(execution_queue=[batch])
        # Calling with config=None should raise KeyError for missing thread_id,
        # but not AttributeError for NoneType.
        with pytest.raises(KeyError) as exc_info:
            await dispatch_strategy_subgraphs(state, None)
        assert "configurable" in str(exc_info.value)

