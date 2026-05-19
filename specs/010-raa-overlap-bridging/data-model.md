# Data Model: Overlap Bridging Registry

This document defines the schema of the overlap bridge registry and the state channel it writes to.

## 1. State Channel

The `bridge_requirements` channel in `RAAState` (defined in `raa/state/channels.py`) is an overwrite channel:

```python
bridge_requirements: dict[tuple, list[str]]
```

- **Key**: A stable-sorted tuple of adjacent batch `group_id` values, e.g. `(1, 3)`.
- **Value**: List of selected bridge requirement IDs as strings, e.g. `["R10", "R14"]` (1 to 3 entries).

## 2. Pair Key Format

Pair keys use the adjacent batch group IDs in stable sorted order (lexicographically or numerically ascending):

```python
def _bridge_pair_key(left: dict, right: dict) -> tuple:
    ids = (left["group_id"], right["group_id"])
    return tuple(sorted(ids))
```

Example: batches with `group_id=1` and `group_id=3` produce key `(1, 3)`.

## 3. Batch Injection

Selected bridge requirement payloads are injected into **both** adjacent batches:
- Appended to `batch["requirements"]` (full normalized payloads).
- Appended to `batch["requirement_ids"]` (string IDs).
- Recorded in `batch["similarity_scores"]` with their bridge score as the similarity value.
