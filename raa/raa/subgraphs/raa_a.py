"""
RAA-A subgraph builder — SAAM-first architectural fragment extraction.

Returns an uncompiled StateGraph. The caller is responsible for
compilation with the appropriate SQLite checkpointer.
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from raa.state.models import ArchFragment
from raa.subgraphs.schemas import StrategySubgraphState


def build_raa_a_subgraph() -> StateGraph:
    """Build an uncompiled RAA-A subgraph (SAAM-first strategy).

    Story 2.1 scaffold: the node returns a minimal ArchFragment with
    strategy metadata. Real SAAM scoring is implemented in Story 2.3.
    """
    builder = StateGraph(StrategySubgraphState)

    def extract_saam(state: StrategySubgraphState) -> dict:
        fragment = ArchFragment(
            metadata={
                "strategy": "raa_a",
                "batch_id": state["batch"].get("group_id", ""),
                "note": "SAAM-first extraction (Story 2.3 implements real scoring)",
            }
        )
        return {"arch_fragment": fragment}

    builder.add_node("extract_saam", extract_saam)
    builder.add_edge(START, "extract_saam")
    builder.add_edge("extract_saam", END)

    return builder
