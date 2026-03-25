"""
Project State Service — Directory scaffolding, quota management, file rotation.

Implements: FR-PSM-001–010, FR-PSM-012/013.
"""

from pathlib import Path
from typing import Any


class ProjectStateService:
    """Manages project directory structure, disk quotas, and file rotation."""

    # Mandatory subdirectories per project (FR-PSM-001)
    MANDATORY_DIRS = [
        "pdf", "structured_requirements", "filtered_requirements",
        "arlo_cache", "arlo_output", "agent_states",
        "raa_output", "aga_output", "sa_output",
    ]

    def __init__(self, media_root: str, quota_mb: int = 500, max_versions: int = 5) -> None:
        self.media_root = Path(media_root)
        self.quota_mb = quota_mb
        self.max_versions = max_versions

    def scaffold_project(self, project_id: str) -> Path:
        """Create the full project directory structure (FR-PSM-001).

        Args:
            project_id: UUID for the new project.

        Returns:
            Path to the created project root.
        """
        raise NotImplementedError

    def scaffold_parallel_dirs(self, project_id: str, workflow_type: int) -> None:
        """Create parallel sub-directories for Workflows 2/3 (FR-PSM-006).

        Creates llm_alpha/, llm_beta/, llm_gamma/, mcp_aggregator/ under
        raa_output/, aga_output/, sa_output/.

        Args:
            project_id: Project UUID.
            workflow_type: 2 or 3.
        """
        raise NotImplementedError

    def check_quota(self, project_id: str) -> dict[str, Any]:
        """Check project disk usage against quota (FR-PSM-007/008).

        Args:
            project_id: Project UUID.

        Returns:
            Dict with 'usage_mb', 'quota_mb', 'percent', 'warning', 'locked'.
        """
        raise NotImplementedError

    def cleanup_level1(self, project_id: str) -> int:
        """Level 1 cleanup: purge arlo_cache/ (FR-PSM-007).

        Returns:
            Bytes freed.
        """
        raise NotImplementedError

    def cleanup_level2(self, project_id: str) -> int:
        """Level 2 cleanup: rotate agent_states/ to keep only last snapshot (FR-PSM-008).

        Returns:
            Bytes freed.
        """
        raise NotImplementedError

    def rotate_files(self, directory: Path, max_versions: int | None = None) -> None:
        """Enforce 5-version rotation in a directory (FR-PSM-010).

        Deletes the oldest file (by mtime) when count >= max_versions.

        Args:
            directory: Path to the directory to rotate.
            max_versions: Override for max file count.
        """
        raise NotImplementedError

    def validate_filename(self, filename: str) -> bool:
        """Validate file naming convention (FR-PSM-004).

        Pattern: {agent_name}_{llm_name}_{YYYYMMDD_HHMMSS}.{ext}

        Args:
            filename: The filename to validate.

        Returns:
            True if the filename conforms.
        """
        raise NotImplementedError
