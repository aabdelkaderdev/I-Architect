# Batch Construction Contracts

The batch construction node must consume ARLO condition groups and output a list of `Batch` payloads in `batch_queue`.

- **Threshold**: Non-ASR candidates must have cosine `similarity >= 0.65`.
- **Cap**: Maximum 10 selected non-ASR candidates per batch.
- **Payloads**: Each batch stores full normalized ASR and non-ASR requirement payloads in `requirements`.
- **Similarity scores**: Per-requirement similarity scores stored in `similarity_scores`.
- **Centroid**: L2-normalized element-wise average of ASR embeddings. Fallback re-embeds `nominal_condition` when no ASR embeddings loadable.
