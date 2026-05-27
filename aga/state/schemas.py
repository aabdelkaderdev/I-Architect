import operator
from typing import TypedDict, Annotated, Optional, Any
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class AGAInput(TypedDict):
    """Input channel for the Architecture Generation Agent."""
    arch_model: dict[str, Any]

class AGAOutput(TypedDict):
    """Output channel for the Architecture Generation Agent."""
    completed_diagrams: list[dict[str, Any]]
    failed_diagrams: list[dict[str, Any]]
    session_report: dict[str, Any]

class AGAState(TypedDict):
    """Internal state channel for the Architecture Generation Agent."""
    arch_model: dict[str, Any]
    diagram_queue: list[dict[str, Any]]
    current_diagram: Optional[dict[str, Any]]
    current_puml_code: str
    current_encoded_url: str
    retry_count: int
    last_error: Optional[dict[str, Any]]
    completed_diagrams: Annotated[list[dict[str, Any]], operator.add]
    failed_diagrams: Annotated[list[dict[str, Any]], operator.add]
    diagram_cursor: int
    planturl_bin_path: str
    session_report: Optional[dict[str, Any]]
    messages: Annotated[list[AnyMessage], add_messages]
