"""Unit tests for final_merge stabilization fixes."""

import os
import tempfile
from unittest import mock

import pytest

from raa.nodes.final_merge import (
    HumanInputRequiredException,
    MergeTimeoutError,
    TraceabilityAuditException,
    _collect_execution_assigned_ids,
    _collect_input_requirement_ids,
    _collect_traced_ids,
    _emit_progress,
    _generate_batch_trace_gap_questions,
    _global_merge,
    _init_embeddings,
    _process_residual_requirements,
    _resolve_all_questions,
    _run_traceability_audit,
    _traceability_missing_diagnostics,
    _write_output_files,
    final_merge,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_state(**overrides):
    """Build a minimal RAAState-compatible dict."""
    state = {
        "arch_model": {"entities": [], "relationships": []},
        "batch_outputs": [],
        "open_questions": [],
        "human_answers": {},
        "requirements": {},
        "unprocessed_requirements": [],
    }
    state.update(overrides)
    return state


# ── Embedding init ───────────────────────────────────────────────────────────


def test_init_embeddings_prefers_non_asr_db_path():
    """_init_embeddings accepts non_asr_db_path (preferred key)."""
    with mock.patch("raa.nodes.final_merge.EmbeddingCache") as mock_cache, \
         mock.patch("raa.nodes.final_merge.get_embedding_model") as mock_model:
        mock_cache.return_value = mock.Mock()
        mock_model.return_value = mock.Mock()
        config = {"configurable": {
            "non_asr_db_path": "/custom/path.db",
            "cache_dir": "/custom/cache",
        }}
        cache, model = _init_embeddings(config)
        assert cache is not None
        assert model is not None
        mock_cache.assert_called_with(db_path="/custom/path.db", model_name=mock.ANY)


def test_init_embeddings_falls_back_to_legacy_aliases():
    """_init_embeddings falls back to non_asr_embeddings_db_path and embedding_cache_dir."""
    with mock.patch("raa.nodes.final_merge.EmbeddingCache") as mock_cache, \
         mock.patch("raa.nodes.final_merge.get_embedding_model") as mock_model:
        mock_cache.return_value = mock.Mock()
        mock_model.return_value = mock.Mock()
        config = {"configurable": {
            "non_asr_embeddings_db_path": "/legacy/path.db",
            "embedding_cache_dir": "/legacy/cache",
        }}
        cache, model = _init_embeddings(config)
        assert cache is not None
        assert model is not None
        mock_cache.assert_called_with(db_path="/legacy/path.db", model_name=mock.ANY)


def test_init_embeddings_model_not_found_disables_similarity():
    """ModelNonExistentException disables similarity with a warning by default."""
    from raa.utils.embedding_cache import ModelNonExistentException

    with mock.patch("raa.nodes.final_merge.EmbeddingCache") as mock_cache:
        mock_cache.side_effect = ModelNonExistentException("/tmp", "test-model")
        cache, model = _init_embeddings({"configurable": {}})
        assert cache is None
        assert model is None


def test_init_embeddings_raises_when_require_flag_set():
    """ModelNonExistentException raises when final_merge_require_embeddings=True."""
    from raa.utils.embedding_cache import ModelNonExistentException

    with mock.patch("raa.nodes.final_merge.EmbeddingCache") as mock_cache:
        mock_cache.side_effect = ModelNonExistentException("/tmp", "test-model")
        config = {"configurable": {"final_merge_require_embeddings": True}}
        with pytest.raises(ModelNonExistentException):
            _init_embeddings(config)


# ── Progress / Timeout ──────────────────────────────────────────────────────


def test_emit_progress_raises_on_timeout():
    """_emit_progress raises MergeTimeoutError when start_time + timeout_s exceeded."""
    with pytest.raises(MergeTimeoutError):
        _emit_progress(
            "test_phase", "testing timeout",
            start_time=0.0, timeout_s=0.001,
        )


def test_final_merge_progress_to_stdout(capsys):
    """Direct final_merge calls can show progress without LangGraph streaming."""
    state = _make_state()
    config = {"configurable": {
        "final_merge_progress_to_stdout": True,
        "final_merge_write_outputs": False,
    }}
    final_merge(state, config=config)
    captured = capsys.readouterr()
    assert "[final_merge] embedding_init: Initializing embeddings" in captured.out
    assert "[final_merge] complete: final_merge complete" in captured.out


def test_final_merge_progress_callback_receives_events():
    """final_merge_progress_callback receives structured phase events."""
    events = []
    state = _make_state()
    config = {"configurable": {
        "final_merge_progress_callback": events.append,
        "final_merge_write_outputs": False,
    }}
    final_merge(state, config=config)
    assert events
    assert any(event["phase"] == "global_merge" for event in events)
    assert any(event["phase"] == "complete" for event in events)


def test_final_merge_includes_metrics():
    """final_merge returns final_merge_metrics in the result dict."""
    state = _make_state()
    result = final_merge(
        state,
        config={"configurable": {"final_merge_write_outputs": False}},
    )
    assert "final_merge_metrics" in result
    metrics = result["final_merge_metrics"]
    assert "batch_outputs_seen" in metrics
    assert "embedding_enabled" in metrics
    assert "llm_calls_attempted" in metrics
    assert "llm_calls_skipped" in metrics
    assert "llm_calls_failed" in metrics
    assert "llm_fallbacks_used" in metrics


def test_global_merge_emits_progress_per_batch():
    """_global_merge emits bounded progress for each batch output."""
    events = []
    config = {"configurable": {"final_merge_progress_callback": events.append}}
    with mock.patch("raa.nodes.final_merge.deduplicate_and_merge_fragment") as dedup:
        dedup.return_value = ({"entities": [], "relationships": []}, [], None)
        _global_merge(
            {"entities": [], "relationships": []},
            [{"batch_id": "b1"}, {"batch_id": "b2"}],
            cache=None,
            model=None,
            config=config,
            start_time=None,
            timeout_s=None,
            metrics={},
        )
    batch_events = [
        event for event in events
        if event["phase"] == "global_merge" and event.get("current_item_id") in {"b1", "b2"}
    ]
    assert len(batch_events) >= 4


def test_global_merge_accepts_wrapped_execution_output():
    """_global_merge unwraps execution-loop records with arch_fragment payloads."""
    wrapped_output = {
        "batch_id": "b1",
        "strategy": "raa_a",
        "skipped": False,
        "arch_fragment": {
            "entities": [{
                "id": "sys_1",
                "name": "System",
                "description": "System for R1",
                "c4_type": "system",
                "requirement_ids": ["R1"],
            }],
            "relationships": [],
        },
    }
    merged, questions = _global_merge(
        {"entities": [], "relationships": []},
        [wrapped_output],
        cache=None,
        model=None,
    )
    assert questions == []
    assert len(merged["entities"]) == 1
    assert merged["entities"][0]["requirement_ids"] == ["R1"]


def test_process_residual_requirements_emits_progress_per_residual():
    """_process_residual_requirements emits progress for every residual."""
    events = []
    metrics = {}
    config = {"configurable": {"final_merge_progress_callback": events.append}}
    arch_model = {"entities": [], "relationships": []}
    _process_residual_requirements(
        [{"id": "R1", "description": "manual review note"}],
        arch_model,
        {"R1": "manual review note"},
        cache=None,
        model=None,
        config=config,
        metrics=metrics,
        start_time=None,
        timeout_s=None,
    )
    assert any(
        event["phase"] == "residual_processing"
        and event.get("current_item_id") == "R1"
        for event in events
    )


# ── Traceability ────────────────────────────────────────────────────────────


def test_traceability_fails_when_req_missing():
    """Requirement in input IDs but nowhere in model or questions fails."""
    arch_model = {"entities": [], "relationships": []}
    state = _make_state(requirements={"1": "some requirement"})
    with pytest.raises(TraceabilityAuditException, match="unmapped or missing"):
        _run_traceability_audit(state, arch_model, [])


def test_traceability_passes_with_entity_requirement_ids():
    """R1 mapped to entity requirement_ids passes traceability."""
    arch_model = {
        "entities": [{"id": "e1", "name": "Test", "requirement_ids": ["R1"]}],
        "relationships": [],
    }
    state = _make_state(requirements={"1": "some requirement"})
    manifest = _run_traceability_audit(state, arch_model, [])
    assert manifest["R1"]["location_type"] == "model"
    assert manifest["R1"]["location_id"] == "e1"


def test_traceability_passes_with_relationship_requirement_ids():
    """R1 mapped to relationship requirement_ids passes traceability."""
    arch_model = {
        "entities": [],
        "relationships": [{
            "id": "rel_1", "source_id": "a", "target_id": "b",
            "requirement_ids": ["R1"],
        }],
    }
    state = _make_state(requirements={"1": "some requirement"})
    manifest = _run_traceability_audit(state, arch_model, [])
    assert manifest["R1"]["location_type"] == "model"
    assert manifest["R1"]["location_id"] == "rel_1"


def test_traceability_canonicalizes_multiple_model_locations():
    """A requirement can appear on multiple C4 model elements but has one manifest entry."""
    arch_model = {
        "entities": [
            {"id": "system_1", "name": "System", "requirement_ids": ["R1"]},
            {"id": "container_1", "name": "Container", "requirement_ids": ["R1"]},
        ],
        "relationships": [{
            "id": "rel_1", "source_id": "system_1", "target_id": "container_1",
            "requirement_ids": ["R1"],
        }],
    }
    state = _make_state(requirements={"1": "some requirement"})
    manifest = _run_traceability_audit(state, arch_model, [])
    assert manifest["R1"]["location_type"] == "model"
    assert manifest["R1"]["location_id"] == "system_1"
    assert [loc["id"] for loc in manifest["R1"]["related_locations"]] == [
        "container_1",
        "rel_1",
    ]


def test_traceability_coverage_gap_question_maps_to_req():
    """coverage_gap_R1 question maps to R1."""
    arch_model = {"entities": [], "relationships": []}
    questions = [{
        "id": "coverage_gap_R1",
        "question_type": "coverage_gap",
        "description": "Requirement R1 is non-architectural.",
        "context": {"req_id": "R1"},
    }]
    state = _make_state(requirements={"1": "some requirement"})
    manifest = _run_traceability_audit(state, arch_model, questions)
    assert manifest["R1"]["location_type"] == "question"


def test_traceability_coverage_gap_no_prefix_maps_to_req():
    """coverage_gap_1 question maps to R1 via suffix matching."""
    arch_model = {"entities": [], "relationships": []}
    questions = [{
        "id": "coverage_gap_1",
        "question_type": "coverage_gap",
        "description": "R1 is non-architectural.",
        "context": {"req_id": "1"},
    }]
    state = _make_state(requirements={"1": "some requirement"})
    manifest = _run_traceability_audit(state, arch_model, questions)
    assert manifest["R1"]["location_type"] == "question"


def test_traceability_question_top_level_requirement_ids_maps_to_req():
    """coverage_gap question maps requirement_ids from the top level."""
    arch_model = {"entities": [], "relationships": []}
    questions = [{
        "id": "coverage_gap_custom",
        "question_type": "coverage_gap",
        "description": "Requirement needs review.",
        "requirement_ids": ["R1"],
    }]
    state = _make_state(requirements={"1": "some requirement"})
    manifest = _run_traceability_audit(state, arch_model, questions)
    assert manifest["R1"]["location_type"] == "question"


def test_traceability_fails_on_multiple_locations():
    """Requirement mapped to both entity and question raises."""
    arch_model = {
        "entities": [{"id": "e1", "name": "Test", "requirement_ids": ["R1"]}],
        "relationships": [],
    }
    questions = [{
        "id": "coverage_gap_R1",
        "question_type": "coverage_gap",
        "description": "...",
        "context": {"req_id": "R1"},
    }]
    state = _make_state(requirements={"1": "some requirement"})
    with pytest.raises(TraceabilityAuditException, match="multiple locations"):
        _run_traceability_audit(state, arch_model, questions)


def test_traceability_missing_diagnostics_are_useful():
    """Missing R1 audit failure includes diagnostic source buckets."""
    arch_model = {"entities": [], "relationships": []}
    state = _make_state(
        requirements={"1": "some requirement"},
        batch_outputs=[{"requirements": ["R1"]}],
        unprocessed_requirements=[{"id": "R1", "description": "leftover"}],
    )
    with pytest.raises(TraceabilityAuditException) as exc:
        _run_traceability_audit(state, arch_model, [])
    message = str(exc.value)
    assert "Requirement 'R1'" in message
    assert "appeared_in_batches" in message
    assert "appeared_in_unprocessed_requirements" in message
    assert "model_entity_ids" in message
    assert "relationship_ids" in message
    assert "candidate_question_ids" in message


# ── Output writing ──────────────────────────────────────────────────────────


def test_write_output_files_disabled():
    """final_merge_write_outputs=False skips file writes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {"configurable": {
            "final_merge_write_outputs": False,
            "output_dir": tmpdir,
        }}
        result = _write_output_files(
            {"entities": []}, [], [], config,
        )
        assert result is True
        assert not os.listdir(tmpdir)  # no files written


def test_write_output_files_writes_atomically():
    """Output files are written atomically (no .tmp artifacts left)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {"configurable": {"output_dir": tmpdir}}
        result = _write_output_files(
            {"entities": [{"id": "e1"}]},
            [],
            [{"type": "context", "system_id": "s1", "name": "test"}],
            config,
        )
        assert result is True
        files = os.listdir(tmpdir)
        assert "arch_model.json" in files
        assert not any(f.endswith(".tmp") for f in files)


# ── Question resolution ─────────────────────────────────────────────────────


def test_judge_resolvable_gets_metadata():
    """judge_resolvable questions get auto_resolved metadata."""
    questions = [{
        "id": "q1",
        "question_type": "hierarchy_conflict",
        "description": "mismatching C4 parent hierarchy for e1/e2",
        "resolution_owner": "judge_resolvable",
        "resolution": None,
        "assumption_flag": False,
        "metadata": {},
    }]
    _resolve_all_questions(
        questions, {}, {"entities": [], "relationships": []}, {}, None, {},
    )
    assert questions[0]["resolution"] is not None
    assert questions[0]["metadata"]["resolution_status"] == "auto_resolved"
    assert questions[0]["metadata"]["resolved_by"] == "judge"


def test_human_preferred_gets_assumed_metadata():
    """human_preferred questions get assumed metadata."""
    questions = [{
        "id": "q1",
        "question_type": "coverage_gap",
        "description": "test coverage gap",
        "resolution_owner": "human_preferred",
        "resolution": None,
        "assumption_flag": False,
        "metadata": {},
        "context": {},
    }]
    _resolve_all_questions(
        questions, {}, {"entities": [], "relationships": []}, {}, None, {},
    )
    assert questions[0]["resolution"] is not None
    assert questions[0]["assumption_flag"] is True
    assert questions[0]["metadata"]["resolution_status"] == "assumed"
    assert questions[0]["metadata"]["resolved_by"] == "final_merge"


def test_interactive_mode_raises_without_allow_assumptions():
    """Interactive mode with unanswered human_preferred raises local exception."""
    questions = [{
        "id": "q1",
        "question_type": "coverage_gap",
        "description": "test coverage gap",
        "resolution_owner": "human_preferred",
        "resolution": None,
        "assumption_flag": False,
        "metadata": {},
        "context": {},
    }]
    config = {"configurable": {"review_mode": "interactive"}}
    with pytest.raises(HumanInputRequiredException, match="q1"):
        _resolve_all_questions(
            questions, {}, {"entities": [], "relationships": []}, {}, config, {},
        )


class _FakeStructuredLLM:
    def __init__(self):
        self.invoke_count = 0

    def invoke(self, _prompt):
        self.invoke_count += 1
        return {"assumption": "Use the existing architecture.", "rationale": "Lowest risk."}


class _FakeJudgeLLM:
    def __init__(self):
        self.with_structured_output_count = 0
        self.structured = _FakeStructuredLLM()

    def with_structured_output(self, _schema):
        self.with_structured_output_count += 1
        return self.structured


def test_final_merge_use_llm_false_skips_supplied_judge_llm():
    """final_merge_use_llm=False does not call a supplied judge_llm."""
    judge_llm = _FakeJudgeLLM()
    questions = [{
        "id": "q1",
        "question_type": "coverage_gap",
        "description": "test coverage gap",
        "resolution_owner": "human_preferred",
        "resolution": None,
        "assumption_flag": False,
        "metadata": {},
        "context": {},
    }]
    metrics = {}
    _resolve_all_questions(
        questions,
        {},
        {"entities": [], "relationships": []},
        {},
        {"configurable": {"judge_llm": judge_llm}},
        metrics,
    )
    assert judge_llm.with_structured_output_count == 0
    assert judge_llm.structured.invoke_count == 0
    assert metrics["llm_calls_skipped"] == 1


def test_final_merge_use_llm_true_calls_supplied_judge_llm_once():
    """final_merge_use_llm=True calls the supplied judge_llm in an assumption path."""
    judge_llm = _FakeJudgeLLM()
    questions = [{
        "id": "q1",
        "question_type": "coverage_gap",
        "description": "test coverage gap",
        "resolution_owner": "human_preferred",
        "resolution": None,
        "assumption_flag": False,
        "metadata": {},
        "context": {},
    }]
    metrics = {}
    _resolve_all_questions(
        questions,
        {},
        {"entities": [], "relationships": []},
        {},
        {"configurable": {"judge_llm": judge_llm, "final_merge_use_llm": True}},
        metrics,
    )
    assert judge_llm.with_structured_output_count == 1
    assert judge_llm.structured.invoke_count == 1
    assert metrics["llm_calls_attempted"] == 1
    assert "Use the existing architecture." in questions[0]["resolution"]


def test_architectural_residual_merge_failure_adds_req_context():
    """coverage_gap from architectural residual merge failure includes context.req_id."""
    with mock.patch("raa.nodes.final_merge._check_architectural") as check_arch, \
         mock.patch("raa.nodes.final_merge._try_merge_residual_entity") as merge_entity:
        check_arch.return_value = (True, None, None, "")
        merge_entity.side_effect = RuntimeError("boom")
        _, questions = _process_residual_requirements(
            [{"id": "R1", "description": "new service must process events"}],
            {"entities": [], "relationships": []},
            {"R1": "new service must process events"},
            cache=mock.Mock(),
            model=mock.Mock(),
            config={"configurable": {}},
            metrics={},
        )
    assert questions
    assert questions[0]["question_type"] == "coverage_gap"
    assert questions[0]["context"]["req_id"] == "R1"


# ── Batch trace gap detection ──────────────────────────────────────────────


def test_final_merge_generates_coverage_gap_for_batch_assigned_untraced():
    """final_merge with R10 in execution_queue but omitted from arch_fragment produces coverage_gap_R10."""
    state = _make_state(
        requirements={"10": "Requirement 10 description"},
        execution_queue=[{
            "batch_id": "batch_1",
            "asr_ids": ["R10"],
            "non_asr_ids": [],
        }],
        batch_outputs=[{
            "batch_id": "batch_1",
            "skipped": False,
            "arch_fragment": {
                "entities": [{
                    "id": "sys_1",
                    "name": "Main System",
                    "description": "Handles other reqs",
                    "c4_type": "system",
                    "requirement_ids": ["R1"],
                }],
                "relationships": [],
            },
        }],
    )
    config = {"configurable": {"final_merge_write_outputs": False}}
    result = final_merge(state, config=config)
    manifest = result["traceability_manifest"]
    assert "R10" in manifest
    assert manifest["R10"]["location_type"] == "question"
    assert manifest["R10"]["location_id"] == "coverage_gap_R10"
    gap_q = next(
        q for q in result["open_questions"]
        if q.get("id") == "coverage_gap_R10"
    )
    assert gap_q["question_type"] == "coverage_gap"
    assert gap_q["requirement_ids"] == ["R10"]
    assert gap_q["metadata"]["source"] == "final_merge_untraced_batch_requirement"
    assert result["final_merge_metrics"]["batch_assigned_trace_gaps_created"] == 1


def test_no_gap_when_entity_already_traces_requirement():
    """If R10 is already mapped to an entity, no coverage_gap is generated."""
    state = _make_state(
        requirements={"10": "Requirement 10 description"},
        execution_queue=[{
            "batch_id": "batch_1",
            "asr_ids": ["R10"],
            "non_asr_ids": [],
        }],
        batch_outputs=[{
            "batch_id": "batch_1",
            "skipped": False,
            "arch_fragment": {
                "entities": [{
                    "id": "sys_1",
                    "name": "Main System",
                    "description": "Handles R10",
                    "c4_type": "system",
                    "requirement_ids": ["R10"],
                }],
                "relationships": [],
            },
        }],
    )
    config = {"configurable": {"final_merge_write_outputs": False}}
    result = final_merge(state, config=config)
    gap_qs = [q for q in result["open_questions"] if q.get("id") == "coverage_gap_R10"]
    assert gap_qs == []
    assert result["traceability_manifest"]["R10"]["location_type"] == "model"


def test_no_duplicate_gap_when_existing_coverage_gap_question():
    """If coverage_gap_R10 already exists in open_questions, no duplicate is added."""
    existing_q = {
        "id": "coverage_gap_R10",
        "question_type": "coverage_gap",
        "description": "Already exists",
        "resolution_owner": "human_preferred",
        "resolution": None,
        "assumption_flag": False,
        "context": {"req_id": "R10"},
        "requirement_ids": ["R10"],
        "metadata": {},
    }
    state = _make_state(
        requirements={"10": "Requirement 10 description"},
        execution_queue=[{
            "batch_id": "batch_1",
            "asr_ids": ["R10"],
            "non_asr_ids": [],
        }],
        open_questions=[existing_q],
    )
    config = {"configurable": {"final_merge_write_outputs": False}}
    result = final_merge(state, config=config)
    gap_qs = [q for q in result["open_questions"] if q.get("id") == "coverage_gap_R10"]
    assert len(gap_qs) == 1


def test_no_duplicate_gap_when_top_level_requirement_ids_question():
    """If a question already references R10 via requirement_ids, no gap generated."""
    existing_q = {
        "id": "some_other_question",
        "question_type": "coverage_gap",
        "description": "Covers R10",
        "resolution_owner": "human_preferred",
        "resolution": None,
        "assumption_flag": False,
        "context": {},
        "requirement_ids": ["R10"],
        "metadata": {},
    }
    state = _make_state(
        requirements={"10": "Requirement 10 description"},
        execution_queue=[{
            "batch_id": "batch_1",
            "asr_ids": ["R10"],
            "non_asr_ids": [],
        }],
        open_questions=[existing_q],
    )
    config = {"configurable": {"final_merge_write_outputs": False}}
    result = final_merge(state, config=config)
    gap_qs = [
        q for q in result["open_questions"]
        if q.get("id") == "coverage_gap_R10"
        and q.get("metadata", {}).get("source") == "final_merge_untraced_batch_requirement"
    ]
    assert len(gap_qs) == 0


def test_diagnostics_include_appeared_in_execution_queue():
    """_traceability_missing_diagnostics reports appeared_in_execution_queue."""
    arch_model = {"entities": [], "relationships": []}
    state = _make_state(
        requirements={"10": "some requirement"},
        execution_queue=[{
            "batch_id": "batch_1",
            "asr_ids": ["R10"],
            "non_asr_ids": [],
        }],
    )
    with pytest.raises(TraceabilityAuditException) as exc:
        _run_traceability_audit(state, arch_model, [])
    message = str(exc.value)
    assert "appeared_in_execution_queue" in message
