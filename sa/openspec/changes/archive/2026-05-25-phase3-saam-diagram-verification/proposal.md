## Why

Implement Axis 3 (SAAM Evaluation & Diagram Verification), the most complex node requiring custom PlantUML parsing and heavily-weighted quality attribute evaluation. This will complete the 100-point scoring rubric for the system.

## What Changes

- Add a PlantUML parser to extract C4 aliases and structural information from diagrams.
- Implement deterministic diagram correctness checking, which evaluates render completeness, entity inclusion, and hierarchy validity.
- Define a `SAAMEvaluationResult` Pydantic model for the SAAM LLM structured output (score 0–30, reasoning, attribute assessments).
- Integrate SAAM LLM validation via `init_chat_model` and `with_structured_output(SAAMEvaluationResult)` using LangChain's auto-strategy selection.
- Replace Node 4 mocks with full SAAM + diagram verification implementation.
- Migrate message imports from deprecated `langchain_core.messages` to `langchain.messages`.

## Capabilities

### New Capabilities

- `axis-saam`: SAAM methodology evaluation of quality attributes, mapping patterns to stimulus-response scenarios.
- `diagram-verification`: Custom PlantUML parsing to extract C4 aliases and deterministic verification of C4 diagram structure.

### Modified Capabilities

- `deterministic-reporting`: Update the final report generation to include the `score_saam` (Node 4) results and diagram issues into the final 100-point rubric breakdown.

## Impact

- Replaces `nodes/axis_saam.py` mock implementation.
- Introduces `utils/plantuml_parser.py` and `prompts/saam_validation.md`.
- Adds `SAAMEvaluationResult` to `state/models.py`.
- Updates `utils/llm.py` import path from `langchain_core.messages` → `langchain.messages`.
- Completes the main processing pipeline up to the Node 5 executive summary.
