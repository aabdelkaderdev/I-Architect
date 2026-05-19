# Research Notes: RAA Final Merge and Output

## Summary

This document researches and defines the core technical decisions for the final merge phase of the RAA pipeline, specifically focusing on the deterministic global merge algorithm, the LLM reconciliation pass for open questions, the programmatic C4 schema validation, the diagram manifest generation, and the file output/checkpoint archiving mechanics.

---

## 1. Global Deterministic Merge

### Decision
The global merge will reuse and scale the 4-step deterministic merge algorithm defined in `RAA_Plan.md` §13:
1. **Entity Deduplication (per type)**: Merge systems, containers, components, persons, and external systems. Canonical snake_case IDs are used as keys. Longest description wins; technology annotations are merged where available.
2. **Relationship Deduplication**: Key = `(source_id, target_id, interaction_type)`. Retain the diagram scope that is consistent with endpoint types, logging warning in case of scope mismatch.
3. **Coverage Union and Orphan Prevention**: Scan all losing fragments and candidate entities. Reject any component/container that is missing its parent entity.
4. **Tree Assembly**: Nest systems -> containers -> components, and distribute relationships into `context_relationships`, `container_relationships`, and `component_relationships` based on `diagram_scope`.

### Rationale
Using a deterministic algorithm rather than LLM synthesis ensures consistency, reproducibility, and prevents arbitrary structural deletions. Reusing the batch-level merge logic ensures code reuse and reliability.

---

## 2. LLM Reconciliation Pass

### Decision
A single, focused LLM call is executed using `llm_judge` from context.
- **Input**: The list of outstanding `open_questions` (e.g. `hierarchy_conflict`, `scope_conflict`, `coverage_gap`) and the partially merged model structure.
- **Prompt**: Highly structured, instructing the model to provide a resolution (such as selecting parent IDs or resolving scope/relationship conflicts) as a structured JSON object.
- **Validation**: The resolved output is programmatically merged back. If the LLM output is malformed or invalid, the pipeline logs a warning, retains the original conflicts in `open_questions`, and proceeds without crashing.

### Rationale
Using a targeted reconciliation pass ensures that we only use the LLM to make judgment calls on conflicts that deterministic rules cannot resolve, while keeping token counts low and avoiding any new structural errors.

---

## 3. Programmatic C4 Schema Validation

### Decision
Programmatic validation will be written in Python.
- **Checks**:
  1. Hierarchy nesting: Ensure all systems contain containers, which in turn contain components.
  2. No orphans: Ensure no component lacks a container parent, and no container lacks a system parent.
  3. ID Uniqueness: Verify that no ID is reused across system, container, component, person, or external system entities.
  4. Relationship Endpoint Existence: Verify that every relationship's `source_id` and `target_id` correspond to a valid entity in the model.
  5. Scope Alignment: Verify that every relationship's `diagram_scope` matches the C4 level of its endpoints:
     - `system` / `person` / `external_system` endpoints -> `context` scope.
     - `container` / `person` / `external_system` endpoints (with at least one container) -> `container` scope.
     - `component` / `container` / `external_system` endpoints (with at least one component) -> `component` scope.

### Rationale
Programmatic validation guarantees strict compliance with C4 requirements without LLM-based hallucination or non-deterministic pass/fail rates.

---

## 4. Diagram Manifest Generation

### Decision
The manifest is generated deterministically during the tree assembly phase of the final merge:
```python
manifest = []
for system in systems:
    manifest.append({
        "diagram_id": f"ctx-{system.id}",
        "diagram_type": "context",
        "focus_entity_id": system.id,
        "label": f"System Context — {system.label}"
    })
    manifest.append({
        "diagram_id": f"cnt-{system.id}",
        "diagram_type": "container",
        "focus_entity_id": system.id,
        "label": f"System Container — {system.label}"
    })
    for container in system.containers:
        manifest.append({
            "diagram_id": f"cmp-{container.id}",
            "diagram_type": "component",
            "focus_entity_id": container.id,
            "label": f"Component Diagram — {container.label}"
        })
```

### Rationale
This guarantees a 1:1 mapping between the model hierarchy and the work queue for the downstream AGA.

---

## 5. Output and Archiving Mechanics

### Decision
- **Output Path**: `projects/{project_name}/output/raa/arch_model.json`. The orchestrator passes the output directory path at invocation time.
- **Archive Path**: `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db`.
- **Ordering**:
  1. Complete global merge and reconciliation.
  2. Perform C4 programmatic validation.
  3. Write `arch_model.json`.
  4. Archive active checkpoint DB to archive folder.
  If steps 1-3 fail, checkpoint archiving is skipped, keeping the active checkpoint in place for troubleshooting.

### Rationale
Keeps checkpoint archiving safe, ensuring we only archive when we are 100% sure the final output is written and validated.
