# Research Report: Hierarchical C4 Tree Serialization and Formatting

This report documents formatting layouts and determinism rules.

## 1. Indented Tree Format

### Decision
Represent the consolidated C4 elements using a nested indent tree structure:
```text
System: [system_id] - [name] ([description])
  Container: [container_id] - [name] ([description])
    Component: [component_id] - [name] ([description])
```

### Rationale
Compared to a raw JSON printout, indented lists use far fewer prompt tokens and are parsed with higher accuracy by context-constrained models.

---

## 2. Determinism and Sorting

### Decision
Sort all entities (systems, containers, components) and relationships lexicographically by their ID/fields at each tree traversal level.

### Rationale
This prevents differences in memory address ordering or database sequences from altering the serialized prompt string, adhering to the pipeline determinism principle.
