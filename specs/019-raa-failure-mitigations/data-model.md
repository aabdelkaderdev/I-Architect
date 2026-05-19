# Data Model: Failure Modes and Embedding Schemas

This document defines the database schemas, state variables, and failure register structures for the RAA Failure Mode Mitigations feature.

---

## 1. Shared Embedding Table Schema

Both `asr_embeddings.db` and `non_asr_embeddings.db` utilize a flat, structured SQLite table:

```sql
CREATE TABLE IF NOT EXISTS embeddings (
  requirement_id INTEGER PRIMARY KEY,  -- Map string IDs like "R12" to integer 12
  embedding BLOB NOT NULL,              -- 1024-element float32 vector (4096 bytes)
  text_hash TEXT NOT NULL,              -- SHA-256 hash of requirement text
  model_name TEXT NOT NULL              -- Fixed value: "mixedbread-ai/mxbai-embed-large-v1"
);
```

---

## 2. Failure Register Schema

The `FailureRegisterEntry` dataclass represents a monitored runtime risk and its active mitigation in the Python code:

```python
@dataclass
@dataclass
class FailureRegisterEntry:
    """Represents a monitored runtime risk and its active mitigation."""

    risk_id: str
    description: str
    mitigation_strategy: str
    section_ref: str
    verified_node: str
```

The Failure Modes Register is documented as a markdown table mapping risk profiles to active runtime mitigations:

| Risk ID | Failure Mode | Mitigation Strategy | Section Ref | Verified Node |
|---|---|---|---|---|
| **FR-RISK-001** | Process killed mid-pipeline (OOM, crash, operator SIGKILL) | SQLite checkpointing (SqliteSaver) saves full state after every super-step. On restart, the runner detects existing state where batch_cursor > 0 and resumes from the last completed batch. | §22H | `runner.py` / `run_with_recovery` |
| **FR-RISK-002** | Checkpoint DB unavailable or corrupt at startup | Try-except block catches sqlite3.DatabaseError on get_state(). Renames corrupted DB to *.corrupted and executes a clean fresh start. | §22H | `runner.py` / `run_with_recovery` |
| **FR-RISK-003** | batch_cursor desync (checkpoint advanced but output not written) | The final_merge node checks best_batch_output keys against range(len(batch_queue)). If any key is missing or corrupted, it logs a warning, rolls back batch_cursor to the missing index, and redirects execution for a targeted rerun. | §22H | `final_merge.py` / `final_merge` |
| **FR-RISK-004** | Embedding SQLite DB missing at RAA startup | Startup validation check in prepare_embeddings node. If asr_embeddings.db is missing/corrupted, raises a blocking RuntimeError. If non_asr_embeddings.db is missing, it is automatically rebuilt. | §22H | `preparation.py` / `prepare_embeddings` |
| **FR-RISK-005** | Embedding SQLite DB locked (concurrent access) | Open connections with Write-Ahead Logging (PRAGMA journal_mode=WAL;). Downstream nodes use read-only URI connections (mode=ro) to avoid locking during parallel reads. | §22H | `preparation.py` / `batch_construction.py` |
| **FR-RISK-006** | Condition group has semantic drift | Coherence gate (§10) splits batch into homogeneous sub-batches, or flags with reduced confidence if splitting fails. | §18 | `coherence_gate.py` / `routing.py` |
| **FR-RISK-007** | No good non-ASR matches for a group | Allow empty non-ASR list; batch proceeds with ASRs only, logging an informational warning. | §18 | `batch_construction.py` / `construct_batches` |
| **FR-RISK-008** | Cross-batch entity naming collisions | running_arch_model constraint injection (§15) + entity deduplication and merging in judge node. | §18 | `judge.py` / `final_merge.py` |
| **FR-RISK-009** | Overlap exceeds 3 bridge requirements | Overlap bridging node enforces a hard cap of maximum 3 bridge requirements per adjacent batch pair. | §18 | `overlap_bridging.py` / `apply_overlap_bridging` |
| **FR-RISK-010** | Judge discards a useful artifact | Residual scan is run before fragment discard to carry forward unique elements with scenario coverage. | §18 | `judge.py` / `evaluate_and_merge` |
| **FR-RISK-011** | Incoherent batch degrades model | reduced_confidence flag + 0.5x SAAM weight multiplier applied in judge node scoring. | §18 | `judge.py` / `evaluate_and_merge` |
| **FR-RISK-012** | Reconciliation LLM introduces new conflicts | Reconciliation pass output is validated against C4 schema rules; if violations increase, the reconciliation is rejected and pre-reconciliation model is preserved. | §18 | `final_merge.py` / `final_merge` |
| **FR-RISK-013** | Embedding text hash mismatch (stale requirement text) | Preparation node checks computed text hashes against DB hashes, logging a warning and recomputing only the modified entries. | §18 | `preparation.py` / `_persist_non_asr_embeddings` |

---

## 3. State Checkpoint Representation

The RAAState fields persisted by the SQLite checkpointer at the end of each super-step include:

```python
class RAAState(TypedDict):
    # Cursor and Execution Queue
    batch_cursor: int                          # Current batch index
    batch_queue: list[dict[str, Any]]          # Normalised and ordered batches
    
    # State flags
    embeddings_ready: bool                     # Fast-path skip indicator
    
    # Accumulated outputs
    running_arch_model: dict[str, Any]         # Consolidated hierarchical C4 model
    best_batch_output: dict[int, dict]         # Map of batch index -> winning ArchFragment
    open_questions: list[dict[str, Any]]       # Active unresolved conflicts/gaps
    
    # Coherence and bridging structures
    bridge_requirements: dict[str, list[str]]  # Keyed by sorted batch pairs -> bridge ID list
    incoherent_batches: list[dict[str, Any]]   # Records of incoherent batches
```
