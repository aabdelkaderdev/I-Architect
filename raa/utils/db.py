"""Database utilities for RAA.

Handles SQLite connection setup, including WAL mode configuration and read-only URI connections.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3


def open_embedding_db(db_path: Path | str, read_only: bool = False) -> sqlite3.Connection:
    """Open a SQLite database connection with WAL journal mode enabled.

    If read_only is True, opens the database in read-only mode via a URI connection.
    """
    path = Path(db_path)
    if read_only:
        # Construct read-only URI. resolve() ensures an absolute path.
        uri = f"file:{path.resolve().as_posix()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
    else:
        conn = sqlite3.connect(str(path))

    # Enable WAL mode to support concurrent read operations
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn
