"""
Progress Overlay Component — Pipeline progress indicator (FR-UI-023).

Full-screen overlay with animated progress bar, phase labels, and ETA.
Blocks user interaction during pipeline execution.
"""

import streamlit as st


def render_progress_overlay(task_id: str) -> None:
    """Render the blocking progress overlay during pipeline execution.

    Polls GET /api/tasks/{task_id}/progress/ every 2 seconds.
    Displays: progress bar, current phase, ETA, cancel button.

    Args:
        task_id: Active Celery task UUID.
    """
    raise NotImplementedError
