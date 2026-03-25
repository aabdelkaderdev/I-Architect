"""
Modal System Component — Full-screen modal dialogs (FR-UI-024/025).

Reusable modal for displaying diagrams, PDFs, diff views, and JSON overlays.
"""

import streamlit as st


def render_modal(title: str, content_type: str, content: any) -> None:
    """Render a full-screen modal dialog.

    Args:
        title: Modal header text.
        content_type: "image", "pdf", "code", "json", or "diff".
        content: Content to display (bytes, str, or dict).
    """
    raise NotImplementedError
