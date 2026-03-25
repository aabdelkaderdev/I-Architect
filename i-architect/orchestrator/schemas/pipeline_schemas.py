"""
Pipeline Schemas — Pydantic DTOs for task management and progress.

Referenced by: FR-TASK-005/006/012/013, IR-TASK-002/003.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PipelineRunRequest(BaseModel):
    """Request payload for POST /api/run/{workflow_type}/."""

    project_id: str = Field(..., description="UUID of the target project.")
    workflow_type: int = Field(..., description="Workflow number: 1, 2, or 3.")
    arlo_enabled: bool = Field(default=True, description="Whether ARLO is engaged.")
    llm_mappings: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Agent → list of LLM config names mapping.",
    )
    arlo_config: Optional[dict] = Field(default=None, description="ARLO-specific configuration.")
    extraction_strategy: Optional[str] = Field(default=None, description="Selected extraction strategy name.")
    target_framework: str = Field(default="C4_Container", description="'C4_Container' or 'UML_Component'.")


class PipelineProgress(BaseModel):
    """Progress metadata stored in Redis hash meta:task:{task_id}."""

    progress_percent: int = Field(default=0, description="Overall progress (0–100).")
    current_phase: str = Field(default="", description="Human-readable phase label.")
    eta_seconds: Optional[float] = Field(default=None, description="Estimated time remaining (ARLO only).")
    completed_batches: Optional[int] = Field(default=None, description="ARLO batch progress.")
    avg_batch_time: Optional[float] = Field(default=None, description="Rolling average batch duration.")
    status: str = Field(default="PENDING", description="PENDING, RUNNING, COMPLETED, FAILED, CANCELLED.")
    error_log: Optional[str] = Field(default=None, description="Stack trace on failure.")


class SSEEvent(BaseModel):
    """Server-Sent Event payload (IR-TASK-003)."""

    eta_seconds: Optional[float] = Field(default=None)
    percent_complete: int = Field(default=0)
    current_phase: str = Field(default="")
    status: str = Field(default="RUNNING")


class TaskResult(BaseModel):
    """Completed task result metadata persisted to PostgreSQL (FR-TASK-010)."""

    task_id: str = Field(..., description="Celery task UUID.")
    project_id: str = Field(..., description="Associated project UUID.")
    status: str = Field(..., description="Final status: COMPLETED, FAILED, CANCELLED.")
    artifact_paths: list[str] = Field(default_factory=list, description="Paths to generated output files.")
    error_log: Optional[str] = Field(default=None, description="Error details if FAILED.")
