# Quickstart: RAA Final Merge and Output

This guide provides snippets showing the implementation details for C4 schema validation, diagram manifest generation, and checkpoint archiving.

---

## 1. C4 Hierarchical Validation and Diagram Manifest Generation

The following snippet shows how the final merge node validates the tree and builds the manifest:

```python
from typing import Dict, List, Any

def validate_and_generate_manifest(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Track all entity IDs and their levels
    seen_ids: Dict[str, str] = {}  # ID -> Level ("system", "container", "component", etc.)
    manifest: List[Dict[str, Any]] = []
    
    # 1. Populate systems, containers, components and register IDs
    for system in model.get("systems", []):
        sys_id = system["id"]
        if sys_id in seen_ids:
            raise ValueError(f"Duplicate entity ID found: {sys_id}")
        seen_ids[sys_id] = "system"
        
        # Add to manifest
        manifest.append({
            "diagram_id": f"ctx-{sys_id}",
            "diagram_type": "context",
            "focus_entity_id": sys_id,
            "label": f"System Context — {system['label']}"
        })
        manifest.append({
            "diagram_id": f"cnt-{sys_id}",
            "diagram_type": "container",
            "focus_entity_id": sys_id,
            "label": f"System Container — {system['label']}"
        })
        
        for container in system.get("containers", []):
            cnt_id = container["id"]
            if cnt_id in seen_ids:
                raise ValueError(f"Duplicate entity ID found: {cnt_id}")
            if container["parent_system_id"] != sys_id:
                raise ValueError(f"Container parent mismatch: {cnt_id}")
            seen_ids[cnt_id] = "container"
            
            manifest.append({
                "diagram_id": f"cmp-{cnt_id}",
                "diagram_type": "component",
                "focus_entity_id": cnt_id,
                "label": f"Component Diagram — {container['label']}"
            })
            
            for component in container.get("components", []):
                cmp_id = component["id"]
                if cmp_id in seen_ids:
                    raise ValueError(f"Duplicate entity ID found: {cmp_id}")
                if component["parent_container_id"] != cnt_id:
                    raise ValueError(f"Component parent mismatch: {cmp_id}")
                seen_ids[cmp_id] = "component"
                
    # 2. Register global entities (persons, external systems)
    for person in model.get("persons", []):
        p_id = person["id"]
        if p_id in seen_ids:
            raise ValueError(f"Duplicate entity ID found: {p_id}")
        seen_ids[p_id] = "person"
        
    for ext_sys in model.get("external_systems", []):
        ext_id = ext_sys["id"]
        if ext_id in seen_ids:
            raise ValueError(f"Duplicate entity ID found: {ext_id}")
        seen_ids[ext_id] = "external_system"
        
    return manifest
```

---

## 2. Checkpoint Archiving

```python
import os
import shutil
import logging

def archive_checkpoint(db_path: str, project_name: str, thread_id: str):
    if not os.path.exists(db_path):
        logging.warning(f"Checkpoint DB not found at: {db_path}")
        return
        
    archive_dir = f"projects/{project_name}/checkpoints/archive/{thread_id}"
    os.makedirs(archive_dir, exist_ok=True)
    archive_path = os.path.join(archive_dir, "raa_graph.db")
    
    try:
        shutil.move(db_path, archive_path)
        logging.info(f"Successfully archived active checkpoint to: {archive_path}")
    except Exception as e:
        logging.error(f"Failed to archive checkpoint DB: {e}")
```
