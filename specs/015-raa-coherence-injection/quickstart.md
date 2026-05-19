# Quickstart: RAA Cross-Batch Coherence Injection

This guide demonstrates how to serialize a hierarchical architecture model into formatted text constraints.

## 1. Hierarchical Serialization

```python
def serialize_arch_model(model: dict) -> str:
    lines = []
    
    # Sort and traverse systems
    systems = sorted(model.get("systems", []), key=lambda x: x["id"])
    for system in systems:
        lines.append(f"System: {system['id']} - {system['name']} ({system.get('description', '')})")
        
        # Sort and traverse containers
        containers = sorted(system.get("containers", []), key=lambda x: x["id"])
        for container in containers:
            lines.append(f"  Container: {container['id']} - {container['name']} ({container.get('description', '')})")
            
            # Sort and traverse components
            components = sorted(container.get("components", []), key=lambda x: x["id"])
            for component in components:
                lines.append(f"    Component: {component['id']} - {component['name']} ({component.get('description', '')})")
                
    return "\n".join(lines)
```

## 2. Constraint Prefix Injection

```python
WARNING_PREFIX = (
    "The following components and relationships are already part of the architecture model. "
    "You must be consistent with them. Do not rename, restructure, or contradict any listed entity or relationship."
)

def build_prompt_constraints(model: dict) -> str:
    serialized = serialize_arch_model(model)
    if not serialized.strip():
        return ""
    return f"{WARNING_PREFIX}\n\n{serialized}"
```
