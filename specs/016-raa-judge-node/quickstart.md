# Quickstart: RAA Per-Batch Judge Node

This guide provides examples of how the deterministic merge and residual scan algorithms process the candidate fragments.

## 1. Entity Deduplication and Hierarchy Conflict Check

```python
def merge_entities(primary: list[dict], residual: list[dict], open_questions: list[dict], fragment_name: str) -> list[dict]:
    merged = {entity["id"]: dict(entity) for entity in primary}
    
    for entity in residual:
        eid = entity["id"]
        if eid in merged:
            # Check for hierarchy conflict on containers
            if "parent_system_id" in entity:
                if entity["parent_system_id"] != merged[eid].get("parent_system_id"):
                    open_questions.append({
                        "question_type": "hierarchy_conflict",
                        "entity_id": eid,
                        "description": "Conflicting parent system IDs during deduplication.",
                        "involved_fragments": ["primary", fragment_name],
                        "parent_id_conflict": {
                            "primary": merged[eid].get("parent_system_id"),
                            fragment_name: entity["parent_system_id"]
                        }
                    })
            # Prefer longer descriptions
            if len(entity.get("description", "")) > len(merged[eid].get("description", "")):
                merged[eid]["description"] = entity["description"]
        else:
            # Orphan check required before adding
            pass  
            
    return list(merged.values())
```

## 2. Orphan Protection during Coverage Union

```python
def check_orphan(entity: dict, primary_container_ids: set) -> bool:
    if "parent_container_id" in entity:
        if entity["parent_container_id"] not in primary_container_ids:
            return True
    return False
```
