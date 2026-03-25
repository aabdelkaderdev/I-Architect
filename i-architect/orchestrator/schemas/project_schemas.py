"""
Project Schemas — Pydantic DTOs for project state management.

Referenced by: FR-PSM-001–017, IR-PSM-001–004.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ProjectCreate(BaseModel):
    """Request payload for creating a new project."""

    name: str = Field(..., description="Human-readable project name.")
    description: str = Field(default="", description="Optional project description.")


class ProjectStatus(BaseModel):
    """Project status response (IR-PSM-001)."""

    project_id: str = Field(..., description="Project UUID.")
    name: str = Field(default="")
    status: str = Field(default="IDLE", description="RUNNING, IDLE, COMPLETED, FAILED.")
    current_step: Optional[str] = Field(default=None, description="Active agent: RAA, AGA, SA, ARLO, or null.")
    task_id: Optional[str] = Field(default=None, description="Active Celery task UUID.")
    locked: bool = Field(default=False, description="True if project is write-locked.")
    quota_warning: bool = Field(default=False, description="True if quota > 80%.")
    quota_percent: float = Field(default=0.0, description="Current disk usage percentage.")


class ProjectExport(BaseModel):
    """Metadata for project export/import operations."""

    project_id: str = Field(...)
    included_dirs: list[str] = Field(
        default_factory=lambda: ["arlo_output", "filtered_requirements"],
        description="Directories included in the export ZIP.",
    )
    excluded_dirs: list[str] = Field(
        default_factory=lambda: ["arlo_cache", "pdf", "agent_states"],
        description="Directories excluded from the export.",
    )
