## Why

The Requirement Filtering Agent (RFA) acts as the gatekeeper between raw ingested text and ARLO. This change defines what the RFA asks the LLM to do and what it expects in return, establishing the normative Signal and Noise classification criteria (grounded in IEEE 830), the prompt template, and the structured output schemas. This ensures only relevant architectural requirements are processed downstream.

## What Changes

- Define the Signal and Noise classification criteria based on IEEE 830 and project taxonomy.
- Create the `filter_classification.md` prompt template for the RFA.
- Define Pydantic models `FilteredRequirement` and `FilterBatch` for the structured output schema.
- Specify the LLM invocation method and retry behavior for structured outputs.

## Capabilities

### New Capabilities
- `rfa-prompt`: Defines the prompt specification, classification taxonomy (Signal vs Noise), and structured output schemas for the Requirement Filtering Agent.

### Modified Capabilities
- none

## Impact

- `ingestion/prompts/filter_classification.md`: New file containing the system and human messages for the RFA.
- Pydantic models to be added for structured output validation.
- Sets the foundation for Phase 8 which will use these schemas and prompts for batching and report generation.
