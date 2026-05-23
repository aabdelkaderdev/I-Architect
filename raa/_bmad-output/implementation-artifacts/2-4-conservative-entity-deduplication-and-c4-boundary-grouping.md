# Story 2.4: Conservative Entity Deduplication and C4 Boundary Grouping

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an Architect,
I want the Judge to merge semantically duplicate entities and create boundary groupings for moderate-similarity deployment units,
so that we prevent entity count bloat while protecting CQRS architectural separation.

## Acceptance Criteria

1. **ID Normalization**: Normalize entity IDs to lowercase `snake_case` (e.g. `User_Service` or `userService` becomes `user_service`) for initial matching.
2. **Cosine Similarity Calculation**: Calculate cosine similarity between entity descriptions using the SQLite embedding cache (`non_asr_embeddings.db`).
3. **On-the-Fly Embedding of Descriptions**: If an entity's description is not yet present in the SQLite cache, the node must generate its embedding at runtime using the FastEmbed model (`mixedbread-ai/mxbai-embed-large-v1` from the configured paths) and save it in the database.
4. **Deterministic Text Hashing**: Use `EmbeddingCache.text_hash(text)` to generate SHA-256 keys for the database queries and storage.
5. **Empty Description Handling**: If an entity description is empty or contains only whitespace, do not generate an embedding. Instead, default the cosine similarity score to `0.0` (unless the normalized IDs match exactly).
6. **Auto-Merge (similarity >= 0.80)**: If cosine similarity between two entities is >= 0.80 AND their requirement IDs overlap, they must be merged:
   - Retain the longest description.
   - Union their technology tags (e.g., split by comma/semicolon, strip whitespace, deduplicate, and join with a standard comma-space separator).
   - Union their requirement IDs.
7. **C4 Boundary Grouping (similarity 0.60 to 0.80)**: If similarity is between 0.60 and 0.80, do not merge them but cluster them into logical C4 boundary groupings in the JSON output (both in entity metadata and in a top-level `boundary_groups` list in `arch_model`).
8. **Open Questions for Moderate-Similarity Conflicts**: Flag moderate-similarity conflicts (similarity between 0.60 and 0.80) and write them to the `change_risk` or `high_coupling` open question list.
9. **Relationship Endpoint Rewriting**: When a primary fragment entity is merged into a running model entity with a different ID, update the matching `source_id` and `target_id` fields in relationships to map to the canonical merged entity ID.
10. **Node Integration**: Update the Judge reconciliation node (`raa/judge/reconcile.py`) to merge the primary fragment's entities and relationships into the running model (`arch_model`) and advance the `batch_cursor` (increment it by 1).
11. **Regression & Unit Testing**: Ensure all existing tests pass and author comprehensive unit tests for the new deduplication and boundary grouping logic.

## Tasks / Subtasks

- [x] Task 1: Create the Deduplication Engine (`raa/judge/deduplication.py`) (AC: #1, #2, #3, #4, #5, #6, #7, #8, #9)
  - [x] 1.1 Implement ID normalization function `normalize_entity_id(entity_id: str) -> str`. It should convert camelCase, PascalCase, or mixed-case string with underscores/hyphens into lowercase `snake_case` (e.g., `user-service` -> `user_service`, `UserService` -> `user_service`).
  - [x] 1.2 Implement similarity calculation utilizing `EmbeddingCache` and the FastEmbed model singleton (loading via `get_embedding_model` from `raa/utils/embedding_cache.py`). Cache computed embeddings of entity descriptions in the SQLite database under a text_hash key.
  - [x] 1.3 Add checks to bypass embedding generation if the description is empty or whitespace-only, defaulting similarity to `0.0`.
  - [x] 1.4 Implement merging logic for `C4Entity` objects (retaining the longest description, unioning technology tags with proper formatting, and unioning requirement IDs).
  - [x] 1.5 Implement a grouping and merging function `deduplicate_and_merge_fragment(primary_fragment: ArchFragment, running_model: dict, cache: EmbeddingCache, model: TextEmbedding) -> tuple[dict, list[dict]]` that processes the primary fragment and merges it into `running_model`. It must return the updated `running_model` dictionary and a list of open questions.
  - [x] 1.6 Ensure that when entities are merged, all relationships in the primary fragment and running model that reference the merged entity ID are rewritten to point to the canonical ID.
- [x] Task 2: Integrate into reconciliation node (`raa/judge/reconcile.py`) (AC: #10)
  - [x] 2.1 Open `non_asr_embeddings.db` using `EmbeddingCache` and get the model using `get_embedding_model(cache_dir, model_name)`.
  - [x] 2.2 Extract the primary fragment from `rank_batch_fragments` (or retrieve it from `judge_rankings` if already ranked).
  - [x] 2.3 Reconcile and merge the primary fragment into the running `arch_model` state.
  - [x] 2.4 Append any new `open_questions` to the state's `open_questions` list.
  - [x] 2.5 Increment `batch_cursor` by 1.
  - [x] 2.6 Return the updated `arch_model`, `batch_cursor`, `judge_rankings`, and `open_questions`.
- [x] Task 3: Author comprehensive unit tests (AC: #11)
  - [x] 3.1 Add `tests/raa/unit/test_judge_deduplication.py` testing ID normalization, similarity calculation (with cache hit/miss and empty description handling), merging, and C4 boundary grouping.
  - [x] 3.2 Update `tests/raa/unit/test_judge_reconcile.py` to assert that `select_primary_fragment` now merges the primary fragment into `arch_model` and increments `batch_cursor`.

### Review Findings

- [x] [Review][Patch] Flag parent C4 hierarchy mismatch as open question on merge [raa/judge/deduplication.py:122-156]
- [x] [Review][Patch] Critical relationship referential integrity failure on entity merge [raa/judge/deduplication.py:256-329]
- [x] [Review][Patch] Missing boundary group assignment in entity metadata [raa/judge/deduplication.py:291-310]
- [x] [Review][Patch] Dangling boundary groups and open questions created for merged entities [raa/judge/deduplication.py:261-310]
- [x] [Review][Patch] Potential TypeError crash when relationship metadata is None [raa/judge/deduplication.py:180]
- [x] [Review][Patch] Duplicate technology tags generated due to case-sensitivity [raa/judge/deduplication.py:106-120]
- [x] [Review][Patch] Non-compliant open question classification [raa/judge/deduplication.py:294-309]
- [x] [Review][Patch] ID normalization does not filter illegal special characters [raa/judge/deduplication.py:45-62]
- [x] [Review][Patch] Pydantic validation crash hazard in type coercion helpers [raa/judge/deduplication.py:203-219]
- [x] [Review][Patch] Use Pydantic v2 model_validate instead of double-splat initialization [raa/judge/deduplication.py:203-219]
- [x] [Review][Patch] Use robust RunnableConfig extraction with fallback [raa/judge/reconcile.py:72-78]
- [x] [Review][Defer] SQLite cache overwrite hazard due to primary key design [raa/utils/embedding_cache.py:121] — deferred, pre-existing
- [x] [Review][Defer] Inefficient non-batched embedding calls for cache misses [raa/judge/deduplication.py:65-96] — deferred, pre-existing

## Dev Notes

### Current Implementation Baseline

Completed predecessor stories provide these files and contracts:

| File | Current State | Story 2.4 Change |
| --- | --- | --- |
| `raa/judge/reconcile.py` | Contains `select_primary_fragment` which ranks batch fragments but does not merge them or advance the cursor. | Update this node to run the deduplication pass and merge the primary fragment into `arch_model` and advance `batch_cursor`. |
| `raa/judge/scoring.py` | Implements the pure fragment scoring and ranking logic. | Unchanged, but used by `reconcile.py` to identify the primary fragment. |
| `raa/utils/embedding_cache.py` | Encapsulates all SQLite read/write for dense vector storage and provides the FastEmbed model loader. | Use `EmbeddingCache` and `get_embedding_model` to fetch and store embeddings for entity descriptions. |
| `raa/state/schemas.py` | Defines `RAAState` keys. | Unchanged, but now we actually populate `arch_model` and increment `batch_cursor`. |

### Story Source

Story 2.4 in the epics file requires the Judge to merge semantically duplicate entities and create boundary groupings for moderate-similarity deployment units. [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.4: Conservative Entity Deduplication and C4 Boundary Grouping`]

PRD FR-11 specifies the cosine similarity thresholds: similarity >= 0.80 and overlapping requirements triggers an auto-merge; similarity 0.60 to 0.80 clusters containers into boundary groupings and flags them in open questions. [Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md#FR-11: Conservative Entity Deduplication and C4 Boundary Grouping`]

### Architecture Guardrails

1. **Deduplication Engine Isolation**: Implement deduplication and merging algorithms in a pure module (`raa/judge/deduplication.py`) and keep the LangGraph node wrapper in `raa/judge/reconcile.py` clean.
2. **Deterministic Merge**: Deduplication, grouping, and merging must be fully deterministic.
3. **No Overwrite of Non-Overlapping Entities**: Non-overlapping or low-similarity entities must be added to the running model without changes.
4. **State Mutability**: Never mutate state lists or dicts in place. Construct and return a new dictionary with the modified keys (e.g. `arch_model`, `batch_cursor`, `open_questions`).

### Testing Requirements

Run at minimum:

```bash
python3 -m pytest tests/raa/unit/test_judge_scoring.py -q
python3 -m pytest tests/raa/unit/test_judge_reconcile.py -q
```

And run new tests:

```bash
python3 -m pytest tests/raa/unit/test_judge_deduplication.py -q
```

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

N/A

### Completion Notes List

- Implemented `raa/judge/deduplication.py` with: `normalize_entity_id` (camelCase/PascalCase/kebab → snake_case), `_compute_entity_similarity` (EmbeddingCache + FastEmbed with on-the-fly generation), `_merge_entities` (longest desc, tech union, req union, canonical ID selection), `_rewrite_relationship_ids`, `_create_boundary_group`, and `deduplicate_and_merge_fragment` (main orchestrator).
- Updated `raa/judge/reconcile.py` to extract the primary fragment from rankings, conditionally load the embedding model (only when both primary fragment and running model have entities), call dedup/merge, and return `arch_model`, `batch_cursor + 1`, and `open_questions`.
- Model loading is skipped when cache=None/model=None — dedup falls back to exact normalized-ID matching only. This avoids loading the embedding model during tests and first-batch scenarios.
- All 352 unit tests pass (46 new dedup tests + 7 updated reconcile tests + 299 existing).
- Design decisions: pure deterministic engine, state immutability (never mutate lists/dicts in place), configurable DB/model paths via RunnableConfig.

### File List

- `raa/judge/deduplication.py` — NEW: deduplication engine
- `raa/judge/reconcile.py` — MODIFIED: integrated dedup/merge into node
- `tests/raa/unit/test_judge_deduplication.py` — NEW: 46 comprehensive unit tests
- `tests/raa/unit/test_judge_reconcile.py` — MODIFIED: updated for Story 2.4 behavior (7 tests)
