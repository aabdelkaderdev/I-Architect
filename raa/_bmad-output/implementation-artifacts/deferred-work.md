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

