from langgraph.graph import StateGraph
from langgraph.constants import START, END
from sa.state.schemas import SAState
from sa.nodes.preparation import node_preparation
from sa.nodes.axis_functional import node_functional
from sa.nodes.axis_asr import node_asr
from sa.nodes.axis_saam import node_saam
from sa.nodes.report import node_report

def build_sa_graph() -> StateGraph:
    builder = StateGraph(SAState)
    
    # Add nodes
    builder.add_node("preparation", node_preparation)
    builder.add_node("axis_functional", node_functional)
    builder.add_node("axis_asr", node_asr)
    builder.add_node("axis_saam", node_saam)
    builder.add_node("report", node_report)
    
    # Wire edges
    builder.add_edge(START, "preparation")
    builder.add_edge("preparation", "axis_functional")
    builder.add_edge("axis_functional", "axis_asr")
    builder.add_edge("axis_asr", "axis_saam")
    builder.add_edge("axis_saam", "report")
    builder.add_edge("report", END)
    
    return builder
