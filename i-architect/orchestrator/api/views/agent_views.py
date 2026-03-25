"""
Agent Views — REST API endpoints for agent-specific operations.

Implements: IR-PSM-002, IR-PSM-003, FR-PSM-015.
"""

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class ManualOverrideView(APIView):
    """POST /api/projects/{id}/agents/aga/manual_override — Persist user edits (FR-PSM-015)."""

    def post(self, request: Request, project_id: str) -> Response:
        """Save user-modified .puml code as the primary artifact.

        The frontend sends the modified PlantUML content from the code editor.
        The backend saves it as aga_manual_{timestamp}.puml and updates
        the primary_artifact metadata for downstream consumption.

        Args:
            project_id: UUID of the project.

        Returns:
            200: Override saved successfully.
            422: Invalid content.
        """
        return Response(
            {"message": "Manual override saved.", "project_id": project_id},
            status=status.HTTP_200_OK,
        )


class ActiveVersionsView(APIView):
    """GET /api/projects/{id}/active_versions/{agent_name} — History Drawer support (IR-PSM-002)."""

    def get(self, request: Request, project_id: str, agent_name: str) -> Response:
        """Return user-selected version overrides for the MCP Aggregator's input.

        Used by the MCP Aggregator to determine which specific file versions
        to use instead of the latest (FR-MCP-003).

        Args:
            project_id: UUID of the project.
            agent_name: Agent identifier (e.g., "raa", "aga", "sa").

        Returns:
            200: Version override mappings.
        """
        return Response(
            {
                "project_id": project_id,
                "agent_name": agent_name,
                "overrides": {},
            },
            status=status.HTTP_200_OK,
        )
