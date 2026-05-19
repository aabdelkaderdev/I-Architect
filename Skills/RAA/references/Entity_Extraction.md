# Entity Extraction — Skill Reference

## 1. Purpose

Guidelines for extracting C4 entities (system, container, component, person, external system) from normalized requirements. Applied by all three RAA subgraphs (A, B, C) during batch analysis. References C4.md for type definitions.

## 2. Input

- **Current batch requirements** (normalized): `list[dict]` with keys `id`, `text`, `is_asr`, `quality_attributes`, `condition_text`.
- **Running architecture model** (`running_arch_model`): the accumulated `ArchModel` from prior batches, serialized into the subgraph prompt as hard constraints.
- **ARLO quality weights**: `dict[str, int]` for quality-attribute-informed entity classification.

## 3. Normative rules

1. **Hierarchy constraint (orphan prevention):** A subgraph must never propose a component without also ensuring a container is present (either in the same fragment or in `running_arch_model`). A subgraph must never propose a container without also ensuring a system is present. This prevents orphan entities from entering the merge pipeline.
2. **Canonical ID derivation:** All entity IDs must be lowercase, snake_case, and derived from the entity's primary noun phrase (e.g., "Payment Gateway System" → `payment_gateway`). IDs must be unique within their entity type across the fragment.
3. **Parent-child boundary assignment:** Every container must carry `parent_system_id`; every component must carry `parent_container_id`. The parent must resolve to an entity in the same fragment or in the running architecture model.
4. **Technology annotation threshold:** Assign technology when the requirement text contains explicit technology signals (framework names, database engines, protocol names). Leave as `null` when no signal exists — never guess.
5. **Level discipline:** Do not extract a component when a container-level entity suffices. Do not extract a container when a system-level entity suffices. Default to the coarser level when granularity is ambiguous.
6. **Person and external system extraction:** Extract person actors when requirements mention human roles or users. Extract external systems when requirements mention third-party services or integrations.
7. **Requirement traceability:** Every extracted entity must carry the `requirement_ids` that justify its existence.

## 4. Decision guidelines

- **System introduction:** Introduce a new system when a set of requirements describes a distinct bounded context not already covered by an existing system.
- **Container introduction:** Introduce a new container when a requirement describes a distinct runtime-deployable unit (separate process, database, or service).
- **Component introduction:** Introduce a component when a requirement describes a distinct code-level responsibility within a container.
- **Ambiguous requirements:** When a requirement is too vague to assign to any entity, record it in the fragment's `rationale.gaps`.
- **Naming:** Prefer domain language from the requirement text. Avoid generic names like "service" or "handler" unless the requirement provides no more specific term.

## 5. Output schema

The subgraph outputs an `ArchFragment` containing:
- `systems: list[ArchSystem]` — systems proposed by this subgraph, each with its `context_relationships` and nested `containers`.
- `containers: list[ArchContainer]` — containers with `parent_system_id`, `container_relationships`, and nested `components`.
- `components: list[ArchComponent]` — components with `parent_container_id` and `component_relationships`.
- `persons: list[ArchPerson]` — person actors.
- `external_systems: list[ArchExternalSystem]` — external system actors.

See `raa/state/types.py` for the complete dataclass field definitions.

## 6. Error cases

| Situation | Handling |
|-----------|----------|
| Requirement mentions a component without any container context | Propose a conservative container to host it; name the container after the component's domain |
| Requirement's implied technology conflicts with an existing entity's technology annotation | Record as a gap in `rationale.gaps`; do not overwrite existing model |
| No entities can be extracted from the batch | Return an empty fragment with `rationale.gaps` listing all batch requirement IDs |
| Entity name collision with running_arch_model | Do not rename existing entities; propose the new entity with a disambiguated ID suffix |
| Ambiguous entity level (e.g., could be a container or a component) | Default to the coarser level (container) and record the ambiguity in `rationale.confidence_notes` |

## 7. Examples

**Worked example from requirements dataset:**

Requirements R12 and R13:
- R12: "The system shall process payments through a payment gateway."
- R13: "A payment worker module must handle asynchronous payment confirmations."

Extracted entities:
- `ArchSystem(id='payment_gateway', label='Payment Gateway', description='Processes payments through external payment provider')`
- `ArchContainer(id='payment_worker', label='Payment Worker', description='Handles asynchronous payment confirmations', parent_system_id='payment_gateway', technology='Celery')`

The proposed `payment_worker` is a container-level entity because requirements describe it as a deployable unit. No component is proposed since no sub-container responsibility is implied.
