# Data Model: Requirement Normalization Types

This document defines the type schemas involved in the normalization step.

## 1. Input Datatypes (ARLO Outputs)

### ASR/Non-ASR Dictionary
```python
class ArloRawRequirement(TypedDict):
    id: int
    is_architecturally_significant: bool
    quality_attributes: list[str]  # Might be absent in non-ASRs
    condition_text: str            # Might be absent in non-ASRs
```

### Parent requirements
```python
requirements: dict[str, str]  # Map of ID strings (e.g. "R1") to text descriptions
```

---

## 2. Output Datatype (Unified Requirement)

All downstream nodes receive the normalized structure defined as a TypedDict:

```python
from typing import TypedDict, Optional

class UnifiedRequirement(TypedDict):
    id: str                         # E.g. "R1"
    text: str                       # Resolved description
    is_asr: bool                    # Renamed from is_architecturally_significant
    quality_attributes: list[str]   # Defaults to empty list []
    condition_text: Optional[str]   # Defaults to None
```
