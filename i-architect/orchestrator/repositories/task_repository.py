"""
Task Repository — Data access for completed task results.

Persists task outcomes to PostgreSQL (FR-TASK-010).
"""

from typing import Any
from core.interfaces.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """PostgreSQL repository for task result persistence."""

    def get_by_id(self, entity_id: str) -> dict | None:
        raise NotImplementedError

    def list_all(self, **filters: Any) -> list[dict]:
        raise NotImplementedError

    def create(self, entity: dict) -> dict:
        raise NotImplementedError

    def update(self, entity_id: str, data: dict[str, Any]) -> dict:
        raise NotImplementedError

    def delete(self, entity_id: str) -> bool:
        raise NotImplementedError

    def get_by_project(self, project_id: str) -> list[dict]:
        """Get all task results for a project.

        Args:
            project_id: Project UUID.

        Returns:
            List of TaskResult dicts.
        """
        raise NotImplementedError
