"""
Named constants for RAA thresholds and limits.

Never inline magic numbers in node code — import from here.
"""

# ── Deduplication thresholds ──────────────────────────────────────────────
DEDUP_MERGE_THRESHOLD = 0.80       # Cosine ≥ this + ID overlap → auto-merge
DEDUP_GROUP_THRESHOLD_LOW = 0.60  # Cosine ≥ this → boundary group (lower bound)
DEDUP_GROUP_THRESHOLD_HIGH = 0.80 # Upper bound for boundary grouping range

# ── Batching thresholds ───────────────────────────────────────────────────
NON_ASR_SIMILARITY_THRESHOLD = 0.65  # Min cosine for non-ASR neighbor retrieval
COHERENCE_THRESHOLD = 0.55           # Min avg batch coherence before splitting

# ── Residual pass thresholds ──────────────────────────────────────────────
RESIDUAL_HIGH_THRESHOLD = 0.75   # Auto-enrich matching container
RESIDUAL_MID_LOW = 0.50         # Lower bound for coupling check

# ── Limits ────────────────────────────────────────────────────────────────
MAX_NON_ASR_PER_BATCH = 10      # Max non-ASR candidates pulled per batch
MAX_BRIDGE_REQUIREMENTS = 3     # Max bridge items injected per overlap pair
RESIDUAL_REBATCH_PCT = 0.15     # Fraction of unprocessed reqs that trigger rebatch
MAX_HUMAN_RETRIES = 3           # Max human review submission attempts

# ── Embedding ────────────────────────────────────────────────────────────────
from pathlib import Path
EMBEDDING_DIM = 1024
EMBEDDING_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"
EMBEDDING_CACHE_DIR = str(Path(__file__).resolve().parent.parent.parent.parent / "models")

# ── Pattern keywords ──────────────────────────────────────────────────────
INFRA_KEYWORDS = ["all", "every", "always", "any"]
