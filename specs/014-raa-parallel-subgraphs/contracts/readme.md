# RAA Parallel Subgraphs Contracts

## Send Routing

- The routing edge MUST return `list[Send]`, not a single `Send` and not a normal edge destination.
- Each `Send` MUST carry payload keys: `batch`, `batch_index`, `quality_weights`, `running_arch_model`, `bridge_requirements`, `strategy`, and `llm`.
- `llm` MUST be retrieved from the runtime config context (`config["context"]`), never from `RAAState`.
- Normal batches (`reduced_confidence` is falsy) emit three `Send` objects targeting `raa_a`, `raa_b`, `raa_c`.
- Reduced-confidence batches emit a single `Send` object targeting `raa_a`.

## Strategy Contracts

- `run_raa_a(payload)` — SAAM-first strategy. References: SAAM.md, Quality_Attributes.md, Entity_Extraction.md, Relationship_Extraction.md, Technology_Inference.md, C4.md, C4_Level_Mapping.md.
- `run_raa_b(payload)` — Pattern-driven strategy. References: Pattern_Selection.md, Quality_Attributes.md, Entity_Extraction.md, Relationship_Extraction.md, Technology_Inference.md, C4.md, C4_Level_Mapping.md.
- `run_raa_c(payload)` — Entity-driven strategy. References: Entity_Extraction.md, Relationship_Extraction.md, Technology_Inference.md, C4.md, C4_Level_Mapping.md.

## LLM Isolation

- Subgraphs consume LLM instances ONLY from `payload["llm"]`. No LLM objects in `RAAState` or returned node updates.
- Missing context LLM keys (`llm_raa_a`, `llm_raa_b`, `llm_raa_c`) MUST raise a clear configuration error.

## Output Contract

- Each subgraph returns `{"batch_outputs": {batch_index: [ArchFragment(...)]}}`.
- `merge_batch_outputs` (from `raa/state/channels.py`) combines fragments from all three strategies under the same batch index.

## Validation Hard Rules

- No container without a resolvable `parent_system_id` (in the same fragment or `running_arch_model`).
- No component without a resolvable `parent_container_id` (in the same fragment or `running_arch_model`).
- Every `ArchRelationship` MUST have `diagram_scope` ∈ {`context`, `container`, `component`}.
- `diagram_scope` MUST match the Section 12 endpoint-type table.
