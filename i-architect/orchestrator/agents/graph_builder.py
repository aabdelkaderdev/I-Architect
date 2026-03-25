"""
Graph Builder — LangGraph workflow definitions.

Defines the directed acyclic graph (DAG) for each workflow type:
  - Workflow 1: Sequential single-LLM pipeline
  - Workflow 2: Parallel multi-LLM with MCP aggregation
  - Workflow 3: Full parallel pipeline with sensitivity analysis
"""

from typing import Any


def build_workflow_1() -> Any:
    """Build the Workflow 1 LangGraph: sequential single-LLM pipeline.

    Graph: Ingestion → Filtering → [ARLO?] → RAA → AGA → SA → PDF.

    Returns:
        Compiled LangGraph StateGraph.
    """
    raise NotImplementedError


def build_workflow_2() -> Any:
    """Build the Workflow 2 LangGraph: parallel multi-LLM pipeline.

    Graph:
      Ingestion → Filtering → [ARLO?] →
        ┌─ RAA_Alpha ─┐
        ├─ RAA_Beta  ──┤ → MCP_RAA →
        └─ RAA_Gamma ──┘
        ┌─ AGA_Alpha ─┐
        ├─ AGA_Beta  ──┤ → MCP_AGA →
        └─ AGA_Gamma ──┘
        ┌─ SA_Alpha  ─┐
        ├─ SA_Beta   ──┤ → MCP_SA → PDF
        └─ SA_Gamma  ──┘

    Returns:
        Compiled LangGraph StateGraph.
    """
    raise NotImplementedError


def build_workflow_3() -> Any:
    """Build the Workflow 3 LangGraph: full parallel with sensitivity analysis.

    Same as Workflow 2, but ARLO's Beta experiment runs simultaneously
    with Alpha, and SA performs median-based scoring for ATAM.

    Returns:
        Compiled LangGraph StateGraph.
    """
    raise NotImplementedError
