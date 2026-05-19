# Research Report: LangGraph State Channels and Reducers

This report documents the orchestration state design.

## 1. List Appending Reducers

### Decision
Use LangGraph's state reducer annotation pattern to define how list state variables merge updates. For example:
```python
from typing import Annotated
import operator

class RaaState(TypedDict):
    normalized_requirements: Annotated[list[dict], operator.add]
```

### Rationale
In LangGraph, writing to a key in a node overrides the previous value unless a reducer function is annotated. Appending lists ensures sequential nodes can accumulate outputs (like normalization adding to the list) without destroying previous inputs.

---

## 2. Gating and Validation Nodes

### Decision
Implement the gating check as an entry condition/validation step directly at the beginning of the graph execution before routing to the normalization node.

### Rationale
Halting early when `embeddings_ready` is false prevents executing subsequent nodes with invalid or missing vector caches.
