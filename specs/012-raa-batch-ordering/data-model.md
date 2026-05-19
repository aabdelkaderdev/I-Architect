# Data Model: Batch Queue Sorting Metadata

This document defines the schemas of sorting configurations.

## 1. Sorting Metadata Schema

Batches in the queue are enriched with sorting metadata:

```python
from typing import TypedDict

class SortingMetadata(TypedDict, total=False):
    score: float             # Calculated score under active strategy
    strategy: str            # "risk_first", "asr_count", or "quality_weight"
    tie_breaker: str         # Lexicographically sorted group ID
```

## 2. Batch Extension

`Batch` in `raa/state/types.py` includes an optional `sorting_metadata` field:

```python
sorting_metadata: SortingMetadata
```

## 3. Pipeline Parameter

`RAAState` in `raa/state/channels.py` includes the optional pipeline parameter:

```python
batch_ordering_strategy: str   # "risk_first" (default), "asr_count", or "quality_weight"
```

The node reads this parameter to select the active ordering strategy. Missing or invalid values fall back to `"risk_first"`.
