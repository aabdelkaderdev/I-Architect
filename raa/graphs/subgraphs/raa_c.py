"""RAA-C subgraph: Entity/relationship-driven architecture analysis.

Consumes LLM from payload["llm"], loads entity-extraction references
(excluding SAAM and Pattern_Selection), and returns a typed ArchFragment
via batch_outputs.
"""

from __future__ import annotations

from typing import Any

from raa.graphs.subgraphs.common import (
    STRATEGY_ENTITY_DRIVEN,
    SubgraphPayload,
    execute_strategy_subgraph,
)


def run_raa_c(payload: SubgraphPayload) -> dict[str, Any]:
    """Execute the entity-driven strategy subgraph.

    Uses Entity_Extraction.md, Relationship_Extraction.md,
    Technology_Inference.md, C4.md, and C4_Level_Mapping.md as the reference
    bundle. Excludes SAAM.md and Pattern_Selection.md.

    Returns:
        {"batch_outputs": {batch_index: [ArchFragment(...)]}}
    """
    return execute_strategy_subgraph(payload, STRATEGY_ENTITY_DRIVEN, source_fragment="raa_c")
