"""
Root URL configuration for the I-Architect orchestrator.
"""

from django.urls import path, include

urlpatterns = [
    path("api/", include("api.urls")),
]
