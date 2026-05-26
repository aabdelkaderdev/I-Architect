## 1. Shared LLM Infrastructure

- [x] 1.1 Define `LLMEvaluationResult` Pydantic `BaseModel` in `sa/state/models.py` with `score: int = Field(ge=0, le=10)` and `reasoning: str` fields
- [x] 1.2 Create `sa/utils/llm.py` helper that uses `init_chat_model` from `langchain.chat_models` to initialize the model and exposes a function that calls `model.with_structured_output(LLMEvaluationResult).invoke(prompt)` with error handling (fallback to score 0)

## 2. LLM Prompt Templates

- [x] 2.1 Create `prompts/functional_depth.md` template with evaluation task, input data format, and constraints from the `Functional_Depth_Evaluation.md` skill
- [x] 2.2 Create `prompts/technology_specificity.md` template with evaluation task, input data format, and ASR quality attribute context

## 3. Node 2: Functional Traceability Implementation

- [x] 3.1 Implement deterministic mapping coverage calculation `(mapped / total) * 15` with zero-division guard
- [x] 3.2 Implement deterministic orphan penalty calculation (-1 per orphan, max -10)
- [x] 3.3 Build depth distribution summary from `traceability_matrix` (percentage at each C4 level)
- [x] 3.4 Integrate LLM call using the shared `llm.py` helper with `with_structured_output(LLMEvaluationResult)` and the `prompts/functional_depth.md` template
- [x] 3.5 Populate and return `score_functional` as an `AxisScore` partial state update

## 4. Node 3: ASR Coverage Implementation

- [x] 4.1 Implement deterministic ASR mapping coverage calculation `(mapped / total) * 15` with zero-division guard
- [x] 4.2 Implement deterministic contradiction penalty calculation (-5 per contradiction)
- [x] 4.3 Integrate LLM call using the shared `llm.py` helper with `with_structured_output(LLMEvaluationResult)` and the `prompts/technology_specificity.md` template
- [x] 4.4 Populate and return `score_asr` as an `AxisScore` partial state update

## 5. Verification

- [x] 5.1 Run pipeline end-to-end with sample inputs to verify nodes execute without crashing
- [x] 5.2 Verify `scoring_report.json` rolls up Node 2 and Node 3 scores correctly alongside mocked Node 4 and Node 5 text
- [x] 5.3 Verify LLM fallback path works when model is unavailable or returns an invalid response
