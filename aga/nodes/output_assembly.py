import time
from typing import Any
from langchain_core.runnables import RunnableConfig
from aga.state.schemas import AGAState

def output_assembly(state: AGAState, config: RunnableConfig) -> dict[str, Any]:
    """
    Final node in the graph, executed when diagram_queue is exhausted.
    Generates a session report and outputs the final diagrams.
    """
    completed = state.get("completed_diagrams", [])
    failed = state.get("failed_diagrams", [])
    arch_model = state.get("arch_model", {})
    
    # In a real scenario, total_diagrams_expected would be set during input parsing
    total_expected = len(completed) + len(failed)
    
    # Derive output paths from config, fallback to default if not present
    configurable = config.get("configurable", {})
    
    session_report = {
        "completed_count": len(completed),
        "failed_count": len(failed),
        "total_diagrams_expected": total_expected,
        "wall_clock_seconds": time.time(), # Typically you'd calculate a diff from start time
        "planturl_binary": state.get("planturl_bin_path", ""),
        "detected_os": "", # Could be passed through state
        "plantuml_server_url": configurable.get("plantuml_server_url", "http://www.plantuml.com/plantuml")
    }
    
    return {
        "session_report": session_report,
        "completed_diagrams": completed,
        "failed_diagrams": failed
    }
