# Interface and Filesystem Contracts: SQLite Checkpointer

This document defines the filesystem boundary rules and integration contracts for the RAA checkpoint database.

## 1. Database Schema and Storage Invariants

- **Location**: `projects/{project_name}/checkpoints/raa_graph.db`
- **Ownership**: The orchestrator configures and provides the path. RAA has write access to the file.
- **Initialization**: Parent directories must exist or be created recursively.
- **WAL Mode**: WAL (Write-Ahead Logging) is enabled automatically upon connection to prevent lockouts during concurrent reads.
- **Connection Flags**: `check_same_thread=False` must be passed to `sqlite3.connect` to support multi-threaded checkpointing from LangGraph worker threads.

## 2. Recovery Boundary

- If `db_path` points to a corrupted SQLite file:
  1. The connection constructor raises `sqlite3.DatabaseError` or a similar exception.
  2. The runner catches the error, logs a `WARNING`, and renames the corrupted file with a `.corrupted` suffix.
  3. The runner recreates the database as a fresh SQLite instance, allowing the pipeline to execute as a fresh run.
- Checkpoint archiving occurs *after* execution completes and the final output is validated.
