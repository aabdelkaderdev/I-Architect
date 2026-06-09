## Why

The Architecture Generation Agent (AGA) requires foundational state structures and configuration classes before any logic or agent graphs can be implemented. This phase establishes the core directory scaffold and data types (TypedDicts and Pydantic models) following the established ARLO and RAA patterns, ensuring consistency across the pipeline and robust validation for the orchestrator-provided inputs.

## What Changes

- Create the complete folder scaffold for the AGA module matching the ARLO/RAA pattern.
- Create `aga/state/config.py` defining the `AGAConfig` runtime configuration dataclass.
- Create `aga/state/schemas.py` defining the core LangGraph state TypedDicts (`AGAInput`, `AGAOutput`, `AGAState`).
- Create `aga/state/models.py` containing Pydantic models for internal state tracking (`DiagramSpec`, `CompletedDiagram`, `FailedDiagram`, `SessionReport`).
- Create Pydantic models in `models.py` to validate the incoming flat JSON architecture model (`ArchModel`, `Entity`, `Relationship`), without using strict validation (`extra="forbid"`).

## Capabilities

### New Capabilities
- `aga-state-management`: Defines the complete state, configuration, and structural foundation for the Architecture Generation Agent.

### Modified Capabilities

## Impact

- Establishes the foundational types and imports for all subsequent AGA phases.
- Imposes an input contract via Pydantic models for the orchestrator providing the `arch_model` dictionary.
