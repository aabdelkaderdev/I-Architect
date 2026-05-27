"""
Architecture Generation Agent (AGA)

This module is responsible for generating C4-compliant PlantUML diagrams from an architecture model.
It integrates with the Orchestrator by accepting a `RunnableConfig` containing output and checkpoint 
paths, and outputs an `AGAOutput` dictionary containing completed diagrams, failed diagrams, and a 
session report.

Public API:
- `create_aga_graph`: Factory function to create and compile the AGA StateGraph.
- `AGAOutput`: TypedDict representing the final output structure of the AGA.
- `CompletedDiagram`: Pydantic model for a successfully generated diagram.
- `FailedDiagram`: Pydantic model for a diagram that failed to generate.
- `SessionReport`: Pydantic model for the overall session summary.
"""

from aga.graphs.aga_graph import create_aga_graph
from aga.state.schemas import AGAOutput
from aga.state.models import CompletedDiagram, FailedDiagram, SessionReport

__all__ = [
    "create_aga_graph",
    "AGAOutput",
    "CompletedDiagram",
    "FailedDiagram",
    "SessionReport",
]
