"""
Celery application configuration for I-Architect.

This module is imported by __init__.py to ensure the app is loaded
when Django starts, making @shared_task decorators work correctly.
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orchestrator.settings")

app = Celery("i_architect")

# Load config from Django settings, using the CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# ─────────────────────────────────────────────
# Celery Beat Schedule (Periodic Tasks)
# ─────────────────────────────────────────────
app.conf.beat_schedule = {
    "check-project-quotas": {
        "task": "tasks.maintenance_tasks.check_project_quotas",
        "schedule": crontab(minute="*/10"),  # Every 10 minutes (FR-PSM-007)
    },
}
