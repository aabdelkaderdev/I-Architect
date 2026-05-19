# Research Report: RAA State Serialization & Channel Reduction

This report documents the research, decisions, and patterns selected for implementing the RAA State Contracts.

## 1. LangGraph JsonPlusSerializer Compatibility

### Decision
Represent C4 architectural entities as Python standard `@dataclass` classes with type annotations. Ensure all fields are primitive types, standard collections (lists, dicts), or other annotated dataclasses.

### Rationale
LangGraph's default checkpointer serializer, `JsonPlusSerializer`, natively supports standard Python types, lists, dictionaries, and Python dataclasses. By sticking to standard Python dataclasses and avoiding complex custom objects, we guarantee that the full graph state can be checkpointed to SQLite without registering custom encoders or encountering serialization crashes.

### Alternatives Considered
- **Pydantic v2 Models**: Pydantic models offer strong validation, but `JsonPlusSerializer` does not serialize them out-of-the-box without custom serializing decorators or converting them to dicts manually at step boundaries.
- **Plain TypedDicts**: While easily serializable, TypedDicts lack object-oriented conveniences (like helper methods for tree traversal) and can lead to silent field mismatches due to lack of class-level constraints.

---

## 2. State Channel Reducers for Parallel Graph Execution

### Decision
Implement custom reducer functions for multi-writer dictionary channels, and utilize `operator.add` for list-based channels.

1. **`open_questions` and `incoherent_batches`**: Use list concatenation reducer (`operator.add` or a custom list-append function) to accumulate items written by different subgraphs or nodes during the same super-step.
2. **`batch_outputs`**: Define a custom merge reducer that merges dictionary payloads from parallel nodes:
   ```python
   def merge_batch_outputs(
       left: dict[int, list[ArchFragment]], 
       right: dict[int, list[ArchFragment]]
   ) -> dict[int, list[ArchFragment]]:
       merged = left.copy()
       for k, v in right.items():
           if k in merged:
               merged[k] = merged[k] + v
           else:
               merged[k] = v
       return merged
   ```

### Rationale
Without explicit reducers, LangGraph applies a last-write-wins strategy, which would silently drop outputs when parallel RAA-A, RAA-B, and RAA-C nodes write to `batch_outputs` concurrently.

---

## 3. SQLite Embedding Database WAL Mode

### Decision
Configure both `asr_embeddings.db` (read-only in RAA) and `non_asr_embeddings.db` (write-read in RAA) to use Write-Ahead Logging (WAL) mode via `PRAGMA journal_mode=WAL;` on connection initialization.

### Rationale
WAL mode improves concurrent read/write performance and prevents SQLite database locks when nodes query or write to databases during graph executions. Since RAA nodes will read embeddings concurrently or in quick succession, WAL mode ensures high reliability.
