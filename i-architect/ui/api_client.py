"""
API Client — HTTP client for communicating with the Django backend.

All UI ↔ Orchestrator communication goes through this module.
"""

import requests
from config import BACKEND_URL


class APIClient:
    """HTTP client for the I-Architect backend API."""

    def __init__(self, base_url: str = BACKEND_URL) -> None:
        self.base_url = base_url.rstrip("/")

    # ── Projects ──

    def list_projects(self) -> list[dict]:
        """GET /api/projects/"""
        raise NotImplementedError

    def create_project(self, name: str, description: str = "") -> dict:
        """POST /api/projects/"""
        raise NotImplementedError

    def get_project(self, project_id: str) -> dict:
        """GET /api/projects/{id}/"""
        raise NotImplementedError

    def delete_project(self, project_id: str) -> None:
        """DELETE /api/projects/{id}/"""
        raise NotImplementedError

    def get_project_status(self, project_id: str) -> dict:
        """GET /api/projects/{id}/status"""
        raise NotImplementedError

    # ── Pipeline ──

    def run_pipeline(self, config: dict) -> dict:
        """POST /api/run/{workflow_type}/"""
        raise NotImplementedError

    def cancel_pipeline(self, task_id: str) -> dict:
        """POST /api/cancel/{task_id}/"""
        raise NotImplementedError

    def get_task_status(self, task_id: str) -> dict:
        """GET /api/status/{task_id}/"""
        raise NotImplementedError

    # ── Agent Overrides ──

    def submit_manual_override(self, project_id: str, content: str) -> dict:
        """POST /api/projects/{id}/agents/aga/manual_override"""
        raise NotImplementedError

    # ── Export/Import ──

    def export_project(self, project_id: str) -> bytes:
        """GET /api/projects/{id}/export"""
        raise NotImplementedError

    def import_project(self, zip_content: bytes) -> dict:
        """POST /api/projects/import"""
        raise NotImplementedError
