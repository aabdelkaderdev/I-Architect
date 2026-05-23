"""
RAA-B subgraph builder — Pattern-driven architectural fragment extraction.

Returns an uncompiled StateGraph. The caller is responsible for
compilation with the appropriate SQLite checkpointer.
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from raa.state.models import ArchFragment
from raa.subgraphs.schemas import StrategySubgraphState


def build_raa_b_subgraph() -> StateGraph:
    """Build an uncompiled RAA-B subgraph (pattern-driven strategy).

    Story 2.1 scaffold: the node returns a minimal ArchFragment with
    strategy metadata. Real pattern extraction is implemented in Story 2.4.
    """
    builder = StateGraph(StrategySubgraphState)

    def extract_patterns(state: StrategySubgraphState) -> dict:
        fragment = ArchFragment(
            metadata={
                "strategy": "raa_b",
                "batch_id": state["batch"].get("group_id", ""),
                "note": "Pattern-driven extraction (Story 2.4 implements real logic)",
            }
        )
        return {"arch_fragment": fragment}

    builder.add_node("extract_patterns", extract_patterns)
    builder.add_edge(START, "extract_patterns")
    builder.add_edge("extract_patterns", END)

    return builder
