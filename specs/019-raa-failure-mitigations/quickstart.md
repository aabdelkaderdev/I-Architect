# Quickstart: Implementing Failure Mitigations

This quickstart provides code snippets and implementation patterns for the startup safety checks, database WAL mode, cache integrity checks, and final merge desync verification.

---

## 1. Opening Connections in WAL and Read-Only Mode

To ensure concurrent safety, always open connections with `journal_mode=WAL` and use `mode=ro` when reading:

```python
import sqlite3
import logging

logger = logging.getLogger(__name__)

def open_embedding_db(db_path: str, read_only: bool = False) -> sqlite3.Connection:
    """Connect to SQLite database in WAL mode, optionally read-only."""
    if read_only:
        # Open in URI read-only mode to prevent write locks and accidental mutations
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    else:
        conn = sqlite3.connect(db_path)
        
    try:
        # Enable Write-Ahead Logging (WAL)
        conn.execute("PRAGMA journal_mode=WAL;")
    except sqlite3.OperationalError as e:
        logger.warning("Could not set WAL mode on %s: %s", db_path, e)
        
    return conn
```

---

## 2. Startup Embedding Verification and Rebuild

Implementation snippet for `prepare_embeddings` inside `raa/nodes/preparation.py`:

```python
from pathlib import Path
import sqlite3

def prepare_embeddings(state: dict) -> dict:
    if state.get("embeddings_ready", False):
        return {}  # Bypass on resume
        
    asr_db_path = "/path/to/asr_embeddings.db"
    non_asr_db_path = "/path/to/non_asr_embeddings.db"
    
    # 1. ASR DB Startup Check
    if not Path(asr_db_path).exists():
        raise RuntimeError("ASR embedding database is missing or corrupt. Please re-run ARLO.")
        
    try:
        with open_embedding_db(asr_db_path, read_only=True) as conn:
            # Query active IDs
            existing_ids = {row[0] for row in conn.execute("SELECT requirement_id FROM embeddings")}
    except sqlite3.DatabaseError as e:
        raise RuntimeError(f"ASR embedding database is corrupt: {e}. Please re-run ARLO.") from e
        
    for req in state.get("asrs", []):
        if req.id not in existing_ids:
            raise RuntimeError(f"ASR requirement ID '{req.id}' is missing from ASR database.")

    # 2. Non-ASR DB Startup & Rebuild Check
    try:
        with open_embedding_db(non_asr_db_path) as conn:
            conn.execute("SELECT 1 FROM embeddings LIMIT 1")
    except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
        logger.warning("Non-ASR embedding DB is corrupt or missing: %s. Rebuilding from scratch.", e)
        # Delete corrupted file
        Path(non_asr_db_path).unlink(missing_ok=True)
        # Recreate DB schema
        with open_embedding_db(non_asr_db_path) as conn:
            conn.execute("""
                CREATE TABLE embeddings (
                    requirement_id INTEGER PRIMARY KEY,
                    embedding BLOB NOT NULL,
                    text_hash TEXT NOT NULL,
                    model_name TEXT NOT NULL
                );
            """)

    # 3. Hash Cache Verification & Stale Checks
    # Look up existing cached embeddings and hashes, compare, recompute if mismatch.
    # ... (see contracts and data-model details)
    
    return {"embeddings_ready": True}
```

---

## 3. Final Merge Desync Detection

Implementation snippet for `final_merge` inside `raa/nodes/final_merge.py`:

```python
def final_merge(state: dict, config: dict | None = None) -> dict:
    batch_queue = state.get("batch_queue", [])
    best_batch_output = state.get("best_batch_output", {})
    
    # 1. Desync Verification
    expected_indices = set(range(len(batch_queue)))
    actual_indices = set(best_batch_output.keys())
    missing_indices = expected_indices - actual_indices
    
    # Check for empty or invalid batch fragments
    for idx, fragment in best_batch_output.items():
        if fragment is None or (not fragment.systems and not fragment.persons):
            missing_indices.add(idx)
            
    if missing_indices:
        min_missing = min(missing_indices)
        logger.warning(
            "Desync detected: missing/corrupt outputs for batch indices %s. "
            "Redirecting batch_cursor to %s for targeted rerun.", 
            missing_indices, min_missing
        )
        # Roll back batch cursor to trigger re-run
        return {
            "batch_cursor": min_missing
        }
        # Note: caller or graph routing will handle the loop back
        
    # Proceed with normal global merge ...
```
