"""
Project Views — REST API endpoints for project CRUD and state management.

Implements: IR-PSM-001–004, FR-PSM-001–003, FR-PSM-016/017.
"""

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class ProjectListCreateView(APIView):
    """GET: List all projects. POST: Create a new project."""

    def get(self, request: Request) -> Response:
        """List all projects with basic metadata.

        Returns:
            200: List of project summaries.
        """
        return Response({"projects": []}, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a new project and scaffold its directory structure (FR-PSM-001).

        Validates uniqueness (FR-PSM-002) and creates all mandatory subdirectories.

        Returns:
            201: Project created successfully.
            409: Duplicate project name.
        """
        return Response({"message": "stub"}, status=status.HTTP_201_CREATED)


class ProjectDetailView(APIView):
    """GET: Project details. DELETE: Delete project."""

    def get(self, request: Request, project_id: str) -> Response:
        """Retrieve full project details.

        Args:
            project_id: UUID of the project.

        Returns:
            200: Project details.
            404: Project not found.
        """
        return Response({"project_id": project_id}, status=status.HTTP_200_OK)

    def delete(self, request: Request, project_id: str) -> Response:
        """Delete a project and its directory tree.

        Args:
            project_id: UUID of the project.

        Returns:
            204: Deleted successfully.
            404: Not found.
        """
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectStatusView(APIView):
    """GET /api/projects/{id}/status — Backend state sync (IR-PSM-001)."""

    def get(self, request: Request, project_id: str) -> Response:
        """Query current project state for UI synchronization (FR-PSM-011).

        Returns JSON matching the IR-PSM-001 schema:
        {status, current_step, task_id, locked, quota_warning, quota_percent}

        Args:
            project_id: UUID of the project.

        Returns:
            200: Current project status.
        """
        return Response(
            {
                "status": "IDLE",
                "current_step": None,
                "task_id": None,
                "locked": False,
                "quota_warning": False,
                "quota_percent": 0.0,
            },
            status=status.HTTP_200_OK,
        )


class ProjectExportView(APIView):
    """GET /api/projects/{id}/export — Download project as ZIP (FR-PSM-016)."""

    def get(self, request: Request, project_id: str) -> Response:
        """Create and stream a downloadable ZIP archive of the project.

        Includes: arlo_output/, filtered_requirements/.
        Excludes: arlo_cache/, pdf/, agent_states/.

        Args:
            project_id: UUID of the project.

        Returns:
            200: ZIP file download.
        """
        return Response({"message": "stub"}, status=status.HTTP_200_OK)


class ProjectImportView(APIView):
    """POST /api/projects/import — Import project from ZIP (FR-PSM-017)."""

    def post(self, request: Request) -> Response:
        """Accept a ZIP archive and create a new project from it.

        Validates internal ZIP structure and maps files to correct directories.

        Returns:
            201: Project imported successfully.
            422: Invalid ZIP structure.
        """
        return Response({"message": "stub"}, status=status.HTTP_201_CREATED)
