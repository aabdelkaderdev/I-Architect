# Interface Contracts: Failure Mode Mitigations

This document outlines the strict behavioral contracts, input/output structures, and error models for the nodes involved in failure mitigation.

---

## 1. Startup Validation Contract (`prepare_embeddings`)

### Input state Channels
- `asrs`: `list[Requirement]` (ASR requirements)
- `non_asr`: `list[Requirement]` (Non-ASR requirements)
- `embeddings_ready`: `bool`

### Connection Configuration
- `asr_embeddings.db`: Path resolved from the orchestrator configuration. Opened in WAL read-only mode (`mode=ro`).
- `non_asr_embeddings.db`: Path resolved from orchestrator configuration. Opened in WAL write-mode.

### Validation Invariants
1. If `embeddings_ready` is `True`, bypass all verification and processing (Fast-path resume).
2. If `asr_embeddings.db` is missing or connection fails, raise `RuntimeError("ASR embedding database is missing or corrupt. Please re-run ARLO.")`.
3. If any requirement in `asrs` has its ID missing from `asr_embeddings.db`, raise `RuntimeError("ASR requirement ID {req_id} missing from ASR database.")`.
4. If `non_asr_embeddings.db` is corrupt (raises `sqlite3.DatabaseError` on open or select), catch the exception, delete the database file, recreate it, and write the schema.
5. If the computed `text_hash` of a requirement in `non_asr` differs from the database `text_hash`, log a warning: `"Stale embedding detected for requirement ID {req_id}. Recomputing."` and overwrite the database entry.

### Output State Update
```json
{
  "embeddings_ready": true
}
```

---

## 2. Final Merge desync Contract (`final_merge`)

### Input State Channels
- `batch_queue`: `list[dict[str, Any]]`
- `best_batch_output`: `dict[int, ArchFragment]`
- `batch_cursor`: `int`

### Verification Invariant
Before executing reconciliation or writing to `arch_model.json`, the node checks:
```python
expected_indices = set(range(len(batch_queue)))
actual_indices = set(best_batch_output.keys())
missing_indices = expected_indices - actual_indices
```
1. If `missing_indices` is not empty:
   - Log a warning: `"Desync detected: missing batch outputs for indices: {missing_indices}"`.
   - Identify the minimum missing index: `min_missing = min(missing_indices)`.
   - Update `batch_cursor` to `min_missing`.
   - Raise a recoverable `ValueError` (or conditional loop back to execution node) to trigger targeted re-runs.
2. If any fragment in `best_batch_output` is corrupted (e.g. `None` or carries empty elements when expected):
   - Treat the index as missing, roll back `batch_cursor`, and raise the error.

### Success Output State Update
```json
{
  "running_arch_model": "<ArchModel instance>",
  "open_questions": "<unresolved reconciliations>"
}
```

---

## 3. Concurrency Database Contract

To support parallel reads across subgraphs:
1. **Pragma Invariant**: Every opened connection must immediately run `PRAGMA journal_mode=WAL;`.
2. **Read-Only Invariant**: All RAA subgraph batch nodes (e.g. `batch_construction`) MUST connect to SQLite databases using read-only URIs:
   ```python
   sqlite3.connect("file:/path/to/db?mode=ro", uri=True)
   ```
3. **Write Isolation**: ARLO and RAA must never write concurrently to the same database. ARLO writes `asr_embeddings.db` synchronously to completion before RAA starts. RAA writes `non_asr_embeddings.db` synchronously during the startup `prepare_embeddings` node before spawning batch subgraphs.
