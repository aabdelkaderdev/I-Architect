"""
File Repository — Filesystem I/O abstraction.

Abstracts file read/write operations for agent outputs and project files.
"""

from pathlib import Path
from typing import Any


class FileRepository:
    """Filesystem repository for reading/writing project files.

    All paths are resolved relative to MEDIA_ROOT/projects/{project_id}/.
    """

    def __init__(self, media_root: str) -> None:
        self.media_root = Path(media_root)

    def read_json(self, project_id: str, relative_path: str) -> dict[str, Any]:
        """Read a JSON file from the project directory.

        Args:
            project_id: Project UUID.
            relative_path: Path relative to the project root.

        Returns:
            Parsed JSON as dict.
        """
        raise NotImplementedError

    def write_json(self, project_id: str, relative_path: str, data: dict[str, Any]) -> Path:
        """Write JSON data to a file (atomic write + rotation).

        Args:
            project_id: Project UUID.
            relative_path: Path relative to the project root.
            data: Data to serialize.

        Returns:
            Path to the written file.
        """
        raise NotImplementedError

    def read_text(self, project_id: str, relative_path: str) -> str:
        """Read a text file.

        Args:
            project_id: Project UUID.
            relative_path: Path relative to the project root.

        Returns:
            File contents as string.
        """
        raise NotImplementedError

    def write_text(self, project_id: str, relative_path: str, content: str) -> Path:
        """Write text content to a file.

        Args:
            project_id: Project UUID.
            relative_path: Path relative to the project root.
            content: Text to write.

        Returns:
            Path to the written file.
        """
        raise NotImplementedError

    def list_files(self, project_id: str, subdirectory: str) -> list[dict[str, Any]]:
        """List files in a project subdirectory with metadata.

        Args:
            project_id: Project UUID.
            subdirectory: Subdirectory name (e.g., "raa_output").

        Returns:
            List of file info dicts with 'name', 'size', 'mtime'.
        """
        raise NotImplementedError
