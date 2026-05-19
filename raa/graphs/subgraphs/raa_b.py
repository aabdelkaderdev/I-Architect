"""RAA-B subgraph: Pattern-driven architecture analysis.

Consumes LLM from payload["llm"], loads pattern-selection references,
and returns a typed ArchFragment via batch_outputs.
"""

from __future__ import annotations

from typing import Any

from raa.graphs.subgraphs.common import (
    STRATEGY_PATTERN_DRIVEN,
    SubgraphPayload,
    execute_strategy_subgraph,
)


def run_raa_b(payload: SubgraphPayload) -> dict[str, Any]:
    """Execute the pattern-driven strategy subgraph.

    Uses Pattern_Selection.md, Quality_Attributes.md, Entity_Extraction.md,
    Relationship_Extraction.md, Technology_Inference.md, C4.md,
    and C4_Level_Mapping.md as the reference bundle.

    Returns:
        {"batch_outputs": {batch_index: [ArchFragment(...)]}}
    """
    return execute_strategy_subgraph(payload, STRATEGY_PATTERN_DRIVEN, source_fragment="raa_b")
