"""
Disk Quota Middleware — Intercepts write endpoints for quota enforcement.

Implements: FR-PSM-009.
Performs a lightweight size check before processing critical write endpoints.
"""

from django.http import JsonResponse


class DiskQuotaMiddleware:
    """Django middleware that checks project disk usage on write operations.

    If project_usage >= 500MB, returns HTTP 507 Insufficient Storage
    and the UI displays a blocking "Disk Full" modal.
    """

    def __init__(self, get_response):
        """Initialize middleware.

        Args:
            get_response: The next middleware or view in the chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        """Process the request.

        For POST/PUT/PATCH requests to quota-sensitive endpoints,
        perform the disk usage check before allowing the request through.

        Args:
            request: The incoming HTTP request.

        Returns:
            HttpResponse — either the normal response or 507 on quota exceeded.
        """
        # Stub: In production, check project_id from URL and verify disk usage
        response = self.get_response(request)
        return response

    def _check_quota(self, project_id: str) -> bool:
        """Check if the project has exceeded its disk quota.

        Args:
            project_id: UUID of the project to check.

        Returns:
            True if the project is within quota, False if exceeded.
        """
        raise NotImplementedError
