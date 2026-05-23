# Story 3.2: Indefinite LangGraph Interrupt Gate

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want the RAA Orchestrator to trigger an indefinite LangGraph interrupt in interactive mode and bypass it in autonomous mode,
so that humans can review models interactively, but scripts can run without blocks.

## Acceptance Criteria

1. **Interrupt Gating Behavior**: Given a populated `human_review_payload` and a config parameter `review_mode` set to `"interactive"` or `"autonomous"`, when the Human Review Gate node executes, it must check `review_mode`.
2. **Interactive Mode Suspends Indefinitely**: If `review_mode` is `"interactive"`, the node must trigger the standard LangGraph `interrupt(payload)` function containing the payload, suspending the graph execution indefinitely with no timeout.
3. **No Automatic Resumption**: The node must not auto-resume or auto-resolve until a standard `Command(resume=...)` is received.
4. **Autonomous Mode Pass-Through**: If `review_mode` is `"autonomous"`, the node must bypass the interrupt entirely and transition immediately to the global resolution phase (Phase 8), returning an empty dictionary `{}`.

## Tasks / Subtasks

- [x] Task 1: Implement `human_review_gate(state: RAAState) -> dict` in `raa/nodes/human_review_gate.py` (AC: #1, #2, #3, #4)
  - [x] 1.1 Import `interrupt` from `langgraph.types` at the top of `raa/nodes/human_review_gate.py`.
  - [x] 1.2 Implement the `human_review_gate(state: RAAState) -> dict` function.
  - [x] 1.3 Check if `state.get("review_mode")` equals `"interactive"`.
  - [x] 1.4 If `"interactive"`, trigger the interrupt: `human_answers = interrupt(state.get("human_review_payload") or {})` and return `{"human_answers": human_answers}`.
  - [x] 1.5 If `"autonomous"` (or any other value), bypass the interrupt and return `{}`.
  - [x] 1.6 Export the new node function by importing it in `raa/nodes/__init__.py` and adding it to `__all__`.

- [x] Task 2: Implement Unit and Integration Tests for `human_review_gate` in `tests/raa/unit/test_human_review_gate.py` (AC: #1, #2, #3, #4)
  - [x] 2.1 Import `human_review_gate` and `patch` in `tests/raa/unit/test_human_review_gate.py`.
  - [x] 2.2 Add unit tests using `unittest.mock.patch` to verify:
    - In `"autonomous"` mode, `interrupt` is not called, and the return value is `{}`.
    - In `"interactive"` mode, `interrupt` is called with `human_review_payload`, and the return value of `interrupt` is returned as the value of `human_answers`.
  - [x] 2.3 Add an integration test using a simple LangGraph `StateGraph` compiled with a memory checkpointer (`MemorySaver`) to verify:
    - Invoking the graph in `"interactive"` mode halts execution at the gate, returning the state containing the interrupt payload.
    - Resuming the graph with `Command(resume=...)` continues execution past the gate and writes the resume payload to `human_answers` channel.
  - [x] 2.4 Run the test suite and verify all tests pass:
    ```bash
    python3 -m pytest tests/raa/unit/test_human_review_gate.py -v
    ```

## Dev Notes

- **LangGraph Interrupt API**: The standard `interrupt()` API suspends execution and can only be resumed using `Command(resume=...)` in LangGraph 1.2.0.
- **Indefinite Wait Constraint**: The PRD and D8 mandate that the interrupt waits indefinitely with no timeout. Do **NOT** implement the `review_timeout_seconds` parameter from the legacy specification.
- **State Channel Alignment**: The return value of the node is written to the `human_answers` state channel.
- **UX Design**: The RAA module is a pure Python backend processing pipeline and does not expose a user interface (UX-DR1).

### Project Structure Notes

- Node function should be implemented in `raa/nodes/human_review_gate.py` alongside `prepare_human_review_payload`.
- Export node function in `raa/nodes/__init__.py`.
- Implement new tests in `tests/raa/unit/test_human_review_gate.py`.

### References

- [Source: `_bmad-output/planning-artifacts/epics.md#Story 3.2: Indefinite LangGraph Interrupt Gate`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#D8 — Human Review Gate Interrupt Mechanism`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#D9 — Human Answers Injection (Resume)`]
- [Source: `raa/state/schemas.py` — `RAAState` definition]
- [Source: `raa/nodes/human_review_gate.py`]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

No debug logs — all 462 tests passed on first implementation pass.

### Completion Notes List

- **Task 1**: Added `human_review_gate(state: RAAState) -> dict` to `raa/nodes/human_review_gate.py`. Imports `interrupt` from `langgraph.types`. In `"interactive"` mode, calls `interrupt(human_review_payload)` and returns the resume value as `human_answers`. In `"autonomous"` mode (or any other value), returns `{}`. Updated docstring to reflect Story 3.2 scope. Exported in `raa/nodes/__init__.py`.
- **Task 2**: Added 14 new tests to `tests/raa/unit/test_human_review_gate.py`: 4 autonomous mode tests (no interrupt call, empty return), 3 interactive mode tests (interrupt called with payload, human_answers returned, empty payload fallback), 2 integration tests using LangGraph `StateGraph` with `MemorySaver` (halt + resume with `Command(resume=...)`, state preservation at interrupt boundary).

### File List

- `raa/nodes/human_review_gate.py` — Added `human_review_gate` function and `interrupt` import
- `raa/nodes/__init__.py` — Updated exports with `human_review_gate` and `__all__`
- `tests/raa/unit/test_human_review_gate.py` — Added 14 Story 3.2 tests (43 total)

### Review Findings

- [x] [Review][Patch] Unvalidated return value of interrupt() could be non-dict [raa/nodes/human_review_gate.py:235]
- [x] [Review][Patch] Explicit None in review_mode is treated as autonomous mode [raa/nodes/human_review_gate.py:228]
- [x] [Review][Defer] Missing execution logs/instrumentation [raa/nodes/human_review_gate.py:220] — deferred, pre-existing
