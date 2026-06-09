"""Static configuration defaults. Single source of truth for all hardcoded values.

Layered strategy (FG-Phase-10 §5 / FG-Phase-13 §3):
- Static defaults live here.
- Runtime overrides arrive via config["configurable"] (thread_id, db_path, LLM instances).
- No YAML, TOML, or .env files beyond pyproject.toml.
"""

# ── Embedding ──

# Cosine similarity threshold for non-ASR to condition-group assignment.
# Non-ASRs scoring above this threshold are assigned to the best-matching
# concern batch; those below become orphans routed to the Foundation Batch.
SIMILARITY_THRESHOLD: float = 0.65

# ── Checkpointing (FG-Phase-34 §3) ──

# Default SqliteSaver path for LangGraph checkpointing.
# Overridable at runtime via config["configurable"]["db_path"].
DB_PATH: str = "./raa_checkpoint.db"

# Default thread_id for LangGraph checkpoint namespace.
THREAD_ID: str = "raa_run_default"

# ── LLM Token Limits (Phase 32) ──

MAX_OUTPUT_TOKENS: int = 4096
MAX_INPUT_TOKENS: int = 128000

# ── Retry Policy (FG-Phase-36 §2.2) ──

RETRY_MAX_ATTEMPTS: int = 5
RETRY_BACKOFF_FACTOR: float = 2.0
RETRY_INITIAL_INTERVAL: float = 0.5
RETRY_MAX_INTERVAL: float = 128.0
RETRY_JITTER: bool = True

# ── Timeout Policy (FG-Phase-39 §2.2) ──

# Per-node run_timeout in seconds. Covers typical structured-output LLM calls
# with headroom for large batches.
NODE_RUN_TIMEOUT: float = 120.0
