import json
from typing import Any, Callable

from langchain_core.messages import AnyMessage, SystemMessage
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest, dynamic_prompt
from langchain.agents.middleware.types import ModelResponse
from langgraph.runtime import Runtime

from aga.state.schemas import AGAState
from aga.tools.encode_plantuml import encode_plantuml
from aga.tools.fetch_plantuml_png import fetch_plantuml_png


class DiagramGenerationMiddleware(AgentMiddleware[AGAState]):
    state_schema = AGAState

    def before_model(self, state: AGAState, runtime: Runtime) -> dict[str, Any] | None:
        count = state.get("retry_count", 0)
        if count >= 5:
            # Reached max retries, halt the agent
            return {"jump_to": "end"}
        return None

    def wrap_tool_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        # Intercept tool calls for error handling and tracking
        response = handler(request)
        
        # If the response contains an error, we can log it or adjust the state.
        # But we also need to increment retry_count. The state updates happen 
        # outside of wrap_tool_call in the main loop or via another hook.
        return response

    def after_model(self, state: AGAState, runtime: Runtime) -> dict[str, Any] | None:
        # Increment retry_count if a tool is called, meaning a retry is happening
        messages = state.get("messages", [])
        if not messages:
            return None
            
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return {"retry_count": state.get("retry_count", 0) + 1}
        return None



@dynamic_prompt
def diagram_prompt_middleware(request: ModelRequest) -> str:
    """Generate the dynamic system prompt based on the current diagram in state."""
    state = request.state
    diagram = state.get("current_diagram")
    if not diagram:
        return "You are an Architecture Generation Agent."
        
    diagram_id = diagram.get("diagram_id", "")
    diagram_type = diagram.get("diagram_type", "")
    focus_entity_id = diagram.get("focus_entity_id", "")
    focus_entity_label = diagram.get("focus_entity_label", "")
    entities = diagram.get("entities", [])
    relationships = diagram.get("relationships", [])
    
    # Task 3.1 & 3.2: Assumption Handling
    # Check node metadata for assumed flag and append [assumed] to the description
    processed_entities = []
    for entity in entities:
        ent_copy = entity.copy()
        metadata = ent_copy.get("metadata", {})
        if metadata.get("assumed") is True:
            desc = ent_copy.get("description", "")
            if desc and not desc.endswith("[assumed]"):
                ent_copy["description"] = f"{desc} [assumed]"
            elif not desc:
                ent_copy["description"] = "[assumed]"
        processed_entities.append(ent_copy)
    
    return f"""You are the Architecture Generation Agent (AGA). Your task is to generate C4-compliant PlantUML diagrams from an architecture model.

## Diagram Specification
- Diagram ID: {diagram_id}
- Diagram Type: {diagram_type}
- Focus Entity: {focus_entity_id}
- Focus Entity Label: {focus_entity_label}

## Entities in Scope
{json.dumps(processed_entities, indent=2)}

## Relationships in Scope
{json.dumps(relationships, indent=2)}

## Retry Policy
- Maximum 5 correction attempts per diagram
- On syntax error: read the error, identify the faulty construct, fix minimally
- Do not restructure the entire diagram on a single error

## Constraints
- Do NOT invent entities or relationships not listed above
- Every PlantUML alias MUST exactly match a canonical entity ID
- Do NOT modify the architecture model — only translate it to diagram code
"""


def create_diagram_agent(tools: list) -> Any:
    """Creates and returns the diagram agent subgraph."""
    return create_agent(
        model="gemini-2.5-pro", # This will be overridden by the runtime context if needed
        tools=tools,
        middleware=[diagram_prompt_middleware, DiagramGenerationMiddleware()],
        state_schema=AGAState
    )
