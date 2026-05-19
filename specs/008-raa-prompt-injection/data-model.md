# Data Model: Prompt Registry Mappings

This document defines the schemas and constants mapping nodes to tags.

## 1. Tag Mapping Matrix

```python
NODE_TAG_REGISTRY = {
    "entity_extraction": ["c4:levels", "c4:notation"],
    "relationship_extraction": ["c4:notation", "c4:technology"],
    "pattern_selection": ["c4:levels"],
    "saam_tradeoff": ["saam:steps", "saam:scenarios"],
    "final_merge": ["c4:levels", "c4:notation", "c4:technology"]
}
```

---

## 2. File Translation Schema

Tags are translated to filenames according to the following logic:

```text
Tag: "c4:levels"  -->  File: "raa/prompts/excerpts/c4_levels.txt"
Tag: "saam:steps" -->  File: "raa/prompts/excerpts/saam_steps.txt"
```

The lookup replaces `:` with `_` and appends `.txt`.
