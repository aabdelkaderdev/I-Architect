# Data Model: Final Architectural Output and Diagram Manifest

This document defines the final schemas produced by the RAA final merge and output node, including the C4-compliant hierarchical output and the diagram manifest.

---

## 1. Diagram Manifest Entry

```python
from typing import TypedDict, Literal

class DiagramManifestEntry(TypedDict):
    diagram_id: str         # Stable, canonical ID: e.g. "ctx-{system_id}", "cnt-{system_id}", "cmp-{container_id}"
    diagram_type: Literal["context", "container", "component"]
    focus_entity_id: str    # System ID for context/container diagrams, Container ID for component diagrams
    label: str              # Human-readable label (e.g. "System Context — payment_service")
```

---

## 2. Final Nested Architectural Model (ArchModel)

```python
from typing import TypedDict, Optional, Any
from .types import ArchSystem, ArchPerson, ArchExternalSystem, ArchPattern, OpenQuestion, ConfidenceRecord, DiagramManifestEntry

class ArchModel(TypedDict):
    systems: list[ArchSystem]                 # Systems with nested container/component hierarchy
    persons: list[ArchPerson]                 # Flat global list of human actors
    external_systems: list[ArchExternalSystem] # Flat global list of external systems
    patterns: list[ArchPattern]               # Globally selected patterns
    diagram_manifest: list[DiagramManifestEntry] # Deterministic work queue for AGA
    confidence_metadata: dict[str, ConfidenceRecord] # Keyed by entity ID
    open_questions: list[OpenQuestion]        # Residual unresolved conflicts/gaps
```

---

## 3. Entity Hierarchical Schemas

### ArchSystem
```python
class ArchSystem(TypedDict):
    id: str
    label: str
    description: str
    requirement_ids: list[str]
    source_fragment: Optional[str]
    confidence: Optional[float]
    context_relationships: list[Any]  # Context-level relationships
    containers: list[Any]             # Nested list of ArchContainer
```

### ArchContainer
```python
class ArchContainer(TypedDict):
    id: str
    label: str
    description: str
    technology: Optional[str]
    requirement_ids: list[str]
    source_fragment: Optional[str]
    confidence: Optional[float]
    parent_system_id: str
    container_relationships: list[Any] # Container-level relationships
    components: list[Any]              # Nested list of ArchComponent
```

### ArchComponent
```python
class ArchComponent(TypedDict):
    id: str
    label: str
    description: str
    technology: Optional[str]
    requirement_ids: list[str]
    source_fragment: Optional[str]
    confidence: Optional[float]
    parent_container_id: str
    component_relationships: list[Any] # Component-level relationships
```
