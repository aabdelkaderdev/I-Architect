"""RAA-A subgraph: SAAM-first conservative architecture analysis.

Consumes LLM from payload["llm"], loads SAAM-focused references,
and returns a typed ArchFragment via batch_outputs.
"""

from __future__ import annotations

from typing import Any

from raa.graphs.subgraphs.common import (
    STRATEGY_SAAM_FIRST,
    SubgraphPayload,
    execute_strategy_subgraph,
)


def run_raa_a(payload: SubgraphPayload) -> dict[str, Any]:
    """Execute the SAAM-first strategy subgraph.

    Uses SAAM.md, Quality_Attributes.md, Entity_Extraction.md,
    Relationship_Extraction.md, Technology_Inference.md, C4.md,
    and C4_Level_Mapping.md as the reference bundle.

    Returns:
        {"batch_outputs": {batch_index: [ArchFragment(...)]}}
    """
    return execute_strategy_subgraph(payload, STRATEGY_SAAM_FIRST, source_fragment="raa_a")
