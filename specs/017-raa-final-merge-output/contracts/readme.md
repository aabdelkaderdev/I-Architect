# Interface and Filesystem Contracts: RAA Final Merge

This document defines the interface contracts, inputs, outputs, and filesystem side-effects of the final merge stage of the RAA pipeline.

## 1. Input State Channels

The final merge node consumes the following channels from the graph state:
- `best_batch_output` (`dict[int, ArchFragment]`): The selected and merged output per batch.
- `running_arch_model` (`ArchModel`): The accumulated working architecture model.
- `open_questions` (`list[OpenQuestion]`): Unresolved conflicts or coverage gaps accumulated across batches.
- `incoherent_batches` (`list[IncoherentBatchRecord]`): Records of batches that failed the coherence gate.

## 2. Configuration & Orchestrator Inputs

The orchestrator must pass the following context parameters at runtime:
- `project_name` (`str`): The active project name, used to resolve output directories.
- `thread_id` (`str`): The execution thread identifier, used to archive checkpoints.
- `output_dir` (`str`): The directory path to write the output model to (default: `projects/{project_name}/output/raa/`).
- `db_path` (`str`): The path to the active SQLite checkpoint database (default: `projects/{project_name}/checkpoints/raa_graph.db`).

## 3. Filesystem Outputs

- **JSON Output File**: `projects/{project_name}/output/raa/arch_model.json`
  - Validated against the C4 JSON Schema.
  - Formatted with indentation for human readability.
- **Archived Checkpoint**: `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db`
  - The SQLite checkpoint DB is moved to this path *only* after successful write and validation of the JSON output.
