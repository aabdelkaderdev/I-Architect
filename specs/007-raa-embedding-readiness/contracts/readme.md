# Embeddings DB Contract

The embedding databases must locate tables named `embeddings` with schema columns: `requirement_id`, `embedding`, `text_hash`, `model_name`.

- `requirement_id INTEGER PRIMARY KEY` — Integer requirement ID.
- `embedding BLOB NOT NULL` — Serialized 1024-element float32 vector.
- `text_hash TEXT NOT NULL` — SHA-256 hex digest of the embedded text for cache validation.
- `model_name TEXT NOT NULL` — FastEmbed model identifier for reproducibility.

All database connections must set journal mode to `WAL` before querying or writing. Non-ASR requirement descriptions must be embedded using FastEmbed `mixedbread-ai/mxbai-embed-large-v1` to ensure shared dimensions.
