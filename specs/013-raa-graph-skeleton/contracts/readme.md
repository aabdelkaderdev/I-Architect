# RAA LangGraph Skeleton Contracts

## Graph Compilation

- The graph MUST be built with `StateGraph(RAAState)` where `RAAState` is imported from `raa.state.channels`.
- The graph MUST NOT define a second, graph-only state schema.

## Embeddings-Ready Gate

- The gate node MUST return `{}` when `state["embeddings_ready"] is True`.
- The gate node MUST raise `ValueError` with a clear message when `embeddings_ready` is `False` or missing.
- The graph MUST halt and not proceed past the gate on failure.

## Channel Ownership (Section 3 Steps 1-5)

| Step | Node | Owns (writes) |
|------|------|---------------|
| 1 | `prepare_embeddings` | `embeddings_ready` |
| 2 | `construct_batches` | initial `batch_queue` |
| 3 | `apply_overlap_bridging` | `batch_queue`, `bridge_requirements` |
| 4 | `apply_coherence_gate` | `batch_queue`, `incoherent_batches` |
| 5 | `order_batch_queue` | final `batch_queue` |

## Node Sequence

Preparation -> `embeddings_ready_gate` -> Batch Construction -> Overlap Bridging -> Coherence Gate -> Batch Queue Ordering -> END

## Reducer Verification

- `batch_queue`, `batch_cursor`, `running_arch_model`, `bridge_requirements`, `embeddings_ready`: overwrite channels (no reducer annotation).
- `open_questions`, `incoherent_batches`: append channels (`operator.add`).
- `batch_outputs`: `merge_batch_outputs` dict-merge.
- `best_batch_output`: `merge_best_batch_output` dict-merge.

## Scope Boundaries

- Section 3 steps 6 (execution loop / judge subgraphs) and 7 (final merge) are NOT wired by this feature.
- No LLM instances, embedding vectors, `normalized_requirements`, or `batches` as state channels.
- Compiled graph's channel set MUST match `RAAState` keys plus LangGraph internal channels only.
