# Implementation Plan: RAA Final Merge and Output

**Branch**: `017-raa-final-merge-output` | **Date**: 2026-05-19 | **Spec**: [specs/017-raa-final-merge-output/spec.md](spec.md)

**Input**: Feature specification from `specs/017-raa-final-merge-output/spec.md`

## Summary

This plan covers the implementation of the final merge node under `raa/nodes/final_merge.py`. It includes logic to perform a global deterministic merge of all batch fragments (`best_batch_output`) and the final `running_arch_model`. It runs a single, focused LLM reconciliation pass using `llm_judge` to resolve outstanding `open_questions` before validation. It validates the output against the C4 schema (ensuring strict hierarchy nesting, valid relationship endpoints, correct relationship diagram scopes, and unique entity IDs). It deterministically generates a `diagram_manifest` work queue for AGA. Finally, it writes the serialized C4 model as `arch_model.json` to the orchestrator-provided path `projects/{project_name}/output/raa/arch_model.json`, and archives the SQLite checkpoint database.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `langchain`, `langgraph`, `pydantic`

**Storage**: Filesystem output (JSON file), SQLite for active checkpoint DB (`raa_graph.db`).

**Testing**: `pytest` unit/integration tests under `tests/` to verify deterministic global merging, LLM-based reconciliation, schema validation, manifest counts, and checkpoint archive functionality.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Fast serialization and validation, minimal overhead.

**Constraints**: Output JSON must strictly match the `C4JsonModel` schema. Checkpoint archiving must happen *after* successful validation and file writing.

**Scale/Scope**: A single node module (`raa/nodes/final_merge.py`) and a unit/integration test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. A C4-compliant entity-relationship JSON model is validated and a precise diagram manifest is generated; RAA does not produce any PlantUML/diagrams/code.
- **Principle II: Deterministic Data Pipeline**: Passed. The global merge and diagram manifest generation are deterministic static templates, and caching is preserved.
- **Principle III: LLM Isolation & Context Injection**: Passed. `llm_judge` is retrieved from the graph context configuration, never serialized into the graph state.
- **Principle IV: Hierarchical Integrity (Orphan Prevention)**: Passed. Validation ensures strict nesting (system -> container -> component), prevents orphan containers/components, and ensures no entity ID reuse across levels.
- **Principle V: Incremental Coherence (Batch-Sequential Model)**: Passed. The active checkpoint DB is archived only after output validation and serialization are completed successfully.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/017-raa-final-merge-output/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1/Design output
├── quickstart.md        # Phase 1/Quickstart guide
├── contracts/
│   └── readme.md        # Phase 1/Interface contracts
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
raa/
└── nodes/
    └── final_merge.py   # Final merge, reconciliation, and output logic
tests/
└── test_final_merge.py  # Unit and integration tests for final merge and validation
```

**Structure Decision**: Single project layout matching the existing `raa/nodes/` and `tests/` conventions in the workspace.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
