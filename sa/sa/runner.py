from typing import Dict, Any
from sa.graphs.core import build_sa_graph

def compile_sa_graph():
    builder = build_sa_graph()
    return builder.compile()

def invoke_sa(arch_model: dict, requirements_data: dict, output_path: str = ".") -> Dict[str, Any]:
    graph = compile_sa_graph()
    initial_state = {
        "arch_model": arch_model,
        "requirements_data": requirements_data,
        "plantuml_context": "",
        "plantuml_container": "",
        "plantuml_component": "",
        "output_path": output_path
    }
    
    final_state = graph.invoke(initial_state)
    return final_state
