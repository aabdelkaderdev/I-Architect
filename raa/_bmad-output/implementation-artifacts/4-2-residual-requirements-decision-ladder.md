# Story 4.2: Residual Requirements Decision Ladder

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want the Judge to process unassigned leftover requirements using the multi-step decision ladder,
So that all secondary requirements are integrated or categorized based on similarity and coupling.

## Acceptance Criteria

1. **Residual Execution**: Given the merged C4 model and the list of `unprocessed_requirements` (populated in Phase 5 queue ordering), when the residual pass executes inside `final_merge`, it must evaluate each leftover requirement sequentially against the merged model.
2. **High Similarity (> 0.75)**: If the cosine similarity of a leftover requirement description/condition to any container's description in the model is $> 0.75$, it must auto-enrich the matching container's description (e.g. by appending `"(Supports {req_id}: {req_desc})"`) and append the requirement ID to the container's `requirement_ids` list.
3. **Moderate Similarity (0.50 to 0.75)**: If similarity is between $0.50$ and $0.75$, it must check coupling (e.g. sharing actors or data flows) using the Judge LLM (or a fallback heuristic):
   - If coupled, it must enrich the container (append to description and append `req_id` to `requirement_ids`) and log `assumption_flag = true` (and `assumed = true`) on the container's metadata and add its ID to the model's `assumption_flags` list.
   - If not coupled, it must exclude the requirement and flag it as a human review query (add to `open_questions` with type `"residual_coupling"` and owner `"human_preferred"`).
4. **Low Similarity (< 0.50) & Architectural**: If similarity is $< 0.50$ and it implies architectural structure (checked via LLM or structural keyword heuristics), it must propose a minimal C4 entity and its relationships. The proposed entity must pass C4 parent-resolution (`enforce_fragment_hierarchy`) and deduplication (`deduplicate_and_merge_fragment`) checks before merging.
5. **Low Similarity (< 0.50) & Non-Architectural**: If similarity is $< 0.50$ and it is non-architectural, it must exclude the requirement and log a `"coverage_gap"` open question with a clear one-sentence rationale.

## Tasks / Subtasks

- [ ] Task 1: Implement Residual Requirements Decision Ladder in `raa/nodes/final_merge.py` (AC: #1, #2, #3, #4, #5)
  - [ ] 1.1 In `final_merge()`, retrieve `state["unprocessed_requirements"]` and run a sequential evaluation loop over each leftover requirement.
  - [ ] 1.2 For similarity comparisons, extract requirement text (condition_text for ASRs; description for non-ASRs) and fetch the vector using the `EmbeddingCache` and `TextEmbedding` model.
  - [ ] 1.3 For each container in the current `arch_model`, embed its description and calculate the cosine similarity. Cache container description embeddings locally to avoid duplicate model calls.
  - [ ] 1.4 Implement **High Similarity (> 0.75)**: auto-enrich description with a suffix and append to `requirement_ids`.
  - [ ] 1.5 Implement **Moderate Similarity (0.50 to 0.75)**: call the Judge LLM with the `judge_residual.md` prompt to check coupling. If `judge_llm` is missing or fails, fall back to actor/flow keyword word-overlap heuristic.
    - If coupled: enrich description, append requirement ID, and set `assumption_flag = True` and `assumed = True` on container metadata (and add ID to `arch_model["assumption_flags"]`).
    - If not coupled: exclude and add a `residual_coupling` question to the output questions.
  - [ ] 1.6 Implement **Low Similarity (< 0.50)**: call the Judge LLM with `judge_residual.md` to check if it implies architectural structure. If `judge_llm` is missing or fails, fall back to structural keyword heuristic.
    - If architectural: parse the proposed minimal C4 entity and relationships, validate them via `enforce_fragment_hierarchy`, and merge them into the running model via `deduplicate_and_merge_fragment`.
    - If non-architectural: exclude the requirement and add a `coverage_gap` question with the LLM-generated (or fallback) one-sentence rationale.
  - [ ] 1.7 Add the new `judge_residual.md` prompt template in `raa/prompts/` to support the LLM structured calls.

- [ ] Task 2: Implement Unit Tests in `tests/raa/unit/test_final_merge.py` (AC: #1, #2, #3, #4, #5)
  - [ ] 2.1 Add test cases verifying sequential processing of multiple `unprocessed_requirements`.
  - [ ] 2.2 Test the > 0.75 threshold case: verifies container description enrichment and ID appending.
  - [ ] 2.3 Test the 0.50 - 0.75 threshold case:
    - Verifies coupled case: sets assumption flags on entity metadata and model `assumption_flags`.
    - Verifies non-coupled case: excludes requirement and generates a `residual_coupling` open question.
  - [ ] 2.4 Test the < 0.50 case:
    - Architectural: verifies that proposed entity passes `enforce_fragment_hierarchy` parent check and is successfully merged.
    - Non-architectural: verifies exclusion and generation of a `coverage_gap` open question with a clear rationale.
  - [ ] 2.5 Test fallbacks: ensures the decision ladder handles missing embedding model/cache or missing LLM gracefully using keyword/heuristics.

## Dev Notes

- **Threshold Constants**: Use `RESIDUAL_HIGH_THRESHOLD = 0.75` and `RESIDUAL_MID_LOW = 0.50` imported from `raa.utils.constants`.
- **Validation and Deduplication**: Ensure that proposed entities are wrapped in an `ArchFragment` and passed to `enforce_fragment_hierarchy` and `deduplicate_and_merge_fragment` to run the standardized validation and merging checks.
- **SQLite Cached Embeddings**: Retrieve existing requirement embeddings from the SQLite caches (`asr_cache` and `non_asr_cache`).

## References

- [Source: `_bmad-output/planning-artifacts/epics.md#Story 4.2: Residual Requirements Decision Ladder`]
- [Source: `raa/utils/c4_validator.py` — for C4 hierarchy validation rules]
- [Source: `raa/judge/deduplication.py` — for ID normalization and fragment merging logic]

## File List

- `raa/prompts/judge_residual.md` (new) — Judge prompt template for residual evaluation
- `raa/nodes/final_merge.py` (modified) — added sequential decision ladder logic
- `tests/raa/unit/test_final_merge.py` (modified) — added unit tests for decision ladder cases
