"""
Pipeline Tasks — Celery task definitions for pipeline orchestration.

Implements: FR-TASK-012–015.
"""

from celery import shared_task


@shared_task(bind=True, name="tasks.pipeline_tasks.run_pipeline")
def run_pipeline(self, project_id: str, workflow_type: int, config: dict) -> dict:
    """Main pipeline entry point — dispatches the appropriate LangGraph workflow.

    1. Acquire project lock.
    2. Build LangGraph based on workflow_type.
    3. Execute graph with progress reporting.
    4. On completion/failure, release lock and persist result.

    Args:
        self: Celery task instance (for self.request.id).
        project_id: UUID of the target project.
        workflow_type: 1, 2, or 3.
        config: Pipeline configuration dict.

    Returns:
        Task result dict with status and artifact paths.
    """
    raise NotImplementedError


@shared_task(bind=True, name="tasks.pipeline_tasks.run_arlo")
def run_arlo(self, project_id: str, config: dict) -> dict:
    """ARLO-only execution (Workflow 1 sub-task).

    Args:
        self: Celery task instance.
        project_id: Project UUID.
        config: ARLO configuration dict.

    Returns:
        ARLO TOON payload dict.
    """
    raise NotImplementedError


@shared_task(bind=True, name="tasks.pipeline_tasks.run_raa")
def run_raa(self, project_id: str, config: dict) -> dict:
    """RAA-only execution.

    Args:
        self: Celery task instance.
        project_id: Project UUID.
        config: RAA configuration dict.

    Returns:
        RAA TOON IR dict.
    """
    raise NotImplementedError


@shared_task(bind=True, name="tasks.pipeline_tasks.run_aga")
def run_aga(self, project_id: str, config: dict) -> dict:
    """AGA-only execution.

    Args:
        self: Celery task instance.
        project_id: Project UUID.
        config: AGA configuration dict.

    Returns:
        AGA artifacts dict (PlantUML code + rendered SVG path).
    """
    raise NotImplementedError


@shared_task(bind=True, name="tasks.pipeline_tasks.run_sa")
def run_sa(self, project_id: str, config: dict) -> dict:
    """SA-only execution.

    Args:
        self: Celery task instance.
        project_id: Project UUID.
        config: SA configuration dict.

    Returns:
        SA evaluation dict.
    """
    raise NotImplementedError
