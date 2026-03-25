"""
Checkpoint Dialog Component — Strict pipeline checkpoint (FR-UI-007).

Blocks page transition until user clicks 'Continue' or 'Go Back'.
"""

import streamlit as st


def render_checkpoint_dialog(message: str) -> str:
    """Render a blocking checkpoint dialog on the current page.

    Args:
        message: Checkpoint message to display.

    Returns:
        "continue" or "back" based on user selection.
    """
    raise NotImplementedError
