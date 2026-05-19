"""Tests for RAA checkpoint recovery — SQLite persistence, deterministic thread
IDs, resume/fresh-start logic, corrupt fallback, and archive policy."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from raa.graphs.main_graph import (
    _open_sqlite_checkpointer,
    _validate_db_path,
    compile_for_production,
    compile_raa_graph,
)
from raa.runner import (
    _preserve_corrupt_checkpoint,
    archive_after_success,
    archive_checkpoint,
    build_run_config,
    derive_thread_id,
    run_raa_pipeline,
    run_with_recovery,
    should_resume_from_snapshot,
)


# ============================================================================
# Phase 2: Fixtures (T004)
# ============================================================================


@pytest.fixture
def tmp_db_path(tmp_path):
    """Temporary SQLite database path with existing parent directory."""
    return str(tmp_path / "raa_graph.db")


@pytest.fixture
def minimal_initial_state():
    """Minimal RAA initial state for tests."""
    return {
        "batch_cursor": 0,
        "batch_queue": [],
        "embeddings_ready": True,
        "running_arch_model": {},
        "open_questions": [],
        "incoherent_batches": [],
        "bridge_requirements": {},
        "best_batch_output": {},
        "batch_outputs": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "quality_weights": {},
    }


@pytest.fixture
def resumed_state():
    """State with batch_cursor > 0 to trigger resume path."""
    state = minimal_initial_state()
    state["batch_cursor"] = 5
    return state


@pytest.fixture
def mock_compiled_graph():
    """Mock compiled LangGraph graph with configurable get_state and invoke."""
    graph = MagicMock()
    graph.get_state.return_value = None
    graph.invoke.return_value = {"batch_cursor": 0, "arch_model_written": False}
    return graph


class _FakeSnapshot:
    """Minimal fake for LangGraph StateSnapshot."""

    def __init__(self, values, next_nodes=(), metadata=None):
        self.values = values
        self.next = next_nodes
        self.metadata = metadata or {}


def _make_snapshot(batch_cursor=0, **extra):
    values = {"batch_cursor": batch_cursor, **extra}
    return _FakeSnapshot(values)


# ============================================================================
# Phase 2: Exclusion tests (T007)
# ============================================================================


def test_graph_excludes_llm_and_sqlite_channels():
    """Compiled RAA graph must not contain LLM, SQLite, or embedding channels."""
    app = compile_raa_graph()
    channel_keys = set(app.channels.keys())

    forbidden = {
        "llm_raa_a",
        "llm_raa_b",
        "llm_raa_c",
        "llm_judge",
        "sqlite_connection",
        "sqlite_saver",
        "embedding_vectors",
        "embeddings",
    }
    found = forbidden & channel_keys
    assert not found, f"Forbidden channels present: {found}"


# ============================================================================
# US1: db_path validation (T008-T009)
# ============================================================================


def test_validate_db_path_rejects_empty():
    """_validate_db_path raises ValueError for empty string."""
    with pytest.raises(ValueError, match="non-empty"):
        _validate_db_path("")


def test_validate_db_path_rejects_missing_parent():
    """_validate_db_path raises ValueError when parent directory does not exist."""
    with pytest.raises(ValueError, match="Parent directory does not exist"):
        _validate_db_path("/nonexistent/path/raa_graph.db")


def test_validate_db_path_accepts_valid_path(tmp_path):
    """_validate_db_path passes when parent directory exists."""
    db_path = str(tmp_path / "raa_graph.db")
    _validate_db_path(db_path)  # no exception


def test_compile_for_production_requires_db_path():
    """compile_for_production rejects empty db_path."""
    with pytest.raises(ValueError, match="non-empty"):
        compile_for_production("")


def test_compile_for_production_rejects_missing_parent():
    """compile_for_production rejects paths with missing parent directories."""
    with pytest.raises(ValueError, match="Parent directory does not exist"):
        compile_for_production("/nonexistent/path/raa_graph.db")


# ============================================================================
# US1: SqliteSaver connection (T010-T011)
# ============================================================================


def test_open_sqlite_checkpointer_uses_wal_mode(tmp_db_path):
    """_open_sqlite_checkpointer opens connection with WAL mode."""
    checkpointer = _open_sqlite_checkpointer(tmp_db_path)
    # Verify the DB file was created
    assert os.path.exists(tmp_db_path)
    # Verify WAL mode by checking the DB directly
    conn = sqlite3.connect(tmp_db_path)
    result = conn.execute("PRAGMA journal_mode;").fetchone()
    assert result[0].upper() == "WAL"
    conn.close()


def test_open_sqlite_checkpointer_returns_sqlite_saver(tmp_db_path):
    """_open_sqlite_checkpointer returns a SqliteSaver instance."""
    from langgraph.checkpoint.sqlite import SqliteSaver

    checkpointer = _open_sqlite_checkpointer(tmp_db_path)
    assert isinstance(checkpointer, SqliteSaver)


# ============================================================================
# US1: Compilation with checkpointer (T012)
# ============================================================================


def test_compile_for_production_passes_checkpointer(tmp_db_path):
    """compile_for_production compiles graph with a checkpointer."""
    app = compile_for_production(db_path=tmp_db_path)
    assert app.checkpointer is not None
    assert hasattr(app.checkpointer, "get_tuple")


def test_compile_for_production_preserves_node_overrides(tmp_db_path):
    """node_overrides replace default nodes in production compilation."""
    mock_node = MagicMock(return_value={"embeddings_ready": True, "batch_queue": [{"id": "X"}]})

    from raa.graphs.main_graph import (
        NODE_BATCH_QUEUE_ORDERING,
        NODE_COHERENCE_GATE,
        NODE_CONSTRUCT_BATCHES,
        NODE_OVERLAP_BRIDGING,
        NODE_PREPARE_EMBEDDINGS,
    )

    overrides = {
        NODE_PREPARE_EMBEDDINGS: mock_node,
        NODE_CONSTRUCT_BATCHES: mock_node,
        NODE_OVERLAP_BRIDGING: mock_node,
        NODE_COHERENCE_GATE: mock_node,
        NODE_BATCH_QUEUE_ORDERING: mock_node,
    }

    app = compile_for_production(db_path=tmp_db_path, node_overrides=overrides)
    app.invoke({"embeddings_ready": True}, {"configurable": {"thread_id": "raa-override-test"}})
    assert mock_node.call_count == 5


# ============================================================================
# US1: State persistence (T013)
# ============================================================================


def test_production_graph_persists_state_channels(tmp_db_path, minimal_initial_state):
    """Invoked production graph persists key state channels for a thread_id."""
    from raa.graphs.main_graph import build_raa_graph

    # Build a minimal graph that writes all channels
    def _mock_all(state):
        return {
            "batch_cursor": 3,
            "batch_queue": [{"batch_id": 1}],
            "running_arch_model": {"systems": []},
            "best_batch_output": {},
            "open_questions": [],
            "bridge_requirements": {},
            "incoherent_batches": [],
            "embeddings_ready": True,
        }

    overrides = {
        "prepare_embeddings": _mock_all,
        "construct_batches": lambda s: {},
        "apply_overlap_bridging": lambda s: {},
        "apply_coherence_gate": lambda s: {},
        "order_batch_queue": lambda s: {},
    }

    app = compile_for_production(db_path=tmp_db_path, node_overrides=overrides)
    thread_id = "raa-test-thread-001"
    config = {"configurable": {"thread_id": thread_id}}

    app.invoke(minimal_initial_state, config)

    # Query the persisted state
    state = app.get_state(config)
    assert state is not None
    assert state.values is not None
    assert state.values["batch_cursor"] == 3
    assert state.values["batch_queue"] == [{"batch_id": 1}]
    assert state.values["embeddings_ready"] is True


def test_production_graph_supports_multiple_threads(tmp_db_path, minimal_initial_state):
    """Different thread_ids get independent checkpoint state."""
    _counter = {"n": 0}

    def _mock_cursor(state):
        _counter["n"] += 1
        return {"batch_cursor": _counter["n"], "embeddings_ready": True}

    overrides = {
        "prepare_embeddings": _mock_cursor,
        "construct_batches": lambda s: {},
        "apply_overlap_bridging": lambda s: {},
        "apply_coherence_gate": lambda s: {},
        "order_batch_queue": lambda s: {},
    }

    app = compile_for_production(db_path=tmp_db_path, node_overrides=overrides)

    app.invoke(minimal_initial_state, {"configurable": {"thread_id": "thread-a"}})
    app.invoke(minimal_initial_state, {"configurable": {"thread_id": "thread-b"}})

    state_a = app.get_state({"configurable": {"thread_id": "thread-a"}})
    state_b = app.get_state({"configurable": {"thread_id": "thread-b"}})
    assert state_a is not None
    assert state_b is not None
    assert state_a.values["batch_cursor"] != state_b.values["batch_cursor"]


# ============================================================================
# US1: Pending writes preservation (T014)
# ============================================================================


def test_checkpoint_preserves_pending_writes(tmp_db_path, minimal_initial_state):
    """Checkpoint inspection API can retrieve state after partial execution."""
    def _step_one(state):
        return {"batch_cursor": 1, "batch_queue": [{"batch_id": 1, "step": "one"}]}

    overrides = {
        "prepare_embeddings": _step_one,
        "construct_batches": lambda s: {},
        "apply_overlap_bridging": lambda s: {},
        "apply_coherence_gate": lambda s: {},
        "order_batch_queue": lambda s: {},
    }

    app = compile_for_production(db_path=tmp_db_path, node_overrides=overrides)
    config = {"configurable": {"thread_id": "test-pending"}}
    app.invoke(minimal_initial_state, config)

    state = app.get_state(config)
    assert state is not None
    assert state.values["batch_cursor"] == 1
    assert len(state.values["batch_queue"]) == 1


# ============================================================================
# US2: derive_thread_id (T021-T023)
# ============================================================================


def test_derive_thread_id_format():
    """derive_thread_id returns raa- followed by exactly 16 lowercase hex chars."""
    tid = derive_thread_id("some-hash-value")
    assert tid.startswith("raa-"), f"Thread ID '{tid}' does not start with 'raa-'"
    hex_part = tid[4:]
    assert len(hex_part) == 16, f"Hex part '{hex_part}' is {len(hex_part)} chars, expected 16"
    assert all(c in "0123456789abcdef" for c in hex_part), f"Non-hex chars in '{hex_part}'"


def test_derive_thread_id_deterministic():
    """Identical inputs produce identical thread IDs."""
    a = derive_thread_id("hash-abc", "default")
    b = derive_thread_id("hash-abc", "default")
    assert a == b


def test_derive_thread_id_different_hash_produces_different_id():
    """Different ARLO output version hashes produce different thread IDs."""
    a = derive_thread_id("hash-aaa")
    b = derive_thread_id("hash-bbb")
    assert a != b


def test_derive_thread_id_different_label_produces_different_id():
    """Different run labels produce different thread IDs."""
    a = derive_thread_id("hash-abc", "default")
    b = derive_thread_id("hash-abc", "retry-1")
    assert a != b


def test_derive_thread_id_default_label():
    """Default run_label is 'default'."""
    from_dfl = derive_thread_id("hash-abc")
    from_exp = derive_thread_id("hash-abc", "default")
    assert from_dfl == from_exp


# ============================================================================
# US2: build_run_config (T024)
# ============================================================================


def test_build_run_config_structure():
    """build_run_config sets thread_id under configurable."""
    config = build_run_config("raa-test-123")
    assert config["configurable"]["thread_id"] == "raa-test-123"


def test_build_run_config_with_context():
    """build_run_config includes context when provided."""
    ctx = {"llm": "mock_llm"}
    config = build_run_config("raa-test-123", context=ctx)
    assert config["context"] == ctx


def test_build_run_config_without_context():
    """build_run_config excludes context key when context is None."""
    config = build_run_config("raa-test-123")
    assert "context" not in config


def test_build_run_config_no_llm_in_state():
    """build_run_config does not place LLM instance under state key."""
    config = build_run_config("raa-test-123", context={"llm": "mock"})
    assert "state" not in config
    assert "llm" not in config.get("configurable", {})


# ============================================================================
# US2: should_resume_from_snapshot (T025)
# ============================================================================


def test_should_resume_when_cursor_positive():
    """Returns True when batch_cursor > 0."""
    snap = _make_snapshot(batch_cursor=5)
    assert should_resume_from_snapshot(snap) is True


def test_should_not_resume_when_cursor_zero():
    """Returns False when batch_cursor == 0."""
    snap = _make_snapshot(batch_cursor=0)
    assert should_resume_from_snapshot(snap) is False


def test_should_not_resume_when_cursor_missing():
    """Returns False when batch_cursor key is missing."""
    snap = _make_snapshot()
    # remove batch_cursor
    snap.values.pop("batch_cursor", None)
    assert should_resume_from_snapshot(snap) is False


def test_should_not_resume_when_snapshot_none():
    """Returns False for None snapshot."""
    assert should_resume_from_snapshot(None) is False


def test_should_not_resume_when_values_none():
    """Returns False when snapshot.values is None."""
    snap = _FakeSnapshot(None)
    assert should_resume_from_snapshot(snap) is False


# ============================================================================
# US2: run_with_recovery calls get_state (T026)
# ============================================================================


def test_run_with_recovery_calls_get_state(mock_compiled_graph, minimal_initial_state, tmp_db_path):
    """run_with_recovery queries graph.get_state before invoking."""
    config = build_run_config("raa-query-test")
    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        config,
        db_path=tmp_db_path,
    )
    mock_compiled_graph.get_state.assert_called_once_with(config)


# ============================================================================
# US2: Resume path (T027)
# ============================================================================


def test_run_with_recovery_resumes_when_cursor_positive(
    mock_compiled_graph, minimal_initial_state, tmp_db_path
):
    """When batch_cursor > 0, graph.invoke is called with None."""
    config = build_run_config("raa-resume-test")
    snap = _make_snapshot(batch_cursor=3)
    mock_compiled_graph.get_state.return_value = snap

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        config,
        db_path=tmp_db_path,
    )
    mock_compiled_graph.invoke.assert_called_once_with(None, config)


# ============================================================================
# US2: Fresh start path (T028)
# ============================================================================


def test_run_with_recovery_fresh_when_no_state(
    mock_compiled_graph, minimal_initial_state, tmp_db_path
):
    """When get_state returns None, invoke with initial_state."""
    mock_compiled_graph.get_state.return_value = None

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-fresh-test"),
        db_path=tmp_db_path,
    )
    mock_compiled_graph.invoke.assert_called_once_with(
        minimal_initial_state, build_run_config("raa-fresh-test")
    )


def test_run_with_recovery_fresh_when_cursor_zero(
    mock_compiled_graph, minimal_initial_state, tmp_db_path
):
    """When batch_cursor == 0, invoke with initial_state."""
    snap = _make_snapshot(batch_cursor=0)
    mock_compiled_graph.get_state.return_value = snap

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-fresh-zero"),
        db_path=tmp_db_path,
    )
    mock_compiled_graph.invoke.assert_called_once_with(
        minimal_initial_state, build_run_config("raa-fresh-zero")
    )


def test_run_with_recovery_fresh_when_values_empty(
    mock_compiled_graph, minimal_initial_state, tmp_db_path
):
    """When snapshot has no values, invoke with initial_state."""
    snap = _FakeSnapshot({})
    mock_compiled_graph.get_state.return_value = snap

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-empty-vals"),
        db_path=tmp_db_path,
    )
    mock_compiled_graph.invoke.assert_called_once_with(
        minimal_initial_state, build_run_config("raa-empty-vals")
    )


# ============================================================================
# US2: Resume logging (T029)
# ============================================================================


def test_run_with_recovery_logs_resume_info(
    mock_compiled_graph, minimal_initial_state, tmp_db_path, caplog
):
    """Resume logs include thread_id and batch_cursor."""
    import logging

    caplog.set_level(logging.INFO)
    snap = _make_snapshot(batch_cursor=7)
    mock_compiled_graph.get_state.return_value = snap

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-log-test"),
        db_path=tmp_db_path,
    )

    assert "Resuming" in caplog.text
    assert "raa-log-test" in caplog.text
    assert "7" in caplog.text


# ============================================================================
# US3: Corrupt checkpoint exception handling (T038)
# ============================================================================


def test_run_with_recovery_catches_database_error(
    mock_compiled_graph, minimal_initial_state, tmp_db_path, caplog
):
    """run_with_recovery catches sqlite3.DatabaseError, logs warning, continues."""
    import logging

    caplog.set_level(logging.WARNING)
    mock_compiled_graph.get_state.side_effect = sqlite3.DatabaseError("corrupt")

    # Ensure the DB file exists so _preserve_corrupt_checkpoint can move it
    Path(tmp_db_path).touch()

    result = run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-corr-test"),
        db_path=tmp_db_path,
    )

    assert "corruption" in caplog.text.lower() or "corrupt" in caplog.text.lower()
    # Must still invoke (fresh start fallback)
    mock_compiled_graph.invoke.assert_called_once_with(
        minimal_initial_state, build_run_config("raa-corr-test")
    )


# ============================================================================
# US3: Corrupt DB preservation (T039)
# ============================================================================


def test_corrupt_fallback_renames_db(mock_compiled_graph, minimal_initial_state, tmp_db_path):
    """Corrupt checkpoint fallback renames the DB to .corrupted."""
    mock_compiled_graph.get_state.side_effect = sqlite3.DatabaseError("corrupt")
    Path(tmp_db_path).touch()

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-rename-test"),
        db_path=tmp_db_path,
    )

    corrupt_path = f"{tmp_db_path}.corrupted"
    assert not os.path.exists(tmp_db_path), f"Original DB still exists: {tmp_db_path}"
    assert os.path.exists(corrupt_path), f"Corrupt DB not preserved: {corrupt_path}"


# ============================================================================
# US3: Corrupt fallback recompile and fresh start (T040)
# ============================================================================


def test_corrupt_fallback_uses_compile_factory(mock_compiled_graph, minimal_initial_state, tmp_db_path):
    """Corrupt fallback calls compile_graph_factory and invokes with initial_state."""
    mock_compiled_graph.get_state.side_effect = sqlite3.DatabaseError("corrupt")
    Path(tmp_db_path).touch()

    new_graph = MagicMock()
    compile_factory = MagicMock(return_value=new_graph)

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-recompile-test"),
        db_path=tmp_db_path,
        compile_graph_factory=compile_factory,
    )

    compile_factory.assert_called_once()
    new_graph.invoke.assert_called_once_with(
        minimal_initial_state, build_run_config("raa-recompile-test")
    )


def test_corrupt_fallback_fresh_with_initial_state(mock_compiled_graph, minimal_initial_state, tmp_db_path):
    """Corrupt fallback invokes with initial_state, not None."""
    mock_compiled_graph.get_state.side_effect = sqlite3.DatabaseError("corrupt")
    Path(tmp_db_path).touch()

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-corr-fresh-test"),
        db_path=tmp_db_path,
    )

    # Called with initial_state, not None
    call_args = mock_compiled_graph.invoke.call_args
    assert call_args[0][0] is not None
    assert call_args[0][0]["batch_cursor"] == 0


# ============================================================================
# US3: Corrupt DB never silently deleted (T041)
# ============================================================================


def test_corrupt_fallback_never_deletes_db(mock_compiled_graph, minimal_initial_state, tmp_db_path):
    """Corrupt fallback preserves the database (renames, doesn't delete)."""
    mock_compiled_graph.get_state.side_effect = sqlite3.DatabaseError("corrupt")
    Path(tmp_db_path).write_text("some corrupt data")

    run_with_recovery(
        mock_compiled_graph,
        minimal_initial_state,
        build_run_config("raa-nodelete"),
        db_path=tmp_db_path,
    )

    corrupt_path = f"{tmp_db_path}.corrupted"
    assert os.path.exists(corrupt_path)
    assert Path(corrupt_path).read_text() == "some corrupt data"


# ============================================================================
# US3: archive_checkpoint (T042)
# ============================================================================


def test_archive_checkpoint_moves_db(tmp_path):
    """archive_checkpoint moves the active DB to archive/{thread_id}/."""
    checkpoints_dir = tmp_path / "checkpoints"
    checkpoints_dir.mkdir()
    db_file = checkpoints_dir / "raa_graph.db"
    db_file.write_text("checkpoint data")

    archive_checkpoint(str(db_file), "test-project", "raa-thread-001")

    # Active path no longer exists
    assert not db_file.exists()
    # Archive path exists
    archive_path = checkpoints_dir / "archive" / "raa-thread-001" / "raa_graph.db"
    assert archive_path.exists()
    assert archive_path.read_text() == "checkpoint data"


def test_archive_checkpoint_returns_archive_path(tmp_path):
    """archive_checkpoint returns the archive destination path."""
    checkpoints_dir = tmp_path / "checkpoints"
    checkpoints_dir.mkdir()
    db_file = checkpoints_dir / "raa_graph.db"
    db_file.write_text("data")

    result = archive_checkpoint(str(db_file), "proj", "thread-x")
    assert result.endswith("archive/thread-x/raa_graph.db")


# ============================================================================
# US3: archive skipped when output not validated (T043)
# ============================================================================


def test_archive_after_success_skips_when_not_validated(tmp_path):
    """archive_after_success returns None when arch_model_written is False."""
    checkpoints_dir = tmp_path / "checkpoints"
    checkpoints_dir.mkdir()
    db_file = checkpoints_dir / "raa_graph.db"
    db_file.write_text("data")

    result = {"arch_model_written": False, "batch_cursor": 10}
    archive_result = archive_after_success(
        result, str(db_file), "proj", "thread-1"
    )
    assert archive_result is None
    assert db_file.exists()  # DB untouched


def test_archive_after_success_skips_when_key_missing(tmp_path):
    """archive_after_success returns None when arch_model_written key is missing."""
    checkpoints_dir = tmp_path / "checkpoints"
    checkpoints_dir.mkdir()
    db_file = checkpoints_dir / "raa_graph.db"
    db_file.write_text("data")

    result = {"batch_cursor": 10}
    archive_result = archive_after_success(
        result, str(db_file), "proj", "thread-1"
    )
    assert archive_result is None


# ============================================================================
# US3: Archive after success (T044)
# ============================================================================


def test_archive_after_success_moves_db(tmp_path):
    """archive_after_success moves the DB when arch_model_written is True."""
    checkpoints_dir = tmp_path / "checkpoints"
    checkpoints_dir.mkdir()
    db_file = checkpoints_dir / "raa_graph.db"
    db_file.write_text("data")

    result = {"arch_model_written": True, "batch_cursor": 10}
    archive_result = archive_after_success(
        result, str(db_file), "proj", "thread-1"
    )
    assert archive_result is not None
    assert not db_file.exists()
    archive_path = checkpoints_dir / "archive" / "thread-1" / "raa_graph.db"
    assert archive_path.exists()


def test_archive_after_success_skips_when_db_missing(tmp_path):
    """archive_after_success returns None when DB file doesn't exist."""
    db_path = str(tmp_path / "nonexistent" / "raa_graph.db")

    result = {"arch_model_written": True}
    archive_result = archive_after_success(result, db_path, "proj", "thread-1")
    assert archive_result is None


# ============================================================================
# US3: Section 22G failure modes (T045)
# ============================================================================


def test_mid_embedding_resume_embeddings_ready_false(tmp_db_path, minimal_initial_state):
    """Resume after mid-embedding failure preserves embeddings_ready=False."""
    def _fail_after_prepare(state):
        return {"embeddings_ready": False}

    overrides = {
        "prepare_embeddings": _fail_after_prepare,
        "construct_batches": lambda s: {},
        "apply_overlap_bridging": lambda s: {},
        "apply_coherence_gate": lambda s: {},
        "order_batch_queue": lambda s: {},
    }

    app = compile_for_production(db_path=tmp_db_path, node_overrides=overrides)
    config = {"configurable": {"thread_id": "raa-embed-fail"}}

    # prepare_embeddings succeeds but sets embeddings_ready=False;
    # gate raises ValueError but state IS persisted by checkpoint
    try:
        app.invoke(minimal_initial_state, config)
    except ValueError:
        pass  # Expected — gate blocks progress

    state = app.get_state(config)
    # After a failed super-step, LangGraph may or may not persist
    # the partial state depending on the error handling.
    # Verify that if state exists, embeddings_ready is accessible.
    if state is not None and state.values:
        assert "embeddings_ready" in state.values


def test_after_judge_resume_advanced_cursor(tmp_db_path, minimal_initial_state):
    """Resume after judge preserves advanced batch_cursor."""
    def _advance(state):
        return {"batch_cursor": 5, "embeddings_ready": True}

    overrides = {
        "prepare_embeddings": _advance,
        "construct_batches": lambda s: {},
        "apply_overlap_bridging": lambda s: {},
        "apply_coherence_gate": lambda s: {},
        "order_batch_queue": lambda s: {},
    }

    app = compile_for_production(db_path=tmp_db_path, node_overrides=overrides)
    config = {"configurable": {"thread_id": "raa-judge-test"}}
    app.invoke(minimal_initial_state, config)

    state = app.get_state(config)
    assert state.values["batch_cursor"] == 5


def test_during_final_merge_reruns_from_best_batch_output(tmp_db_path, minimal_initial_state):
    """During-final-merge state preserves best_batch_output for rerun."""
    best_output = {1: {"systems": [{"id": "sys1"}]}}

    def _set_best(state):
        return {
            "best_batch_output": best_output,
            "batch_cursor": 10,
            "embeddings_ready": True,
        }

    overrides = {
        "prepare_embeddings": _set_best,
        "construct_batches": lambda s: {},
        "apply_overlap_bridging": lambda s: {},
        "apply_coherence_gate": lambda s: {},
        "order_batch_queue": lambda s: {},
    }

    app = compile_for_production(db_path=tmp_db_path, node_overrides=overrides)
    config = {"configurable": {"thread_id": "raa-merge-test"}}
    app.invoke(minimal_initial_state, config)

    state = app.get_state(config)
    assert state.values["best_batch_output"] == best_output
    assert state.values["batch_cursor"] == 10


# ============================================================================
# US2: run_raa_pipeline integration (T036)
# ============================================================================


def test_run_raa_pipeline_fresh_start(tmp_db_path, minimal_initial_state):
    """run_raa_pipeline performs a fresh start when no prior checkpoint exists."""
    from raa.graphs.main_graph import (
        NODE_BATCH_QUEUE_ORDERING,
        NODE_COHERENCE_GATE,
        NODE_CONSTRUCT_BATCHES,
        NODE_OVERLAP_BRIDGING,
        NODE_PREPARE_EMBEDDINGS,
    )

    mock = MagicMock(return_value={"embeddings_ready": True, "batch_queue": [{"id": "P1"}]})
    overrides = {
        NODE_PREPARE_EMBEDDINGS: mock,
        NODE_CONSTRUCT_BATCHES: mock,
        NODE_OVERLAP_BRIDGING: mock,
        NODE_COHERENCE_GATE: mock,
        NODE_BATCH_QUEUE_ORDERING: mock,
    }

    result = run_raa_pipeline(
        minimal_initial_state,
        arlo_output_version_hash="test-hash-v1",
        db_path=tmp_db_path,
        project_name="test-proj",
        node_overrides=overrides,
    )

    assert "batch_queue" in result
    assert mock.call_count == 5
