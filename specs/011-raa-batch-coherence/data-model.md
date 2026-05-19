# Data Model: Coherence Gate Schema

This document defines the schemas and state indicators for the coherence gate.

## 1. Batch Coherence Metadata

`Batch` TypedDict (in `raa/state/types.py`) extended with optional coherence fields:

```python
# Section 10 metadata (added by coherence gate)
coherence_score: float       # Average intra-batch cosine similarity
is_split: bool                # True when this batch was produced by a split
source_batch_id: int          # Original batch_id before split (None for unsplit)
```

## 2. Incoherent Batch Recording

When a split fails re-evaluation, an `IncoherentBatchRecord` is appended to state:

```python
@dataclass
class IncoherentBatchRecord:
    batch_id: int
    coherence_score: float
    reduced_confidence: bool
```

## 3. Requirement Embeddings

Every requirement payload in the batch's `requirements` list must carry an embedding vector under the key `embedding` (preferred) or `vector`. The coherence gate raises `ValueError` when neither key is present.
