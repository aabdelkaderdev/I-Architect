# Batch Queue Ordering Contracts

The queue ordering node must sort the batch execution queue.

- **Strategies**: `risk_first` (default), `asr_count`, `quality_weight`.
- **risk_first**: max risk priority per quality attribute (Security=4, Reliability=3, Performance=2, Usability=1, others=0).
- **asr_count**: count of architecturally significant requirements only (no non-ASR/bridge).
- **quality_weight**: sum of ARLO `quality_weights` for ASR requirement quality attributes.
- **Invalid fallback**: unknown/missing strategy → `risk_first` with warning log.
- **Tie-breaking**: lexicographical `group_id` ascending.
- **Output**: `batch_queue` with every batch annotated with `sorting_metadata`.
