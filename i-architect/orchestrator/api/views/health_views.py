"""
Health Check View — System health endpoint.
"""

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class HealthCheckView(APIView):
    """GET /api/health/ — Basic liveness check for Docker health checks."""

    def get(self, request: Request) -> Response:
        """Return 200 OK if the Django server is running.

        Returns:
            200: Service is healthy.
        """
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)
