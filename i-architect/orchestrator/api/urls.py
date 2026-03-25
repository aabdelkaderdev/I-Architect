"""
API URL configuration.

Maps all REST endpoints defined in IR-TASK-002, IR-PSM-001–004.
"""

from django.urls import path

from api.views.project_views import (
    ProjectListCreateView,
    ProjectDetailView,
    ProjectStatusView,
    ProjectExportView,
    ProjectImportView,
)
from api.views.pipeline_views import (
    PipelineRunView,
    PipelineCancelView,
    PipelineProgressSSEView,
    TaskStatusView,
)
from api.views.agent_views import (
    ManualOverrideView,
    ActiveVersionsView,
)
from api.views.health_views import HealthCheckView

urlpatterns = [
    # ── Health ──
    path("health/", HealthCheckView.as_view(), name="health-check"),

    # ── Projects ──
    path("projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    path("projects/<str:project_id>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<str:project_id>/status", ProjectStatusView.as_view(), name="project-status"),
    path("projects/<str:project_id>/export", ProjectExportView.as_view(), name="project-export"),
    path("projects/import", ProjectImportView.as_view(), name="project-import"),

    # ── Pipeline Execution ──
    path("run/<str:workflow_type>/", PipelineRunView.as_view(), name="pipeline-run"),
    path("cancel/<str:task_id>/", PipelineCancelView.as_view(), name="pipeline-cancel"),
    path("tasks/<str:task_id>/progress/", PipelineProgressSSEView.as_view(), name="pipeline-progress-sse"),
    path("status/<str:task_id>/", TaskStatusView.as_view(), name="task-status"),

    # ── Agent Overrides ──
    path(
        "projects/<str:project_id>/agents/aga/manual_override",
        ManualOverrideView.as_view(),
        name="aga-manual-override",
    ),
    path(
        "projects/<str:project_id>/active_versions/<str:agent_name>",
        ActiveVersionsView.as_view(),
        name="active-versions",
    ),
]
