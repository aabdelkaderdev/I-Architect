from typing import Any
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig

from aga.state.schemas import AGAState

def diagram_loop_entry(state: AGAState, config: RunnableConfig) -> dict[str, Any]:
    """
    Prepares the state for the next diagram to be generated.
    Advances the cursor and resets per-diagram state variables.
    """
    cursor = state.get("diagram_cursor", 0)
    queue = state.get("diagram_queue", [])
    
    if cursor < len(queue):
        updates = {
            "current_diagram": queue[cursor],
            "diagram_cursor": cursor + 1,
            "retry_count": 0,
            "current_puml_code": "",
            "current_encoded_url": "",
            "last_error": None
        }
        
        # Clear messages from the previous diagram to avoid context bloat
        messages = state.get("messages", [])
        if messages:
            updates["messages"] = [RemoveMessage(id=m.id) for m in messages if m.id]
            
        return updates
    
    # If no more diagrams, we return an empty dict, which signals conditional logic later
    return {}

def should_continue_diagrams(state: AGAState) -> str:
    """
    Conditional edge routing after diagram_loop_entry.
    Returns 'agent_node' if a diagram is ready, else 'output_assembly'.
    """
    cursor = state.get("diagram_cursor", 0)
    queue = state.get("diagram_queue", [])
    
    # Notice that diagram_loop_entry already advanced the cursor for the CURRENT diagram,
    # so if cursor was 0, it is now 1. But wait! The condition here checks if the current_diagram
    # is set.
    
    if state.get("current_diagram") and cursor <= len(queue):
        return "agent_node"
        
    return "output_assembly"

def record_diagram_result(state: AGAState, config: RunnableConfig) -> dict[str, Any]:
    """
    Evaluates the result of the agent_node and updates completed or failed diagrams.
    """
    import os
    import json
    diagram = state.get("current_diagram")
    if not diagram:
        return {}

    messages = state.get("messages", [])
    retry_count = state.get("retry_count", 0)
    current_puml = state.get("current_puml_code", "")
    
    # Try to find a successful tool message containing image_bytes
    success = False
    png_bytes = b""
    
    for msg in reversed(messages):
        if getattr(msg, "name", "") == "fetch_plantuml_png" and getattr(msg, "content", ""):
            content = msg.content
            # Handle string representation of dict if needed (LangChain sometimes stringifies dicts)
            if isinstance(content, str):
                try:
                    # In case it's a JSON string without bytes, or we parse it
                    content_dict = json.loads(content.replace("'", '"'))
                    if "error" not in content_dict:
                        success = True
                        break
                except:
                    if "image_bytes" in content and "error" not in content.lower():
                        success = True
                        break
            elif isinstance(content, dict):
                if "error" not in content:
                    png_bytes = content.get("image_bytes", b"")
                    success = True
                    break

    output_dir = config.get("configurable", {}).get("output_dir", ".")
    
    if success:
        diagram_id = diagram.get("diagram_id")
        base_filename = os.path.join(output_dir, f"{diagram_id}")
        
        output_path_png = f"{base_filename}.png"
        output_path_puml = f"{base_filename}.puml"
        output_path_json = f"{base_filename}.json"
        
        # Write files if we have an output directory
        if output_dir:
            if png_bytes:
                with open(output_path_png, "wb") as f:
                    f.write(png_bytes)
            
            if current_puml:
                with open(output_path_puml, "w", encoding="utf-8") as f:
                    f.write(current_puml)
            
            with open(output_path_json, "w", encoding="utf-8") as f:
                json.dump(diagram, f, indent=2)

        completed = {
            "diagram_id": diagram_id,
            "diagram_type": diagram.get("diagram_type"),
            "png_bytes": png_bytes,
            "plantuml_source": current_puml,
            "output_path": output_path_png
        }
        return {"completed_diagrams": [completed]}
    else:
        failed = {
            "diagram_id": diagram.get("diagram_id"),
            "diagram_type": diagram.get("diagram_type"),
            "error_message": "Agent failed to generate valid PlantUML",
            "attempts": retry_count,
            "last_puml": current_puml
        }
        return {"failed_diagrams": [failed]}
