# Deferred Work Items

## Deferred from: code review of 2-4-conservative-entity-deduplication-and-c4-boundary-grouping.md (2026-05-23)

- **SQLite cache overwrite hazard due to primary key design**: The cache DB uses `req_id TEXT PRIMARY KEY`. Storing an entity embedding under its ID will overwrite any requirement embedding sharing that ID, and overwrites past descriptions for the same ID.
- **Inefficient non-batched embedding calls**: Embedding generation makes sequential individual calls (`model.embed([desc])`) on cache misses rather than batching them.
