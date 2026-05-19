"""RAA graph construction and compilation."""

from raa.graphs.main_graph import (
    NODE_BATCH_QUEUE_ORDERING,
    NODE_COHERENCE_GATE,
    NODE_CONSTRUCT_BATCHES,
    NODE_EMBEDDINGS_READY_GATE,
    NODE_OVERLAP_BRIDGING,
    NODE_PREPARE_EMBEDDINGS,
    SECTION_3_PIPELINE_STEPS,
    build_raa_graph,
    compile_for_production,
    compile_raa_graph,
    embeddings_ready_gate,
)

__all__ = [
    "NODE_BATCH_QUEUE_ORDERING",
    "NODE_COHERENCE_GATE",
    "NODE_CONSTRUCT_BATCHES",
    "NODE_EMBEDDINGS_READY_GATE",
    "NODE_OVERLAP_BRIDGING",
    "NODE_PREPARE_EMBEDDINGS",
    "SECTION_3_PIPELINE_STEPS",
    "build_raa_graph",
    "compile_for_production",
    "compile_raa_graph",
    "embeddings_ready_gate",
]

# Re-export subgraph package for convenience
from raa.graphs import subgraphs  # noqa: E402, F401 — public sub-package
