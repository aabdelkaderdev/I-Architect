# Research Report: Deterministic Architecture Merge

This report documents the merge algorithm decisions for the Judge Node.

## 1. Programmatic Python Merge Algorithm

### Decision
The 4-step merge algorithm (Entity Deduplication, Relationship Deduplication, Coverage Union, Tree Assembly) will be written as deterministic Python functions utilizing dictionary lookups keyed by canonical entity ID. The LLM (`llm_judge`) will only be used for SAAM scoring of the initial fragments.

### Rationale
Relying on an LLM to merge complex JSON hierarchies routinely results in hallucinated structures, lost attributes, and orphaned nested elements. Programmatic merging guarantees that canonical IDs match, scopes are preserved, and orphans are strictly rejected according to the project's C4 compliance mandate.

---

## 2. Orphan Component Protection

### Decision
During the residual scan (Coverage Union step), if a losing fragment proposes a valid component but its specified `parent_container_id` is missing from the primary selected fragment (and `running_arch_model`), the merge script explicitly rejects the component. Instead, it generates a dictionary entry logged to the `open_questions` state with the type `coverage_gap`.

### Rationale
This prevents structurally broken data from corrupting the C4 hierarchical tree, ensuring the output remains compatible with AGA down the line.
