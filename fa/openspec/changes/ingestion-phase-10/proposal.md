## Why

This change completes Phase 10 of the Data Ingestion & Requirement Filtering pipeline. It is needed to define the clear boundary between the ingestion pipeline and the orchestrator, specifying the handoff points and responsibilities. It also formalises the directory structure and design principles, establishing a solid foundation for integration with the broader architecture (ARLO, RAA, AGA, SA).

## What Changes

- **Orchestrator Interface Definition**: Specifies what inputs the orchestrator must provide (`file_path`, configs, LLM via `context=` kwarg, `db_path`, `thread_id`), how it invokes the compiled pipeline graph via `build_ingestion_graph(db_path).invoke(...)`, and what state it receives back.
- **Orchestrator Responsibilities**: Explicitly delegates infrastructure concerns (directory creation, config validation, file existence checks, error handling, checkpoint lifecycles) to the orchestrator.
- **Directory Layout Specification**: Defines the file and directory layout for both the `ingestion/` runtime code package and the `Skills/Ingestion/` resource bundle.
- **Design Principles**: Documents 8 core principles governing the module (e.g., separating deterministic ingestion from LLM filtering, library-native over abstraction, strict boundary ownership, and passthrough for clean input).
- **Integration Handoffs**: Clarifies how the pipeline feeds downstream consumers (ARLO, RAA, etc.) without having direct dependencies on them.

## Capabilities

### New Capabilities

- `orchestrator-interface`: Defines the boundary and invocation contract between the orchestrator and the ingestion graph.
- `directory-layout-and-design`: Specifies the complete directory layout and the design principles that govern the ingestion module.

### Modified Capabilities

- *(None)*

## Impact

- Provides a strict contract for the Orchestrator to integrate and run the `ingestion` module.
- Establishes the final file structure for the `ingestion` codebase and associated skills.
- Impacts how downstream consumers (ARLO) receive extracted requirements via the state output.
