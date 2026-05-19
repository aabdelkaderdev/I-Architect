# Data Model: Embedding Databases Schema

This document details the SQLite database schemas used to persist embeddings.

## 1. SQLite Table Schema

Both `asr_embeddings.db` and `non_asr_embeddings.db` contain a single table named `embeddings` with the following structure:

```sql
CREATE TABLE IF NOT EXISTS embeddings (
    requirement_id INTEGER PRIMARY KEY,
    embedding BLOB NOT NULL,
    text_hash TEXT NOT NULL,
    model_name TEXT NOT NULL
);
```

### Column Descriptions
- `requirement_id`: Integer requirement ID derived from normalized requirement IDs (e.g. `"R12"` → `12`).
- `embedding`: A binary BLOB containing the 1024 float32 values serialized via `struct.pack`.
- `text_hash`: SHA-256 hex digest of the text that was embedded. Used for cache-integrity checks on rerun.
- `model_name`: The FastEmbed model used to generate the embedding (e.g. `"mixedbread-ai/mxbai-embed-large-v1"`).

---
## 2. Model Parameters

- **Embedding Model**: `mixedbread-ai/mxbai-embed-large-v1`
- **Output Dimensions**: 1024
- **Precision**: 32-bit floats
- **Cache Integrity**: SHA-256 hash of requirement text stored in `text_hash`
