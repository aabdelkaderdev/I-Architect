# Deferred Work Items

## Deferred from: code review of 2-4-conservative-entity-deduplication-and-c4-boundary-grouping.md (2026-05-23)

- **SQLite cache overwrite hazard due to primary key design**: The cache DB uses `req_id TEXT PRIMARY KEY`. Storing an entity embedding under its ID will overwrite any requirement embedding sharing that ID, and overwrites past descriptions for the same ID.
- **Inefficient non-batched embedding calls**: Embedding generation makes sequential individual calls (`model.embed([desc])`) on cache misses rather than batching them.

## Deferred from: code review of 3-1-open-question-classification-and-human-review-payload-generation.md (2026-05-23)

- **Question type classification mapping is hardcoded**: `_HUMAN_PREFERRED_TYPES` and `_JUDGE_RESOLVABLE_TYPES` are hardcoded as static global constants, preventing dynamic registration of custom types. [raa/nodes/human_review_gate.py:15]
- **Suggested resolutions are hardcoded**: Suggested resolutions are hardcoded in `_SUGGESTED_RESOLUTIONS`, preventing runtime configuration or localization. [raa/nodes/human_review_gate.py:20]
- **Hardcoded filtered keys during question context normalization**: The dictionary comprehension for `context` manually filters out hardcoded keys like `"question_type"`, `"type"`, `"description"`, and `"summary"`. [raa/nodes/human_review_gate.py:64]
- **Potential serialization failure on custom metadata/context values**: Calling `q.model_dump()` may fail to serialize complex nested objects in `context` or `metadata`. [raa/nodes/human_review_gate.py:158]
- **Unit test mock state bypasses RAAState definition**: The `_make_state` helper function uses primitive mock dictionaries instead of proper schemas, potentially hiding type mismatch issues. [tests/raa/unit/test_human_review_gate.py:15]
- **Lack of validation constraints on OpenQuestion fields**: Fields like `id` and `question_type` have no string constraints, allowing empty values. [raa/state/models.py:29]

## Deferred from: code review of 3-2-indefinite-langgraph-interrupt-gate.md (2026-05-23)

- **Missing execution logs/instrumentation**: The human_review_gate node triggers an indefinite interrupt or bypasses it silently without logging. Adding simple debug/info logging would help track when the gate is entered, suspended, and resumed. [raa/nodes/human_review_gate.py:220]

## Deferred from: code review of 3-3-authoritative-human-answer-mapping-and-conflict-resolution.md (2026-05-23)

- **Silent Dropping of Overrides when judge_llm is Missing**: If no `judge_llm` is configured, `_parse_human_override` catches the exception/missing config and returns empty instructions. While safe, this silently drops free-text overrides. [raa/nodes/conflict_resolution.py]

## Deferred from: code review of 3-3-authoritative-human-answer-mapping-and-conflict-resolution.md (2026-05-24)

- **Silent Dropping of Overrides when judge_llm is Missing**: If no `judge_llm` is configured, `_parse_human_override` catches the exception/missing config and returns empty instructions. While safe, this silently drops free-text overrides. [raa/nodes/conflict_resolution.py] — deferred, pre-existing

## Deferred from: code review of 4-3-100-percent-requirements-traceability-audit.md (2026-05-24)

- **BH-4 — TraceabilityAuditException causes full superstep state loss**: When `final_merge` raises `TraceabilityAuditException`, LangGraph discards all state updates for that superstep (arch_model, traceability_manifest, diagram_manifest are all lost). Per LangGraph fault-tolerance docs, the correct fix is an `error_handler=` registered on the `final_merge` node in the graph builder, routing to a failure state. The `final_merge` function correctly propagates the exception; the gap is in the graph construction code (outside this story's scope). [graph builder — not yet implemented]
- **BH-2 — O(n·m) quadratic question-matching loop**: The inner `for norm_req_id in input_ids` loop inside `for q in all_questions` is O(questions × requirements). Acceptable at current scale; pre-index by question ID or req_id to reduce to O(n+m) when volume grows. [raa/nodes/final_merge.py:908]
- **ECH-1 — Zero-requirement audit passes vacuously**: If all four input ID sources are empty, `trace_map` is `{}` and the audit silently returns `{}`. No warning or log. Add a guard: `if not input_ids: logger.warning("Traceability audit: no input requirements found — audit trivially passes.")`. [raa/nodes/final_merge.py:862]
- **AA-1 — arch_model relationship req_ids not in initial ID collection**: A requirement that exists only in a `C4Relationship.requirement_ids` but not in any of the four input sources (`requirements`, `normalized_asrs`, `normalized_non_asr`, `unprocessed_requirements`) is silently ignored by the audit. Requires a spec clarification to fix. [raa/nodes/final_merge.py:844-856]
