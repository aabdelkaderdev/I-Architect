"""
BaseRepository — Abstract Base Class for data access.

Defines a generic repository interface following the Repository Pattern.
Concrete implementations use Django ORM or filesystem I/O.
"""

from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Generic abstract repository for CRUD operations.

    Type parameter T represents the domain entity type.
    """

    @abstractmethod
    def get_by_id(self, entity_id: str) -> T | None:
        """Retrieve an entity by its unique identifier.

        Args:
            entity_id: The unique identifier of the entity.

        Returns:
            The entity if found, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self, **filters: Any) -> list[T]:
        """List all entities, optionally filtered.

        Args:
            **filters: Optional keyword arguments for filtering.

        Returns:
            List of matching entities.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, entity: T) -> T:
        """Persist a new entity.

        Args:
            entity: The entity to create.

        Returns:
            The created entity (with any generated fields populated).
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id: str, data: dict[str, Any]) -> T:
        """Update an existing entity.

        Args:
            entity_id: The unique identifier of the entity to update.
            data: Dictionary of fields to update.

        Returns:
            The updated entity.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete an entity by its identifier.

        Args:
            entity_id: The unique identifier of the entity to delete.

        Returns:
            True if the entity was deleted, False if not found.
        """
        raise NotImplementedError
