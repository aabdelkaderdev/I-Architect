# Data Model: Judge Conflict Records and Confidence Metadata

This document defines the schemas used by the Judge node to record merge conflicts and track confidence scores.

## 1. Open Questions (Conflicts & Gaps)

```python
from typing import TypedDict, Literal, Optional

class OpenQuestion(TypedDict):
    question_type: Literal["hierarchy_conflict", "scope_conflict", "coverage_gap"]
    entity_id: str
    description: str
    involved_fragments: list[str]  # e.g. ["raa_a", "raa_b"]
    parent_id_conflict: Optional[dict[str, str]]  # e.g. {"raa_a": "sys_1", "raa_b": "sys_2"}
    scope_conflict: Optional[dict[str, str]]      # e.g. {"raa_b": "system", "raa_c": "container"}
```

---

## 2. Confidence Metadata

```python
from typing import TypedDict

class ConfidenceRecord(TypedDict):
    reduced_confidence: bool
    batch_index: int
    base_saam_score: float
    weighted_score: float  # Multiplied by 0.5 if reduced_confidence == True
```
