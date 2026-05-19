# Research Report: Embedding Verification and WAL Concurrency

This report details design decisions for RAA preparation and database handling.

## 1. Concurrency Management with SQLite

### Decision
Both `asr_embeddings.db` and `non_asr_embeddings.db` must be initialized/opened with SQLite's Write-Ahead Logging (WAL) journal mode.

### Rationale
During LangGraph run, multiple subgraphs read embeddings in parallel. Standard rollback journals lock the database on writes. By executing:
```sql
PRAGMA journal_mode=WAL;
```
SQLite allows concurrent readers to proceed even while writes are occurring, avoiding query blockages or timeouts.

### Alternatives Considered
- **Default Rollback Journal**: Rejected because concurrent execution of parallel strategies (RAA-A, RAA-B, RAA-C) could result in locking exceptions.

---

## 2. Embedding Generator

### Decision
Use FastEmbed library (`fastembed`) with model `mixedbread-ai/mxbai-embed-large-v1` running locally.

### Rationale
This matches the exact vector dimensions (1024) and embedding model used in the ARLO step. Using different models would prevent meaningful cosine similarity comparisons.
