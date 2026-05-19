# Quickstart: RAA Preparation & Embeddings

This guide explains how to connect to the SQLite embedding databases and check readiness.

## 1. Opening Database in WAL Mode

When opening connection to the SQLite files, enable WAL mode:

```python
import sqlite3

def get_db_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn
```

## 2. Reading and Writing Vectors

Vectors are stored as binary BLOBs. To convert back and forth between float lists and binary data:

```python
import numpy as np

def serialize_vector(vector: list[float]) -> bytes:
    return np.array(vector, dtype=np.float32).tobytes()

def deserialize_vector(blob: bytes) -> list[float]:
    return np.frombuffer(blob, dtype=np.float32).tolist()
```

## 3. Running Verification Node

The preparation node reads the graph state containing the normalized requirements list:

```python
def check_embeddings_readiness(state: dict) -> dict:
    # 1. Verify ASR embeddings in db
    # 2. Check cached non-ASRs; embed missing ones
    # 3. Write missing non-ASRs to non_asr_embeddings.db
    return {
        "embeddings_ready": True
    }
```
