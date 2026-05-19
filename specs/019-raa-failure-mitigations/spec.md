# Feature Specification: RAA Failure Mode Mitigations

**Feature Branch**: `019-raa-failure-mitigations`

**Created**: 2026-05-19

**Status**: Draft

**Input**: User description: "Create a focused feature for failure mode mitigations. Scope strictly to RAA_Plan.md Section 18 and Section 22H. Define the deliverable as remaining runtime mitigations, WAL mode, startup blocking errors, desync recovery, and updated failure register rows."

## User Scenarios & Testing *(mandatory)*

This feature is designed for system operators and developers who run and monitor the Requirement Analysis Agent (RAA) pipeline. It ensures the pipeline runs reliably, handles unexpected errors or interruptions gracefully, and minimizes compute cost by recovering state rather than restarting.

### User Story 1 - Resilient Recovery from Pipeline Interruptions (Priority: P1)

As a pipeline operator, I want the system to persist its progress at every step so that if the process is killed mid-run (e.g., due to OOM, timeouts, or system restarts), it can resume from the last completed batch without repeating expensive LLM calls or re-embedding requirements.

**Why this priority**: RAA execution is long-running and LLM-heavy. Restarting from scratch on failure is costly and introduces significant delays.

**Independent Test**:
- **Given** a multi-batch pipeline run,
- **When** the process is terminated mid-execution (e.g., via SIGKILL during batch 2), and then restarted with the same configuration,
- **Then** the pipeline resumes execution precisely at batch 2, using the previously completed batch 1 results and existing embeddings without repeating their computation or LLM calls.

**Acceptance Scenarios**:

1. **Given** the RAA pipeline is executing batch 2 of 4, **When** a SIGKILL occurs and the pipeline is restarted with the same thread ID, **Then** the system loads the state checkpoint, skips batch 1, and resumes processing batch 2.
2. **Given** an interrupted pipeline, **When** resumed, **Then** the previously computed non-ASR embeddings in SQLite are reused directly if the hashes match the input requirements.

---

### User Story 2 - Startup Safety Checks and Diagnostics (Priority: P1)

As a pipeline operator, I want the system to validate the integrity of its environment and inputs before starting the analysis so that I am immediately notified of blocking issues (such as missing required data) rather than discovering them after wasting time and resources.

**Why this priority**: Fails fast and prevents corrupted outputs or runtime crashes deep in execution.

**Independent Test**:
- **Given** the pipeline is started,
- **When** the required ASR embedding database is missing or incomplete,
- **Then** the pipeline halts immediately, outputs a clear diagnostic error, and does not invoke downstream LLMs.

**Acceptance Scenarios**:

1. **Given** the pipeline starts and `asr_embeddings.db` is missing, **When** the validation node runs, **Then** it raises a blocking startup error instructing the operator to re-run the ARLO agent.
2. **Given** the pipeline starts and `non_asr_embeddings.db` is missing, **When** the validation node runs, **Then** it automatically triggers a background rebuild of the non-ASR database and proceeds without raising an error.

---

### User Story 3 - Automatic Database Concurrency & File Lock Mitigation (Priority: P2)

As a developer, I want the pipeline to support concurrent reads of the embedding databases without locking or corruption so that multiple batch nodes can run safely in parallel.

**Why this priority**: Essential to avoid intermittent deadlock failures in multi-batch environment scenarios.

**Independent Test**:
- **Given** multiple concurrent RAA batch nodes querying the embedding databases,
- **When** reading embeddings simultaneously,
- **Then** no SQLite "database is locked" errors are thrown, and all queries return data successfully.

**Acceptance Scenarios**:

1. **Given** the pipeline is running in WAL (Write-Ahead Logging) mode, **When** batch nodes access the embedding databases concurrently, **Then** the SQLite connections execute read operations in parallel without blocking or throwing lock exceptions.

---

### User Story 4 - Desync Recovery during Final Merge (Priority: P2)

As a pipeline operator, I want the final merge node to verify the presence and validity of all batch outputs before producing the final C4 model, automatically recovering any missing batch outputs.

**Why this priority**: Prevents producing incomplete models if a specific batch output is corrupted or lost from state.

**Independent Test**:
- **Given** the pipeline has completed all batches but one batch output is missing or corrupt in state,
- **When** the final merge node is executed,
- **Then** it detects the missing data and triggers a targeted re-run of only that specific batch to recover the model.

**Acceptance Scenarios**:

1. **Given** the pipeline is in the final merge phase and `best_batch_output` is missing a key for a completed batch, **When** validation fails, **Then** the system triggers a targeted re-run of the missing batch, updates the state, and successfully merges the final C4 model.

---

### Edge Cases

- **Checkpoint DB Corruption**: If the checkpoint database is corrupted or locked, the system logs a `WARNING` and falls back to a fresh start instead of crashing.
- **Stale Embeddings**: If requirement text is changed after embedding, the text hash will mismatch. The system must detect this hash mismatch, log a warning, and recompute only the affected embeddings rather than the entire database.
- **Incoherent Batch Semantic Drift**: If a condition group's semantic coherence falls below 0.55 and fails to split, it runs as a single-RAA batch with a 0.5× SAAM weight multiplier applied to prevent model degradation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (Startup ASR Embeddings Verification)**: The system MUST verify that the ASR embedding database exists and contains an embedding for every ASR requirement in the state channel. If any ASR is missing, it MUST raise a blocking error instructing the operator to re-run ARLO.
- **FR-002 (Automatic Non-ASR Embedding Rebuild)**: The system MUST automatically rebuild `non_asr_embeddings.db` from scratch if it is missing or corrupted.
- **FR-003 (FastEmbed Model Alignment)**: The embedding strategy MUST use the identical model and version as ARLO (`mixedbread-ai/mxbai-embed-large-v1`) to preserve the shared vector space.
- **FR-004 (Cache Integrity via Hash)**: The system MUST check the `text_hash` of each requirement. Requirements with missing or stale hashes MUST be recomputed, and a warning log MUST be emitted.
- **FR-005 (SQLite WAL Mode)**: The system MUST open embedding databases in WAL (Write-Ahead Logging) mode and use read-only connections for batch nodes to prevent write contention and lock timeouts.
- **FR-006 (Checkpoint Recovery & State Resumption)**: The system MUST persist state (including `batch_cursor`, `batch_queue`, `running_arch_model`, `best_batch_output`, and `open_questions`) after every super-step. On resume, the system MUST query the checkpointer and skip completed batches based on `batch_cursor`.
- **FR-007 (Desync Recovery during Merge)**: The final merge node MUST validate all `best_batch_output` keys against the expected batches. Any missing or invalid key MUST trigger a targeted re-run of that specific batch.
- **FR-008 (Checkpoint DB Fallback)**: If the checkpoint DB is unavailable or corrupt at startup, the system MUST log a `WARNING` and fall back to a fresh start.
- **FR-009 (Semantic Coherence Gate)**: The system MUST calculate batch coherence. If coherence is < 0.55 and sub-clusters also fail, the batch MUST run as a single-RAA batch with a `reduced_confidence` flag and a 0.5× SAAM scoring multiplier in the judge step.
- **FR-010 (Failure Modes Register Integration)**: The system MUST maintain a failure modes register mapping all Section 18 and Section 22H risks to their active mitigations.

### Key Entities *(include if feature involves data)*

- **Failure Register Row**: Represents a monitored runtime risk. Key attributes:
  - `risk_id`: Unique identifier (e.g., `FR-RISK-001`).
  - `description`: Short description of the failure mode.
  - `mitigation_strategy`: The automated action taken to address the risk.
  - `triggered`: Boolean indicating if the failure mode occurred during the run.
- **Embedding Cache Entry**: Records the state of a stored requirement embedding. Key attributes:
  - `requirement_id`: Mapped requirement ID (string).
  - `embedding`: The 1024-float vector stored as a blob.
  - `text_hash`: SHA-256 hash of the requirement text.
  - `model_name`: FastEmbed model identifier.
- **State Checkpoint**: The persisted state snapshot stored in the SQLite checkpointer. Key attributes:
  - `thread_id`: Stable run identifier.
  - `batch_cursor`: Integer index of the current batch.
  - `running_arch_model`: Hierarchical architecture model tree.
  - `best_batch_output`: Dict of merged fragments.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of pipeline executions interrupted by OOM or simulated crashes resume successfully from the last completed batch.
- **SC-002**: Startup validation checks execute in under 2 seconds, blocking execution immediately if prerequisite databases are missing.
- **SC-003**: 0 deadlocks or SQLite "database is locked" errors are encountered during concurrent batch reads.
- **SC-004**: Stale requirement hashes are identified and recomputed, adding less than 1 second of overhead per recomputed requirement.
- **SC-005**: Incoherent batches are flagged with 100% accuracy, applying the 0.5× SAAM multiplier in the judge.

## Assumptions

- SQLite WAL mode is supported by the OS and filesystem.
- The checkpointer database is persisted in the orchestrator-configured path `projects/{project_name}/checkpoints/raa_graph.db`.
- The orchestrator creates the necessary `checkpoints/` and `output/` directories before invoking the pipeline.
