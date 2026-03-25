"""
Pipeline Views — REST API endpoints for pipeline execution and monitoring.

Implements: IR-TASK-002, FR-TASK-012–015.
"""

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse


class PipelineRunView(APIView):
    """POST /api/run/{workflow_type}/ — Dispatch a pipeline run (FR-TASK-013)."""

    def post(self, request: Request, workflow_type: str) -> Response:
        """Check project lock → Acquire lock → Dispatch Celery task → Return task_id.

        Args:
            workflow_type: Workflow number as string ("1", "2", or "3").

        Returns:
            202: Task dispatched, body contains {task_id}.
            409: Project already locked by another run.
            422: Invalid workflow type or configuration.
        """
        return Response(
            {"task_id": "stub-task-id", "status": "DISPATCHED"},
            status=status.HTTP_202_ACCEPTED,
        )


class PipelineCancelView(APIView):
    """POST /api/cancel/{task_id}/ — Request graceful cancellation (FR-TASK-015)."""

    def post(self, request: Request, task_id: str) -> Response:
        """Set the cancel:task:{task_id} Redis key to True.

        The running agent detects this token and exits gracefully within
        one batch cycle (FR-TASK-008).

        Args:
            task_id: Celery task UUID to cancel.

        Returns:
            200: Cancellation signal sent.
            404: Task not found.
        """
        return Response(
            {"message": "Cancellation signal sent.", "task_id": task_id},
            status=status.HTTP_200_OK,
        )


class PipelineProgressSSEView(APIView):
    """GET /api/tasks/{task_id}/progress/ — SSE progress stream (FR-TASK-012)."""

    def get(self, request: Request, task_id: str) -> StreamingHttpResponse:
        """Stream progress updates via Server-Sent Events.

        Emits events every 2 seconds containing:
        {eta_seconds, percent_complete, current_phase, status}

        Uses Django's StreamingHttpResponse (no WebSocket dependency).

        Args:
            task_id: Celery task UUID to monitor.

        Returns:
            StreamingHttpResponse with text/event-stream content type.
        """

        def _event_stream():
            """Generator yielding SSE events. Stub — yields a single event."""
            yield "data: {\"eta_seconds\": null, \"percent_complete\": 0, \"current_phase\": \"Initializing...\", \"status\": \"PENDING\"}\n\n"

        return StreamingHttpResponse(
            _event_stream(),
            content_type="text/event-stream",
        )


class TaskStatusView(APIView):
    """GET /api/status/{task_id}/ — Poll task status (FR-TASK-014)."""

    def get(self, request: Request, task_id: str) -> Response:
        """Read meta:task:{id} from Redis and return progress JSON.

        Args:
            task_id: Celery task UUID.

        Returns:
            200: Current task progress and status.
            404: Task not found.
        """
        return Response(
            {
                "task_id": task_id,
                "progress_percent": 0,
                "current_phase": "",
                "eta_seconds": None,
                "status": "PENDING",
            },
            status=status.HTTP_200_OK,
        )
