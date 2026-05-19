# Data Model: Checkpoint Structures and Configurations

This document defines the structures and schemas used by the SQLite checkpoint saver and runner entrypoint.

---

## 1. Thread Config Schema

The LangGraph configuration dict used to identify checkpoints:

```python
from typing import TypedDict

class ConfigurableFields(TypedDict):
    thread_id: str  # Format: raa-{sha256_hash_16_chars}

class LangGraphRunnableConfig(TypedDict):
    configurable: ConfigurableFields
```

---

## 2. Checkpoint State Summary

When querying `graph.get_state(config)`, the returned state includes:

```python
from typing import TypedDict, Any

class StateValues(TypedDict):
    batch_cursor: int
    best_batch_output: dict[int, Any]
    running_arch_model: dict[str, Any]
    open_questions: list[Any]

class LangGraphState(TypedDict):
    values: StateValues
    next: tuple[str, ...]
    config: LangGraphRunnableConfig
    metadata: dict[str, Any]
    created_at: str
    parent_config: Optional[LangGraphRunnableConfig]
```

---

## 3. Run Context and Configuration

The runner entrypoint consumes these fields to compile and run the graph:

```python
from typing import TypedDict, Optional

class RunnerConfig(TypedDict):
    project_name: str
    db_path: str                 # Path to the sqlite3 checkpointer db
    thread_id: Optional[str]     # Override thread_id (optional)
    run_label: str               # concanted in thread ID computation (default: "default")
    durability: str              # checkpoint durability mode (default: "sync")
```
