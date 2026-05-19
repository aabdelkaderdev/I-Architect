# Data Model: Batch Payload Schema

This document defines the schemas of the batch construction outputs.

## 1. Batch Payload Schema

Each condition group produces a single `Batch` with the following fields:

```python
from typing import TypedDict

class Batch(TypedDict, total=False):
    batch_id: int
    group_id: int
    requirement_ids: list[str]
    group_centroid: list[float] | None
    reduced_confidence: bool
    cluster: list[str]
    requirements: list[dict]
    similarity_scores: dict[str, float]
    non_asr_candidates: list[dict]
```

### Field Descriptions

- `group_id`: ARLO condition group identifier.
- `cluster`: List of condition group labels or cluster membership tags.
- `centroid` (via `group_centroid`): 1024-element centroid vector for this group.
- `requirements`: Full normalized ASR and non-ASR requirement payloads (dicts, not just IDs).
- `similarity_scores`: Per-requirement cosine similarity scores keyed by requirement ID.
- `non_asr_candidates`: Non-ASR candidate payloads with `id`, `text`, and `similarity`.
