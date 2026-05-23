# Story 3.3: Authoritative Human Answer Mapping & Conflict Resolution

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want the graph to apply human answers authoritatively to override pre-computed suggestions when resuming,
so that human design preferences override the autonomous agent's default choices.

## Acceptance Criteria

1. **Authoritative Answer Mapping**: Given a suspended graph and a resume command payload containing human answers, when the graph resumes from the interrupt, it must map the human answers to their matching open questions.
2. **Override Suggestions**: The mapped human answers must override any pre-computed Judge suggestions (e.g., the pre-computed suggested answer or resolution).
3. **Reset Assumption Flags**: The node must set `assumption_flag = false` (in the entity's metadata and remove the entity ID from the model's `assumption_flags` list) for all entities resolved directly by a human answer.
4. **Structural Validity Check**: If the human's free-text override contains structurally invalid instructions (e.g., trying to place a component directly under a system without a container, referencing non-existent parent IDs, or violating relationship scopes), the system must catch the validation error, log a `scope_conflict` open question, and apply fallback constraints (revert the change to the default safe state or canonical layout rules).

## Tasks / Subtasks

- [x] Task 1: Implement the Conflict Resolution Node (AC: #1, #2, #3, #4)
  - [x] 1.1 Create `raa/nodes/conflict_resolution.py` with standard node signature:
    ```python
    def conflict_resolution(state: RAAState, config: RunnableConfig | None = None) -> dict:
    ```
  - [x] 1.2 Normalize `human_answers` structure from the `human_answers` channel. Handle both a flat dictionary `{question_id: answer_text}` and a list of dictionary answers `{"answers": [{"question_id": "...", "answer": "..."}]}` or nested `{"answers": {"q_id": "text"}}` safely.
  - [x] 1.3 Map each answer to its matching `OpenQuestion` in `state["open_questions"]`. If a match is found:
    - Update the question's `resolution` field to the human answer.
    - Set the question's `assumption_flag` to `False`.
    - Retrieve all entities referenced in the question's context (scanning keys `entity_a_id`, `entity_b_id`, `entity_id`, and `promoted_component_id` at both root and nested context levels).
  - [x] 1.4 Apply overrides to the `arch_model`:
    - For each referenced entity resolved directly by a human answer, locate the entity in `arch_model["entities"]` (or nested containers/components).
    - Set `entity.metadata["assumption_flag"] = False` (and `entity.metadata["assumed"] = False` to be robust).
    - Remove the entity's ID from the `arch_model.get("assumption_flags", [])` list.
  - [x] 1.5 Implement an LLM interpreter step to parse the free-text human directions into concrete C4 structural actions (e.g., changing parent system/container references, merging elements, adding relationships):
    - Use a Chevron rendered mustache template from `raa/prompts/parse_human_override.md`.
    - Use the injected `judge_llm` from the config (`config["configurable"]["judge_llm"]`) with structured output to get the target structural modifications.
  - [x] 1.6 Run the metamodel validation check on the modified model using `enforce_fragment_hierarchy(fragment, running_model)` from `raa.utils.c4_validator`:
    - If `enforce_fragment_hierarchy` returns any hierarchy or endpoint conflicts (such as orphan components, system parent mismatches, or unresolved relationship endpoints):
      - Catch the validation error/conflict.
      - Log a new open question of type `scope_conflict` containing a descriptive summary of the validation failure.
      - Revert the invalid modification (fallback constraint) and apply the canonical default layout rules.
  - [x] 1.7 Export the node in `raa/nodes/__init__.py`.

- [x] Task 2: Implement Unit and Integration Tests (AC: #1, #2, #3, #4)
  - [x] 2.1 Create `tests/raa/unit/test_conflict_resolution.py` testing the `conflict_resolution` node.
  - [x] 2.2 Verify that flat, nested, and list-style `human_answers` map and override pre-computed suggestions correctly.
  - [x] 2.3 Verify that entities resolved by human answers have their `assumption_flag` set to `False` in metadata and are removed from `assumption_flags` list.
  - [x] 2.4 Mock structural violations in the interpreter output to verify that validation failures are caught, log a `scope_conflict` open question, and fall back to valid C4 rules.
  - [x] 2.5 Run the entire test suite to ensure all tests pass:
    ```bash
    python3 -m pytest
    ```

## Dev Notes

- **C4 Metamodel Enforcement**: The validator `raa.utils.c4_validator.enforce_fragment_hierarchy` must be used to ensure structural validity.
- **LLM Selection**: Use the `judge_llm` slot for parsing the human answer.
- **Append-only Reduction**: Since `open_questions` is an append-only channel, the node must return the updated list of questions to be appended or return the fully resolved list in the final output stage.

### Project Structure Notes

- Keep all logic within `raa/nodes/conflict_resolution.py`.
- No modifications to external dependencies or libraries outside `requirements.txt` or `pyproject.toml`.

### References

- [Source: `_bmad-output/planning-artifacts/epics.md#Story 3.3: Authoritative Human Answer Mapping & Conflict Resolution`]
- [Source: `raa/utils/c4_validator.py` — `enforce_fragment_hierarchy`]
- [Source: `raa/state/models.py` — `OpenQuestion` and `ArchFragment` schemas]
- [Source: `raa/nodes/human_review_gate.py`]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

No debug logs — all 498 tests passed on first implementation pass.

### Completion Notes List

- **Task 1**: Created `raa/nodes/conflict_resolution.py` with `conflict_resolution(state, config)` node. Implements: (1) answer normalization from flat dict, list-style, and nested dict formats; (2) question/answer mapping with entity ID collection from both root-level and nested context keys; (3) arch model override application clearing assumption flags on resolved entities; (4) LLM interpreter using `load_prompt` + `judge_llm.with_structured_output(HumanOverrideInstructions)` to parse free-text into C4 structural modifications (entity parent changes, merges, deletes, relationship CRUD); (5) C4 metamodel validation via `enforce_fragment_hierarchy` with fallback to safe state on hierarchy conflicts. Created `raa/prompts/parse_human_override.md` prompt template with Chevron/Mustache syntax. Exported in `raa/nodes/__init__.py`.
- **Task 2**: Created `tests/raa/unit/test_conflict_resolution.py` with 34 tests covering: answer normalization (6 tests), answer mapping (5 tests), arch model overrides (3 tests), structural modifications (9 tests), LLM interpreter with mocking (4 tests), full node integration (5 tests), validation fallback (1 test).

### File List

- `raa/nodes/conflict_resolution.py` — **NEW**: Conflict resolution node
- `raa/prompts/parse_human_override.md` — **NEW**: LLM prompt template for human override parsing
- `raa/nodes/__init__.py` — Added `conflict_resolution` export
- `tests/raa/unit/test_conflict_resolution.py` — **NEW**: 34 unit tests

### Review Findings

- [ ] [Review][Patch] Duplicate open questions in `RAAState` append channel [raa/nodes/conflict_resolution.py:478-481]
- [ ] [Review][Patch] Redundant Multi-Pass Loop over Unified Instructions [raa/nodes/conflict_resolution.py:470-477]
- [ ] [Review][Patch] Dangling Relationships on Entity Deletion [raa/nodes/conflict_resolution.py:290-295]
- [ ] [Review][Patch] Mismatched/Missing Question IDs during Answer Mapping [raa/nodes/conflict_resolution.py:108-112]
- [ ] [Review][Patch] Lack of Validation for `action` Fields in Modifications [raa/nodes/conflict_resolution.py:252-330]
- [x] [Review][Defer] Silent Dropping of Overrides when `judge_llm` is Missing [raa/nodes/conflict_resolution.py] — deferred, pre-existing

