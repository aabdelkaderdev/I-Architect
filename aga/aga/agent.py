from langchain.agents import create_agent
from aga.tools import encode_plantuml, fetch_plantuml_png, handle_tool_errors

def build_agent(model):
    """
    Builds the ReAct agent using the current LangChain create_agent API.
    Wires the plantuml tools and error-handling middleware.
    """
    # System prompt will be refined in Phase 3
    system_prompt = "You are an Architecture Generation Agent."
    
    return create_agent(
        model=model,
        tools=[encode_plantuml, fetch_plantuml_png],
        middleware=[handle_tool_errors],
        system_prompt=system_prompt
    )
