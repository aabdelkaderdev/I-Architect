# Data Model: Serialized Constraint payload

This document defines the serialized output schemas.

## 1. Constraint Payload Model

```python
from typing import TypedDict

class SerializedConstraints(TypedDict):
    constraint_text: str  # Prefixed C4 tree structure
```
