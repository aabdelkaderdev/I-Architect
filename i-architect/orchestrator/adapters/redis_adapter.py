"""
Redis Adapter — Facade for Redis lock, cache, and metadata operations.

Implements: FR-TASK-001–003, FR-TASK-005–007, FR-TASK-009.
"""

from typing import Any, Optional


class RedisAdapter:
    """Facade for Redis operations used across the pipeline.

    Key namespaces:
    - lock:project:{project_id} — Distributed project lock (FR-TASK-001)
    - meta:task:{task_id} — Task progress hash (FR-TASK-005)
    - cancel:task:{task_id} — Cancellation token (FR-TASK-003)
    - render_cache:{hash} — PlantUML render cache (FR-PUML-005)
    """

    def __init__(self, redis_url: str) -> None:
        """Initialize Redis adapter.

        Args:
            redis_url: Redis connection URL.
        """
        self.redis_url = redis_url

    def acquire_lock(self, project_id: str, task_id: str, ttl_seconds: int = 3600) -> bool:
        """Acquire a distributed project lock (FR-TASK-001).

        Uses SETNX with TTL. Only one pipeline run per project at a time.

        Args:
            project_id: Project UUID.
            task_id: Celery task UUID (stored as lock value).
            ttl_seconds: Lock TTL for auto-expiry.

        Returns:
            True if lock acquired, False if project already locked.
        """
        raise NotImplementedError

    def release_lock(self, project_id: str) -> None:
        """Release the project lock (FR-TASK-002).

        Args:
            project_id: Project UUID.
        """
        raise NotImplementedError

    def set_progress(self, task_id: str, progress: dict[str, Any]) -> None:
        """Update task progress in Redis hash (FR-TASK-005).

        Args:
            task_id: Celery task UUID.
            progress: Progress dictionary matching PipelineProgress schema.
        """
        raise NotImplementedError

    def get_progress(self, task_id: str) -> Optional[dict[str, Any]]:
        """Read task progress from Redis hash (FR-TASK-006).

        Args:
            task_id: Celery task UUID.

        Returns:
            Progress dictionary, or None if not found.
        """
        raise NotImplementedError

    def set_cancellation(self, task_id: str) -> None:
        """Set the cancellation token for a running task (FR-TASK-003).

        Args:
            task_id: Celery task UUID.
        """
        raise NotImplementedError

    def check_cancellation(self, task_id: str) -> bool:
        """Check if a cancellation has been requested (FR-TASK-007).

        Args:
            task_id: Celery task UUID.

        Returns:
            True if cancellation was requested.
        """
        raise NotImplementedError

    def cache_render(self, cache_key: str, content: bytes, ttl_seconds: int = 600) -> None:
        """Cache a PlantUML render result.

        Args:
            cache_key: Hash-based cache key.
            content: Rendered SVG/PNG bytes.
            ttl_seconds: Cache TTL.
        """
        raise NotImplementedError

    def get_cached_render(self, cache_key: str) -> Optional[bytes]:
        """Retrieve a cached render result.

        Args:
            cache_key: Hash-based cache key.

        Returns:
            Cached bytes, or None if miss.
        """
        raise NotImplementedError
