import operator
from typing import Any, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from dataclasses import dataclass
from langchain_core.language_models import BaseChatModel

from aga.state.schemas import AGAState
from aga.nodes.server_guard import server_guard
from aga.nodes.input_parsing import input_parsing
from aga.nodes.diagram_loop import diagram_loop_entry, should_continue_diagrams, record_diagram_result
from aga.nodes.diagram_generation import create_diagram_agent
from aga.nodes.output_assembly import output_assembly

@dataclass
class Context:
    llm: Optional[BaseChatModel] = None
    thread_id: str = "default-thread"

def create_aga_graph(tools: list = None, checkpointer: SqliteSaver = None):
    builder = StateGraph(AGAState)
    
    if tools is None:
        from aga.tools.encode_plantuml import encode_plantuml
        from aga.tools.fetch_plantuml_png import fetch_plantuml_png
        tools = [encode_plantuml, fetch_plantuml_png]
        
    diagram_agent = create_diagram_agent(tools)
    
    builder.add_node("server_guard", server_guard)
    builder.add_node("input_parsing", input_parsing)
    builder.add_node("diagram_loop_entry", diagram_loop_entry)
    builder.add_node("agent_node", diagram_agent)
    builder.add_node("record_diagram_result", record_diagram_result)
    builder.add_node("output_assembly", output_assembly)
    
    builder.add_edge(START, "server_guard")
    builder.add_edge("server_guard", "input_parsing")
    builder.add_edge("input_parsing", "diagram_loop_entry")
    
    builder.add_conditional_edges(
        "diagram_loop_entry",
        should_continue_diagrams,
        {
            "agent_node": "agent_node",
            "output_assembly": "output_assembly"
        }
    )
    
    builder.add_edge("agent_node", "record_diagram_result")
    builder.add_edge("record_diagram_result", "diagram_loop_entry")
    builder.add_edge("output_assembly", END)
    
    graph = builder.compile(checkpointer=checkpointer)
    return graph
