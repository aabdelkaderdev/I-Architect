# Story 4.3: 100% Requirements Traceability Audit

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want the RAA Orchestrator to execute a final traceability audit on all input requirement IDs,
so that we guarantee zero silent requirement drops and ensure 100% accounting.

## Acceptance Criteria

1. **Traceability Validation**: Given the list of all input requirement IDs and the final compiled model state, when the finalization audit executes, then it must verify that every single input requirement ID is traceable to exactly one location (either a processed batch, a mapped container/component, or a `coverage_gap`/`residual_coupling` question).
2. **Immediate Failure**: It must fail the execution run immediately with a `TraceabilityAuditException` if any requirements are unmapped or missing (silent drop) or mapped to multiple locations.
3. **Bulk Control**: It must prohibit any bulk acceptance or bulk rejection of leftovers.

## Tasks / Subtasks

- [x] Task 1: Implement Traceability Audit in `raa/nodes/final_merge.py` (AC: #1, #2, #3)
  - [x] 1.1 In `_run_traceability_audit`, collect all input requirement IDs from inputs (asrs, non-asrs, unprocessed requirements, and requirements dict).
  - [x] 1.2 Build a trace registry mapping each requirement ID to its location (processed batch, final model entity/relationship, or coverage gap/residual coupling question).
  - [x] 1.3 Add a precise check to verify that each leftover requirement is handled individually, raising `TraceabilityAuditException` if bulk handling is detected.
  - [x] 1.4 Raise `TraceabilityAuditException` if a requirement is unmapped (silent drop) or mapped to multiple locations.
  - [x] 1.5 Populate `traceability_manifest` in `final_merge` return payload.
- [x] Task 2: Implement Unit Tests in `tests/raa/unit/test_final_merge.py` (AC: #1, #2, #3)
  - [x] 2.1 Add test cases covering batch-traced requirements, model-traced requirements, and question-traced requirements.
  - [x] 2.2 Test failure cases for unmapped requirements, multi-mapped requirements, and bulk rejection patterns.

## Dev Notes

- **Trace registry**: Check execution queue (processed batches), `arch_model` entities/relationships, and `all_questions` (open questions from deduplication/merging/residuals).
- **Exception**: Raise `TraceabilityAuditException` defined in `raa/nodes/final_merge.py`.

### Project Structure Notes

- Alignment with unified project structure: added helper `_run_traceability_audit` inside `raa/nodes/final_merge.py` and unit tests in `tests/raa/unit/test_final_merge.py`.

### References

- [Source: `_bmad-output/planning-artifacts/epics.md#Story 4.3: 100% Requirements Traceability Audit`]

## Dev Agent Record

### Agent Model Used

Antigravity

### Debug Log References

N/A

### Completion Notes List

- All 3 acceptance criteria implemented and verified with targeted unit tests.
- 6 new unit tests added covering all audit paths (success, failure, duplicates, bulk rejection).
- Full regression suite: all 599 tests pass (0 failures).

### File List

- `raa/nodes/final_merge.py` (modified) — implemented `_run_traceability_audit` and integrated it into `final_merge`.
- `tests/raa/unit/test_final_merge.py` (modified) — added `TestTraceabilityAudit` with test cases.

### Review Findings

- [x] [Review][Defer] BH-4: Hard TraceabilityAuditException causes full superstep state loss — LangGraph discards all state writes from a failed superstep (per docs). `final_merge`'s output (`arch_model`, `traceability_manifest`, `diagram_manifest`) is lost on audit failure. The correct fix per LangGraph fault-tolerance docs is an `error_handler=` on the `final_merge` node registration in the graph builder (outside this story's scope). The function itself should keep raising — the handler must be external. — deferred, requires graph builder change outside this diff
- [x] [Review][Decision→Patch] AA-2 (resolved): Bulk rejection heuristic — false positive patched via ECH-3 (exact-match); bypass limitation is accepted and documented. `_run_traceability_audit` docstring to note that bulk detection is best-effort for LLM-generated question IDs.
- [x] [Review][Patch] BH-1: `to_r_id` normalisation asymmetry in bulk-rejection check — fixed via word-boundary regex in bulk-rejection check.
- [x] [Review][Patch] BH-3: Triple blank line after `TraceabilityAuditException` class body — removed extra blank line.
- [x] [Review][Patch] BH-5: `import json` inside `_write_output_files` function body — moved to module-level import.
- [x] [Review][Patch] ECH-2: Requirement on multiple model entities triggers false "multiple locations" failure — added `"model"` dedup guard alongside `"batch"` guard.
- [x] [Review][Patch] ECH-3: Substring bulk-rejection check produces false positives for short IDs — replaced `in` with `re.search` word-boundary and `endswith` exact-suffix.
- [x] [Review][Patch] ECH-5: No test for `normalized_non_asr` as a traceability source — added 2 test cases (success + failure).
- [x] [Review][Patch] ECH-6: Duplicate question entries possible for non-numeric IDs with matching suffixes — added `(type == "question" and id == q_id)` dedup guard.
- [x] [Review][Defer] BH-2: O(n·m) quadratic question-matching loop [raa/nodes/final_merge.py:908] — The inner loop over all `input_ids` inside the outer loop over `all_questions` is O(questions × requirements). Pre-existing structural issue; acceptable for current scale. — deferred, pre-existing
- [x] [Review][Defer] ECH-1: Zero-requirement audit passes vacuously with no warning [raa/nodes/final_merge.py:862] — If all four ID sources are empty, `trace_map` is `{}` and the audit returns `{}` silently. No logging or guard. Pre-existing design gap. — deferred, pre-existing
- [x] [Review][Defer] AA-1: `arch_model["relationships"]` req_ids not included in initial ID collection [raa/nodes/final_merge.py:844-856] — A requirement existing only in a relationship (not in any of the four input sources) is silently ignored by the audit. Design gap; would need a spec change to fix. — deferred, pre-existing
