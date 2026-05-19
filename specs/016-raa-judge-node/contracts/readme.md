# RAA Per-Batch Judge Node Contracts

The judge node must use `llm_judge` from the execution context for SAAM scoring.
If `reduced_confidence` is true in the batch metadata, the SAAM scores must be multiplied by `0.5`.
The merge algorithm must be deterministic code (no LLM text generation for the merge output).
Orphaned components (missing parent containers) and orphaned containers (missing parent systems) must NEVER be added to the merged output.
All unresolved conflicts and coverage gaps must be formatted and appended to the `open_questions` state variable.
The finalized entities must be assembled into a nested C4 tree structure before updating the `running_arch_model`.
The `batch_cursor` state value must be incremented by 1 at the end of the node execution.
