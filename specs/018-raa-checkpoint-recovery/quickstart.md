# Quickstart: SQLite Checkpointing and Crash Recovery

This guide provides examples showing how to configure `SqliteSaver`, calculate deterministic thread IDs, manage resume logic, and handle corrupted checkpoints.

---

## 1. Production Compilation and Connection

```python
import sqlite3
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

def compile_graph_with_checkpointer(builder, db_path: str) -> Any:
    # Ensure parent directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Establish connection with thread safety flags
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    # Enable WAL mode for concurrent reads
    conn.execute("PRAGMA journal_mode=WAL;")
    
    # Initialize checkpointer
    checkpointer = SqliteSaver(conn)
    checkpointer.setup()
    
    return builder.compile(checkpointer=checkpointer)
```

---

## 2. Deterministic Thread ID Calculation

```python
import hashlib
import json

def get_deterministic_thread_id(arlo_output: dict, run_label: str = "default") -> str:
    # Normalize inputs to ensure stability
    serialized_inputs = json.dumps(arlo_output, sort_keys=True)
    hash_payload = f"{serialized_inputs}:{run_label}".encode("utf-8")
    
    # Generate SHA-256 and truncate to 16 hex characters
    sha256_hash = hashlib.sha256(hash_payload).hexdigest()
    short_hash = sha256_hash[:16]
    
    return f"raa-{short_hash}"
```

---

## 3. Fresh-Start vs. Resume Wrapper with Corruption Fallback

```python
import logging
import os
import sqlite3

def execute_with_recovery(graph, initial_state: dict, thread_id: str, db_path: str, context: dict) -> dict:
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Check for existing checkpoint state
        state = graph.get_state(config)
    except (sqlite3.DatabaseError, Exception) as e:
        logging.warning(f"Checkpoint DB corruption detected at {db_path}: {e}. Falling back to fresh start.")
        
        # Rename corrupted file and trigger fresh start
        if os.path.exists(db_path):
            os.rename(db_path, f"{db_path}.corrupted")
        
        # Re-compile graph with a fresh DB (assuming connection function creates it)
        graph = compile_graph_with_checkpointer(graph.builder, db_path)
        state = None
        
    if state and state.values and state.values.get("batch_cursor", 0) > 0:
        logging.info(f"Resuming RAA pipeline from checkpoint (batch_cursor={state.values['batch_cursor']})")
        # Resume with None state (restores checkpoint state)
        return graph.invoke(None, config, context=context)
    else:
        logging.info("Starting fresh RAA pipeline run.")
        # Start fresh with initial state payload
        return graph.invoke(initial_state, config, context=context)
```
