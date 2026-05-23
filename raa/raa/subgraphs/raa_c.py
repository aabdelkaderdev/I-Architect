"""
RAA-C subgraph builder — Entity/relationship-driven architectural fragment extraction.

Returns an uncompiled StateGraph. The caller is responsible for
compilation with the appropriate SQLite checkpointer.
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from raa.state.models import ArchFragment
from raa.subgraphs.schemas import StrategySubgraphState


def build_raa_c_subgraph() -> StateGraph:
    """Build an uncompiled RAA-C subgraph (entity/relationship strategy).

    Story 2.1 scaffold: the node returns a minimal ArchFragment with
    strategy metadata. Real entity extraction is implemented in Story 2.5.
    """
    builder = StateGraph(StrategySubgraphState)

    def extract_entities(state: StrategySubgraphState) -> dict:
        fragment = ArchFragment(
            metadata={
                "strategy": "raa_c",
                "batch_id": state["batch"].get("group_id", ""),
                "note": "Entity extraction (Story 2.5 implements real logic)",
            }
        )
        return {"arch_fragment": fragment}

    builder.add_node("extract_entities", extract_entities)
    builder.add_edge(START, "extract_entities")
    builder.add_edge("extract_entities", END)

    return builder
