"""
Project Repository — Data access for project entities.

Uses Django ORM for metadata persistence.
"""

from typing import Any
from core.interfaces.base_repository import BaseRepository


class ProjectRepository(BaseRepository):
    """Django ORM repository for Project entities."""

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
