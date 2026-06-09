## Why

This change replaces the mock passthrough nodes for Node 2 (Functional Traceability) and Node 3 (ASR Coverage) with real scoring logic. This introduces the first deterministic grading math and LLM skill integrations, providing actionable, evaluated scores rather than stubs, bringing the Scoring Agent closer to full evaluation capability.

## What Changes

- **Node 2 (Functional Traceability)**: Implement deterministic mapping coverage and orphan penalty calculations. Introduce an LLM call using the `Functional_Depth_Evaluation.md` skill to evaluate the C4 depth resolution.
- **Node 3 (ASR Coverage)**: Implement deterministic ASR mapping and contradiction penalty calculations. Introduce an LLM call using a new `Technology Specificity` skill to evaluate technology choices against ASRs.
- **Structured Outputs**: Use LangChain's `init_chat_model` for model initialization and `model.with_structured_output(PydanticSchema)` for type-safe, validated LLM responses — no manual JSON parsing needed.

## Capabilities

### New Capabilities
- `axis-functional-traceability`: Computes mapping coverage, depth of resolution (via LLM), and orphan penalties for functional requirements.
- `axis-asr-coverage`: Computes ASR mapping coverage, technology specificity (via LLM), and contradiction penalties for Architecturally Significant Requirements.

### Modified Capabilities
- 

## Impact

- `nodes/axis_functional.py` and `nodes/axis_asr.py` will be modified to contain the new deterministic logic and LLM integrations.
- New prompt templates `prompts/functional_depth.md` and `prompts/technology_specificity.md` will be created.
- A new Pydantic `BaseModel` (`LLMEvaluationResult`) will be defined for the structured output schema used by `with_structured_output`.
- A shared LLM helper utility will be added to initialize the model via `init_chat_model` and bind the structured output schema.
- Node 5 reporting will automatically pick up the real scores since it already rolls up the data deterministically from Phase 1.
