"""
Pipeline State — LangGraph TypedDict state schema.

Central state object shared across all LangGraph nodes in the pipeline.
Every agent reads from and writes to this state.
"""

from typing import TypedDict, Optional, Any


class PipelineState(TypedDict, total=False):
    """Shared state for the LangGraph pipeline graph.

    Fields are populated progressively by each agent node.
    """

    # ── Context ──
    project_id: str
    task_id: str
    workflow_type: int  # 1, 2, or 3
    target_framework: str  # "C4_Container" or "UML_Component"
    cancel_requested: bool
    uploaded_filename: str  # Original uploaded requirements filename (FR-PDF-005/005b)
    llm_mappings: dict[str, list[str]]  # Agent → LLM config names (FR-PDF-005b)

    # ── Ingestion / Extraction ──
    uploaded_files: list[str]
    raw_requirements: list[dict[str, Any]]
    extraction_result: dict[str, Any]
    extraction_strategy: str

    # ── Filtering ──
    filtered_requirements: list[dict[str, Any]]
    filtering_stats: dict[str, Any]

    # ── ARLO ──
    arlo_enabled: bool
    arlo_config: dict[str, Any]
    arlo_toon_payload: dict[str, Any]

    # ── RAA ──
    raa_toon_ir: dict[str, Any]  # ToonIR dict

    # ── AGA ──
    aga_plantuml_code: str
    aga_rendered_svg: bytes
    aga_correction_history: list[dict[str, Any]]

    # ── SA ──
    sa_evaluation: dict[str, Any]  # SAEvaluation dict

    # ── MCP (Workflows 2/3) ──
    parallel_outputs: dict[str, list[dict[str, Any]]]
    aggregated_outputs: dict[str, dict[str, Any]]
    divergence_warnings: list[dict[str, Any]]

    # ── Progress ──
    progress_percent: int
    current_phase: str
    error_log: Optional[str]
