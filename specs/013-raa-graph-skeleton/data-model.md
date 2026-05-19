# Data Model: RAA Graph State Schema

This feature reuses the authoritative `RAAState` TypedDict defined in `raa/state/channels.py`. No duplicate or graph-only state schema is introduced.

## Authoritative State Definition

See `raa/state/channels.py` for the full `RAAState` TypedDict with all channels, reducers, and documentation.

### Channel Summary

**Single-writer (overwrite) channels:**
- `batch_queue: list[Batch]`
- `batch_cursor: int`
- `batch_ordering_strategy: str`
- `running_arch_model: ArchModel`
- `bridge_requirements: dict[tuple, list[str]]`
- `embeddings_ready: bool`

**Multi-writer (append reducer via `operator.add`) channels:**
- `open_questions: Annotated[list[OpenQuestion], add]`
- `incoherent_batches: Annotated[list[IncoherentBatchRecord], add]`

**Multi-writer (dict-merge reducer) channels:**
- `batch_outputs: Annotated[dict[int, list[ArchFragment]], merge_batch_outputs]`
- `best_batch_output: Annotated[dict[int, ArchFragment], merge_best_batch_output]`

**Reused ARLO channels:**
- `asrs: list[dict]`
- `non_asr: list[dict]`
- `condition_groups: list[dict]`
- `quality_weights: dict[str, int]`
