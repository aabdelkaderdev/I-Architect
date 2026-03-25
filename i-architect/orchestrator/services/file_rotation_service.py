"""
File Rotation Service — Atomic file writes and version rotation.

Implements: FR-PSM-010, NFR-PSM-005.
"""

from pathlib import Path


class FileRotationService:
    """Handles atomic file writes and 5-version retention across agent outputs."""

    def __init__(self, max_versions: int = 5) -> None:
        self.max_versions = max_versions

    def save_with_rotation(self, directory: Path, filename: str, content: bytes) -> Path:
        """Write content to file with atomic rename and version rotation.

        Uses write-to-temp-then-rename for data integrity (NFR-PSM-005).

        Args:
            directory: Target directory.
            filename: Target filename.
            content: File content as bytes.

        Returns:
            Path to the saved file.
        """
        raise NotImplementedError

    def rotate(self, directory: Path) -> None:
        """Enforce max version retention in a directory.

        Args:
            directory: Directory to enforce rotation on.
        """
        raise NotImplementedError
